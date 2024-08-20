from abc import abstractmethod, ABC
from typing import Self, Callable, overload
import dis
import inspect


from .internal.ExtensionInternal import ExtensionsInternal
from .validators.IpropertyValidator import IPropertyValidator
from .validators.LengthValidator import (
    LengthValidator,
    ExactLengthValidator,
    MaximumLengthValidator,
    MinimumLengthValidator,
)
from .validators.NotNullValidator import NotNullValidator
from .validators.RegularExpressionValidator import RegularExpressionValidator
from .validators.NotEmptyValidator import NotEmptyValidator

from .validators.LessThanValidator import LessThanValidator
from .validators.LessThanOrEqualValidator import LessThanOrEqualValidator
from .validators.EqualValidator import EqualValidator
from .validators.NotEqualValidator import NotEqualValidator
from .validators.GreaterThanValidator import GreaterThanValidator
from .validators.GreaterThanOrEqualValidator import GreaterThanOrEqualValidator
from .validators.PredicateValidator import PredicateValidator

from .IValidationRule import IValidationRule
from .IValidationContext import ValidationContext


class DefaultValidatorExtensions:
    """
    ruleBuilder actua como self, ya que es la instancia padre que se le pasa a traves de la herencia
    """

    @staticmethod
    def configurable[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]") -> IValidationRule[T, TProperty]:
        return ruleBuilder.Rule

    def not_null[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]") -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.set_validator(NotNullValidator[T, TProperty]())

    def matches[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", pattern: str) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.set_validator(RegularExpressionValidator[T](pattern))

    @overload
    def length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", min: Callable[[T], None], max: Callable[[T], None]) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", min: int, max: int) -> "IRuleBuilder[T, TProperty]":
        ...

    def length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", min: int | T, max: int | T) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.set_validator(LengthValidator[T](min, max))

    def exact_length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", exactLength: int) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.set_validator(ExactLengthValidator[T](exactLength))

    def max_length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", max_length: int) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.set_validator(MaximumLengthValidator[T](max_length))

    def min_length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", min_length: int) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.set_validator(MinimumLengthValidator[T](min_length))

    def with_message[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", errorMessage: str) -> "IRuleBuilder[T, TProperty]":
        DefaultValidatorExtensions.configurable(ruleBuilder).Current.set_error_message(errorMessage)
        return ruleBuilder

    def not_empty[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]") -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.set_validator(NotEmptyValidator[T, TProperty]())

    # region less_than
    @overload
    def less_than[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def less_than[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def less_than[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = DefaultValidatorExtensions.get_display_name(valueToCompare)
            return ruleBuilder.set_validator(LessThanValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(LessThanValidator(value=valueToCompare))

    # endregion
    # region less_than_or_equal_to
    @overload
    def less_than_or_equal_to[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def less_than_or_equal_to[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def less_than_or_equal_to[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = DefaultValidatorExtensions.get_display_name(valueToCompare)
            return ruleBuilder.set_validator(LessThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(LessThanOrEqualValidator(value=valueToCompare))

    # endregion
    # region equal
    @overload
    def equal[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def equal[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def equal[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = DefaultValidatorExtensions.get_display_name(valueToCompare)
            return ruleBuilder.set_validator(EqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(EqualValidator(value=valueToCompare))

    # region must
    @overload
    def must[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", predicate: Callable[[TProperty], bool]) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def must[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", predicate: Callable[[T, TProperty], bool]) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def must[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", predicate: Callable[[T, TProperty, ValidationContext[T]], bool]) -> "IRuleBuilder[T, TProperty]":
        ...

    def must[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]", predicate: Callable[[TProperty], bool] | Callable[[T, TProperty], bool] | Callable[[T, TProperty, ValidationContext[T]], bool]
    ) -> "IRuleBuilder[T, TProperty]":
        num_args = len(inspect.signature(predicate).parameters)

        if num_args == 1:
            return ruleBuilder.must(lambda _, val: predicate(val))
        elif num_args == 2:
            return ruleBuilder.must(lambda x, val, _: predicate(x, val))
        elif num_args == 3:
            return ruleBuilder.set_validator(
                PredicateValidator[T, TProperty](lambda instance, property, propertyValidatorContext: predicate(instance, property, propertyValidatorContext)),
            )
        raise Exception(f"Number of arguments exceeded. Passed {num_args}")

    # endregion

    # endregion
    # region not_equal
    @overload
    def not_equal[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def not_equal[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def not_equal[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = DefaultValidatorExtensions.get_display_name(valueToCompare)
            return ruleBuilder.set_validator(NotEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(NotEqualValidator(value=valueToCompare))

    # endregion
    # region greater_than
    @overload
    def greater_than[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def greater_than[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def greater_than[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = DefaultValidatorExtensions.get_display_name(valueToCompare)
            return ruleBuilder.set_validator(GreaterThanValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(GreaterThanValidator(value=valueToCompare))

    # endregion
    # region GreaterThanOrEqual
    @overload
    def greater_than_or_equal_to[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def greater_than_or_equal_to[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def greater_than_or_equal_to[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = DefaultValidatorExtensions.get_display_name(valueToCompare)
            return ruleBuilder.set_validator(GreaterThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(GreaterThanOrEqualValidator(value=valueToCompare))

    @staticmethod
    def get_display_name[T, TProperty](expression: Callable[[T], TProperty]) -> str:
        name = {x.opname: x.argval for x in dis.Bytecode(expression)}["LOAD_ATTR"]
        return ExtensionsInternal.split_pascal_case(name)

    # endregion


class IRuleBuilderInternal[T, TProperty](ABC):
    @property
    @abstractmethod
    def Rule(self) -> IValidationRule[T, TProperty]:
        ...


class IRuleBuilder[T, TProperty](IRuleBuilderInternal, DefaultValidatorExtensions):
    @staticmethod
    @abstractmethod
    def set_validator(validator: IPropertyValidator[T, TProperty]) -> Self:
        ...


class IRuleBuilderOptions[T, TProperty](IRuleBuilder[T, TProperty]):
    @abstractmethod
    def DependentRules(action) -> Self:
        ...
