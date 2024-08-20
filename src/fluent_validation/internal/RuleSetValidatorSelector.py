from typing import Iterable, override
from src.fluent_validation.IValidationContext import IValidationContext
from src.fluent_validation.IValidationRule import IValidationRule
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector
from src.fluent_validation.internal.IncludeRule import IIncludeRule



def get_or_add(dictionary:dict, key:str, factory)->set:
    if key not in dictionary:
        dictionary[key] = factory()
    return dictionary[key]

class RulesetValidatorSelector(IValidatorSelector):
    
    DefaultRuleSetName:str = "default"
    WildcardRuleSetName:str = "*"

    DefaultRuleSetNameInArray:list[str]= [DefaultRuleSetName]

    @property
    def RuleSets(self)->Iterable[str]:
        return self._rulesetsToExecute

    def __init__(self, rulesetsToExecute:Iterable[str]):
        self._rulesetsToExecute:Iterable[str] = rulesetsToExecute

    @override
    def CanExecute(self, rule:IValidationRule, propertyPath:str, context:IValidationContext):

        executed:set = get_or_add(context.RootContextData,"_FV_RuleSetsExecuted", lambda: set())

        if (rule.RuleSets is None | len(rule.RuleSets) == 0) & self._rulesetsToExecute.Any():
            if self.IsIncludeRule(rule):
                return True

        if (rule.RuleSets is None | len(rule.RuleSets) == 0) and not self._rulesetsToExecute.Any():
            executed.add(self.DefaultRuleSetName)
            return True

        if self.DefaultRuleSetName.lower() in self._rulesetsToExecute:
            if rule.RuleSets is None | len(rule.RuleSets) == 0 | self.DefaultRuleSetName.lower() in rule.RuleSets:
                executed.add(self.DefaultRuleSetName)
                return True

        # if rule.RuleSets is not None & len(rule.RuleSets) > 0 & self._rulesetsToExecute.Any():
        #     #FIXME [ ]: 
        #     intersection = [rule.RuleSets.intersection(self._rulesetsToExecute.lower())]
        #     if intersection.Any():
        #         for r in intersection.ForEach(r => executed.add(r))
        #         return True

        if self.WildcardRuleSetName in self._rulesetsToExecute:
            if rule.RuleSets is None | len(rule.RuleSets) == 0:
                executed.add(self.DefaultRuleSetName)
            else:
                for r in rule.RuleSets:
                    executed.add(r)
            return True
        return False

    def IsIncludeRule(rule:IValidationRule)->bool:
        return issubclass(rule,IIncludeRule)

    @staticmethod
    def LegacyRulesetSplit(ruleSet:str)->list[str]:
        return [x.strip() for x in ruleSet.split(",","")]


    #TODOH: Check

    # internal static string[] LegacyRulesetSplit(string ruleSet) {
    # 	var ruleSetNames = ruleSet.Split(',', ';')
    # 		.Select(x => x.Trim())
    # 		.ToArray();

    # 	return ruleSetNames;
    # }