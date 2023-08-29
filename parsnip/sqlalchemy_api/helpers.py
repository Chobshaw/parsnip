from typing import get_type_hints
from sqlalchemy.orm import (
    DeclarativeBase,
    Composite,
)

from .data_containers import SqlAlchemyField
from .dtypes import is_sqlalchemy_class


def fields_dict(
    class_or_instance: type[DeclarativeBase] | DeclarativeBase,
    *,
    include_composites: bool = False
) -> dict[str, SqlAlchemyField]:
    if not is_sqlalchemy_class(class_or_instance):
        raise TypeError(
            'Must inherit from, or be an instance of DeclarativeBase.'
        )

    cls = (
        class_or_instance
        if isinstance(class_or_instance, type)
        else type(class_or_instance)
    )

    type_hints = get_type_hints(cls)
    composite_field_components = []

    fields_dict = {}
    for name, type_hint in type_hints.items():
        property = getattr(cls, name).property
        if isinstance(property, Composite):
            composite_field_components.extend(property.attrs)
        fields_dict[name] = SqlAlchemyField(
            name, type=type_hint, property=property
        )

    if not include_composites:
        for name in composite_field_components:
            fields_dict.pop(name)

    return fields_dict


def fields(
    class_or_instance: type[DeclarativeBase] | DeclarativeBase,
    *,
    include_composites: bool = False
) -> tuple[SqlAlchemyField, ...]:
    return tuple(
        field
        for field in fields_dict(
            class_or_instance, include_composites=include_composites
        ).values()
    )
