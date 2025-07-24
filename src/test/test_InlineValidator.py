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

from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation import ValidationResult
from fluent_validation.InlineValidator import InlineValidator


class Customer:
    def __init__(
        self,
        Id: int = 0,
        Name: str = None,
    ) -> None:
        self.Id: int = Id
        self.Name: str = Name

    def Validate(self) -> ValidationResult:
        Validator = InlineValidator[Customer](
            Customer,
            lambda v: v.rule_for(lambda x: x.Name).not_null(),
            lambda v: v.rule_for(lambda x: x.Id).not_equal(0),
        )
        return Validator.validate(self)


class InlineValidatorTester(unittest.TestCase):
    def test_Uses_inline_validator_to_build_rules(self):
        cust = Customer()
        result = cust.Validate()

        self.assertEqual(len(result.errors), 2)


if __name__ == "__main__":
    unittest.main()
