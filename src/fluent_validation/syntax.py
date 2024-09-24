from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Self, Callable, overload, TYPE_CHECKING

from fluent_validation.DefaultValidatorExtensions import DefaultValidatorExtensions
from fluent_validation.DefaultValidatorOptions import DefaultValidatorOptions

if TYPE_CHECKING:
    from fluent_validation.IValidator import IValidator
    from fluent_validation.abstract_validator import AbstractValidator

from .validators.IpropertyValidator import IPropertyValidator


from .IValidationRule import IValidationRule


class IRuleBuilderInternal_one_generic[T](ABC):
    @property
    @abstractmethod
    def ParentValidator(self) -> AbstractValidator[T]: ...


class IRuleBuilderInternal[T, TProperty](IRuleBuilderInternal_one_generic[T]):
    @property
    @abstractmethod
    def Rule(self) -> IValidationRule[T, TProperty]: ...


class IRuleBuilder[T, TProperty](IRuleBuilderInternal[T, TProperty], DefaultValidatorExtensions[T, TProperty], DefaultValidatorOptions[T, TProperty]):
    def __getattr__(self, __name: str) -> Callable[..., IRuleBuilder[T, TProperty]]:
        """
        Unlike C#, Python does not have extension methods, so we have to hard-code the custom method directly into 'IRuleBuilder' class in order to use it.

        ```csharp
        public static IRuleBuilderOptions<T, IList<TElement>> ListMustContainFewerThan<T, TElement>(this IRuleBuilder<T, IList<TElement>> ruleBuilder, int num) {
          ...
        }
        ```

        The code above will be translated as:

        ```python
        def ListMustContainFewerThan(ruleBuilder:IRuleBuilder[T,list[TElement]], num:int)->IRuleBuilderOptions[T,list[TElement]]: ...
        IRuleBuilder.Foo = Foo
        ```

        Since the linter won't be able to find it, we need to specify that any method not declared in IRuleBuilder will be of type IRuleBuilder itself,
        so we can continue using the rest of the validating methods even after calling one of these.

        We can achieve this by overriding '__getattr__' special method with Callable class from typing module.
        """
        func = self.__dict__.get(__name, None)
        if func is None:
            raise AttributeError(f"'{__name}' method does not exits")
        return func

    @overload
    def set_validator(self, validator: IPropertyValidator[T, TProperty]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def set_validator(self, validator: IValidator[TProperty], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def set_validator(self, validator: Callable[[T], IValidator[TProperty]], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def set_validator(self, validator: Callable[[T, TProperty], IValidator[TProperty]], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: ...

    @abstractmethod
    def set_validator(self, validator, *ruleSets) -> IRuleBuilderOptions[T, TProperty]: ...


class IRuleBuilderInitial[T, TProperty](IRuleBuilder[T, TProperty]): ...


class IRuleBuilderOptions[T, TProperty](IRuleBuilder[T, TProperty]):
    @abstractmethod
    def DependentRules(action) -> Self:
        """Creates a scope for declaring dependent rules."""
        ...


class IRuleBuilderOptionsConditions[T, TProperty](IRuleBuilder[T, TProperty]):
    """Rule builder that starts the chain for a child collection"""

    ...


class IRuleBuilderInitialCollection[T, TElement](IRuleBuilder[T, TElement]): ...


class IConditionBuilder(ABC):
    @abstractmethod
    def otherwise(self, action: Callable[[], None]) -> None:
        """Rules to be invoked if the condition fails."""

    ...
