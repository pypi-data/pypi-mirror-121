from typing import Any, Callable, Iterable, MutableSequence, Sequence, TypeVar, Union, Optional, \
    Tuple, overload

_T = TypeVar('_T')
_CT = TypeVar('_CT', covariant=True)
_CRT = TypeVar('_CRT', covariant=True)
_CF = Union[Callable[..., _CRT], _CRT]

def append(x: Any, seqs: Iterable = ...) -> _CF: ...
def prepend(x: Any, seqs: Iterable = ...) -> _CF: ...
def pop(seqs: MutableSequence[_T], index: int = ...) -> _T: ...
def shift(seqs: MutableSequence[_T]) -> _T: ...
def update(index: int, v: Any, seqs: MutableSequence) -> Sequence: ...
def update_range(upset: Any, seqs: Sequence = ...,
                 start: Any=..., stop: Any=..., step: Any=...) -> _CF: ...
def adjust(index: int, f: Callable, seqs: MutableSequence) -> Any: ...
def slices(_s: tuple, seqs: Sequence) -> slice: ...

def chunked(n: int, iterable: Iterable = ...) -> _CF: ...
def windowed(n: int, seq: Sequence = ...,
             fillvalue: Optional[Any] = ..., step: int = ...) -> _CF: ...

def padded(v: Any, n: int, iterable: Iterable = ..., next_multiple: bool = ...): ...

def take(n: int, iterable: Iterable = ...) -> _CF: ...
@overload
def drop(n: int, seqs: Sequence) -> Sequence: ...
@overload
def drop(n: int) -> Callable[[Sequence], Sequence]: ...

def tail(n: int, iterable: Iterable = ...) -> _CF: ...
def tabulate(f: Callable, start: int = ...) -> Iterable: ...
def consume(n: int, iterator: Iterable): ...

def nth(idx: Union[str, int], iterable: Iterable = ...) -> _CF: ...

def nth_or_last(n: int, iterable: Iterable = ..., default = ...) -> _CF: ...

def iterate(f: Callable, start: int = ...) -> _CF: ...
    # (f, start) -> start, f(start), f(f(start)), ...

def split_at(pred: Callable[..., bool], iterable: Iterable = ...,
             maxsplit: int = ..., keep_separator: bool = ...) -> _CF: ...
def split_before(pred: Callable[..., bool], iterable: Iterable = ..., maxsplit: int = ...) -> _CF: ...
def split_after(pred: Callable[..., bool], iterable: Iterable = ..., maxsplit: int = ...) -> _CF: ...
def split_when(pred: Callable[..., bool], iterable: Iterable = ..., maxsplit: int = ...) -> _CF: ...
def split_into(sizes: Iterable[int], iterable: Iterable = ...) -> _CF: ...
def distribute(n: int, iterable: Iterable = ...) -> _CF: ...
    # distribute(2, [1, 2, 3, 4, 5, 6]) -> (1, 3, 5), (2, 4, 6)

def adjacent(pred: Callable[..., bool], iterable: Iterable = ..., distance: int = ...) -> _CF: ...
    # >>> list(adjacent(lambda x: x == 3, range(6)))
    # [(False, 0), (False, 1), (True, 2), (True, 3), (True, 4), (False, 5)]

def locate(pred: Callable[..., bool], iterable: Iterable = ...,
           window_size: Optional[int] = ...) -> _CF:
    """
         >>> list(locate(bool, [0, 1, 1, 0, 1, 0, 0]))
         [1, 2, 4]
    """
    ...


def lstrip_f(pred: Callable[..., bool], iterable: Iterable = ...) -> _CF:
    """
         >>> iterable = (None, False, None, 1, 2, None, 3, False, None)
         >>> pred = lambda x: x in {None, False, ''}
         >>> list(lstrip_f(pred, iterable))
         [1, 2, None, 3, False, None]
    """
    ...

def rstrip_f(pred: Callable[..., bool], iterable: Iterable = ...) -> _CF:
    """
         >>> iterable = (None, False, None, 1, 2, None, 3, False, None)
         >>> pred = lambda x: x in {None, False, ''}
         >>> list(rstrip_f(pred, iterable))
         [None, False, None, 1, 2, None, 3]
    """
    ...

def strip_f(pred: Callable[..., bool], iterable: Iterable = ...):
    """ more_itertools.strip
        >>> iterable = (None, False, None, 1, 2, None, 3, False, None)
        >>> pred = lambda x: x in {None, False, ''}
        >>> list(strip_f(pred, iterable))
        [1, 2, None, 3]
    """
    ...


def all_eq(iterable: Iterable) -> bool:
    """ more_itertools.all_equal
        >>> all_eq('aaaa')
        True
        >>> all_eq('aaab')
        False
    """
    ...


def quantify(pred: Callable[..., bool], iterable: Iterable = ...) -> _CF:
    """ more_itertools.quantify
        >>> quantify(bool, [True, False, True])
        2
    """
    ...

def ncycles(n: int, iterable: Iterable = ...) -> _CF:
    """
        >>> list(ncycles(e, ["a", "b"])
        ['a', 'b', 'a', 'b', 'a', 'b']
    """
    ...

def dotproduct(vec1: Iterable, vec2: Iterable = ...) -> _CF:
    """
        >>> dotproduct([10, 10], [20, 20])
        400
    """
    ...


def grouper(n: int, iterable: Iterable = ..., fillvalue: Any = ...) -> _CF:
    """
        >>> list(grouper('ABCDEFG', 3, 'x'))
        [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]
    """
    ...


def partition_f(pred: Callable[..., bool], iterable: Iterable = ...) -> _CF:
    """
        >>> is_odd = lambda x: x % 2 != 0
        >>> iterable = range(10)
        >>> even_items, odd_items = partition_f(is_odd, iterable)
        >>> list(even_items), list(odd_items)
        ([0, 2, 4, 6, 8], [1, 3, 5, 7, 9])

    If *pred* is None, :func:`bool` is used.

        >>> iterable = [0, 1, False, True, '', ' ']
        >>> false_items, true_items = partition_f(None, iterable)
        >>> list(false_items), list(true_items)
        ([0, False, ''], [1, True, ' '])
    """
    ...


def unique_set(iterable: Iterable, key: Optional[Callable] = None) -> Iterable:
    """
        >>> list(unique_set('AAAABBBCCDAABBB'))
        ['A', 'B', 'C', 'D']
        >>> list(unique_set('ABBCcAD', str.lower))
        ['A', 'B', 'C', 'D']
    """
    ...


def iter_except(f: Callable, exception: Iterable[Exception],
                first: Optional[Callable] = ...) -> Iterable:
    """
        >>> l = [0, 1, 2]
        >>> list(iter_except(l.pop, IndexError))
        [2, 1, 0]
    """
    ...


def zip_eq(*iterables: Iterable) -> Iterable: ...

def find_true(pred: Callable[..., bool], iterable: Iterable = ...) -> _CF: ...

def diff(s1: Sequence, s2: Sequence) -> Tuple: ...
def startswith(prefix: Any, s: Sequence, start: Any=..., end: Any=...) -> bool: ...
def endswith(suffix: Any, s: Sequence, start: Any=..., end: Any=...) -> bool: ...
def symdiff(func: Callable, seq1: Sequence, seq2: Sequence) -> Tuple: ...
