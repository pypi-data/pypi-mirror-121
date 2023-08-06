from io import TextIOWrapper, BytesIO
from operator import attrgetter
from os import makedirs, remove
from os.path import join as join_path
from pathlib import Path
from tarfile import open as tar_open
from tempfile import TemporaryDirectory
from typing import Optional, Dict, Any, Callable, Literal, Union, List, Tuple, Iterable, overload, Sequence

import numpy as np
import pandas as pd
from catboost import CatBoost, Pool, CatBoostClassifier
from scipy.stats import gmean
from sklearn.model_selection import BaseCrossValidator, BaseShuffleSplit
from tqdm import tqdm

from stackmorelayers.typing import KWARGS_OR_FACTORY, SPLITTER, DATASET, PATH, SPLIT_ITERABLE
from stackmorelayers.utils import string_to_tarfile, empty_kwarg_factory

__all__ = (
    "CatBoostEnsemble",
)

CB_BLENDING_DUMP_BASENAME = "catboost_blending_coefficients.txt"


class CatBoostEnsemble:
    """Ensemble of the CatBoost models"""
    __slots__ = (
        'model_factory',
        'get_model_kwargs',
        'n_models',
        'models',
        'blending_coefficients',
        'cat_features',
        'elapsed_iters',
        'validation_scores',
        'rng',
        'is_fit'
    )

    def __init__(
            self,
            model_factory: Callable[..., CatBoost] = CatBoostClassifier,
            *,
            cat_features: Optional[Union[Iterable[int], Iterable[str]]] = None,
            n_models: int = 5,
            model_kwargs: KWARGS_OR_FACTORY = empty_kwarg_factory,
            seed: Optional[int] = None
    ) -> None:
        """
        Ensemble of the CatBoost models.

        Args:
            model_factory:  model constructor
            cat_features:   list of categorical features
            n_models:       number of models to use
            model_kwargs:   keyword arguments passed to the model constructors
            seed:           RNG seed
        """

        if not hasattr(model_factory, '__call__'):
            raise TypeError("Parameter model_factory must be a Callable that returns a model instance")
        self.model_factory = model_factory

        if isinstance(model_kwargs, dict):
            self.get_model_kwargs = lambda: model_kwargs
        elif hasattr(model_kwargs, '__call__'):
            self.get_model_kwargs = model_kwargs
        else:
            raise TypeError("Parameter model_kwargs must be a dictionary or Callable that returns a dictionary")

        if not np.issubdtype(type(n_models), np.integer) or not 0 < n_models < 100_000:
            raise TypeError("Parameter n_models must be an int from [1, 99_999]")
        self.n_models = n_models

        if cat_features is not None:
            if not hasattr(cat_features, '__iter__'):
                raise TypeError("Parameter cat_features must be an Iterable of indices or feature names, or None")
            self.cat_features: Optional[Union[Tuple[str, ...], Tuple[int, ...]]] = tuple(cat_features)  # type: ignore
        else:
            self.cat_features = cat_features

        self.models: List[CatBoost] = []
        self.blending_coefficients: List[float] = []

        self.elapsed_iters = 0
        self.rng = np.random.default_rng(seed)
        self.validation_scores: List[Dict[str, Any]] = []
        self.is_fit = False

    def _reset(self) -> None:
        self.is_fit = False
        self.models = []
        self.blending_coefficients = []
        self.elapsed_iters = 0
        self.validation_scores = []

    @overload
    def fit(self,
            train_dataset: DATASET,
            eval_dataset: None,
            *,
            splitter: SPLIT_ITERABLE,
            groups: None,
            fit_kwargs: KWARGS_OR_FACTORY,
            pool_constructor_kwargs: KWARGS_OR_FACTORY) -> 'CatBoostEnsemble':
        pass

    @overload
    def fit(self,
            train_dataset: DATASET,
            eval_dataset: None,
            *,
            splitter: BaseCrossValidator,
            groups: Optional[Union[pd.Series, np.ndarray]],
            fit_kwargs: KWARGS_OR_FACTORY,
            pool_constructor_kwargs: KWARGS_OR_FACTORY) -> 'CatBoostEnsemble':
        pass

    @overload
    def fit(self,
            train_dataset: DATASET,
            eval_dataset: DATASET,
            *,
            splitter: None,
            groups: None,
            fit_kwargs: KWARGS_OR_FACTORY,
            pool_constructor_kwargs: KWARGS_OR_FACTORY) -> 'CatBoostEnsemble':
        pass

    def fit(self,
            train_dataset: DATASET,
            eval_dataset: Optional[DATASET] = None,
            *,
            splitter: Optional[SPLITTER] = None,
            groups: Optional[Union[pd.Series, np.ndarray]] = None,
            fit_kwargs: KWARGS_OR_FACTORY = empty_kwarg_factory,
            pool_constructor_kwargs: KWARGS_OR_FACTORY = empty_kwarg_factory) -> 'CatBoostEnsemble':
        """
        Fit models.

        Args:
            train_dataset:            fitting data
            eval_dataset:             model evaluation data
            splitter:                 index splitter
                                      (Iterable of indexer array pairs | sklearn CrossValidator | None)
            groups:                   split groups
                                      (could only be used if split_iterator is sklearn CrossValidator or ShuffleSplit)
            fit_kwargs:               keyword arguments passed to the fit method of the CatBoost models
                                      (dict | () -> dict)
            pool_constructor_kwargs:  keyword arguments passed to the catboost.Pool constructors
                                      (dict | () -> dict)
        Returns:
            Self
        """
        self._reset()

        if isinstance(fit_kwargs, dict):
            def get_fit_kwargs():
                return fit_kwargs
        elif hasattr(fit_kwargs, '__call__'):
            get_fit_kwargs = fit_kwargs
        else:
            raise TypeError("Parameter fit_kwargs must be a dictionary or Callable that returns a dictionary")

        if isinstance(pool_constructor_kwargs, dict):
            def get_pool_constructor_kwargs():
                return pool_constructor_kwargs
        elif hasattr(pool_constructor_kwargs, '__call__'):
            get_pool_constructor_kwargs = pool_constructor_kwargs
        else:
            raise TypeError(
                "Parameter pool_constructor_kwargs must be a dictionary or Callable that returns a dictionary"
            )

        if splitter is None:
            if groups is not None:
                raise TypeError("Parameter groups cannot be set if splitter is not used")
            if not isinstance(train_dataset, Pool):
                features, labels = train_dataset
                train_dataset = Pool(features, labels, cat_features=self.cat_features, **get_pool_constructor_kwargs())
            if not isinstance(eval_dataset, Pool):
                if eval_dataset is None:
                    raise TypeError("Parameter eval_dataset should not be None if splitter is None")
                features, labels = eval_dataset
                eval_dataset = Pool(features, labels, cat_features=self.cat_features, **get_pool_constructor_kwargs())

            def get_train_eval() -> Tuple[Pool, Pool]:
                return train_dataset, eval_dataset

        elif eval_dataset is not None:
            raise TypeError("Parameter eval_dataset should not be set if splitter is set")

        elif isinstance(train_dataset, Pool):
            raise TypeError("Parameter train_dataset cannot be a catboost.Pool if splitter is set")

        else:
            features, labels = train_dataset
            if isinstance(features, pd.DataFrame):
                features_idx_selector = features.iloc
            else:
                features_idx_selector = features
            if isinstance(labels, pd.Series):
                labels_idx_selector = labels.iloc
            else:
                labels_idx_selector = labels

            if isinstance(splitter, (BaseShuffleSplit, BaseCrossValidator)):
                n_splits = splitter.get_n_splits(features, labels, groups)
                splitter = splitter.split(features, labels, groups)
            else:
                if groups is not None:
                    raise TypeError(
                        "Parameter groups cannot be set if splitter is not sklearn CrossValidator or ShuffleSplit"
                    )
                if not isinstance(splitter, Sequence):
                    splitter = tuple(splitter)
                n_splits = len(splitter)
                splitter = iter(splitter)

            if n_splits != self.n_models:
                raise ValueError(f"The number of splits {n_splits} does not match the number of model {self.n_models}")
            del n_splits

            def get_train_eval() -> Tuple[Pool, Pool]:
                train_idx, eval_idx = next(splitter)  # type: ignore
                train_split = Pool(
                    features_idx_selector[train_idx],
                    labels_idx_selector[train_idx],
                    cat_features=self.cat_features,
                    **get_pool_constructor_kwargs()
                )
                eval_split = Pool(
                    features_idx_selector[eval_idx],
                    labels_idx_selector[eval_idx],
                    cat_features=self.cat_features,
                    **get_pool_constructor_kwargs()
                )
                return train_split, eval_split

        try:
            del features, labels
        except NameError:
            pass

        for _ in tqdm(range(self.elapsed_iters, self.n_models)):

            model = self.model_factory(
                cat_features=self.cat_features,
                random_seed=self.rng.integers(0, 2 ** 63),
                **self.get_model_kwargs()
            )
            train_set, eval_set = get_train_eval()
            model.fit(
                train_set,
                eval_set=eval_set,
                **get_fit_kwargs()
            )
            self.models.append(model)
            self.blending_coefficients.append(1.0)
            self.validation_scores.append(model.get_best_score())

            self.elapsed_iters += 1

        self.is_fit = True
        return self

    def apply(self,
              dataset: Union[Pool, pd.DataFrame, np.ndarray],
              method: Literal['predict', 'predict_proba', 'predict_log_proba'] = 'predict',
              *,
              avg_method: Literal['mean', 'gmean', 'concat'] = 'mean') -> np.ndarray:
        """
        Apply models to data.

        Args:
            dataset:     input data
            method:      applying method. Possible values:
                         ('predict' | 'predict_proba' | 'predict_log_proba')
            avg_method:  ensemble prediction averaging method. Possible values:
                         ('mean' | 'gmean' | 'concat')
        Returns:
            Array of predictions
        """
        if not self.is_fit:
            raise RuntimeError("You should train your model before making any predictions")

        result = np.array([
            getattr(model, method)(dataset) * coeff
            for model, coeff in zip(self.models, self.blending_coefficients)
        ])
        if avg_method == 'mean':
            result = result.mean(0)
        elif avg_method == 'gmean':
            result = gmean(result)
        elif avg_method != 'concat':
            raise RuntimeError(f"Does not have such an option: {avg_method}")
        return result

    def save_models(self, path: PATH, *, exist_ok: bool = False) -> Path:
        """
        Save models and their meta info to disk. The resulting file can be read back using the load_models method.

        Args:
            path:      prefix of the save file
            exist_ok:  whether to rewrite possibly existing file at the path location
        Returns:
            Save file path
        """
        if not self.is_fit:
            raise RuntimeError("You should train your model before saving")
        path = Path(path)
        makedirs(path.parent, exist_ok=True)

        with tar_open(path, 'w:bz2' if exist_ok else 'x:bz2') as tar:
            with TemporaryDirectory() as tmp_path:
                model_path = join_path(tmp_path, 'tmp.cbm')
                for i, model in enumerate(self.models, 1):
                    model.save_model(model_path)
                    tar.add(model_path, f'catboost_{i:05}.cbm')

            fileobj, tar_info = string_to_tarfile(
                CB_BLENDING_DUMP_BASENAME,
                '\n'.join(map(str, self.blending_coefficients))
            )
            tar.addfile(tar_info, fileobj=fileobj)
        return path

    def load_models(self, path: PATH) -> 'CatBoostEnsemble':
        """
        Load previously saved CatBoostEnsemble from disk.

        Args:
            path:  save file path
        Returns:
            Self
        """
        self._reset()
        with tar_open(path, 'r:bz2') as tar, TemporaryDirectory() as tmp_path:
            for member in sorted(tar, key=attrgetter('name')):
                member_name = member.name
                if member_name.endswith('.cbm'):
                    tar.extract(member, tmp_path)
                    model = self.model_factory(
                        cat_features=self.cat_features,
                        random_seed=self.rng.integers(0, 2 ** 63),
                        **self.get_model_kwargs()
                    )
                    model_path = join_path(tmp_path, member_name)
                    model.load_model(model_path)
                    remove(model_path)
                    self.models.append(model)
                    self.n_models += 1
                elif member_name == CB_BLENDING_DUMP_BASENAME:
                    try:
                        for i, cf in enumerate(map(str.strip, TextIOWrapper(tar.extractfile(member) or BytesIO())), 1):
                            self.blending_coefficients.append(float(cf))
                    except ValueError as e:
                        raise ValueError(f"Cannot parse to float {i} line in {member_name}") from e

        if self.n_models != len(self.blending_coefficients):
            raise ValueError("The number of blending coefficients does not match the number of models")

        self.elapsed_iters = self.n_models
        self.is_fit = True
        return self

    def reseed(self, seed: Optional[int] = None) -> 'CatBoostEnsemble':
        """
        Reseed random number generator.

        Args:
            seed:  rng seed
        Returns:
            Self
        """
        self.rng = np.random.default_rng(seed)
        return self
