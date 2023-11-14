'''from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable

from stc.common.scripts.FluentValidation.validators import PropertyValidator
from stc.common.scripts.FluentValidation.validators.IpropertyValidator import IPropertyValidator

class MemberInfo():
	pass


class Comparison(Enum):
    Equal = 1
    NotEqual = 2
    LessThan = 3
    GreaterThan = 4
    GreaterThanOrEqual = 5
    LessThanOrEqual = 6


class IComparisonValidator(IPropertyValidator):
    Comparison: Comparison
    MemberToCompare: MemberInfo
    ValueToCompare: object


class AbstractComparisonValidator[T, TProperty](PropertyValidator[T,TProperty], IComparisonValidator):
    _valueToCompareFuncForNullables:Callable[[T], tuple[bool,TProperty]]
    private readonly Func[T, TProperty] _valueToCompareFunc;
    private readonly string _comparisonMemberDisplayName;

    protected AbstractComparisonValidator(TProperty value) {
        value.Guard("value must not be null.", nameof(value));
        ValueToCompare = value;
    }

    protected AbstractComparisonValidator(Func[T, (bool HasValue, TProperty Value)] valueToCompareFunc, MemberInfo member, string memberDisplayName) {
        _valueToCompareFuncForNullables = valueToCompareFunc;
        _comparisonMemberDisplayName = memberDisplayName;
        MemberToCompare = member;
    }

    protected AbstractComparisonValidator(Func[T, TProperty] valueToCompareFunc, MemberInfo member, string memberDisplayName) {
        _valueToCompareFunc = valueToCompareFunc;
        _comparisonMemberDisplayName = memberDisplayName;
        MemberToCompare = member;
    }

    public sealed override bool IsValid(ValidationContext[T] context, TProperty propertyValue) {
        if(propertyValue == null) {
            // If we're working with a nullable type then this rule should not be applied.
            // If you want to ensure that it's never null then a NotNull rule should also be applied.
            return true;
        }

        var valueToCompare = GetComparisonValue(context);

        if (!valueToCompare.HasValue || !IsValid(propertyValue, valueToCompare.Value)) {
            context.MessageFormatter.AppendArgument("ComparisonValue", valueToCompare.HasValue ? valueToCompare.Value : "");
            context.MessageFormatter.AppendArgument("ComparisonProperty", _comparisonMemberDisplayName ?? "");
            return false;
        }

        return true;
    }

    public (bool HasValue, TProperty Value) GetComparisonValue(ValidationContext[T] context) {
        if(_valueToCompareFunc != null) {
            var value = _valueToCompareFunc(context.InstanceToValidate);
            return (value != null, value);
        }
        if (_valueToCompareFuncForNullables != null) {
            return _valueToCompareFuncForNullables(context.InstanceToValidate);
        }

        return (ValueToCompare != null, ValueToCompare);
    }

    public abstract bool IsValid(TProperty value, TProperty valueToCompare);

    public abstract Comparison Comparison { get; }
    public MemberInfo MemberToCompare { get; private set; }

    public TProperty ValueToCompare { get; }

    object IComparisonValidator.ValueToCompare =]
        MemberToCompare != null || _valueToCompareFunc != null ? null : ValueToCompare;
    }
'''
