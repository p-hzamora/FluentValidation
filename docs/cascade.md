# Setting the Cascade mode

You can set the cascade mode to customise how FluentValidation executes rules and validators when a particular rule in the validator class, or validator in the rule fails.

## Rule-Level Cascade Modes
Imagine you have two validators defined as part of a single rule definition, a `not_null` validator and a `not_equal` validator:

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_for(lambda x: x.Surname).not_null().not_equal("foo")
```

This will first check whether the Surname property is not null and then will check if it's not equal to the string "foo". If the first validator (`not_null`) fails, then by default, the call to `not_equal` will still be invoked. This can be changed for this specific rule only by specifying a cascade mode of `Stop` (omitting the class and constructor definition from now on assume that they are still present as above):

```python
rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().not_equal("foo")
```

Now, if the `not_null` validator fails then the `not_equal` validator will not be executed. This is particularly useful if you have a complex chain where each validator depends on the previous validator to succeed.

The two cascade modes are:
- `Continue` (the default) - always invokes all rules in a validator class, or all validators in a rule, depending on where it is used (see below).
- `Stop` - stops executing a validator class as soon as a rule fails, or stops executing a rule as soon as a validator fails, depending on where it is used (see below).

```eval_rst
.. warning::
  The Stop option is only available in FluentValidation 9.1 and newer. In older versions, you can use StopOnFirstFailure instead (see "Stop vs StopOnFirstFailure").
```

If you have a validator class with multiple rules, and would like this `Stop` behaviour to be set for all of your rules, you could do e.g.:
```python
rule_for(lambda x: x.Forename).Cascade(CascadeMode.Stop).not_null().not_equal("foo")
rule_for(lambda x: x.MiddleNames).Cascade(CascadeMode.Stop).not_null().not_equal("foo")
rule_for(lambda x: x.Surname).Cascade(CascadeMode.Stop).not_null().not_equal("foo")
```
To avoid repeating `Cascade(CascadeMode.Stop)`, you can set a default value for the rule-level cascade mode by setting the `AbstractValidator.RuleLevelCascadeMode` property, resulting in
```python
RuleLevelCascadeMode = CascadeMode.Stop

rule_for(lambda x: x.Forename).not_null().not_equal("foo")
rule_for(lambda x: x.MiddleNames).not_null().not_equal("foo")
rule_for(lambda x: x.Surname).not_null().not_equal("foo")
```
With default global settings, this code will stop executing any rule whose `not_null` call fails, and not call `not_equal`, but it will then continue to the next rule, and always execute all three, regardless of failures. See "Validator Class-Level Cascade Modes" for how to control this behavior. This particular behaviour is useful if you want to create a list of all validation failures, as opposed to only returning the first one.

See "Global Default Cascade Modes" for setting the default value of this property.

## Validator Class-Level Cascade Modes
As well as being set at the rule level, the cascade mode can also be set at validator class-level, using the property `AbstractValidator.ClassLevelCascadeMode`. This controls the cascade behaviour _in between_ rules within that validator, but does not affect the rule-level cascade behaviour described above.

For example, the code above will execute all three rules, even if any of them fail. To stop execution of the validator class completely if any rule fails, you can set `AbstractValidator.ClassLevelCascadeMode` to `Stop`. This will result in complete "fail fast" behavior, and return only return a maximum of one error.

See "Global Default Cascade Modes" for setting the default value of this property.

## Global Default Cascade Modes
To set the default cascade modes at rule-level and/or validator class-level globally, set `ValidatorOptions.Global.DefaultRuleLevelCascadeMode` and/or `ValidatorOptions.Global.DefaultClassLevelCascadeMode` during your application's startup routine. Both of these default to `Continue`.

```eval_rst
.. warning::
  The RuleLevelCascadeMode, ClassLevelCascadeMode, and their global defaults are only available in FluentValidation 11 and newer. See below.
```

## Introduction of RuleLevelCascadeMode and ClassLevelCascadeMode (and deprecation of CascadeMode)
The `AbstractValidator.RuleLevelCascadeMode`, `AbstractValidator.ClassLevelCascadeMode`, and their global defaults were introduced in FluentValidation 11

In older versions, there was only one property controlling cascade modes: `AbstractValidator.CascadeMode`. Changing this value would set the cascade mode at both validator class-level and rule-level. Therefore, for example, if you wanted to have the above-described functionality where you create a list of validation errors, by stopping on failure at rule-level to avoid crashes, but continuing at validator class-level, you would need to set `AbstractValidator.CascadeMode` to `Continue`, and then repeat `Cascade(CascadeMode.Stop)` on every rule chain (or use the deprecated `StopOnFirstFailure` with a warning see "Stop vs StopOnFirstFailure").

The new properties enable finer control of the cascade mode at the different levels, with less repetition.

```eval_rst
.. warning::
  In FluentValidation11, there are _no_ breaking changes to cascade modes. The `AbstractValidator.CascadeMode` property (and its global default property) are still present, and they function exactly the same as they did before, but they do so by setting / returning the values of `RuleLevelCascadeMode` and `ClassLevelCascadeMode`, as opposed to being used by the code directly.

  However, `AbstractValidator.CascadeMode` and its global default are deprecated, and will be removed in a future version. To convert to the new properties, see `the upgrade guide <upgrading-to-11.html#cascade-mode-changes>`_.
```

## Stop vs StopOnFirstFailure

In FluentValidation 9.0 and older, the `CascadeMode.StopOnFirstFailure` option was used to provide control over the default cascade mode at rule-level, but its use was not intuitive. There was no  `CascadeMode.Stop` option. 

With `StopOnFirstFailure`,  the following would provide the example behavior described previously (stop any rule if it fails, but then continue executing at validator class-level, so that all rules are executed):

```python
CascadeMode = CascadeMode.StopOnFirstFailure

rule_for(lambda x: x.Forename).not_null().not_equal("foo")
rule_for(lambda x: x.MiddleNames).not_null().not_equal("foo")
rule_for(lambda x: x.Surname).not_null().not_equal("foo")
```
If they all fail, you will get three validation errors. That is the equivalent of doing

```python
rule_for(lambda x: x.Forename).Cascade(CascadeMode.StopOnFirstFailure).not_null().not_equal("foo")
rule_for(lambda x: x.MiddleNames).Cascade(CascadeMode.StopOnFirstFailure).not_null().not_equal("foo")
rule_for(lambda x: x.Surname).Cascade(CascadeMode.StopOnFirstFailure).not_null().not_equal("foo")
```
This behaviour caused a lot of confusion over the years, so the `Stop` option was introduced in FluentValidation 9.1. Using `Stop` instead of `StopOnFirstFailure`, _any_ failure at all would stop execution, so only the first failure result would be returned.

The `Stop` option was introduced rather than changing the behaviour of `StopOnFirstFailure` as this would've been a very subtle breaking change, so we thought it was best to maintain the existing behaviour while adding a new option. `StopOnFirstFailure` was marked as Obsolete in FluentValidation 9.1, and generated compiler warnings.

See also the FluentValidation 11 changes described above, that further change how the above code would be written. `StopOnFirstFailure` is still available as of version 11 and has no breaking changes to how it functions. However, in a future version, it _will_ be removed, now that it's possible to replicate its behavior using the new properties `AbstractValidator.RuleLevelCascadeMode` and `AbstractValidator.ClassLevelCascadeMode`.
