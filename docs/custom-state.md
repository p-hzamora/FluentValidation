# Custom State

There may be an occasion where you'd like to return contextual information about the state of your validation rule when it was run. The `WithState` method allows you to associate any custom data with the validation results.

We could assign a custom state by modifying a line to read:

```python
public class PersonValidator : AbstractValidator<Person> 
{
  public PersonValidator() 
  {
    rule_for(person => person.Surname).not_null()
    rule_for(person => person.Forename).not_null().WithState(person => 1234)  
  }
}
```

This state is then available within the `CustomState` property of the `ValidationFailure`.

```python
var validator = new PersonValidator()
var result = validator.Validate(new Person())
foreach (var failure in result.Errors) 
{
  Console.WriteLine($"Property: {failure.PropertyName} State: {failure.CustomState}")
}
```

The output would be:

```
Property: Surname State:
Property: Forename State: 1234
```

By default the `CustomState` property will be `null` if `WithState` hasn't been called.
