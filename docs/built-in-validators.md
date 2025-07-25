# Built-in Validators

FluentValidation ships with several built-in validators. The error message for each validator can contain special placeholders that will be filled in when the error message is constructed.

## not_null Validator
Ensures that the specified property is not null.

Example:
```python
self.rule_for(lambda customer: customer.Surname).not_null()
```
Example error: *'Surname' must not be empty.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## not_empty Validator
Ensures that the specified property is not null, an empty string or whitespace (or the default value for value types, e.g., 0 for `int`).
when used on an IEnumerable (such as arrays, collections, lists, etc.), the validator ensures that the IEnumerable is not empty.

Example:
```python
self.rule_for(lambda customer: customer.Surname).not_empty()
```
Example error: *'Surname' should not be empty.*
String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## not_equal Validator

Ensures that the value of the specified property is not equal to a particular value (or not equal to the value of another property).

Example:
```python
#Not equal to a particular value
self.rule_for(lambda customer: customer.Surname).not_equal("Foo")

#Not equal to another property
self.rule_for(lambda customer: customer.Surname).not_equal(lambda customer: customer.Forename)
```
Example error: *'Surname' should not be equal to 'Foo'*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{ComparisonValue}` – Value that the property should not equal
* `{ComparisonProperty}` – Name of the property being compared against (if any)
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

Optionally, a comparer can be provided to ensure a specific type of comparison is performed:

```python
self.rule_for(lambda customer: customer.Surname).not_equal("Foo", StringComparer.OrdinalIgnoreCase)
```

```eval_rst
.. warning::
  FluentValidation versions prior to 9 perform a *culture specific* comparison when using `equal` or `not_equal` with string properties. Starting with version 9, this is changed to an ordinal comparison.
```

If you are using FluentValidation 8.x (or older), you can force an ordinal comparison by using

```python
self.rule_for(lambda customer: customer.Surname).not_equal("Foo", StringComparer.Ordinal)
```
If you are using FluentValidation 9 (or newer), ordinal will be the default behaviour. If you wish to do a culture-specific comparison instead, you should pass `StringComparer.CurrentCulture` as the second parameter.

## equal Validator
Ensures that the value of the specified property is equal to a particular value (or equal to the value of another property).

Example:
```python
#equal to a particular value
self.rule_for(lambda customer: customer.Surname).equal("Foo")

#equal to another property
self.rule_for(lambda customer: customer.Password).equal(lambda customer: customer.PasswordConfirmation)
```
Example error: *'Surname' should be equal to 'Foo'*
String format args:
* `{PropertyName}` – Name of the property being validated
* `{ComparisonValue}` – Value that the property should equal
* `{ComparisonProperty}` – Name of the property being compared against (if any)
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

```python
self.rule_for(lambda customer: customer.Surname).equal("Foo", StringComparer.OrdinalIgnoreCase)
```

```eval_rst
.. warning::
  FluentValidation versions prior to 9 perform a *culture specific* comparison when using `equal` or `not_equal` with string properties. Starting with version 9, this is changed to an ordinal comparison.
```

If you are using FluentValidation 8.x (or older), you can force an ordinal comparison by using

```python
self.rule_for(lambda customer: customer.Surname).equal("Foo", StringComparer.Ordinal)
```

If you are using FluentValidation 9 (or newer), ordinal will be the default behaviour. If you wish to do a culture-specific comparison instead, you should pass `StringComparer.CurrentCulture` as the second parameter.

## length Validator
Ensures that the length of a particular string property is within the specified range. However, it doesn't ensure that the string property isn't null.

Example:
```python
self.rule_for(lambda customer: customer.Surname).length(1, 250) #must be between 1 and 250 chars (inclusive)
```
Example error: *'Surname' must be between 1 and 250 characters. You entered 251 characters.*

Note: Only valid on string properties.

String format args:
* `{PropertyName}` – Name of the property being validated
* `{min_length}` – Minimum length
* `{max_length}` – Maximum length
* `{total_length}` – Number of characters entered
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## max_length Validator
Ensures that the length of a particular string property is no longer than the specified value.

Example:
```python
self.rule_for(lambda customer: customer.Surname).MaximumLength(250) #must be 250 chars or fewer
```
Example error: *The length of 'Surname' must be 250 characters or fewer. You entered 251 characters.*

Note: Only valid on string properties.

String format args:
* `{PropertyName}` – Name of the property being validated
* `{max_length}` – Maximum length
* `{total_length}` – Number of characters entered
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## min_length Validator
Ensures that the length of a particular string property is longer than the specified value.

Example:
```python
self.rule_for(lambda customer: customer.Surname).MinimumLength(10) #must be 10 chars or more
```
Example error: *The length of 'Surname' must be at least 10 characters. You entered 5 characters.*

Note: Only valid on string properties.

String format args:
* `{PropertyName}` – Name of the property being validated
* `{min_length}` – Minimum length
* `{total_length}` – Number of characters entered
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Less Than Validator
Ensures that the value of the specified property is less than a particular value (or less than the value of another property).

Example:
```python
#Less than a particular value
self.rule_for(lambda customer: customer.CreditLimit).less_than(100)

