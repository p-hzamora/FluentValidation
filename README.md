<p>
<img src="https://github.com/p-hzamora/FluentValidation/blob/main/logo/fluent-validation-python-logo.svg" alt="FluentValidation" width="250px" />
</p>

<!-- ![Unit Tests](https://img.shields.io/badge/Unit%20Tests-95.16%-d9c824.svg) -->
![PyPI version](https://img.shields.io/pypi/v/fluent_validation.svg)
![downloads](https://img.shields.io/pypi/dm/fluent_validation?label=downloads)
![License: Apache](https://img.shields.io/badge/license-Apache-green.svg)

# FluentValidation
A validation library for Python that uses a fluent interface
and lambda expressions for building strongly-typed validation rules.

The original library is written in .NET.

---
### Supporting the project
This module has been translated by [@p-hzamora](https://github.com/p-hzamora).

If you use FluentValidation in a commercial project, please sponsor the project financially. FluentValidation is developed and supported by [@JeremySkinner](https://github.com/JeremySkinner) for free in his spare time and financial sponsorship helps keep the project going. You can sponsor the project via either [GitHub sponsors](https://github.com/sponsors/JeremySkinner) or [OpenCollective](https://opencollective.com/FluentValidation).

---

### Table of contents
#### Getting started
- [Installation](https://github.com/p-hzamora/FluentValidation/blob/main/docs/installation.md)
- [Creating your first validator](https://github.com/p-hzamora/FluentValidation/blob/main/docs/start.md)
- [Chaining Validator](https://github.com/p-hzamora/FluentValidation/blob/main/docs/start.md#chaining-validators)
- [Throwing Exceptions](docs/start.md#Throwing-Exceptions)
- [Complex Properties](docs/start.md#complex-properties)
- [Collections](docs/collections.md) (Not available)



#### Configuring Validators
- [Overriding the Message](docs/configuring.md#overriding-the-message)
  - [Placeholders](docs/configuring.md#placeholders)
- [Overriding the Property Name](docs/configuring.md#overriding-the-property-name)
- [Conditions](docs/conditions.md)

#### Building Rules
- [Built-in Validators](docs/built-in-validators.md#built-in-validators)
  - [NotNull Validator](docs/built-in-validators.md#not_null-validator)
  - [NotEmpty Validator](docs/built-in-validators.md#not_empty-validator)
  - [NotEqual Validator](docs/built-in-validators.md#not_equal-validator)
  - [Equal Validator](docs/built-in-validators.md#equal-validator)
  - [Length Validator](docs/built-in-validators.md#length-validator)
  - [MaxLength Validator](docs/built-in-validators.md#max_length-validator)
  - [MinLength Validator](docs/built-in-validators.md#min_length-validator)
  - [Less Than Validator](docs/built-in-validators.md#less-than-validator)
  - [Less Than Or Equal Validator](docs/built-in-validators.md#less-than-or-equal-validator)
  - [Greater Than Validator](docs/built-in-validators.md#greater-than-validator)
  - [Greater Than Or Equal Validator](docs/built-in-validators.md#greater-than-or-equal-validator)
  - [Predicate Validator](docs/built-in-validators.md#predicate-validator)
  - [Regular Expression Validator](docs/built-in-validators.md#regular-expression-validator)
  - [Email Validator](docs/built-in-validators.md#email-validator) (Not available)
  - [Credit Card Validator](docs/built-in-validators.md#credit-card-validator) (Not available)
  - [Enum Validator](docs/built-in-validators.md#enum-validator) (Not available)
  - [Enum Name Validator](docs/built-in-validators.md#enum-name-validator) (Not available)
  - [Empty Validator](docs/built-in-validators.md#empty-validator)
  - [Null Validator](docs/built-in-validators.md#null-validator)
  - [ExclusiveBetween Validator](docs/built-in-validators.md#exclusivebetween-validator) (Not available)
  - [InclusiveBetween Validator](docs/built-in-validators.md#inclusivebetween-validator) (Not available)
  - [PrecisionScale Validator](docs/built-in-validators.md#precisionscale-validator) (Not available)

- [Custom Validators](docs/custom-validators.md) [Not available]

#### Other Features
- [Including Rules](docs/including-rules.md)
- [Validating specific properties](docs/specific-properties.md)
- [RuleSets](docs/rulesets.md)
- [Setting the Cascade mode](docs/cascade.md)

#### Localization
- [Localization](docs/localization.md)

---

### Get Started

FluentValidation can be installed using the `pip` package manager.

```
pip install fluent_validation
```

<!-- [Review our documentation](https://docs.fluentvalidation.net) for instructions on how to use the package. -->

---

### Example
```python
from fluent_validation import AbstractValidator

def BeAValidPostcode(postcode:str)->bool:
  # custom postcode validating logic goes here

class CustomerValidator(AbstractValidator[Customer]):
  def __init__(self)-> None:
    super().__init__()
    self.rule_for(lambda x: x.Surname).not_empty()
    self.rule_for(lambda x: x.Forename).not_empty().with_message("Please specify a first name")
    self.rule_for(lambda x: x.Discount).not_equal(0).when(lambda x: x.HasDiscount)
    self.rule_for(lambda x: x.Address).length(20, 250)
    self.rule_for(lambda x: x.Postcode).must(BeAValidPostcode).with_message("Please specify a valid postcode")



customer = Customer()
validator = CustomerValidator()

# Execute the validator
results = validator.validate(customer)

# Inspect any validation failures.
success = results.is_valid
failures = results.errors
```

### License, Copyright etc

<!-- FluentValidation has adopted the [Code of Conduct](https://github.com/FluentValidation/FluentValidation/blob/main/.github/CODE_OF_CONDUCT.md) defined by the Contributor Covenant to clarify expected behavior in our community. -->

<!-- For more information see the [.NET Foundation Code of Conduct](https://dotnetfoundation.org/code-of-conduct). -->

FluentValidation is copyright &copy 2008-2022 .NET Foundation, [Jeremy Skinner](https://jeremyskinner.co.uk) and other contributors and is licensed under the [Apache2 license](https://github.com/JeremySkinner/FluentValidation/blob/master/License.txt).

### Sponsors

The original project is sponsored by the following organisations whose support help keep this project going:

- [Microsoft](https://microsoft.com) for their financial contribution 
- [JetBrains](https://www.jetbrains.com/?from=FluentValidation) for providing licenses to their developer tools

The original project is part of the [.NET Foundation](https://dotnetfoundation.org).