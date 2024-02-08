from abc import abstractmethod, ABC
from typing import Any, Self, Callable, overload
import dis

from .validators.IpropertyValidator import IPropertyValidator
from .validators.LengthValidator import (
    LengthValidator,
    ExactLengthValidator,
    MaximumLengthValidator,
    MinimumLengthValidator,
)
from .validators.NotNullValidator import NotNullValidator
from .validators.RegularExpressionValidator import RegularExpressionValidator
from .validators.IsInstance import IsInstance
from .validators.NotEmptyValidator import NotEmptyValidator

from .validators.LessThanValidator import LessThanValidator
from .validators.LessThanOrEqualValidator import LessThanOrEqualValidator
from .validators.EqualValidator import EqualValidator
from .validators.NotEqualValidator import NotEqualValidator
from .validators.GreaterThanValidator import GreaterThanValidator
from .validators.GreaterThanOrEqualValidator import GreaterThanOrEqualValidator
from .IValidationRule import IValidationRule


class DefaultValidatorExtensions:
    """
    ruleBuilder actua como self, ya que es la instancia padre que se le pasa a traves de la herencia
    """

    def configurable[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]") -> IValidationRule[T, TProperty]:
        return ruleBuilder.Rule

    def NotNull[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]") -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(NotNullValidator[T, TProperty]())

    def Matches[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", pattern: str) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(RegularExpressionValidator[T](pattern))

    @overload
    def Length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", min: Callable[[T], None], max: Callable[[T], None]) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def Length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", min: int, max: int) -> "IRuleBuilder[T, TProperty]":
        ...

    def Length[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", min: int | T, max: int | T) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(LengthValidator[T](min, max))

    def ExactLength[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", exactLength: int) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(ExactLengthValidator[T](exactLength))

    def MaxLength[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", MaxLength: int) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(MaximumLengthValidator[T](MaxLength))

    def MinLength[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", MinLength: int) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(MinimumLengthValidator[T](MinLength))

    def IsInstance[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", instance: Any) -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(IsInstance[T](instance))

    def WithMessage[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", errorMessage: str) -> "IRuleBuilder[T, TProperty]":
        DefaultValidatorExtensions.configurable(ruleBuilder).Current.set_error_message(errorMessage)
        return ruleBuilder

    def NotEmpty[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]") -> "IRuleBuilder[T, TProperty]":
        return ruleBuilder.SetValidator(NotEmptyValidator[T, TProperty]())

    # region LessThan
    @overload
    def LessThan[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def LessThan[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def LessThan[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = {x.opname: x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
            return ruleBuilder.SetValidator(LessThanValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.SetValidator(LessThanValidator(value=valueToCompare))

    # endregion
    # region LessThanOrEqualTo
    @overload
    def LessThanOrEqualTo[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def LessThanOrEqualTo[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def LessThanOrEqualTo[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = {x.opname: x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
            return ruleBuilder.SetValidator(LessThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.SetValidator(LessThanOrEqualValidator(value=valueToCompare))

    # endregion
    # region Equal
    @overload
    def Equal[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def Equal[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def Equal[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = {x.opname: x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
            return ruleBuilder.SetValidator(EqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.SetValidator(EqualValidator(value=valueToCompare))

    # endregion
    # region NotEqual
    @overload
    def NotEqual[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def NotEqual[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def NotEqual[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = {x.opname: x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
            return ruleBuilder.SetValidator(NotEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.SetValidator(NotEqualValidator(value=valueToCompare))

    # endregion
    # region GreaterThan
    @overload
    def GreaterThan[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def GreaterThan[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def GreaterThan[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = {x.opname: x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
            return ruleBuilder.SetValidator(GreaterThanValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.SetValidator(GreaterThanValidator(value=valueToCompare))

    # endregion
    # region GreaterThanOrEqual
    @overload
    def GreaterThanOrEqualTo[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: TProperty) -> "IRuleBuilder[T, TProperty]":
        ...

    @overload
    def GreaterThanOrEqualTo[T, TProperty](ruleBuilder: "IRuleBuilder[T, TProperty]", valueToCompare: Callable[[T], TProperty]) -> "IRuleBuilder[T, TProperty]":
        ...

    def GreaterThanOrEqualTo[T, TProperty](
        ruleBuilder: "IRuleBuilder[T, TProperty]",
        valueToCompare: Callable[[T], TProperty] | TProperty,
    ) -> "IRuleBuilder[T, TProperty]":
        if callable(valueToCompare):
            func = valueToCompare
            name = {x.opname: x.argval for x in dis.Bytecode(valueToCompare)}["LOAD_ATTR"]
            return ruleBuilder.SetValidator(GreaterThanOrEqualValidator[T, TProperty](valueToCompareFunc=func, memberDisplayName=name))

        return ruleBuilder.SetValidator(GreaterThanOrEqualValidator(value=valueToCompare))

    # endregion


class IRuleBuilderInternal[T, TProperty](ABC):
    @property
    @abstractmethod
    def Rule(self) -> IValidationRule[T, TProperty]:
        ...


class IRuleBuilder[T, TProperty](IRuleBuilderInternal, DefaultValidatorExtensions):
    @staticmethod
    @abstractmethod
    def SetValidator(validator: IPropertyValidator[T, TProperty]) -> Self:
        ...


class IRuleBuilderOptions[T, TProperty](IRuleBuilder[T, TProperty]):
    @abstractmethod
    def DependentRules(action) -> Self:
        ...
