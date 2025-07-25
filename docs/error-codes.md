# Custom Error Codes

A custom error code can also be associated with validation rules by calling the `WithErrorCode` method:

```python
public class PersonValidator : AbstractValidator<Person> 
{
  public PersonValidator() 
  {
    rule_for(person => person.Surname).not_null().WithErrorCode("ERR1234")        
    rule_for(person => person.Forename).not_null()
  }
}
```

The resulting error code can be obtained from the `ErrorCode` property on the `ValidationFailure`:

```python
var validator = new PersonValidator()
var result = validator.Validate(new Person())
foreach (var failure in result.Errors)
{
  print(f"Property: {failure.PropertyName} Error Code: {failure.ErrorCode}")
}
```

The output would be:

```
Property: Surname Error Code: ERR1234
Property: Forename Error Code: NotNullValidator
```

## ErrorCode and Error Messages

The `ErrorCode` is also used to determine the default error message for a particular validator. At a high level:

* The error code is used as the lookup key for an error message. For example, a `not_null()` validator has a default error code of `NotNullValidator`, which used to look up the error messages from the `LanguageManager`. [See the documentation on localization.](localization)
* If you provide an error code, you could also provide a localized message with the name of that error code to create a custom message.
* If you provide an error code but no custom message, the message will fall back to the default message for that validator. You're not required to add a custom message.
* Using `ErrorCode` can also be used to override the default error message. For example, if you use a custom `must()` validator, but you'd like to reuse the `not_null()` validator's default error message, you can call `WithErrorCode("NotNullValidator")` to achieve this result.