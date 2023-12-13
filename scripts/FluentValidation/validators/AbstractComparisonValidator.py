from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, overload, override
from stc.common.scripts.FluentValidation.IValidationContext import ValidationContext

from stc.common.scripts.FluentValidation.validators.PropertyValidator import PropertyValidator
from stc.common.scripts.FluentValidation.validators.IpropertyValidator import IPropertyValidator

IComparable = TypeVar("IComparable",bound="Comparable")

class Comparable(object):
    def __init__(self, value):
        self._value = value

    def __lt__(self, __value: IComparable) -> bool:
        return self._value < __value._value

    def __le__(self, __value: IComparable) -> bool:
        return self._value <= __value._value

    def __eq__(self, __value: IComparable) -> bool:
        return self._value == __value._value

    def __nq__(self, __value: IComparable) -> bool:
        return self._value != __value._value

    def __gt__(self, __value: IComparable) -> bool:
        return self._value > __value._value

    def __ge__(self, __value: IComparable) -> bool:
        return self._value >= __value._value

    

class Comparison(Enum):
    Equal = 1
    NotEqual = 2
    LessThan = 3
    GreaterThan = 4
    GreaterThanOrEqual = 5
    LessThanOrEqual = 6


class IComparisonValidator(IPropertyValidator):
    @property
    @abstractmethod
    def Comparison(self)->Comparison: ...
    @property
    @abstractmethod
    def MemberToCompare(self)-> MemberInfo: ...
    @property
    @abstractmethod
    def ValueToCompare(self)-> object: ...


class AbstractComparisonValidator[T, TProperty](PropertyValidator[T,TProperty], IComparisonValidator):
    @overload
    def __init__(self, value:TProperty): ...
    @overload
    def __init__(self, valueToCompareFunc:Callable[[T], TProperty], member:MemberInfo, memberDisplayName:str): ...
    @overload
    def __init__(self, valueToCompareFunc:Callable[[T], tuple[bool, TProperty]], member:MemberInfo, memberDisplayName:str): ...



    def __init__(self
            , valueToCompareFunc= None
            , member= None
            , memberDisplayName= None
            , value= None
            ):
        self._valueToCompareFuncForNullables:Callable[[T], tuple[bool,TProperty]]
        self._valueToCompareFunc:Callable[[T], TProperty]
        self._comparisonMemberDisplayName:str

        if  valueToCompareFunc is None and  \
            member is None and \
            memberDisplayName is None and \
            value is not None:
            self.ValueToCompare = value
        
        elif isinstance(valueToCompareFunc(), tuple):
            self._valueToCompareFuncForNullables = valueToCompareFunc
            self._comparisonMemberDisplayName = memberDisplayName
            self.MemberToCompare = member

        else:
            self._valueToCompareFunc = valueToCompareFunc
            self._comparisonMemberDisplayName = memberDisplayName
            self.MemberToCompare = member


    @override
    def is_valid(self, context:ValidationContext[T], propertyValue:TProperty)->bool:
        if propertyValue is None:
            # If we're working with a nullable type then this rule should not be applied.
            # If you want to ensure that it's never null then a NotNull rule should also be applied.
            return True

        valueToCompare = self.GetComparisonValue(context)

        if not valueToCompare[0] or not self.IsValid(propertyValue, valueToCompare[1]):
            context.MessageFormatter.AppendArgument("ComparisonValue", valueToCompare[1] if valueToCompare[0] else "")
            context.MessageFormatter.AppendArgument("ComparisonProperty", self._comparisonMemberDisplayName if self._comparisonMemberDisplayName is not None else "")
            return False
        return True


    def GetComparisonValue(self, context:ValidationContext[T])->tuple[bool, TProperty]:
        if self._valueToCompareFunc is not None:
            value = self._valueToCompareFunc(context.instance_to_validate)
            return (value is not None, value)
        if self._valueToCompareFuncForNullables is not None:
            return self._valueToCompareFuncForNullables(context.instance_to_validate)

        return (self.ValueToCompare is not None, self.ValueToCompare)

    @abstractmethod
    def is_valid(value:TProperty , valueToCompare:TProperty)->bool: ...

    @property
    @abstractmethod
    def Comparison(self)->Comparison: ...
    
    @property
    def MemberToCompare(self)->MemberInfo: self._MemberInfo

    @property
    def ValueToCompare(self)->TProperty: self._TProperty
    @ValueToCompare.setter
    def ValueToCompare(self, value): self._valueToCompareFunc = lambda: value
