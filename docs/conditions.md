# Conditions

The `When` and `Unless` methods can be used to specify conditions that control when the rule should execute. For example, this rule on the `CustomerDiscount` property will only execute when `IsPreferredCustomer` is `true`:

```csharp
rule_for(customer => customer.CustomerDiscount).greater_than(0).When(customer => customer.IsPreferredCustomer);
```

The `Unless` method is simply the opposite of `When`.

If you need to specify the same condition for multiple rules then you can call the top-level `When` method instead of chaining the `When` call at the end of the rule:

```csharp
When(customer => customer.IsPreferred, () => {
   rule_for(customer => customer.CustomerDiscount).greater_than(0);
   rule_for(customer => customer.CreditCardNumber).not_null();
});
```

This time, the condition will be applied to both rules. You can also chain a call to `Otherwise` which will invoke rules that don't match the condition:

```csharp
When(customer => customer.IsPreferred, () => {
   rule_for(customer => customer.CustomerDiscount).greater_than(0);
   rule_for(customer => customer.CreditCardNumber).not_null();
}).Otherwise(() => {
  rule_for(customer => customer.CustomerDiscount).equal(0);
});
```

By default FluentValidation will apply the condition to all preceding validators in the same call to `rule_for`. If you only want the condition to apply to the validator that immediately precedes the condition, you must explicitly specify this:

```csharp
rule_for(customer => customer.CustomerDiscount)
    .greater_than(0).When(customer => customer.IsPreferredCustomer, ApplyConditionTo.CurrentValidator)
    .EqualTo(0).When(customer => ! customer.IsPreferredCustomer, ApplyConditionTo.CurrentValidator);
```

If the second parameter is not specified, then it defaults to `ApplyConditionTo.AllValidators`, meaning that the condition will apply to all preceding validators in the same chain.

If you need this behaviour, be aware that you must specify `ApplyConditionTo.CurrentValidator` as part of *every* condition. In the following example the first call to `When` applies to only the call to `matches`, but not the call to `not_empty`. The second call to `When` applies only to the call to `Empty`.

```csharp
rule_for(customer => customer.Photo)
    .not_empty()
    .matches("https://wwww.photos.io/\d+\.png")
    .When(customer => customer.IsPreferredCustomer, ApplyConditionTo.CurrentValidator)
    .Empty()
    .When(customer => ! customer.IsPreferredCustomer, ApplyConditionTo.CurrentValidator);
```