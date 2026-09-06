#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 07 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|
"""
Debug module containing a wide variety of Python object types
to stress-test Sphinx ``autodoc`` and ``sphinx_localtoc`` discovery.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum, Flag, auto
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Protocol,
    TypedDict,
    TypeAlias,
    Generic,
    TypeVar,
)
from contextlib import contextmanager
from abc import ABC, ABCMeta, abstractmethod

# ------------------------------------------------------------
# Module-level constants
# ------------------------------------------------------------

PI = 3.14159
DEBUG_ENABLED: bool = True
MAX_ITEMS: int = 100

__all__ = [
    "PI",
    "DEBUG_ENABLED",
    "MAX_ITEMS",
]

# ------------------------------------------------------------
# Type aliases
# ------------------------------------------------------------

JSON: TypeAlias = dict[str, Any]
Callback: TypeAlias = Callable[[int], str]

T = TypeVar("T")

# ------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------

class DebugError(Exception):
    """Base debug exception."""


class FatalDebugError(DebugError):
    """Fatal error."""


# ------------------------------------------------------------
# Enums
# ------------------------------------------------------------

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Status(IntEnum):
    OK = 0
    WARNING = 1
    ERROR = 2


class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


# ------------------------------------------------------------
# Protocols and TypedDicts
# ------------------------------------------------------------

class SupportsClose(Protocol):
    def close(self) -> None: ...


class UserDict(TypedDict):
    id: int
    name: str
    active: bool


# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------

def simple_function(x: int, y: int = 0) -> int:
    """Simple function with defaults."""
    return x + y


async def async_function(delay: float) -> str:
    """Async function."""
    return f"Delayed by {delay}"


def generator_function(n: int) -> Iterator[int]:
    """Generator function."""
    for i in range(n):
        yield i


lambda_function = lambda x: x * 2  # noqa: E731


@contextmanager
def managed_resource() -> Iterator[str]:
    """Context manager function."""
    yield "resource"


# ------------------------------------------------------------
# Decorators
# ------------------------------------------------------------

def debug_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """Simple decorator."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


# ------------------------------------------------------------
# Classes
# ------------------------------------------------------------

class BaseClass(ABC):
    """Abstract base class."""

    @abstractmethod
    def run(self) -> None:
        """Run the object."""


class MetaClass(ABCMeta):
    """Custom metaclass."""
    pass


class ComplexClass(BaseClass, metaclass=MetaClass):
    """Complex class with many members."""

    class NestedClass:
        """Nested inner class."""
        value = 42

    CLASS_CONSTANT = "CONST"

    def __init__(self, name: str):
        self._name = name

    def run(self) -> None:
        """Concrete implementation."""
        pass

    def instance_method(self, value: int) -> int:
        """Instance method."""
        return value * 2

    @classmethod
    def class_method(cls) -> str:
        """Class method."""
        return cls.__name__

    @staticmethod
    def static_method() -> str:
        """Static method."""
        return "static"

    @property
    def name(self) -> str:
        """Property getter."""
        return self._name

    def __repr__(self) -> str:
        return f"<RegularClass name={self._name!r}>"


# ------------------------------------------------------------
# Dataclasses
# ------------------------------------------------------------

@dataclass
class DataClassExample:
    """Dataclass with defaults and factory."""
    id: int
    tags: list[str] = field(default_factory=list)
    active: bool = True


# ------------------------------------------------------------
# Generic classes
# ------------------------------------------------------------

class Box(Generic[T]):
    """Generic container."""

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value


# ------------------------------------------------------------
# Callable object
# ------------------------------------------------------------

class CallableObject:
    """Instance is callable."""

    def __call__(self, x: int) -> int:
        return x + 1


# ------------------------------------------------------------
# Iterator / Iterable
# ------------------------------------------------------------

class Counter(Iterable[int]):
    """Custom iterable."""

    def __init__(self, limit: int):
        self.limit = limit

    def __iter__(self) -> Iterator[int]:
        for i in range(self.limit):
            yield i


# ------------------------------------------------------------
# Private objects (should be detected but marked private)
# ------------------------------------------------------------

def _private_function() -> None:
    pass


class _PrivateClass:
    pass
