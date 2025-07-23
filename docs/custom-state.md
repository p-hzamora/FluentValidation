# Custom State

There may be an occasion where you'd like to return contextual information about the state of your validation rule when it was run. The `with_state` method allows you to associate any custom data with the validation results.

We could assign a custom state by modifying a line to read:

```python
public class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_for(lambda person: person.Surname).not_null()
        self.rule_for(lambda person: person.Forename).not_null().with_state(person => 1234)  
```

This state is then available within the `CustomState` property of the `ValidationFailure`.

```python
validator = PersonValidator()
result = validator.validate(Person())

for failure in result.errors:
  print(f"Property: {failure.PropertyName} State: {failure.CustomState}")
```

The output would be:

```
Property: Surname State:
Property: Forename State: 1234
```

By default the `CustomState` property will be `None` if `with_state` hasn't been called.
