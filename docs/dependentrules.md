# Dependent Rules


By default, all rules in FluentValidation are separate and cannot influence one another. This is intentional and necessary for asynchronous validation to work. However, there may be some cases where you want to ensure that some rules are only executed after another has completed. You can use `dependent_rules` to do this.

To use dependent rules, call the `dependent_rules` method at the end of the rule that you want others to depend on. This method accepts a lambda expression inside which you can define other rules that will be executed only if the first rule passes:

```python
self.rule_for(x => x.Surname).not_null()
.dependent_rules(lambda:

    self.rule_for(x => x.Forename).not_null()
)
```

Here the rule against Forename will only be run if the Surname rule passes.

_Author's note_: Personally I do not particularly like using dependent rules as I feel it's fairly hard to read, especially with a complex set of rules. In many cases, it can be simpler to use `when` conditions combined with `CascadeMode` to prevent rules from running in certain situations. Even though this can sometimes mean more duplication, it is often easier to read.