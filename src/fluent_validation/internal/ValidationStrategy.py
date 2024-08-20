from typing import Callable


class ValidationStrategy[T]:
    def __init__(self):
        self._properties: list[str]
        self._ruleSets: list[str]
        self._throw: bool = False
        # self._customSelector:IValidatorSelector

    def IncludeProperties(self, *properties: str) -> "ValidationStrategy[T]":
        if self._properties is None:
            self._properties = list(properties)
        else:
            self._properties.extend(properties)
        return self


    def IncludeProperties(self, *propertyExpressions:Callable[[T,object]])->"ValidationStrategy[T]":
        if (self._properties == None):
            self._properties = list(MemberNameValidatorSelector.MemberNamesFromExpressions(propertyExpressions));
        }
        else {
            self._properties.AddRange(MemberNameValidatorSelector.MemberNamesFromExpressions(propertyExpressions));
        }

        return self

#     def IncludeRulesNotInRuleSet(self)->"ValidationStrategy[T]":
#         self._ruleSets ??= new List<string>();
#         self._ruleSets.Add(RulesetValidatorSelector.DefaultRuleSetName);
#         return self

#     def IncludeAllRuleSets()->"ValidationStrategy[T]":
#         self._ruleSets ??= new List<string>();
#         self._ruleSets.Add(RulesetValidatorSelector.WildcardRuleSetName);
#         return self

#     def IncludeRuleSets(params string[] ruleSets)->"ValidationStrategy[T]":
#         if (ruleSets != None && ruleSets.Length > 0) {
#             if (self._ruleSets == None) {
#                 self._ruleSets = new List<string>(ruleSets);
#             }
#             else {
#                 self._ruleSets.AddRange(ruleSets);
#             }
#         }

#         return self

#     def UseCustomSelector(IValidatorSelector selector)->"ValidationStrategy[T]":
#         if (selector == None) throw new ArgumentNoneException(nameof(selector));
#         _customSelector = selector;
#         return self

#     def ThrowOnFailures()->"ValidationStrategy[T]":
#         _throw = true;
#         return self

    private IValidatorSelector GetSelector() {
        IValidatorSelector selector = None;

        if (self._properties != None || self._ruleSets != None || _customSelector != None) {
            var selectors = new List<IValidatorSelector>(3);

            if (_customSelector != None) {
                selectors.Add(_customSelector);
            }

            if (self._properties != None) {
                selectors.Add(ValidatorOptions.Global.ValidatorSelectors.MemberNameValidatorSelectorFactory(self._properties.ToArray()));
            }

            if (self._ruleSets != None) {
                selectors.Add(ValidatorOptions.Global.ValidatorSelectors.RulesetValidatorSelectorFactory(self._ruleSets.ToArray()));
            }

            selector = selectors.Count == 1 ? selectors[0] : ValidatorOptions.Global.ValidatorSelectors.CompositeValidatorSelectorFactory(selectors);
        }
        else {
            selector = ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory();
        }

        return selector;
    }

    def BuildContext(self, instance:T)->"ValidationContext[T]":
        return ValidationContext[T](instance, None, GetSelector()) {
            ThrowOnFailures = _throw
