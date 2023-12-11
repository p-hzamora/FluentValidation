from enum import Enum

class CascadeMode(Enum):
    Continue=0
    Stop = 1    


class ValidatorConfiguration:
    # private Func<Type, MemberInfo, LambdaExpression, string> _propertyNameResolver = DefaultPropertyNameResolver;
    # private Func<Type, MemberInfo, LambdaExpression, string> _displayNameResolver = DefaultDisplayNameResolver;
    # private Func<MessageFormatter> _messageFormatterFactory = () => new MessageFormatter();
    # private Func<IPropertyValidator, string> _errorCodeResolver = DefaultErrorCodeResolver;
    # private ILanguageManager _languageManager = new LanguageManager();

    # original C# Library has this vars as CascadeMode.Continue
    _defaultClassLevelCascadeMode:CascadeMode = CascadeMode.Continue
    _defaultRuleLevelCascadeMode:CascadeMode = CascadeMode.Stop

    #region Properties
    @property
    def DefaultClassLevelCascadeMode(self)->CascadeMode: return self._defaultClassLevelCascadeMode
    @DefaultClassLevelCascadeMode.setter
    def DefaultClassLevelCascadeMode(self,value): self._defaultClassLevelCascadeMode= value
    
    @property
    def DefaultRuleLevelCascadeMode(self)->CascadeMode: return self._defaultRuleLevelCascadeMode
    @DefaultRuleLevelCascadeMode.setter
    def DefaultRuleLevelCascadeMode(self,value): self._defaultRuleLevelCascadeMode= value
    #endregion


class ValidatorOptions:
    Global:ValidatorConfiguration = ValidatorConfiguration()
