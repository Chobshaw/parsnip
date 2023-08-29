from typing import Any


class MissingForeignKeyDictMixinError(AttributeError):
    def __init__(self, obj: Any) -> None:
        super().__init__(
            f'{obj.__name__} object has no attribute "from_dict". '
            'All foreign key classes must also have '
            'the SqlAlchemyDictMixin or define a "from_dict" method.'
        )
