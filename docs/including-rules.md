# Including Rules

You can include rules from other validators provided they validate the same type. This allows you to split rules across multiple classes and compose them together (in a similar way to how other languages support traits). For example, imagine you have 2 validators that validate different aspects of a `Person`:

```python
class PersonAgeValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_for(lambda x: x.DateOfBirth).must(self.BeOver18)

    def BeOver18(self, date: datetime) -> bool: ...


class PersonNameValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_for(lambda x: x.Surname).not_null().length(0, 255)
        self.rule_for(lambda x: x.Forename).not_null().length(0, 255)
```

Because both of these validators are targetting the same model type (`Person`), you can combine them using `Include`:

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self):
        self.Include(PersonAgeValidator())
        self.Include(PersonNameValidator())
```

```eval_rst
.. note::
    You can only include validators that target the same type as the root validator.
```
