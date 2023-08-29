from typing import Any, Self
from collections.abc import Mapping
import warnings

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Relationship

from parsnip.sqlalchemy_api._exceptions import MissingForeignKeyDictMixinError
from parsnip.sqlalchemy_api._typing import Property
from parsnip.sqlalchemy_api.data_containers import SqlAlchemyField
from parsnip.sqlalchemy_api.helpers import fields_dict_old


def _get_foreign_key_col(property: Property) -> Column:
    if len(property.local_columns) > 1:
        warnings.warn(
            f'More than one local column present for column: {property.key}. '
            'This could cause unexpected behaviour.',
            RuntimeWarning,
        )
    return next(iter(property.local_columns))


def _get_foreign_key(column: Column) -> ForeignKey:
    if len(column.foreign_keys) > 1:
        warnings.warn(
            'More than one foreign key present '
            f'for column: {column.name}. '
            'This could cause unexpected behaviour.',
            RuntimeWarning,
        )
    return next(iter(column.foreign_keys))


class SqlAlchemyDictMixin:
    @staticmethod
    def _get_field_from_relationship(attr_val: Any, field: SqlAlchemyField):
        foreign_key_col = _get_foreign_key_col(field.property)
        foreign_key = _get_foreign_key(foreign_key_col)
        foreign_key_id = (
            attr_val.get(foreign_key.column.name)
            if isinstance(attr_val, dict)
            else getattr(attr_val, foreign_key.column.name, None)
        )
        if foreign_key_id is not None:
            return SqlAlchemyField(foreign_key_col.name, value=foreign_key_id)

        foreign_key_cls = field.property.entity.class_
        if isinstance(attr_val, dict):
            try:
                return SqlAlchemyField(
                    field.name,
                    value=foreign_key_cls.from_dict(attr_val),
                )
            except AttributeError as exception:
                raise MissingForeignKeyDictMixinError(foreign_key_cls)
        try:
            return SqlAlchemyField(
                field.name,
                value=foreign_key_cls.from_dict(attr_val.to_dict(deep=False)),
            )
        except AttributeError as exception:
            raise MissingForeignKeyDictMixinError(foreign_key_cls)
        except TypeError as exception:
            raise exception(
                'All inputs for foreign key classes must either '
                'be of type: dict, or define a "to_dict" method.'
            )

    @classmethod
    def _get_instance_field(cls, attr_val: Any, field: SqlAlchemyField):
        if isinstance(field.property, Relationship):
            return cls._get_field_from_relationship(attr_val, field)
        return SqlAlchemyField(field.name, value=attr_val)

    @classmethod
    def from_dict(cls, obj: Mapping) -> Self:
        fields_dict = fields_dict(cls)

        model_attrs = {}
        for attr_name, attr_val in obj.items():
            field = fields_dict.get(attr_name)
            if field is None:
                warnings.warn(
                    f'Key: {attr_name}, '
                    f'not a recognised field in class: {cls.__name__}. '
                    'Remove this key from input to avoid this warning.',
                    RuntimeWarning,
                )
                continue
            new_field = cls._get_instance_field(attr_val=attr_val, field=field)
            model_attrs[new_field.name] = new_field.value

        return cls(**model_attrs)

    def to_dict(self) -> dict[str, Any]:
        fields_dict = fields_dict(self)
        return {name: field.value for name, field in fields_dict.items()}
