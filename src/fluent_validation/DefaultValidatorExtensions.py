from __future__ import annotations
from typing import Callable, overload, TYPE_CHECKING
import inspect

from src.fluent_validation.MemberInfo import MemberInfo
from src.fluent_validation.internal.AccessorCache import AccessorCache


if TYPE_CHECKING:
    from src.fluent_validation.syntax import IRuleBuilder


from src.fluent_validation.ValidatorOptions import ValidatorOptions
from .internal.ExtensionInternal import ExtensionsInternal
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

from .IValidationContext import ValidationContext


class DefaultValidatorExtensions[T, TProperty]:
    """
    ruleBuilder actua como self, ya que es la instancia padre que se le pasa a traves de la herencia
    """

    def not_null(ruleBuilder: IRuleBuilder[T, TProperty]) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(NotNullValidator[T, TProperty]())

    def matches(ruleBuilder: IRuleBuilder[T, TProperty], pattern: str) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(RegularExpressionValidator[T](pattern))

    @overload
    def length(ruleBuilder: IRuleBuilder[T, TProperty], min: Callable[[T], None], max: Callable[[T], None]) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def length(ruleBuilder: IRuleBuilder[T, TProperty], min: int, max: int) -> IRuleBuilder[T, TProperty]: ...

    def length(ruleBuilder: IRuleBuilder[T, TProperty], min: int | T, max: int | T) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(LengthValidator[T](min, max))

    def exact_length(ruleBuilder: IRuleBuilder[T, TProperty], exactLength: int) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(ExactLengthValidator[T](exactLength))

    def max_length(ruleBuilder: IRuleBuilder[T, TProperty], max_length: int) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(MaximumLengthValidator[T](max_length))

    def min_length(ruleBuilder: IRuleBuilder[T, TProperty], min_length: int) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(MinimumLengthValidator[T](min_length))

    def not_empty(ruleBuilder: IRuleBuilder[T, TProperty]) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(NotEmptyValidator[T, TProperty]())

    # region less_than
    @overload
    def less_than(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: TProperty) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def less_than(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]: ...

    def less_than(
        ruleBuilder: IRuleBuilder[T, TProperty],
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> IRuleBuilder[T, TProperty]:
        if callable(valueToCompare):
            func = valueToCompare
            member = MemberInfo(valueToCompare)

            name = DefaultValidatorExtensions.get_display_name(member, valueToCompare)
            return ruleBuilder.set_validator(LessThanValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(LessThanValidator(value=valueToCompare))

    # endregion
    # region less_than_or_equal_to
    @overload
    def less_than_or_equal_to(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: TProperty) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def less_than_or_equal_to(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]: ...

    def less_than_or_equal_to(
        ruleBuilder: IRuleBuilder[T, TProperty],
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> IRuleBuilder[T, TProperty]:
        if callable(valueToCompare):
            func = valueToCompare
            member = MemberInfo(valueToCompare)
            name = DefaultValidatorExtensions.get_display_name(member, valueToCompare)
            return ruleBuilder.set_validator(LessThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(LessThanOrEqualValidator(value=valueToCompare))

    # endregion
    # region equal
    @overload
    def equal(ruleBuilder: IRuleBuilder[T, TProperty], toCompare: TProperty, comparer: Callable[[TProperty, str], bool] = None) -> IRuleBuilder[T, TProperty]: ...  # return IRuleBuilderOptions

    @overload
    def equal(
        ruleBuilder: IRuleBuilder[T, TProperty], toCompare: Callable[[T], TProperty], comparer: Callable[[TProperty, str], bool] = None
    ) -> IRuleBuilder[T, TProperty]: ...  # return IRuleBuilderOptions[T, TProperty]:

    def equal(
        ruleBuilder: IRuleBuilder[T, TProperty], toCompare: TProperty, comparer: Callable[[TProperty, str], bool] = None
    ) -> IRuleBuilder[T, TProperty]:  # return IRuleBuilderOptions[T,TProperty]
        expression = toCompare
        if not comparer:
            comparer = lambda x, y: x == y  # noqa: E731

        if not callable(toCompare):
            return ruleBuilder.set_validator(EqualValidator[T, TProperty](toCompare, comparer))

        member = MemberInfo(expression)
        func = AccessorCache[T].GetCachedAccessor(member, expression)
        name = ruleBuilder.get_display_name(member, expression)
        return ruleBuilder.set_validator(
            EqualValidator[T, TProperty](
                comparisonProperty=func,
                member=member,
                memberDisplayName=name,
                comparer=comparer,
            )
        )

    # region must
    @overload
    def must(ruleBuilder: IRuleBuilder[T, TProperty], predicate: Callable[[TProperty], bool]) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def must(ruleBuilder: IRuleBuilder[T, TProperty], predicate: Callable[[T, TProperty], bool]) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def must(ruleBuilder: IRuleBuilder[T, TProperty], predicate: Callable[[T, TProperty, ValidationContext[T]], bool]) -> IRuleBuilder[T, TProperty]: ...

    def must(
        ruleBuilder: IRuleBuilder[T, TProperty], predicate: Callable[[TProperty], bool] | Callable[[T, TProperty], bool] | Callable[[T, TProperty, ValidationContext[T]], bool]
    ) -> IRuleBuilder[T, TProperty]:
        num_args = len(inspect.signature(predicate).parameters)

        if num_args == 1:
            return ruleBuilder.must(lambda _, val: predicate(val))
        elif num_args == 2:
            return ruleBuilder.must(lambda x, val, _: predicate(x, val))
        elif num_args == 3:
            return ruleBuilder.set_validator(
                PredicateValidator[T, TProperty](
                    lambda instance, property, propertyValidatorContext: predicate(
                        instance,
                        property,
                        propertyValidatorContext,
                    )
                )
            )
        raise Exception(f"Number of arguments exceeded. Passed {num_args}")

    # endregion

    # endregion
    # region not_equal
    @overload
    def not_equal(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: TProperty) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def not_equal(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]: ...

    def not_equal(
        ruleBuilder: IRuleBuilder[T, TProperty],
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> IRuleBuilder[T, TProperty]:
        if callable(valueToCompare):
            func = valueToCompare
            member = MemberInfo(valueToCompare)
            name = DefaultValidatorExtensions.get_display_name(member, valueToCompare)
            return ruleBuilder.set_validator(NotEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(NotEqualValidator(value=valueToCompare))

    # endregion
    # region greater_than
    @overload
    def greater_than(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: TProperty) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def greater_than(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]: ...

    def greater_than(
        ruleBuilder: IRuleBuilder[T, TProperty],
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> IRuleBuilder[T, TProperty]:
        if callable(valueToCompare):
            func = valueToCompare
            member = MemberInfo(valueToCompare)
            name = DefaultValidatorExtensions.get_display_name(member, valueToCompare)
            return ruleBuilder.set_validator(GreaterThanValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(GreaterThanValidator(value=valueToCompare))

    # endregion
    # region GreaterThanOrEqual
    @overload
    def greater_than_or_equal_to(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: TProperty) -> IRuleBuilder[T, TProperty]: ...

    @overload
    def greater_than_or_equal_to(ruleBuilder: IRuleBuilder[T, TProperty], valueToCompare: Callable[[T], TProperty]) -> IRuleBuilder[T, TProperty]: ...

    def greater_than_or_equal_to(
        ruleBuilder: IRuleBuilder[T, TProperty],
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> IRuleBuilder[T, TProperty]:
        if callable(valueToCompare):
            func = valueToCompare
            member = MemberInfo(valueToCompare)
            name = DefaultValidatorExtensions.get_display_name(member, valueToCompare)
            return ruleBuilder.set_validator(GreaterThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(GreaterThanOrEqualValidator(value=valueToCompare))

    @staticmethod
    def get_display_name(member: MemberInfo, expression: Callable[[T], TProperty]) -> str:
        name = ValidatorOptions.Global.PropertyNameResolver(type(T), member, expression)
        if name is None:
            return name
        return ExtensionsInternal.split_pascal_case(name)

    # endregion