#Less than another property
self.rule_for(lambda customer: customer.CreditLimit).less_than(lambda customer: customer.MaxCreditLimit)
```
Example error: *'Credit Limit' must be less than 100.*

Notes: Only valid on types that implement `IComparable[T]`

String format args:
* `{PropertyName}` – Name of the property being validated
* `{ComparisonValue}` – Value to which the property was compared
* `{ComparisonProperty}` – Name of the property being compared against (if any)
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Less Than Or equal Validator
Ensures that the value of the specified property is less than or equal to a particular value (or less than or equal to the value of another property).

Example:
```python
#Less than a particular value
self.rule_for(lambda customer: customer.CreditLimit).less_than_or_equal_to(100)

#Less than another property
self.rule_for(lambda customer: customer.CreditLimit).less_than_or_equal_to(lambda customer: customer.MaxCreditLimit)
```
Example error: *'Credit Limit' must be less than or equal to 100.*
Notes: Only valid on types that implement `IComparable[T]`
* `{PropertyName}` – Name of the property being validated
* `{ComparisonValue}` – Value to which the property was compared
* `{ComparisonProperty}` – Name of the property being compared against (if any)
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Greater Than Validator
Ensures that the value of the specified property is greater than a particular value (or greater than the value of another property).

Example:
```python
#Greater than a particular value
self.rule_for(lambda customer: customer.CreditLimit).greater_than(0)

#Greater than another property
self.rule_for(lambda customer: customer.CreditLimit).greater_than(lambda customer: customer.MinimumCreditLimit)
```
Example error: *'Credit Limit' must be greater than 0.*
Notes: Only valid on types that implement `IComparable[T]`
* `{PropertyName}` – Name of the property being validated
* `{ComparisonValue}` – Value to which the property was compared
* `{ComparisonProperty}` – Name of the property being compared against (if any)
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Greater Than Or equal Validator
Ensures that the value of the specified property is greater than or equal to a particular value (or greater than or equal to the value of another property).

Example:
```python
#Greater than a particular value
self.rule_for(lambda customer: customer.CreditLimit).greater_than_or_equal_to(1)

#Greater than another property
rule_for(lambda customer: customer.CreditLimit).greater_than_or_equal_to(lambda customer: customer.self.MinimumCreditLimit)
```
Example error: *'Credit Limit' must be greater than or equal to 1.*
Notes: Only valid on types that implement `IComparable[T]`
* `{PropertyName}` – Name of the property being validated
* `{ComparisonValue}` – Value to which the property was compared
* `{ComparisonProperty}` – Name of the property being compared against (if any)
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Predicate Validator
(Also known as `must`)

Passes the value of the specified property into a delegate that can perform custom validation logic on the value.

Example:
```
self.rule_for(lambda customer: customer.Surname).must(lambda surname: surname == "Foo")
```

Example error: *The specified condition was not met for 'Surname'*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

Note that there is an additional overload for `must` that also accepts an instance of the parent object being validated. This can be useful if you want to compare the current property with another property from inside the predicate:

```
rule_for(lambda customer: customer.Surname).must((customer, lambda surname): surname != customer.Forename)
```

Note that in this particular example, it would be better to use the cross-property version of `not_equal`.

## Regular Expression Validator
Ensures that the value of the specified property matches the given regular expression.

Example:
```python
self.rule_for(lambda customer: customer.Surname).matches("some regex here")
```
Example error: *'Surname' is not in the correct format.*
String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{RegularExpression}` – Regular expression that was not matched
* `{PropertyPath}` - The full path of the property

## Email Validator
Ensures that the value of the specified property is a valid email address format.

Example:
```python
self.rule_for(lambda customer: customer.Email).email_address()
```
Example error: *'Email' is not a valid email address.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

The email address validator can work in 2 modes. The default mode just performs a simple check that the string contains an "@" sign which is not at the beginning or the end of the string. This is an intentionally naive check to match the behaviour of ASP.NET Core's `EmailAddressAttribute`, which performs the same check. For the reasoning behind this, see [this post](https://github.com/dotnet/corefx/issues/32740):

From the comments:

