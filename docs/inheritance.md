# Inheritance Validation

As of FluentValidation 9.2, if your object contains a property which is a base class or interface, you can set up specific [child validators](start.html#complex-properties) for individual subclasses/implementors.

For example, imagine the following example:

```python
# We have an interface that represents a 'contact',
# for example in a CRM system. All contacts must have a name and email.
class IContact(BaseModel):
    Name: str
    Email: str

# A Person is a type of contact, with a name and a DOB.
class Person(IContact):
    DateOfBirth: datetime

# An organisation is another type of contact,
# with a name and the address of their HQ.
class Organisation(IContact):
    Headquarters: Address


# Our model class that we'll be validating.
# This might be a request to send a message to a contact.
class ContactRequest(BaseModel):
    Contact: IContact
    MessageToSend: str
```

Next we create validators for Person and Organisation:

```python
class PersonValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)

        self.rule_for(lambda x: x.Name).not_null()
        self.rule_for(lambda x: x.Email).not_null()
        self.rule_for(lambda x: x.DateOfBirth).greater_than(datetime.min)


class OrganisationValidator(AbstractValidator[Organisation]):
    def __init__(self):
        super().__init__(Organisation)

        self.rule_for(lambda x: x.Name).not_null()
        self.rule_for(lambda x: x.Email).not_null()
        self.rule_for(lambda x: x.Headquarters).set_validator(AddressValidator())
```

Now we create a validator for our `ContactRequest`. We can define specific validators for the `Contact` property, depending on its runtime type. This is done by calling `set_inheritance_validator`, passing in a function that can be used to define specific child validators:

```python
class ContactRequestValidator(AbstractValidator[ContactRequest]):
    def __init__(self):
        super().__init__(ContactRequest)

        # fmt: off
        self.rule_for(lambda x: x.Contact).set_inheritance_validator(lambda v: (
            v.add(OrganisationValidator()),
            v.add(PersonValidator()),
        ))
        # fmt: on
```

There are also overloads of `add` available that take a callback, which allows for lazy construction of the child validators.

This method also works with [collections](collections), where each element of the collection may be a different subclass. For example, taking the above example if instead of a single `Contact` property, the `ContactRequest` instead had a collection of contacts:

```python
class ContactRequest(BaseModel):
    Contacts:list[IContact] = Field(...,list)
```

...then you could define inheritance validation for each item in the collection:

```python
class ContactRequestValidator(AbstractValidator[ContactRequest]):
    def __init__(self):
        super().__init__(ContactRequest)
        
        # fmt: off
        self.rule_for_each(lambda x: x.Contact).set_inheritance_validator(lambda v: (
            v.add(OrganisationValidator()),
            v.add(PersonValidator()),
        ))
        # fmt: on
```
