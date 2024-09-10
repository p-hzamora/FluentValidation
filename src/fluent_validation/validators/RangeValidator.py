from abc import ABC, abstractmethod
from typing import override
from ..IValidationContext import ValidationContext

from ..validators import PropertyValidator
from ..validators.IpropertyValidator import IPropertyValidator


class IComparer[T](ABC):
    """
    Resumen:
        Compares two objects and returns a value indicating whether one is less than,
        equal to, or greater than the other.

    Parámetros:
    x:
        The first object to compare.

    y:
        The second object to compare.

    Devuelve:
        A signed integer that indicates the relative values of x and y, as shown in the
        following table.
        Value – Meaning
        Less than zero –x is less than y.
        Zero –x equals y.
        Greater than zero –x is greater than y.
    """

    @abstractmethod
    def Compare(x: T = None, y: T = None) -> int: ...


class IBetweenValidator(IPropertyValidator):
    From: object
    To: object


class RangeValidator[T, TProperty](PropertyValidator[T, TProperty], IBetweenValidator):
    _explicitComparer: IComparer[TProperty]

    def __init__(self, ini: TProperty, to: TProperty, comparer: IComparer[TProperty]):
        self._to = to
        self._from = ini

        self._explicitComparer = comparer

        if comparer.Compare(to, ini) == -1:
            raise Exception(f"'{self._to} To should be larger than from.")

    @property
    def From(self):
        return self._from

    @property
    def To(self):
        return self._to

    def HasError(self, value: TProperty) -> bool: ...

    @override
    def is_valid(self, context: ValidationContext[T], value: TProperty):
        # If the value is null then we abort and assume success.
        # This should not be a failure condition - only a not_null/not_empty should cause a null to fail.
        if value is None:
            return True

        if self.HasError(value):
            context.MessageFormatter.AppendArgument("From", self.From)
            context.MessageFormatter.AppendArgument("To", self.To)
            return False

        return True

    def Compare(self, a: TProperty, b: TProperty) -> int:
        return self._explicitComparer.Compare(a, b)


# public static class RangeValidatorFactory {
# 	public static ExclusiveBetweenValidator<T, TProperty> CreateExclusiveBetween<T,TProperty>(TProperty from, TProperty to)
# 		where TProperty : IComparable<TProperty>, IComparable =>
# 		new ExclusiveBetweenValidator<T, TProperty>(from, to, ComparableComparer<TProperty>.Instance);

# 	public static InclusiveBetweenValidator<T, TProperty> CreateInclusiveBetween<T,TProperty>(TProperty from, TProperty to)
# 		where TProperty : IComparable<TProperty>, IComparable {
# 		return new InclusiveBetweenValidator<T, TProperty>(from, to, ComparableComparer<TProperty>.Instance);
# 	}
# }
