# Custom Validators

There are several ways to create a custom, reusable validator. The recommended way is to make use of the [Predicate Validator](built-in-validators.html#predicate-validator) to write a custom validation function, but you can also use the `custom` method to take full control of the validation process.

For these examples, we'll imagine a scenario where you want to create a reusable validator that will ensure a List object contains fewer than 10 items.

## Predicate Validator
The simplest way to implement a custom validator is by using the `must` method, which internally uses the `PredicateValidator`.

Imagine we have the following class:
```python
@dataclass
class Pet: ...


class Person:
    def __init__(self, pet: Optional[list[Pet]] = None):
        self.Pets: list[Pet] = pet if pet is not None else []
```

To ensure our list property contains fewer than 10 items, we could do this:

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_for(lambda x: x.Pets).must(lambda list: len(list) < 10).with_message("The list must contain fewer than 10 items")

```

To make this logic reusable, we can wrap it an extension method that acts upon any `list[T]` type.

```python
class MyCustomValidators:
    def ListMustContainFewerThan[T, TElement](ruleBuilder: IRuleBuilder[T, list[TElement]], num: int) -> IRuleBuilderOptions[T, list[TElement]]:
        return ruleBuilder.must(lambda list: len(list) > num).with_message("The list contains too many items")

    IRuleBuilder.ListMustContainFewerThan = ListMustContainFewerThan

```

Here we create an extension method on `IRuleBuilder[T,TProperty]`, and we use a generic type constraint to ensure this method only appears in intellisense for List types. Inside the method, we call the must method in the same way as before but this time we call it on the passed-in `RuleBuilder` instance. We also pass in the number of items for comparison as a parameter. Our rule definition can now be rewritten to use this method:

```python
self.rule_for(lambda x: x.Pets).ListMustContainFewerThan(10)
```

## Custom message placeholders

We can extend the above example to include a more useful error message. At the moment, our custom validator always returns the message "The list contains too many items" if validation fails. Instead, let's change the message so it returns "'Pets' must contain fewer than 10 items." This can be done by using custom message placeholders. FluentValidation supports several message placeholders by default including `{PropertyName}` and `{PropertyValue}` ([see this list for more](https://github.com/p-hzamora/FluentValidation/blob/main/docs/built-in-validators.md#built-in-validators)), but we can also add our own.

We need to modify our extension method slightly to use a different overload of the `must` method, one that accepts a `ValidationContext<T>` instance. This context provides additional information and methods we can use when performing validation:

```python
def ListMustContainFewerThan[T, TElement](ruleBuilder: IRuleBuilder[T, list[TElement]], num: int) -> IRuleBuilderOptions[T, list[TElement]]:
    def _lambda[T](rootObject, list, context: ValidationContext[T]) -> bool:
        context.MessageFormatter.AppendArgument("MaxElements", num)
        return len(list) < num

    return ruleBuilder.must(lambda rootObject, list_, context: _lambda(rootObject, list_, context)).with_message("{PropertyName} must contain fewer than {MaxElements} items.")
```

Note that the overload of must that we're using now accepts 3 parameters: the root (parent) object, the property value itself, and the context. We use the context to add a custom message replacement value of `MaxElements` and set its value to the number passed to the method. We can now use this placeholder as `{MaxElements}` within the call to `with_message`.

The resulting message will now be `'Pets' must contain fewer than 10 items.` We could even extend this further to include the number of elements that the list contains like this:

```python
def ListMustContainFewerThan[T, TElement](ruleBuilder: IRuleBuilder[T, list[TElement]], num: int) -> IRuleBuilderOptions[T, list[TElement]]:
    def _lambda[T](rootObject, list, context: ValidationContext[T]) -> bool:
        (context.MessageFormatter
        .AppendArgument("MaxElements", num)
        .AppendArgument("TotalElements",len(list)))
        return len(list) < num

    return ruleBuilder.must(lambda rootObject, list_, context: _lambda(rootObject, list_, context)).with_message("{PropertyName} must contain fewer than {MaxElements} items. The list contains {TotalElements} element")

```

## Writing a Custom Validator

If you need more control of the validation process than is available with `must`, you can write a custom rule using the `Custom` method. This method allows you to manually create the `ValidationFailure` instance associated with the validation error. Usually, the framework does this for you, so it is more verbose than using `must`.


```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        # fmt:off
        self.rule_for(lambda x: x.Pets).custom(lambda list, context:(
                context.AddFailure("The list must contain 10 items or fewer") 
                if(len(list) > 10) 
                else None
            )
        )
        # fmt:on
```

The advantage of this approach is that it allows you to return multiple errors for the same rule (by calling the `context.AddFailure` method multiple times). In the above example, the property name in the generated error will be inferred as "Pets", although this could be overridden by calling a different overload of `AddFailure`:

```python
context.AddFailure(propertyName="SomeOtherProperty", errorMessage="The list must contain 10 items or fewer")
# Or you can instantiate the ValidationFailure directly:
context.AddFailure(ValidationFailure(propertyName="SomeOtherProperty", errorMessage="The list must contain 10 items or fewer"))
```

As before, this could be wrapped in an extension method to simplify the consuming code.

```python
  def ListMustContainFewerThan[T, TElement](ruleBuilder: IRuleBuilder[T, list[TElement]], num: int) -> IRuleBuilderOptions[T, list[TElement]]:
      #fmt:off
      return ruleBuilder.custom(lambda list,context: (
          context.AddFailure("The list contains too many items") if len(list) > num else None
          )
      )
      #fmt:on

  IRuleBuilder.ListMustContainFewerThan = ListMustContainFewerThan
```

## Reusable Property Validators

In some cases where your custom logic is very complex, you may wish to move the custom logic into a separate class. This can be done by writing a class that inherits from the abstract `PropertyValidator[T, TProperty]` class (this is how all of FluentValidation's built-in rules are defined).

```eval_rst
.. note::
  This is an advanced technique that is usually unnecessary - the `must` and `Custom` methods explained above are usually more appropriate.
```

We can recreate the above example using a custom `PropertyValidator` implementation like this:

```python
class ListCountValidator[T, TCollectionElement](PropertyValidator[T, list[TCollectionElement]]):
    _max: int

    def __init__(self, max: int):
        self._max = max

    @override
    def is_valid(self, context: ValidationContext[T], _list: TCollectionElement) -> bool:
        if _list is not None and len(_list) >= self._max:
            context.MessageFormatter.AppendArgument("MaxElements", self._max)
            return False
        return True

    @override
    def get_default_message_template(self, error_code):
        return "{PropertyName} must contain fewer than {MaxElements} items."
```
when you inherit from `PropertyValidator` you must override the `is_valid` method. This method receives two values - the `ValidationContext[T]` representing the current validation run, and the value of the property. The method should return a boolean indicating whether validation was successful. The generic type parameters on the base class represent the root instance being validated, and the type of the property that our custom validator can act upon. In this case we're constraining the custom validator to types that implement `list[TCollectionElement]` although this can be left open if desired.

Note that the error message to use is specified by overriding `GetDefaultMessageTemplate`.

To use the new custom validator you can call `set_validator` when defining a validation rule.

```python 
class PersonValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_for(lambda person: person.Pets).set_validator(ListCountValidator(10))
```

As with the first example, you can wrap this in an extension method to make the syntax nicer:
```python
class MyValidatorExtensions:
    def ListMustContainFewerThan[T, TElement](ruleBuilder: IRuleBuilder[T, list[TElement]], num: int) -> IRuleBuilderOptions[T, list[TElement]]:
        return ruleBuilder.set_validator(ListCountValidator(num))


    IRuleBuilder.ListMustContainFewerThan = ListMustContainFewerThan
```

...which can then be chained like any other validator:

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_for(lambda person: person.Pets).ListMustContainFewerThan(10)
```

As another simpler example, this is how FluentValidation's own `not_null` validator is implemented:

```python
class NotNullValidator[T, TProperty](PropertyValidator[T, TProperty]):
  @override
  def is_valid(ValidationContext<T> context, TProperty value) {
    return value is not None
  }

  @override
  def get_default_message_template(self, error_code)->str:
    return "'{PropertyName}' must not be empty."

```
