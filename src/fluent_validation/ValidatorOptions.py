from typing import Any, Callable, Iterable, Type

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.internal.CompositeValidatorSelector import CompositeValidatorSelector
from fluent_validation.internal.DefaultValidatorSelector import DefaultValidatorSelector
from fluent_validation.internal.IValidatorSelector import IValidatorSelector
from fluent_validation.internal.MemberNameValidatorSelector import MemberNameValidatorSelector
from fluent_validation.internal.MessageFormatter import MessageFormatter

from fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector
from fluent_validation.validators.IpropertyValidator import IPropertyValidator
from .enums import CascadeMode as _CascadeMode, Severity as _Severity
from .internal.Resources.LanguageManager import LanguageManager
from .internal.Resources.ILanguageManager import ILanguageManager


class ValidatorSelectorOptions:
    def __init__(self):
        self._defaultValidatorSelector: Callable[[], IValidatorSelector] = lambda: self.DefaultSelector
        self._memberNameValidatorSelector: Callable[[Iterable[str]], IValidatorSelector] = lambda properties: MemberNameValidatorSelector(properties)
        self._rulesetValidatorSelector: Callable[[Iterable[str]], IValidatorSelector] = lambda ruleSets: RulesetValidatorSelector(ruleSets)
        self._compositeValidatorSelectorFactory: Callable[[Iterable[IValidatorSelector]], IValidatorSelector] = lambda selectors: CompositeValidatorSelector(selectors)

    @property
    def DefaultSelector(self) -> IValidatorSelector:
        return DefaultValidatorSelector()

    @property
    def DefaultValidatorSelectorFactory(self) -> Callable[[], IValidatorSelector]:
        return self._defaultValidatorSelector

    @DefaultValidatorSelectorFactory.setter
    def DefaultValidatorSelectorFactory(self, value) -> None:
        self._defaultValidatorSelector = value if value else lambda: self.DefaultSelector

    @property
    def MemberNameValidatorSelectorFactory(self) -> Callable[[Iterable[str]], IValidatorSelector]:
        return self._memberNameValidatorSelector

    @MemberNameValidatorSelectorFactory.setter
    def MemberNameValidatorSelectorFactory(self, value) -> None:
        self._memberNameValidatorSelector = value if value else lambda properties: MemberNameValidatorSelector(properties)

    @property
    def RulesetValidatorSelectorFactory(self) -> Callable[[Iterable[str]], IValidatorSelector]:
        return self._rulesetValidatorSelector

    @RulesetValidatorSelectorFactory.setter
    def RulesetValidatorSelectorFactory(self, value) -> None:
        self._rulesetValidatorSelector = value if value else lambda ruleSets: RulesetValidatorSelector(ruleSets)

    @property
    def CompositeValidatorSelectorFactory(self) -> Callable[[Iterable[IValidatorSelector]], IValidatorSelector]:
        return self._compositeValidatorSelectorFactory

    @CompositeValidatorSelectorFactory.setter
    def CompositeValidatorSelectorFactory(self, value) -> None:
        self._compositeValidatorSelectorFactory = value if value else lambda selectors: CompositeValidatorSelector(selectors)


