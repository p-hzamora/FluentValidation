from typing import Callable, Iterable

from src.fluent_validation.internal.CompositeValidatorSelector import CompositeValidatorSelector
from src.fluent_validation.internal.DefaultValidatorSelector import DefaultValidatorSelector
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector
from src.fluent_validation.internal.MemberNameValidatorSelector import MemberNameValidatorSelector
from src.fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector
from .enums import CascadeMode
from .internal.Resources.LanguageManager import LanguageManager
from .internal.Resources.ILanguageManager import ILanguageManager


class ValidatorSelectorOptions:
    def __init__(self):
        self._defaultValidatorSelector: Callable[[], IValidatorSelector] = lambda: self.DefaultSelector
        self._memberNameValidatorSelector: Callable[[Iterable[str]], IValidatorSelector] = lambda properties: MemberNameValidatorSelector(properties)
        self._rulesetValidatorSelector: Callable[[Iterable[str]], IValidatorSelector] = lambda ruleSets: RulesetValidatorSelector(ruleSets)
        self._compositeValidatorSelectorFactory: Callable[[Iterable[IValidatorSelector]], IValidatorSelector] = lambda selectors: CompositeValidatorSelector(selectors)

    @property
    def DefaultSelector() -> IValidatorSelector:
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
        # private Func<Type, MemberInfo, LambdaExpression, string> _propertyNameResolver = DefaultPropertyNameResolver
        # private Func<Type, MemberInfo, LambdaExpression, string> _displayNameResolver = DefaultDisplayNameResolver
        # private Func<MessageFormatter> _messageFormatterFactory = () => new MessageFormatter()
        # private Func<IPropertyValidator, string> _errorCodeResolver = DefaultErrorCodeResolver
        self._languageManager: ILanguageManager = LanguageManager()

        # original C# Library has this vars as CascadeMode.Continue
        self._defaultClassLevelCascadeMode: CascadeMode = CascadeMode.Continue
        self._defaultRuleLevelCascadeMode: CascadeMode = CascadeMode.Stop

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
    def LanguageManager(self) -> ILanguageManager:
        return self._languageManager

    @LanguageManager.setter
    def LanguageManager(self, value: ILanguageManager):
        self._languageManager = value

    # endregion

    @property
    def ValidatorSelectors(self) -> ValidatorSelectorOptions:
        return ValidatorSelectorOptions()


class ValidatorOptions:
    Global: ValidatorConfiguration = ValidatorConfiguration()

