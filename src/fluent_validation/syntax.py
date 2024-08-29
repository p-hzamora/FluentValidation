from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Self, Callable, overload, TYPE_CHECKING

from src.fluent_validation.DefaultValidatorExtensions import DefaultValidatorExtensions
from src.fluent_validation.DefaultValidatorOptions import DefaultValidatorOptions

if TYPE_CHECKING:
    from src.fluent_validation.IValidator import IValidator
    # from src.fluent_validation.abstract_validator import AbstractValidator

from .validators.IpropertyValidator import IPropertyValidator


from .IValidationRule import IValidationRule


class IRuleBuilderInternal_one_generic[T](ABC):
    ...
    # @property
    # @abstractmethod
    # def ParentValidator(self) -> AbstractValidator[T]: ...


class IRuleBuilderInternal[T, TProperty](IRuleBuilderInternal_one_generic[T]):
    @property
    @abstractmethod
    def Rule(self) -> IValidationRule[T, TProperty]: ...


class IRuleBuilder[T, TProperty](IRuleBuilderInternal, DefaultValidatorExtensions):
    @overload
    def set_validator(self, validator: IPropertyValidator[T, TProperty]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def set_validator(self, validator: IValidator[TProperty], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def set_validator(self, validator: Callable[[T], IValidator[TProperty]], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def set_validator(self, validator: Callable[[T, TProperty], IValidator[TProperty]], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: ...

    @abstractmethod
    def set_validator(self, validator, *ruleSets): ...


class IRuleBuilderOptions[T, TProperty](IRuleBuilder[T, TProperty]):
    @abstractmethod
    def DependentRules(action) -> Self: ...


class IRuleBuilderOptionsConditions[T, TProperty](
    IRuleBuilder[T, TProperty],
): ...


class IRuleBuilderInitialCollection[T, TElement](IRuleBuilder[T, TElement]): ...


class IConditionBuilder(ABC):
    def Otherwise(action: Callable[..., None]) -> None: ...
