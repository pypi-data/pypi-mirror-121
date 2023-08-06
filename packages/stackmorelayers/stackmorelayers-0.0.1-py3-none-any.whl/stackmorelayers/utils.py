from functools import partial
from io import BytesIO
from re import search, compile as re_compile, Pattern
from tarfile import TarInfo
from time import time
from typing import Tuple, Dict, Any, Iterable, TypeVar, Union, Iterator

__all__ = (
    'string_to_tarfile',
    'empty_kwarg_factory'
)

_T = TypeVar('_T')


def filter_search(regex: Union[str, Pattern], iterable: Iterable[_T]) -> Iterator[_T]:
    """
    Filter the elements of the input iterable by searching for the given pattern in its values.

    Args:
        regex:     pattern to search
        iterable:  input iterable
    Returns:
        Filter iterator
    """
    return filter(partial(search, re_compile(regex)), iterable)


def string_to_tarfile(filename: str, string: str) -> Tuple[BytesIO, TarInfo]:
    """
    Write string to a tarfile.

    Args:
        filename:  tarfile name
        string:    input string
    Returns:
        (BytesIO handle, TarInfo)
    """
    encoded = string.encode()
    s = BytesIO(encoded)

    tar_info = TarInfo(filename)
    tar_info.mtime = int(time())
    tar_info.size = len(encoded)
    return s, tar_info


def empty_kwarg_factory() -> Dict[str, Any]:
    """
    Empty keyword arguments factory.

    Returns:
        Empty dict
    """
    return {}
