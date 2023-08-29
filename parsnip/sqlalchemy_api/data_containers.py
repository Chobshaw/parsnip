from typing import Optional

from ._typing import Property
from parsnip.data_containers import Field


class SqlAlchemyField(Field):
    __slots__ = ('property',)

    def __init__(
        self,
        name: str,
        type: Optional[type] = None,
        property: Optional[Property] = None,
    ) -> None:
        super().__init__(name, type)
        self.property = property