> "The check is intentionally naive because doing something infallible is very hard. The email really should be validated in some other way, such as through an email confirmation flow where an email is actually sent. The validation attribute is designed only to catch egregiously wrong values such as for a U.I."

Alternatively, you can use the old email validation behaviour that uses a regular expression consistent with the .NET 4.x version of the ASP.NET `EmailAddressAttribute`. You can use this behaviour in FluentValidation by calling `rule_for(lambda x: x.Email).email_address(EmailValidationMode.Net4xRegex)`. Note that this approach is deprecated and will generate a warning as regex-based email validation is not recommended.

```eval_rst
.. note::
  In FluentValidation 9, the ASP.NET Core-compatible "simple" check is the default mode. In FluentValidation 8.x (and older), the Regex mode is the default.
```

## Credit Card Validator
Checks whether a string property could be a valid credit card number.

Example:
```python
self.rule_for(lambda x: x.CreditCard).credit_card()
```
Example error: *'Credit Card' is not a valid credit card number.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Enum Validator
Checks whether a numeric value is valid to be in that enum. This is used to prevent numeric values from being cast to an enum type when the resulting value would be invalid. For example, the following is possible:

```python
class ErrorLevel(enum):
  Error = 1,
  Warning = 2,
  Notice = 3

@dataclass
class Model
  errorLevel: ErrorLevel = 0

self.var model = Model(errorLevel = 4)
```
<!-- self.model.errorLevel = (ErrorLevel)4 -->

<!-- The compiler will allow this, but a value of 4 is technically not valid for this enum. The Enum validator can prevent this from happening. -->

```python
self.rule_for(lambda x: x.errorLevel).is_in_enum()
```
Example error: *'Error Level' has a range of values which does not include '4'.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Enum Name Validator
Checks whether a string is a valid enum name.

Example:
```python
# For a case sensitive comparison
self.rule_for(lambda x: x.ErrorLevelName).is_enum_name(ErrorLevel)

# For a case-insensitive comparison
self.rule_for(lambda x: x.ErrorLevelName).is_enum_name(ErrorLevel, caseSensitive=False)
```
Example error: *'Error Level' has a range of values which does not include 'Foo'.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Empty Validator
Opposite of the `not_empty` validator. Checks if a property value is null, or is the default value for the type.
when used on an IEnumerable (such as arrays, collections, lists, etc.), the validator ensures that the IEnumerable is empty.

Example:
```python
self.rule_for(lambda x: x.Surname).empty()
```
Example error: *'Surname' must be empty.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## Null Validator
Opposite of the `not_null` validator. Checks if a property value is null.

Example:
```python
self.rule_for(lambda x: x.Surname).Null()
```
Example error: *'Surname' must be empty.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{PropertyPath}` - The full path of the property

## exclusive_between Validator
Checks whether the property value is in a range between the two specified numbers (exclusive).

Example:
```python
self.rule_for(lambda x: x.Id).exclusive_between(1,10)
```
Example error: *'Id' must be between 1 and 10 (exclusive). You entered 1.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{From}` – Lower bound of the range
* `{To}` – Upper bound of the range
* `{PropertyPath}` - The full path of the property

## inclusive_between Validator
Checks whether the property value is in a range between the two specified numbers (inclusive).

Example:
```python
self.rule_for(lambda x: x.Id).inclusive_between(1,10)
```
Example error: *'Id' must be between 1 and 10. You entered 0.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{From}` – Lower bound of the range
* `{To}` – Upper bound of the range
* `{PropertyPath}` - The full path of the property

## PrecisionScale Validator
Checks whether a decimal value has the specified precision and scale.

Example:
```python
self.rule_for(lambda x: x.Amount).precision_scale(4, 2, False)
```
Example error: *'Amount' must not be more than 4 digits in total, with allowance for 2 decimals. 5 digits and 3 decimals were found.*

String format args:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Current value of the property
* `{ExpectedPrecision}` – Expected precision
* `{ExpectedScale}` – Expected scale
* `{Digits}` – Total number of digits in the property value
* `{ActualScale}` – Actual scale of the property value
* `{PropertyPath}` - The full path of the property

Note that the 3rd parameter of this method is `ignoreTrailingZeros`. when set to `True`, trailing zeros after the decimal point will not count towards the expected number of decimal places. 

Example:
- when `ignoreTrailingZeros` is `False` then the decimal `123.4500` will be considered to have a precision of 7 and scale of 4
- when `ignoreTrailingZeros` is `True` then the decimal `123.4500` will be considered to have a precision of 5 and scale of 2. 

Note that prior to FluentValidation 11.4, this this method was called `ScalePrecision` instead and had its parameters reversed. For more details [see this GitHub issue](https://github.com/p-hzamora/FluentValidation/issues/2030)