class ValidatorConfiguration:
    def __init__(self):
        self._propertyNameResolver: Callable[[Type, MemberInfo, Callable[..., Any]], str] = self.DefaultPropertyNameResolver
        self._displayNameResolver: Callable[[Type, MemberInfo, Callable[..., Any]], str] = self.DefaultDisplayNameResolver
        self._messageFormatterFactory: Callable[[], MessageFormatter] = lambda: MessageFormatter()
        self._errorCodeResolver: Callable[[IPropertyValidator], str] = self.DefaultErrorCodeResolver
        self._languageManager: ILanguageManager = LanguageManager()

        self._defaultClassLevelCascadeMode: _CascadeMode = _CascadeMode.Continue
        self._defaultRuleLevelCascadeMode: _CascadeMode = _CascadeMode.Continue

        self._PropertyChainSeparator: str = "."
        self._severity: _Severity = _Severity.Error

    @property
    def CascadeMode(self) -> _CascadeMode:
        if self._defaultClassLevelCascadeMode == self._defaultRuleLevelCascadeMode:
            return self._defaultClassLevelCascadeMode
        elif self._defaultClassLevelCascadeMode == _CascadeMode.Continue and self._defaultRuleLevelCascadeMode == _CascadeMode.Stop:
            return _CascadeMode.Stop  # COMMENT: Original is CascadeMode.StopOnFirstFailure
        else:
            raise Exception(
                "There is no conversion to a single CascadeMode value from the current combination of "
                + "DefaultClassLevelCascadeMode and DefaultRuleLevelCascadeMode. "
                + "Please use these properties instead of the deprecated CascadeMode going forward."
            )

    @CascadeMode.setter
    def CascadeMode(self, value: _CascadeMode) -> None:
        self.DefaultClassLevelCascadeMode = value
        self.DefaultRuleLevelCascadeMode = value

    # region Properties
    @property
    def DefaultClassLevelCascadeMode(self) -> CascadeMode:
        return self._defaultClassLevelCascadeMode

    @DefaultClassLevelCascadeMode.setter
    def DefaultClassLevelCascadeMode(self, value):
        self._defaultClassLevelCascadeMode = value

    @property
    def DefaultRuleLevelCascadeMode(self) -> CascadeMode:
        return self._defaultRuleLevelCascadeMode

    @DefaultRuleLevelCascadeMode.setter
    def DefaultRuleLevelCascadeMode(self, value):
        self._defaultRuleLevelCascadeMode = value

    @property
    def Severity(self) -> _Severity:
        """Default severity level"""
        return self._severity

    @Severity.setter
    def Severity(self, value: _Severity) -> None:
        self._severity = value

    @property
    def PropertyChainSeparator(self) -> str:
        return self._PropertyChainSeparator

    @PropertyChainSeparator.setter
    def PropertyChainSeparator(self, value: str) -> str:
        self._PropertyChainSeparator = value

    @property
    def LanguageManager(self) -> ILanguageManager:
        return self._languageManager

    @LanguageManager.setter
    def LanguageManager(self, value: ILanguageManager):
        self._languageManager = value

    @property
    def ValidatorSelectors(self) -> ValidatorSelectorOptions:
        return ValidatorSelectorOptions()

    @property
    def MessageFormatterFactory(self) -> Callable[[], MessageFormatter]:
        return self._messageFormatterFactory

    @MessageFormatterFactory.setter
    def MessageFormatterFactory(self, value: None | Callable[[], MessageFormatter]):
        if not value:
            value = lambda: MessageFormatter()  # noqa: E731
        self._messageFormatterFactory = value

    @property
    def PropertyNameResolver(self) -> Callable[[Type, MemberInfo, Callable[..., Any]], str]:
        return self._propertyNameResolver

    @PropertyNameResolver.setter
    def PropertyNameResolver(self, value: None | Callable[[Type, MemberInfo, Callable[..., Any]], str]) -> None:
        self._propertyNameResolver = value if value is not None else self.DefaultPropertyNameResolver

    @property
    def DisplayNameResolver(self) -> Callable[[Type, MemberInfo, Callable[..., Any]], str]:
        return self._displayNameResolver

    @DisplayNameResolver.setter
    def DisplayNameResolver(self, value: None | Callable[[Type, MemberInfo, Callable[..., Any]], str]) -> None:
        self._displayNameResolver = value if value is not None else self.DefaultDisplayNameResolver

    # public bool DisableAccessorCache { get; set; }
    # endregion

    @property
    def ErrorCodeResolver(self) -> Callable[[IPropertyValidator], str]:
        return self._errorCodeResolver

    @ErrorCodeResolver.setter
    def ErrorCodeResolver(self, value: Callable[[IPropertyValidator], str]) -> None:
        self._errorCodeResolver = value if value is not None else self.DefaultErrorCodeResolver

    # public Func<ValidationFailure, IValidationContext, object, IValidationRule, IRuleComponent, ValidationFailure> OnFailureCreated { get; set; }

    @staticmethod
    def DefaultPropertyNameResolver(_type: Type, memberInfo: MemberInfo, expression: Callable[..., str]):
        from fluent_validation.internal.PropertyChain import PropertyChain

        if expression is not None:
            chain = PropertyChain.FromExpression(expression)
            if len(chain) > 0:
                return chain.ToString()
        return memberInfo.Name

    @staticmethod
    def DefaultDisplayNameResolver(_type: Type, memberInfo: MemberInfo, expression: Callable[..., str]):
        return None

    @staticmethod
    def DefaultErrorCodeResolver(validator: IPropertyValidator):
        return validator.Name


class ValidatorOptions:
    Global: ValidatorConfiguration = ValidatorConfiguration()
