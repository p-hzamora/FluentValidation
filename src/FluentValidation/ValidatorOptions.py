from .enums import CascadeMode
from .internal.Resources.LanguageManager import LanguageManager
from .internal.Resources.ILanguageManager import ILanguageManager


class ValidatorConfiguration:
    def __init__(self):
        # private Func<Type, MemberInfo, LambdaExpression, string> _propertyNameResolver = DefaultPropertyNameResolver;
        # private Func<Type, MemberInfo, LambdaExpression, string> _displayNameResolver = DefaultDisplayNameResolver;
        # private Func<MessageFormatter> _messageFormatterFactory = () => new MessageFormatter();
        # private Func<IPropertyValidator, string> _errorCodeResolver = DefaultErrorCodeResolver;
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


class ValidatorOptions:
    Global: ValidatorConfiguration = ValidatorConfiguration()
