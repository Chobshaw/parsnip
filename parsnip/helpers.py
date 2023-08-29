import dataclasses
import inspect
from typing import Any, get_type_hints

import attrs

from parsnip.data_containers import Field


def asdict(
    instance: Any, *, deep: bool = True, flatten: bool = False
) -> dict[str, Any]:
    # TODO: Add legacy class and flatten implementation
    if dataclasses.is_dataclass(instance):
        if not deep:
            return dict(
                (field.name, getattr(instance, field.name))
                for field in dataclasses.fields(instance)
            )
        return dataclasses.asdict(instance)
    if attrs.has(instance):
        return attrs.asdict(instance, recurse=deep)
    raise TypeError(f'Object: {instance}, not a dataclass or an attrs class.')


def _get_class_fields_dict(cls: type) -> dict[str, Field]:
    type_hints = get_type_hints(cls)
    if hasattr(cls, '__init__'):
        for key, val in inspect.signature(
            getattr(cls, '__init__')
        ).parameters.items():
            if key == 'self' or key in type_hints:
                continue
            type_hints[key] = (
                val.annotation if val.annotation != inspect._empty else None
            )
    return {
        name: Field(name=name, type=type_hint)
        for name, type_hint in type_hints.items()
    }


def fields(obj: type | Any) -> tuple[Field, ...]:
    if dataclasses.is_dataclass(obj):
        fields = dataclasses.fields(obj)
    elif attrs.has(obj):
        fields = attrs.fields(obj)
    else:
        raise TypeError(f'Object: {obj}, not a dataclass or an attrs class.')
    return (Field.from_foreign_field(field) for field in fields)


def fields_dict(obj: type | Any, *, aliased: bool = False) -> dict[str, Field]:
    if aliased:
        return {field.alias: field for field in fields(obj)}
    return {field.name: field for field in fields(obj)}
