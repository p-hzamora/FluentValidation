from abc import abstractmethod
from enum import Enum, auto
from typing import Any, Callable, overload, override

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.IValidationContext import ValidationContext

from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.validators.IpropertyValidator import IPropertyValidator_no_generic


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
    less_than = auto()
    LessThanOrEqual = auto()
    equal = auto()
    not_equal = auto()
    greater_than = auto()
    GreaterThanOrEqual = auto()


class IComparisonValidator(IPropertyValidator_no_generic):
    @property
    @abstractmethod
    def Comparison(self) -> Comparison: ...

    @property
    @abstractmethod
    def MemberToCompare(self) -> MemberInfo: ...

    @property
    @abstractmethod
    def ValueToCompare(self) -> Any: ...


class AbstractComparisonValidator[T, TProperty](PropertyValidator[T, TProperty], IComparisonValidator):
    @overload
    def __init__(self, value: TProperty): ...

    @overload
    def __init__(self, valueToCompareFunc: Callable[[T], TProperty], member: MemberInfo, memberDisplayName: str): ...

    @overload
    def __init__(self, valueToCompareFunc: Callable[[T], tuple[bool, TProperty]], member: MemberInfo, memberDisplayName: str): ...

    def __init__(self, valueToCompareFunc=None, member=None, memberDisplayName=None, value=None):
        self._valueToCompareFuncForNullables: Callable[[T], tuple[bool, TProperty]] = None
        self._valueToCompareFunc: Callable[[T], TProperty] = None
        self._comparisonMemberDisplayName: str = None
        self._MemberToCompare: MemberInfo = member

        if valueToCompareFunc is None and memberDisplayName is None and value is not None:
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
            # If you want to ensure that it's never null then a not_null rule should also be applied.
            return True

        valueToCompare = self.GetComparisonValue(context)

        if not valueToCompare[0] or not self._is_valid(propertyValue, valueToCompare[1]):
            context.MessageFormatter.AppendArgument("ComparisonValue", valueToCompare[1] if valueToCompare[0] else "")
            context.MessageFormatter.AppendArgument("ComparisonProperty", self._comparisonMemberDisplayName if self._comparisonMemberDisplayName is not None else "")
            return False
        return True

    def GetComparisonValue(self, context: ValidationContext[T]) -> tuple[bool, TProperty]:
        if self._valueToCompareFunc is not None:
            value = self._valueToCompareFunc(context.instance_to_validate)
            return (value is not None, value)
        if self._valueToCompareFuncForNullables is not None:
            return self._valueToCompareFuncForNullables(context.instance_to_validate)

        return (self.ValueToCompare is not None, self.ValueToCompare)

    def _is_valid(self, value: TProperty, valueToCompare: TProperty) -> bool:
        dicc = {
            Comparison.less_than: Comparable(value) < Comparable(valueToCompare),
            Comparison.LessThanOrEqual: Comparable(value) <= Comparable(valueToCompare),
            Comparison.equal: Comparable(value) == Comparable(valueToCompare),
            Comparison.not_equal: Comparable(value) != Comparable(valueToCompare),
            Comparison.greater_than: Comparable(value) > Comparable(valueToCompare),
            Comparison.GreaterThanOrEqual: Comparable(value) >= Comparable(valueToCompare),
        }
        if valueToCompare is None:
            return False
        return dicc[self.Comparison]

    @property
    @abstractmethod
    def Comparison(self) -> Comparison:
        """
        Propiedad indispensable en aquellas clases que hereden de AbstractComparisonValidator
        - Comparison.less_than           : value < valueToCompare
        - Comparison.LessThanOrEqual    : value <= valueToCompare
        - Comparison.equal              : value == valueToCompare
        - Comparison.not_equal           : value != valueToCompare
        - Comparison.greater_than        : value > valueToCompare
        - Comparison.GreaterThanOrEqual : value >= valueToCompare
        """
        ...

    @property
    def ValueToCompare(self) -> TProperty:
        return self._valueToCompare

    @ValueToCompare.setter
    def ValueToCompare(self, value):
        self._valueToCompareFunc = lambda _: value

    @property
    def MemberToCompare(self) -> MemberInfo:
        return self._MemberToCompare
