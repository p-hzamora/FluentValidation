# RuleSets

RuleSets allow you to group validation rules together which can be executed together as a group whilst ignoring other rules:

For example, let's imagine we have 3 properties on a Person object (Id, Surname and Forename) and have a validation rule for each. We could group the Surname and Forename rules together in a “Names” RuleSet:

```python
from dataclasses import dataclass

class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_set(
            "Names",
            lambda: (
                self.rule_for(lambda x: x.Surname).not_null(),
                self.rule_for(lambda x: x.Forename).not_null(),
            ),
        )
        self.rule_for(lambda x: x.Id).not_equal(0)
```

Here the two rules on Surname and Forename are grouped together in a “Names” RuleSet. We can invoke only these rules by passing additional options to the validate method:

```python
validator = PersonValidator()
person = Person()
result = validator.validate(person, lambda options: options.IncludeRuleSets("Names"))
```

This allows you to break down a complex validator definition into smaller segments that can be executed in isolation. If you call `validate` without passing a ruleset then only rules not in a RuleSet will be executed.

You can execute multiple rulesets by passing multiple ruleset names to `IncludeRuleSets`:

```python
result = validator.validate(
    person,
    lambda options: (
        options.IncludeRuleSets(
            "Names",
            "MyRuleSet",
            "SomeOtherRuleSet",
        )
    ),
)
```

You can also include all the rules not part of a ruleset by using calling `IncludeRulesNotInRuleSet`, or by using the special name "default" (case insensitive):

```python
validator.validate(
    person,
    lambda options: (
        # Option 1: IncludeRulesNotInRuleSet is the equivalent of using the special ruleset name "default"
        options.IncludeRuleSets("Names").IncludeRulesNotInRuleSet(),
        # Option 2: This does the same thing.
        options.IncludeRuleSets("Names", "default"),
    ),
)
```

This would execute rules in the MyRuleSet set, and those rules not in any ruleset. Note that you shouldn't create your own ruleset called "default", as FluentValidation will treat these rules as not being in a ruleset.

You can force all rules to be executed regardless of whether or not they're in a ruleset by calling `IncludeAllRuleSets` (this is the equivalent of using `IncludeRuleSets("*")` )

```python
validator.validate(
    person,
    lambda options: (options.IncludeAllRuleSets()),
)
```
<!-- 
## RuleSets in FluentValidation 9.0 (or older)

```eval_rst
.. warning::
  The syntax in this section is deprecated and will be removed in FluentValidation 10.
```

Invoking RuleSets in FluentValidation 9.0 and older requires the use of a slightly different syntax, by passing the ruleset names to a named `ruleSet` parameter:

```python
validator = PersonValidator()
person = Person()
result = validator.validate(person, ruleSet: "Names")
```

This is the equivalent of the first example above which executes a single ruleset.

You can execute multiple rulesets by using a comma-separated list of strings:

```python
validator.validate(person, ruleSet: "Names,MyRuleSet,SomeOtherRuleSet")
```

You can also include all the rules not part of a ruleset by using the special name "default" (case insensitive):

```python
validator.validate(person, ruleSet: "default,MyRuleSet")
```

This would execute rules in the MyRuleSet set, and those rules not in any ruleset. Note that you shouldn't create your own ruleset called "default", as FluentValidation will treat these rules as not being in a ruleset.

You can force all rules to be executed regardless of whether or not they're in a ruleset by specifying a ruleset of "*":

```python
validator.validate(person, ruleSet: "*")
``` -->
