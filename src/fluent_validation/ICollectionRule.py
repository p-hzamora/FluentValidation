from __future__ import annotations
from abc import abstractmethod
from typing import Callable

from fluent_validation.IValidationRule import IValidationRule


class ICollectionRule[T, TElement](IValidationRule[T, TElement]):
    """
    Represents a rule defined against a collection with rule_for_each.
    : T -> Root object
    : TElement -> Type of each element in the collection
    """

    @property
    @abstractmethod
    def Filter(self) -> Callable[[TElement], bool]:
        """
        Filter that should include/exclude items in the collection.
        """

    @property
    @abstractmethod
    def IndexBuilder(self) -> Callable[[T, list[TElement], TElement, int], str]:
        """
        Constructs the indexer in the property name associated with the error message.
        By default this is "[" + index + "]"
        """
