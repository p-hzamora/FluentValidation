from abc import abstractmethod
from enum import Enum, auto
from typing import Callable, overload, override
from ..IValidationContext import ValidationContext

from ..validators.PropertyValidator import PropertyValidator
from ..validators.IpropertyValidator import IPropertyValidator


class Comparable(object):
    def __init__(self, value):
        self._value = value

    def __lt__(self, __value: "Comparable") -> bool:
        return self._value < __value._value

    def __le__(self, __value: "Comparable") -> bool:
        return self._value <= __value._value

    def __eq__(self, __value: "Comparable") -> bool:
        return self._value == __value._value

    def __nq__(self, __value: "Comparable") -> bool:
        return self._value != __value._value

    def __gt__(self, __value: "Comparable") -> bool:
        return self._value > __value._value

    def __ge__(self, __value: "Comparable") -> bool:
        return self._value >= __value._value


class Comparison(Enum):
    LessThan = auto()
    LessThanOrEqual = auto()
    Equal = auto()
    NotEqual = auto()
    GreaterThan = auto()
    GreaterThanOrEqual = auto()


class IComparisonValidator(IPropertyValidator):
    @property
    @abstractmethod
    def Comparison(self) -> Comparison:
        ...

    @property
    @abstractmethod
    def ValueToCompare(self) -> object:
        ...


class AbstractComparisonValidator[T, TProperty](
    PropertyValidator[T, TProperty], IComparisonValidator
):
    @overload
    def __init__(self, value: TProperty):
        ...

    @overload
    def __init__(
        self, valueToCompareFunc: Callable[[T], TProperty], memberDisplayName: str
    ):
        ...

    @overload
    def __init__(
        self,
        valueToCompareFunc: Callable[[T], tuple[bool, TProperty]],
        memberDisplayName: str,
    ):
        ...

    def __init__(self, valueToCompareFunc=None, memberDisplayName=None, value=None):
        self._valueToCompareFuncForNullables: Callable[
            [T], tuple[bool, TProperty]
        ] = None
        self._valueToCompareFunc: Callable[[T], TProperty] = None
        self._comparisonMemberDisplayName: str = None

        if (
            valueToCompareFunc is None
            and memberDisplayName is None
            and value is not None
        ):
            self._valueToCompare = value

        elif callable(valueToCompareFunc):
            self._valueToCompareFunc = valueToCompareFunc
            self._comparisonMemberDisplayName = memberDisplayName

        else:
            self._valueToCompareFuncForNullables = valueToCompareFunc
            self._comparisonMemberDisplayName = memberDisplayName

    @override
    def is_valid(self, context: ValidationContext[T], propertyValue: TProperty) -> bool:
        if propertyValue is None:
            # If we're working with a nullable type then this rule should not be applied.
            # If you want to ensure that it's never null then a NotNull rule should also be applied.
            return True

        valueToCompare = self.GetComparisonValue(context)

        if not valueToCompare[0] or not self._is_valid(
            propertyValue, valueToCompare[1]
        ):
            context.MessageFormatter.AppendArgument(
                "ComparisonValue", valueToCompare[1] if valueToCompare[0] else ""
            )
            context.MessageFormatter.AppendArgument(
                "ComparisonProperty",
                self._comparisonMemberDisplayName
                if self._comparisonMemberDisplayName is not None
                else context.PropertyPath,
            )
            return False
        return True

    def GetComparisonValue(
        self, context: ValidationContext[T]
    ) -> tuple[bool, TProperty]:
        if self._valueToCompareFunc is not None:
            value = self._valueToCompareFunc(context.instance_to_validate)
            return (value is not None, value)
        if self._valueToCompareFuncForNullables is not None:
            return self._valueToCompareFuncForNullables(context.instance_to_validate)

        return (self.ValueToCompare is not None, self.ValueToCompare)

    def _is_valid(self, value: TProperty, valueToCompare: TProperty) -> bool:
        dicc = {
            Comparison.LessThan: Comparable(value) < Comparable(valueToCompare),
            Comparison.LessThanOrEqual: Comparable(value) <= Comparable(valueToCompare),
            Comparison.Equal: Comparable(value) == Comparable(valueToCompare),
            Comparison.NotEqual: Comparable(value) != Comparable(valueToCompare),
            Comparison.GreaterThan: Comparable(value) > Comparable(valueToCompare),
            Comparison.GreaterThanOrEqual: Comparable(value)
            >= Comparable(valueToCompare),
        }
        if valueToCompare is None:
            return False
        return dicc[self.Comparison]

    @property
    @abstractmethod
    def Comparison(self) -> Comparison:
        """
        Propiedad indispensable en aquellas clases que hereden de AbstractComparisonValidator
        - Comparison.LessThan           : value < valueToCompare
        - Comparison.LessThanOrEqual    : value <= valueToCompare
        - Comparison.Equal              : value == valueToCompare
        - Comparison.NotEqual           : value != valueToCompare
        - Comparison.GreaterThan        : value > valueToCompare
        - Comparison.GreaterThanOrEqual : value >= valueToCompare
        """
        ...

    @property
    def ValueToCompare(self) -> TProperty:
        return self._valueToCompare
        

    @ValueToCompare.setter
    def ValueToCompare(self, value):
        self._valueToCompareFunc = lambda _: value