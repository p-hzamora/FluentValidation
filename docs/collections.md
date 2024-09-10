# Collections

## Collections of Simple Types

You can use the `rule_for_each` method to apply the same rule to multiple items in a collection:

```python
from dataclasses import dataclass

@dataclass
class Person:
    AddressLines:list[str]
```

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__()
        self.rule_for_each(lambda x: x.AddressLines).not_null()
```

The above rule will run a not_null check against each item in the `AddressLines` collection.

As of version 8.5, if you want to access the index of the collection element that caused the validation failure, you can use the special `{CollectionIndex}` placeholder:

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__()
        self.rule_for_each(lambda x: x.AddressLines).not_null().with_message("Address {CollectionIndex} is required.")
```

## Collections of Complex Types

You can also combine `rule_for_each` with `set_validator` when the collection is of another complex objects. For example:

```python
from decimal import Decimal

@dataclass
class Order:
    Total:Decimal

@dataclass
class Customer:
    Orders:list[Order]
```

```python
class OrderValidator(AbstractValidator[Order]):
    def __init__(self) -> None:
        super().__init__()
        self.rule_for(lambda x: x.Total).greater_than(0)


class CustomerValidator(AbstractValidator[Customer]):
    def __init__(self) -> None:
        super().__init__()
        self.rule_for_each(lambda x: x.Orders).set_validator(OrderValidator())
```

<!-- Alternatively, as of FluentValidation 8.5, you can also define rules for child collection elements in-line using the `ChildRules` method:

```python
public class CustomerValidator : AbstractValidator<Customer> 
{
  public CustomerValidator() 
  {
    rule_for_each(x => x.Orders).ChildRules(order => 
    {
      order.rule_for(x => x.Total).greater_than(0)
    })
  }
}
```

You can optionally include or exclude certain items in the collection from being validated by using the `Where` method. Note this must come directly after the call to `rule_for_each`:

```python
rule_for_each(x => x.Orders)
  .Where(x => x.Cost != null)
  .set_validator(new OrderValidator())
```

As of version 8.2, an alternative to using `rule_for_each` is to call `ForEach` as part of a regular `rule_for`. With this approach you can combine rules that act upon the entire collection with rules which act upon individual elements within the collection. For example, imagine you have the following 2 rules:

```python
# This rule acts on the whole collection (using rule_for)
rule_for(x => x.Orders)
  .must(x => x.Count <= 10).with_message("No more than 10 orders are allowed")

# This rule acts on each individual element (using rule_for_each)
rule_for_each(x => x.Orders)
  .must(order => order.Total > 0).with_message("Orders must have a total of more than 0")
```

The above 2 rules could be re-written as:

```python
rule_for(x => x.Orders)
  .must(x => x.Count <= 10).with_message("No more than 10 orders are allowed")
  .ForEach(orderRule => 
  {
    orderRule.must(order => order.Total > 0).with_message("Orders must have a total of more than 0")
  })
```

We recommend using 2 separate rules as this is clearer and easier to read, but the option of combining them is available with the `ForEach` method. -->
