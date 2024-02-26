# Overriding the Message

You can override the default error message for a validator by calling the with_message method on a validator definition:

```
rule_for(customer => customer.Surname).not_null().with_message("Please ensure that you have entered your Surname");
```

Note that custom error messages can contain placeholders for special values such as `{PropertyName}` - which will be replaced in this example with the name of the property being validated. This means the above error message could be re-written as:

```
rule_for(customer => customer.Surname).not_null().with_message("Please ensure you have entered your {PropertyName}");
```

...and the value `Surname` will be inserted.

## Placeholders

As shown in the example above, the message can contain placeholders for special values such as `{PropertyName}` - which will be replaced at runtime. Each built-in validator has its own list of placeholders.

The placeholders used in all validators are:
* `{PropertyName}` – Name of the property being validated
* `{PropertyValue}` – Value of the property being validated
These include the predicate validator (`must` validator), the email and the regex validators.

Used in comparison validators: (`equal`, `not_equal`, `greater_than`, `GreaterThanOrEqual`, etc.)
* `{ComparisonValue}` – Value that the property should be compared to
* `{ComparisonProperty}` – Name of the property being compared against (if any)

Used only in the length validator:
* `{min_length}` – Minimum length
* `{max_length}` – Maximum length
* `{total_length}` – Number of characters entered

For a complete list of error message placeholders see the [Built in Validators page](built-in-validators). Each built in validator has its own supported placeholders.

It is also possible to use your own custom arguments in the validation message. These can either be static values or references to other properties on the object being validated. This can be done by using the overload of `with_message` that takes a lambda expression, and then passing the values to `string.Format` or by using string interpolation.

```csharp
//Using constant in a custom message:
rule_for(customer => customer.Surname)
  .not_null()
  .with_message(customer => string.Format("This message references some constant values: {0} {1}", "hello", 5))
//Result would be "This message references some constant values: hello 5"

//Referencing other property values:
rule_for(customer => customer.Surname)
  .not_null()
  .with_message(customer => $"This message references some other properties: Forename: {customer.Forename} Discount: {customer.Discount}");
//Result would be: "This message references some other properties: Forename: Jeremy Discount: 100"
```

If you want to override all of FluentValidation's default error messages, check out FluentValidation's support for [Localization](localization).

# Overriding the Property Name

The default validation error messages contain the property name being validated. For example, if you were to define a validator like this:
```
rule_for(customer => customer.Surname).not_null();
```

...then the default error message would be *'Surname' must not be empty*. Although you can override the entire error message by calling `with_message`, you can also replace just the property name by calling `WithName`:

```
rule_for(customer => customer.Surname).not_null().WithName("Last name");
```

Now the error message would be *'Last name' must not be empty.*

Note that this only replaces the name of the property in the error message. When you inspect the `Errors` collection on the `ValidationResult`, this error will still be associated with a property called `Surname`.
If you want to completely rename the property, you can use the `OverridePropertyName` method instead.

There is also an overload of `WithName` that accepts a lambda expression in a similar way to `with_message` in the previous section.

Property name resolution is also pluggable. By default, the name of the property extracted from the `MemberExpression` passed to `rule_for`. If you want to change this logic, you can set the `DisplayNameResolver` property on the `ValidatorOptions` class:

```csharp
ValidatorOptions.Global.DisplayNameResolver = (type, member, expression) => 
{
  if(member != null) 
  {
     return member.Name + "Foo";
  }
  return null;
};
```

This is not a realistic example as it changes all properties to have the suffix `Foo`, but hopefully illustrates the point.
