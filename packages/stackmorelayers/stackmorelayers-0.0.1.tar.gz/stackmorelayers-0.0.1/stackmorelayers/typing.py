from os import PathLike
from typing import Union, Dict, Any, Callable, Iterable, Tuple

import numpy as np
import pandas as pd
from catboost import Pool
from numpy.typing import NDArray
from sklearn.model_selection import BaseCrossValidator, BaseShuffleSplit

__all__ = (
    'KWARGS',
    'KWARG_FACTORY',
    'KWARGS_OR_FACTORY',

    'ARRAY_INDEXER',
    'SPLIT_ITERABLE',
    'SPLITTER',

    'FEATURES',
    'TARGET',
    'DATASET',

    'PATH'
)

KWARGS = Dict[str, Any]
KWARG_FACTORY = Callable[[], Dict[str, Any]]
KWARGS_OR_FACTORY = Union[KWARGS, KWARG_FACTORY]

ARRAY_INDEXER = NDArray[np.integer]
SPLIT_ITERABLE = Iterable[Tuple[ARRAY_INDEXER, ARRAY_INDEXER]]
SPLITTER = Union[SPLIT_ITERABLE, BaseCrossValidator, BaseShuffleSplit]

FEATURES = Union[pd.DataFrame, np.ndarray]
TARGET = Union[pd.Series, np.ndarray]
DATASET = Union[Pool, Tuple[FEATURES, TARGET]]

PATH = Union[PathLike[str], str]
