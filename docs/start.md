# Creating your first validator

To define a set of validation rules for a particular object, you will need to create a class that inherits from `AbstractValidator[T]`, where `T` is the type of class that you wish to validate.

For example, imagine that you have a Customer class:

```python
from dataclasses import dataclass

@dataclass
class Customer: 
  Id:int = None
  Surname:str = None
  Forename:str = None
  Discount:float = None
  Address:str = None

```

You would define a set of validation rules for this class by inheriting from `AbstractValidator[Customer]`:

```python
from fluent_validation import AbstractValidator

class CustomerValidator(AbstractValidator[Customer]):
  ...
```

The validation rules themselves should be defined in the validator class's constructor.

To specify a validation rule for a particular property, call the `rule_for` method, passing a lambda expression
that indicates the property that you wish to validate. For example, to ensure that the `Surname` property is not None,
the validator class would look like this:

```python
from fluent_validation import AbstractValidator

class CustomerValidator(AbstractValidator[Customer]):
  def __init__(self)-> None:
    super().__init__()
    self.rule_for(lambda customer: customer.Surname).not_null()
```
To run the validator, instantiate the validator object and call the `validate` method, passing in the object to validate.

```python
customer = Customer()
validator = CustomerValidator()

result = validator.validate(customer)
```

The `validate` method returns a `ValidationResult` object. This contains two properties:

- `is_valid` - a boolean that says whether the validation succeeded.
- `errors` - a collection of `ValidationFailure` objects containing details about any validation failures.

The following code would write any validation failures to the console:

```python
customer = Customer()
validator = CustomerValidator()

results = validator.validate(customer)

if not results.is_valid:
  for failure in results.errors:
    print(f"Property {failure.PropertyName} failed validation. Error was: {failure.ErrorMessage}")
```

You can also call `to_string` on the `ValidationResult` to combine all error messages into a single string. By default, the messages will be separated with new lines, but if you want to customize this behaviour you can pass a different separator character to `to_string`.

```python
results = validator.validate(customer)
allMessages:str = results.to_string("~")     # In this case, each message will be separated with a `~`
```

*Note* : if there are no validation errors, `to_string()` will return an empty string.

# Chaining validators

You can chain multiple validators together for the same property:

```python
from fluent_validation import AbstractValidator

CustomerValidator(AbstractValidator[Customer]):
  def __init__(self)-> None:
    super().__init__()
    rule_for(lambda customer: customer.Surname).not_null().not_equal("foo")

```

This would ensure that the surname is not None and is not equal to the string 'foo'.

# Throwing Exceptions

Instead of returning a `ValidationResult`, you can alternatively tell fluent_validation to throw an exception if validation fails by using the `validate_and_throw` method:

```python
customer = Customer()
validator = CustomerValidator()

validator.validate_and_throw(customer)
```

This throws a `ValidationException` which contains the error messages in the errors property.

```python
from fluent_validation import AbstractValidator
```

The `validate_and_throw` method is helpful wrapper around fluent_validation's options API, and is the equivalent of doing the following:

```python
validator.validate(customer, lambda options: options.ThrowOnFailures())
```

If you need to combine throwing an exception with [Rule Sets](rulesets), or validating individual properties, you can combine both options using this syntax:

```python
validator.validate(
    customer,
    lambda options: (
        options.ThrowOnFailures(),
        options.IncludeRuleSets("MyRuleSets"),
        options.IncludeProperties(lambda x: x.Name),
    ),
)
```

<!-- It is also possible to customize type of exception thrown, [which is covered in this section](advanced.html#customizing-the-validation-exception). -->

# Complex Properties

Validators can be re-used for complex properties. For example, imagine you have two classes, Customer and Address:

```python
@dataclass
class Customer 
  Name:str=None
  Address:Address=None

@dataclass
class Address 
  Line1:str = None
  Line2:str = None
  Town:str = None
  Country:str = None
  Postcode:str = None
```

... and you define an AddressValidator:

```python
class AddressValidator(AbstractValidator[Address]):
  def __init__(self):
    super().__init__()
    self.rule_for(lambda address: address.Postcode).not_null()
    #etc
```

... you can then re-use the AddressValidator in the CustomerValidator definition:

```python
class CustomerValidator(AbstractValidator[Customer]):
  def __init__(self):
    super().__init__()
    self.rule_for(lambda customer: customer.Name).not_null()
    rule_for(lambda customer: customer.Address).set_validator(AddressValidator())
```

... so when you call `validate` on the CustomerValidator it will run through the validators defined in both the CustomerValidator and the AddressValidator and combine the results into a single ValidationResult.

If the child property is None, then the child validator will not be executed.

Instead of using a child validator, you can define child rules inline, eg:

```python
rule_for(lambda customer: customer.Address.Postcode).not_null()
```

In this case, a None check will *not* be performed automatically on `Address`, so you should explicitly add a condition

```python
rule_for(lambda customer: customer.Address.Postcode).not_null().when(lambda customer: customer.Address != None)
```
