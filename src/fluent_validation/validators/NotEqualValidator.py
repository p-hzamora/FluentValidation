from typing import Callable, override

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.validators.AbstractComparisonValidator import Comparison

from .EqualValidator import EqualValidator, IEqualityComparer


class NotEqualValidator[T, TProperty](EqualValidator[T, TProperty]):
    def __init__(
        self,
        valueToCompare: TProperty = None,
        comparer: IEqualityComparer[TProperty] = None,
        comparisonProperty: Callable[[T], TProperty] = None,
        member: MemberInfo = None,
        memberDisplayName: str = None,
    ):
        super().__init__(
            valueToCompare,
            comparer,
            comparisonProperty,
            member,
            memberDisplayName,
        )

    @override
    @property
    def Comparison(self) -> Comparison:
        return Comparison.not_equal

    def Compare(self, comparisonValue: TProperty, propertyValue: TProperty) -> bool:
        return not super().Compare(comparisonValue, propertyValue)
