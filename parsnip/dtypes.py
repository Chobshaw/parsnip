from enum import Enum, EnumType

from typing import Any


def is_enum(obj: Any) -> bool:
    return issubclass(obj, Enum) or isinstance(obj, Enum)


def get_enum(val: Any, enum_cls: EnumType) -> Enum:
    try:
        return enum_cls(val)
    except ValueError as exception:
        return enum_cls[val]
    except KeyError:
        raise exception
