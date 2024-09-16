from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional, Type, overload, override, Callable, TYPE_CHECKING
from fluent_validation.IValidator import IValidator
from fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector
from fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator
from fluent_validation.validators.NoopPropertyValidator import NoopPropertyValidator

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import IValidationContext, ValidationContext
    from fluent_validation.internal.IValidatorSelector import IValidatorSelector


class IChildValidatorAdaptor:
    @property
    @abstractmethod
    def ValidatorType(self): ...


class ChildValidatorAdaptor[T, TProperty](NoopPropertyValidator[T, TProperty], IAsyncPropertyValidator[T, TProperty], IChildValidatorAdaptor):
    @property
    def ValidatorType(self) -> Type:
        return self._validator_type

    @property
    def RuleSets(self) -> list[str]:
        return self._rule_sets

    @RuleSets.setter
    def RuleSets(self, value: list[str]):
        self._rule_sets = value

    @overload
    def __init__(self, validator: IValidator[TProperty], validatorType: Type): ...
    @overload
    def __init__(self, validator: Callable[[ValidationContext[T], TProperty], IValidator[TProperty]], validatorType: Type): ...

    def __init__(self, validator=None, validatorType=None):
        self._validatorProvider: None | Callable[[ValidationContext[T], TProperty], IValidator[TProperty]] = None
        self._validator: None | IValidator[TProperty] = None
        self._rule_sets:Optional[list[str]] = None

        if isinstance(validator, IValidator) and not callable(validator):
            self._validator: IValidator[TProperty] = validator
            self._validator_type: Type = validatorType
        else:
            self._validatorProvider: Callable[[ValidationContext[T], TProperty], IValidator[TProperty]] = validator
            self._validator_type = validatorType

    @override
    def is_valid(self, context: ValidationContext[T], value: None | TProperty) -> bool:
        if value is None:
            return True

        validator = self.GetValidator(context, value)

        if validator is None:
            return True

        newContext = self.CreateNewValidationContextForChildValidator(context, value)

        originalIndex, currentIndex = self.HandleCollectionIndex(context)

        # FIXME [x]!: Due to the asynchronous nested loop, the 'context' var does not update with the newContext validation, although the method works properly
        validator.validate(newContext)

        self.ResetCollectionIndex(context, originalIndex, currentIndex)
        return True

    @override
    async def IsValidAsync(self, context: ValidationContext[T], value: TProperty) -> bool:
        if value is None:
            return True

        validator = self.GetValidator(context, value)

        if validator is None:
            return True

        newContext = self.CreateNewValidationContextForChildValidator(context, value)

        originalIndex, currentIndex = self.HandleCollectionIndex(context)

        await validator.ValidateAsync(newContext)  # COMMENT: cancellation as second attr not implemented

        self.ResetCollectionIndex(context, originalIndex, currentIndex)

        return True

    def GetValidator(self, context: ValidationContext[T], value: TProperty) -> IValidator:
        return self._validatorProvider(context, value) if self._validatorProvider is not None else self._validator

    def CreateNewValidationContextForChildValidator(self, context: ValidationContext[T], value: TProperty) -> IValidationContext:
        selector = self.GetSelector(context, value)
        newContext = context.CloneForChildValidator(value, True, selector)

        if not context.IsChildCollectionContext:
            newContext.PropertyChain.Add(context.RawPropertyName)

        return newContext

    def GetSelector(self, context: ValidationContext[T], value: TProperty) -> Optional[IValidatorSelector]:
        if self.RuleSets is not None:
            if len(self.RuleSets) > 0:
                return RulesetValidatorSelector(self.RuleSets)
        return None

    def HandleCollectionIndex(self, context: ValidationContext[T]) -> tuple[Optional[Any], Optional[Any]]:
        originalIndex = None
        if (index := context.MessageFormatter.PlaceholderValues.get("CollectionIndex", None)) is not None:
            originalIndex = context.RootContextData.get("__FV_CollectionIndex", None)
            context.RootContextData["__FV_CollectionIndex"] = index
        return originalIndex, index

    def ResetCollectionIndex(self, context: ValidationContext[T], originalIndex: Any, index: Any) -> None:
        if index is not None:
            if originalIndex is not None:
                context.RootContextData["__FV_CollectionIndex"] = originalIndex
            else:
                context.RootContextData.pop("__FV_CollectionIndex")
        return originalIndex, index
