from collections.abc import Mapping

from types import NoneType
from typing import Any, NewType, Self, Union, get_args, get_origin
import warnings

from .helpers import fields_dict, asdict
from .dtypes import get_enum, is_enum


def has_dict_mixin(obj: Any) -> bool:
    return issubclass(obj, DictMixin) or isinstance(obj, DictMixin)


def _get_attribute(field_val: Any, field_type: type) -> Any:
    if field_type is None:
        return field_val
    if field_type is NoneType and field_val is not None:
        raise TypeError(
            f'Value: {field_val}, cannot be coerced to type: NoneType.'
        )
    if isinstance(field_val, field_type):
        return field_val
    if get_origin(field_type) == Union:
        for arg in get_args(field_type):
            try:
                return _get_attribute(field_val, arg)
            except TypeError:
                continue
    if isinstance(field_type, NewType):
        return _get_attribute(field_val, field_type.__supertype__)
    if has_dict_mixin(field_type):
        return field_type.from_dict(field_val)
    if is_enum(field_type):
        return get_enum(field_val, field_type)
    if isinstance(field_val, Mapping):
        return field_type(**field_val)
    return field_type(field_val)


class DictMixin:
    @classmethod
    def from_dict(cls, obj: Mapping, *, aliased: bool = False) -> Self:
        cls_fields_dict = fields_dict(cls, aliased=aliased)
        attributes = {}
        for attr_name, attr_val in obj.items():
            field = cls_fields_dict.get(attr_name)
            if field is None:
                warnings.warn(
                    f'Key: {attr_name}, '
                    f'not a recognised field in class: {cls.__name__}. '
                    'Remove this key from input to avoid this warning.',
                    RuntimeWarning,
                )
                continue
            if not field.init:
                continue
            attributes[attr_name] = _get_attribute(attr_val, field.type)
        return cls(**attributes)

    def to_dict(self, deep: bool = True) -> dict:
        return asdict(self, deep=deep)
