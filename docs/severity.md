# Setting the Severity Level

Given the following example that validates a `Person` object:

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)

        self.rule_for(lambda person: person.Surname).not_null()
        self.rule_for(lambda person: person.Forename).not_null()

```

By default, if these rules fail they will have a severity of `Error`. This can be changed by calling the `with_severity` method. For example, if we wanted a missing surname to be identified as a warning instead of an error then we could modify the above line to:

```
rule_for(x => x.Surname).not_null().with_severity(Severity.Warning)
```

In version 9.0 and above a callback can be used instead, which also gives you access to the item being validated:

```
rule_for(person => person.Surname).not_null().with_severity(person => Severity.Warning)
```

In this case, the `ValidationResult` would still have an `is_valid` result of `False`. However, in the list of `Errors`, the `ValidationFailure` associated with this field will have its `Severity` property set to `Warning`:

```python
validator = PersonValidator()
result = validator.validate(Person())
for failure in result.errors:
    print(f"Property: {failure.PropertyName} Severity: {failure.Severity}")

```

The output would be:

```
Property: Surname Severity: Warning
Property: Forename Severity: Error
```

By default, the severity level of every validation rule is `Error`. Available options are `Error`, `Warning`, or `Info`.

To set the severity level globally, you can set the `Severity` property on the static `G` class during your application's startup routine:

```python
ValidatorOptions.Global.Severity = Severity.Info
```

This can then be overridden by individual rules.