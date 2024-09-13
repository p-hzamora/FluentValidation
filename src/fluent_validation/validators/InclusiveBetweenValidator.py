from .ExclusiveBetweenValidator import IBetweenValidator
from .RangeValidator import IComparer, RangeValidator


class IInclusiveBetweenValidator(IBetweenValidator): ...


class InclusiveBetweenValidator[T, TProperty](RangeValidator[T, TProperty], IInclusiveBetweenValidator):
    """Performs range validation where the property value must be between the two specified values (inclusive)."""

    def __init__(self, from_: TProperty, to: TProperty, comparer:IComparer[T]):  # comparer:IComparer[TProperty]
        super().__init__(from_, to, comparer)

    def HasError(self, value: TProperty) -> bool:
        return self.Compare(value, self.From) < 0 or self.Compare(value, self.To) > 0
