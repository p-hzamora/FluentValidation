from __future__ import annotations
from decimal import Decimal
from typing import Callable, Optional, overload, TYPE_CHECKING
import inspect

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.internal.AccessorCache import AccessorCache
from fluent_validation.validators.EmptyValidator import EmptyValidator
from fluent_validation.validators.NullValidator import NullValidator
from fluent_validation.validators.InclusiveBetweenValidator import InclusiveBetweenValidator
from fluent_validation.validators.RangeValidator import IComparer, RangeValidatorFactory
from fluent_validation.validators.ExclusiveBetweenValidator import ExclusiveBetweenValidator
from fluent_validation.DefaultValidatorOptions import DefaultValidatorOptions

if TYPE_CHECKING:
    from fluent_validation.InlineValidator import InlineValidator
    from fluent_validation.syntax import IRuleBuilder


from fluent_validation.ValidatorOptions import ValidatorOptions
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
from .validators.CreditCardValidator import CreditCardValidator
from .validators.ScalePrecisionValidator import ScalePrecisionValidator


from .IValidationContext import ValidationContext


class DefaultValidatorExtensions[T, TProperty]:
    """
    ruleBuilder actua como self, ya que es la instancia padre que se le pasa a traves de la herencia
    """

    def not_null(ruleBuilder: IRuleBuilder[T, TProperty]) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(NotNullValidator[T, TProperty]())

    def null(ruleBuilder: IRuleBuilder[T, TProperty]) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderOptions[T, TProperty]:
        return ruleBuilder.set_validator(NullValidator[T, TProperty]())

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

    def empty(ruleBuilder: IRuleBuilder[T, TProperty]) -> IRuleBuilder[T, TProperty]:
        return ruleBuilder.set_validator(EmptyValidator[T, TProperty]())

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

            name = ruleBuilder.get_display_name(member, valueToCompare)
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
            name = ruleBuilder.get_display_name(member, valueToCompare)
            return ruleBuilder.set_validator(LessThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(LessThanOrEqualValidator(value=valueToCompare))

    # endregion
    # region equal
    @overload
    def equal(ruleBuilder: IRuleBuilder[T, TProperty], toCompare: TProperty) -> IRuleBuilder[T, TProperty]: ...  # return IRuleBuilderOptions
    @overload
    def equal(ruleBuilder: IRuleBuilder[T, TProperty], toCompare: str) -> IRuleBuilder[T, TProperty]: ...  # return IRuleBuilderOptions
    @overload
    def equal(
        ruleBuilder: IRuleBuilder[T, TProperty], toCompare: Callable[[T], TProperty], comparer: Optional[Callable[[TProperty, str], bool]] = None
    ) -> IRuleBuilder[T, TProperty]: ...  # return IRuleBuilderOptions
    @overload
    def equal(
        ruleBuilder: IRuleBuilder[T, TProperty], toCompare: Callable[[T], str], comparer: Optional[Callable[[TProperty, str], bool]] = None
    ) -> IRuleBuilder[T, TProperty]: ...  # return IRuleBuilderOptions[T, TProperty]:

    def equal(
        ruleBuilder: IRuleBuilder[T, TProperty], toCompare: str | Callable[[T], TProperty], comparer: Optional[Callable[[TProperty, str], bool]] = None
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

    # endregion

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
            name = ruleBuilder.get_display_name(member, valueToCompare)
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
            name = ruleBuilder.get_display_name(member, valueToCompare)
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
            name = ruleBuilder.get_display_name(member, valueToCompare)
            return ruleBuilder.set_validator(GreaterThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.set_validator(GreaterThanOrEqualValidator(value=valueToCompare))

    # endregion

    @overload
    def inclusive_between(ruleBuilder: IRuleBuilder[T, TProperty], from_: TProperty, to: TProperty) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T,TProperty]:
    @overload
    def inclusive_between(
        ruleBuilder: IRuleBuilder[T, TProperty], from_: TProperty, to: TProperty, comparer: Optional[IComparer[T]]
    ) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T,TProperty] :

    def inclusive_between(ruleBuilder: IRuleBuilder[T, Optional[TProperty]], from_: TProperty, to: TProperty, comparer: Optional[IComparer[T]] = None) -> IRuleBuilder[T, TProperty]:
        if comparer is None:
            return ruleBuilder.set_validator(RangeValidatorFactory.CreateInclusiveBetween(from_, to))
        return ruleBuilder.set_validator(InclusiveBetweenValidator[T, TProperty](from_, to, comparer))

    @overload
    def exclusive_between(ruleBuilder: IRuleBuilder[T, TProperty], from_: TProperty, to: TProperty) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T,TProperty]:
    @overload
    def exclusive_between(
        ruleBuilder: IRuleBuilder[T, TProperty], from_: TProperty, to: TProperty, comparer: Optional[IComparer[T]]
    ) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T,TProperty] :

    def exclusive_between(ruleBuilder: IRuleBuilder[T, Optional[TProperty]], from_: TProperty, to: TProperty, comparer: Optional[IComparer[T]] = None) -> IRuleBuilder[T, TProperty]:
        if comparer is None:
            return ruleBuilder.set_validator(RangeValidatorFactory.CreateExclusiveBetween(from_, to))
        return ruleBuilder.set_validator(ExclusiveBetweenValidator[T, TProperty](from_, to, comparer))

    def credit_card(ruleBuilder: IRuleBuilder[T, str]) -> IRuleBuilder[T, str]:  # IRuleBuilderOptions[T, str]
        return ruleBuilder.set_validator(CreditCardValidator[T]())

    # def IsInEnum(ruleBuilder: IRuleBuilder[T,TProperty] )->IRuleBuilder[T,TProperty]: # IRuleBuilderOptions[T,TProperty]
    #     return ruleBuilder.set_validator(EnumValidator[T,TProperty]())

    # region precision_scale
    @overload
    def precision_scale(ruleBuilder: IRuleBuilder[T, Decimal], precision: int, scale: int, ignoreTrailingZeros: bool) -> IRuleBuilder[T, Decimal]: ...  # IRuleBuilderOptions<T, Decimal>: ...
    @overload
    def precision_scale(ruleBuilder: IRuleBuilder[T, None], precision: int, scale: int, ignoreTrailingZeros: bool) -> IRuleBuilder[T, None]: ...  # IRuleBuilderOptions<T, None>: ...

    def precision_scale[TPrecision](ruleBuilder: IRuleBuilder[T, TPrecision], precision: int, scale: int, ignoreTrailingZeros: bool) -> IRuleBuilder[T, TPrecision]:  # IRuleBuilderOptions<T, Decimal?>
        return ruleBuilder.set_validator(ScalePrecisionValidator[T](scale, precision, ignoreTrailingZeros))

    # endregion

    # 	static IRuleBuilderOptionsConditions[T,TProperty] Custom[T,TProperty](ruleBuilder: IRuleBuilder[T,TProperty] , Action<TProperty, ValidationContext<T>> action) {
    # 		if (action == null) throw ArgumentNullException(nameof(action))
    # 		return (IRuleBuilderOptionsConditions[T,TProperty])ruleBuilder.Must((parent, value, context) => {
    # 			action(value, context)
    # 			return true
    # 		})
    # 	}

    # 	static IRuleBuilderOptionsConditions[T,TProperty] CustomAsync[T,TProperty](ruleBuilder: IRuleBuilder[T,TProperty] , Func<TProperty, ValidationContext<T>, CancellationToken, Task> action) {
    # 		if (action == null) throw ArgumentNullException(nameof(action))
    # 		return (IRuleBuilderOptionsConditions[T,TProperty])ruleBuilder.MustAsync(async (parent, value, context, cancel) => {
    # 			await action(value, context, cancel)
    # 			return true
    # 		})
    # 	}

    # 	static IRuleBuilderOptions<T, IEnumerable<TElement>> ForEach<T, TElement>(IRuleBuilder<T, IEnumerable<TElement>> ruleBuilder,
    # 		Action<IRuleBuilderInitialCollection<IEnumerable<TElement>, TElement>> action) {
    # 		var innerValidator = InlineValidator<IEnumerable<TElement>>()

    # 		# https://github.com/FluentValidation/FluentValidation/issues/1231
    # 		# We need to explicitly set a display name override on the nested validator
    # 		# so that it matches what would happen if the user had called RuleForEach initially.
    # 		var originalRule = DefaultValidatorOptions.Configurable(ruleBuilder)
    # 		var collectionRuleBuilder = innerValidator.RuleForEach(x => x)
    # 		var collectionRule = DefaultValidatorOptions.Configurable(collectionRuleBuilder)

    # 		collectionRule.PropertyName = str.Empty

    # 		collectionRule.SetDisplayName(context => {
    # 			return originalRule.GetDisplayName(((IValidationContext) context).ParentContext)
    # 		})

    # 		action(collectionRuleBuilder)
    # 		return ruleBuilder.set_validator(innerValidator)
    # 	}

    # 	static IRuleBuilderOptions<T, str> IsEnumName<T>(IRuleBuilder<T, str> ruleBuilder, Type enumType, bool caseSensitive = true)
    # 		=> ruleBuilder.set_validator(StringEnumValidator<T>(enumType, caseSensitive))

    def child_rules[T, TProperty](
        ruleBuilder: IRuleBuilder[T, TProperty], action: None | Callable[[InlineValidator[TProperty], None]]
    ) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderOptions[T,TProperty]
        from fluent_validation.internal.ChildRulesContainer import ChildRulesContainer

        if action is None:
            raise ValueError("action")
        validator = ChildRulesContainer[TProperty]()
        # parentValidator = ((IRuleBuilderInternal[T]) ruleBuilder).ParentValidator
        parentValidator = ruleBuilder.ParentValidator

        ruleSets: list[str]

        # TODOH: Checked
        if isinstance(parentValidator, ChildRulesContainer):
            if parentValidator.RuleSetsToApplyToChildRules is not None:
                ruleSets = parentValidator.RuleSetsToApplyToChildRules
        else:
            ruleSets = DefaultValidatorOptions.configurable(ruleBuilder).RuleSets

        # Store the correct rulesets on the child validator in case
        # we have nested calls to child_rules, which can then pick up from
        # the parent validator.
        validator.RuleSetsToApplyToChildRules = ruleSets

        action(validator)

        for rule in validator.Rules:
            if rule.RuleSets is None:
                rule.RuleSets = ruleSets

        return ruleBuilder.set_validator(validator)

    # 	static IRuleBuilderOptions[T,TProperty] SetInheritanceValidator[T,TProperty](ruleBuilder: IRuleBuilder[T,TProperty] , Action<PolymorphicValidator[T,TProperty]> validatorConfiguration) {
    # 		if (validatorConfiguration == null) throw ArgumentNullException(nameof(validatorConfiguration))
    # 		var validator = PolymorphicValidator[T,TProperty]()
    # 		validatorConfiguration(validator)
    # 		return ruleBuilder.SetAsyncValidator((IAsyncPropertyValidator[T,TProperty]) validator)
    # 	}

    @staticmethod
    def get_display_name(member: MemberInfo, expression: Callable[[T], TProperty]) -> None | str:
        # FIXME [x]: The original code called 'DisplayNameResolver' but break some tests
        if (display_name_resolver := ValidatorOptions.Global.DisplayNameResolver(type(T), member, expression)) is not None:
            return display_name_resolver
        if member is not None:
            return ExtensionsInternal.split_pascal_case(member.Name)
        return None
