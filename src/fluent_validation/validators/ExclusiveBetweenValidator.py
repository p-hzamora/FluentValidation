from abc import abstractmethod
from typing import Any

from fluent_validation.validators.IpropertyValidator import IPropertyValidator
from .RangeValidator import IComparer, RangeValidator


class ExclusiveBetweenValidator[T, TProperty](RangeValidator[T, TProperty]):
    """Performs range validation where the property value must be between the two specified values (exclusive)."""

    def __init__(self, from_: TProperty, to: TProperty, comparer:IComparer[T]):  # comparer:IComparer[TProperty]
        super().__init__(from_, to, comparer)

    def HasError(self, value: TProperty) -> bool:
        return self.Compare(value, self.From) <= 0 or self.Compare(value, self.To) >= 0


class IBetweenValidator(IPropertyValidator):
    @property
    @abstractmethod
    def From(self) -> Any: ...
    
    @property
    @abstractmethod
    def To(self) -> Any: ...
