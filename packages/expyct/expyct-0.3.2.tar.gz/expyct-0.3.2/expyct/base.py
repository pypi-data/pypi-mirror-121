import abc
import inspect
import typing
from dataclasses import dataclass

T = typing.TypeVar("T")


@dataclass
class MapBefore:
    """Mixing for applying a function before checking equality.

    Attributes:
        map_before : the mapping function to apply
    """

    map_before: typing.Optional[typing.Callable] = None

    def map(self, other):
        if self.map_before:
            return self.map_before(other)
        else:
            return other


@dataclass
class Satisfies:
    """Mixin for checking equality by using a predicate function.

    If `satisfies(obj)` returns `True`, then it is equal.

    Attributes:
        satisfies : object must satisfy predicate
    """

    satisfies: typing.Optional[typing.Callable[[typing.Any], bool]] = None

    def __eq__(self, other):
        if self.satisfies:
            try:
                return self.satisfies(other)
            except Exception:
                return False
        return True


@dataclass
class Equals(typing.Generic[T]):
    """Mixin for checking equality using a specific object to compare against.

    Attributes:
        equals : the object to check equality with
    """

    equals: typing.Optional[T] = None

    def __eq__(self, other):
        if self.equals is not None:
            if not other == self.equals:
                return False
        return True


@dataclass
class Vars:
    """Mixin for checking the presence of specific object attributes.

    The attributes are compared as a dict. So anything that can be compared
    with a dict can be used as `vars` argument, including other expyct objects like `expyct.Dict`.

    Attributes:
        vars : object attributes (result of `vars()`) must equal
    """

    vars: typing.Optional[typing.Any] = None

    def __eq__(self, other):
        if self.vars is not None:
            if not vars(other) == self.vars:
                return False
        return True


@dataclass
class Optional:
    """Mixin for matching with `None`.

    Attributes:
        optional : whether `None` is allowed
    """

    optional: typing.Optional[bool] = None

    def __eq__(self, other):
        if other is None:
            if self.optional is not None:
                return self.optional is True
            else:
                return False
        return True


@dataclass
class Instance:
    """Match any object that is a class instance.

    Attributes:
        type : type of object must equal to given type
        instance_of : object must be an instance of given type
    """

    type: typing.Optional[typing.Type] = None
    instance_of: typing.Optional[typing.Type] = None

    def __eq__(self, other):
        # TODO check
        if (
            inspect.ismodule(other)
            or inspect.isclass(other)
            or inspect.isfunction(other)
            or inspect.ismethod(other)
        ):
            return False
        if self.type and type(other) != self.type:
            return False
        if self.instance_of and not isinstance(other, self.instance_of):
            return False
        return True


@dataclass
class Type:
    """Match any object that is a type.

    Attributes:
        superclass_of : the type of which the matched object must be a superclass
        subclass_of : the type of which the matched object must be a subclass
    """

    superclass_of: typing.Optional[typing.Type] = None
    subclass_of: typing.Optional[typing.Type] = None

    def __eq__(self, other):
        if not (type(other) == type or type(other) == abc.ABCMeta):
            return False
        if self.superclass_of and not issubclass(self.superclass_of, other):
            return False
        if self.subclass_of and not issubclass(other, self.subclass_of):
            return False
        return True
