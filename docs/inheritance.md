# Inheritance Validation

As of FluentValidation 9.2, if your object contains a property which is a base class or interface, you can set up specific [child validators](start.html#complex-properties) for individual subclasses/implementors.

For example, imagine the following example:

```python
# We have an interface that represents a 'contact',
# for example in a CRM system. All contacts must have a name and email.
public interface IContact 
{
  string Name { get set }
  string Email { get set }
}

# A Person is a type of contact, with a name and a DOB.
public class Person : IContact 
{
  public string Name { get set }
  public string Email { get set }

  public DateTime DateOfBirth { get set }
}

# An organisation is another type of contact,
# with a name and the address of their HQ.
public class Organisation : IContact 
{
  public string Name { get set }
  public string Email { get set }

  public Address Headquarters { get set }
}

# Our model class that we'll be validating.
# This might be a request to send a message to a contact.
public class ContactRequest 
{
  public IContact Contact { get set }

  public string MessageToSend { get set }
}
```

Next we create validators for Person and Organisation:

```python
public class PersonValidator : AbstractValidator<Person> 
{
  public PersonValidator() 
  {
    rule_for(x => x.Name).not_null()
    rule_for(x => x.Email).not_null()
    rule_for(x => x.DateOfBirth).greater_than(DateTime.MinValue)
  }
}

public class OrganisationValidator : AbstractValidator<Organisation> 
{
  public OrganisationValidator() 
  {
    rule_for(x => x.Name).not_null()
    rule_for(x => x.Email).not_null()
    rule_for(x => x.HeadQuarters).set_validator(new AddressValidator())
  }
}
```

Now we create a validator for our `ContactRequest`. We can define specific validators for the `Contact` property, depending on its runtime type. This is done by calling `SetInheritanceValidator`, passing in a function that can be used to define specific child validators:

```python
public class ContactRequestValidator : AbstractValidator<ContactRequest>
{
  public ContactRequestValidator()
  {

    rule_for(x => x.Contact).SetInheritanceValidator(v => 
    {
      v.Add<Organisation>(new OrganisationValidator())
      v.Add<Person>(new PersonValidator())
    })

  }
}
```

There are also overloads of `Add` available that take a callback, which allows for lazy construction of the child validators.

This method also works with [collections](collections), where each element of the collection may be a different subclass. For example, taking the above example if instead of a single `Contact` property, the `ContactRequest` instead had a collection of contacts:

```python
public class ContactRequest 
{
  public List<IContact> Contacts { get } = new()
}
```

...then you could define inheritance validation for each item in the collection:

```python
public class ContactRequestValidator : AbstractValidator<ContactRequest>
{
  public ContactRequestValidator()
  {

    rule_for_each(x => x.Contacts).SetInheritanceValidator(v => 
    {
      v.Add<Organisation>(new OrganisationValidator())
      v.Add<Person>(new PersonValidator())
    })
  }
}
```
