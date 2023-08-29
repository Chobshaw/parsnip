import dataclasses
from typing import Optional, Self

import attrs


class Field:
    __slots__ = ('name', 'type', 'init', 'alias')

    def __init__(
        self,
        name: str,
        type: Optional[type] = None,
        init: bool = True,
        alias: Optional[str] = None,
    ) -> None:
        self.name = name
        self.type = type
        self.init = init
        self.alias = alias if alias is not None else name

    @classmethod
    def from_foreign_field(
        cls, field: dataclasses.Field | attrs.Attribute
    ) -> Self:
        alias = field.alias if isinstance(field, attrs.Attribute) else None
        return cls(field.name, field.type, field.init, alias)
