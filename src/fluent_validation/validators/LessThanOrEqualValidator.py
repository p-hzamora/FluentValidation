from typing import Callable, overload, override
from fluent_validation.validators.AbstractComparisonValidator import (
    AbstractComparisonValidator,
    Comparison,
)


class LessThanOrEqualValidator[T, TProperty](AbstractComparisonValidator[T, TProperty]):
    @overload
    def __init__(self, value: TProperty): ...

    @overload
    def __init__(self, valueToCompareFunc: Callable[[T], TProperty], memberDisplayName: str): ...

    @overload
    def __init__(
        self,
        valueToCompareFunc: Callable[[T], tuple[bool, TProperty]],
        memberDisplayName: str,
    ): ...

    def __init__(self, value=None, valueToCompareFunc=None, memberDisplayName=None):
        super().__init__(
            valueToCompareFunc=valueToCompareFunc,
            memberDisplayName=memberDisplayName,
            value=value,
        )

    @override
    @property
    def Comparison(self) -> Comparison:
        return Comparison.LessThanOrEqual

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)
