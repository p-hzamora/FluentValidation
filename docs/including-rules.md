# Including Rules

You can include rules from other validators provided they validate the same type. This allows you to split rules across multiple classes and compose them together (in a similar way to how other languages support traits). For example, imagine you have 2 validators that validate different aspects of a `Person`:

```python
public class PersonAgeValidator : AbstractValidator<Person>  
{
  public PersonAgeValidator() 
  {
    rule_for(x => x.DateOfBirth).must(BeOver18)
  }

  protected bool BeOver18(DateTime date) 
  {
    #...
  }
}

public class PersonNameValidator : AbstractValidator<Person> 
{
  public PersonNameValidator() 
  {
    rule_for(x => x.Surname).not_null().length(0, 255)
    rule_for(x => x.Forename).not_null().length(0, 255)
  }
}
```

Because both of these validators are targetting the same model type (`Person`), you can combine them using `Include`:

```python
public class PersonValidator : AbstractValidator<Person> 
{
  public PersonValidator()
   {
    Include(new PersonAgeValidator())
    Include(new PersonNameValidator())
  }
}
```

```eval_rst
.. note::
    You can only include validators that target the same type as the root validator.
```
