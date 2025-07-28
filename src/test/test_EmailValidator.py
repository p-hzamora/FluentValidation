# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion

import sys
import unittest
from pathlib import Path
from parameterized import parameterized


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from fluent_validation.InlineValidator import InlineValidator
from fluent_validation.validators.EmailValidator import EmailValidationMode
from CultureScope import CultureScope
from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402


class EmailValidatorTests(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()

    @parameterized.expand(
        [
            [""],
            ["testperso"],
            ["first.last@test..co.uk"],
            ["thisisaverylongstringcodeplex.com"],
        ]
    )
    def test_Invalid_email_addressex_regex(self, email: str):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Email).email_address(EmailValidationMode.Net4xRegex))
        result = validator.validate(Person(Email=email))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Email' is not a valid email address.")

    @parameterized.expand(
        [
            [None],
            ["testperson@gmail.com"],
            ["TestPerson@gmail.com"],
            ["testperson+label@gmail.com"],
            ['"Abc\\@def"@example.com'],
            ['"Fred Bloggs"@example.com'],
            ['"Joe\\Blow"@example.com'],
            ['"Abc@def"@example.com'],
            ["customer/department=shipping@example.com"],
            ["$A12345@example.com"],
            ["!def!xyz%abc@example.com"],
            ["__somename@example.com"],
            ["first.last@test.co.uk"],
        ]
    )
    def test_Valid_email_addresses_regex(self, email: str):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Email).email_address(EmailValidationMode.Net4xRegex))
        result = validator.validate(Person(Email=email))
        self.assertTrue(result.is_valid, f"The email address {email} should be valid")

    @parameterized.expand(
        [
            [None],
            ["1234@someDomain.com"],
            ["firstName.lastName@someDomain.com"],
            ["\u00a0@someDomain.com"],
            ["!#$%&'*+-/=?^_`|~@someDomain.com"],
            ['"firstName.lastName"@someDomain.com'],
            ["someName@someDomain.com"],
            ["someName@some~domain.com"],
            ["someName@some_domain.com"],
            ["someName@1234.com"],
            ["someName@someDomain\uffef.com"],
        ]
    )
    def test_Valid_email_addresses_aspnetcore_compatible(self, email: str):
        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Email).email_address(EmailValidationMode.AspNetCoreCompatible)
        self.assertTrue(validator.validate(Person(Email=email)).is_valid)

    @parameterized.expand(
        [
            [str(0)],
            [""],
            [" \r \t \n"],
            ["@someDomain.com"],
            ["@someDomain@abc.com"],
            ["someName"],
            ["someName@"],
            ["someName@a@b.com"],
        ]
    )
    def test_Fails_email_validation_aspnetcore_compatible(self, email: str):
        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Email).email_address(EmailValidationMode.AspNetCoreCompatible)
        self.assertFalse(validator.validate(Person(Email=email)).is_valid)


if __name__ == "__main__":
    unittest.main()
