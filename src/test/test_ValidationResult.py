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

import unittest
import sys
import json
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.results.ValidationFailure import ValidationFailure
from fluent_validation.results.ValidationResult import ValidationResult


class ValidationResultTests(unittest.TestCase):
    def test_Should_be_valid_when_there_are_no_errors(self):
        result = ValidationResult()
        self.assertTrue(result.is_valid)

    def test_Should_not_be_valid_when_there_are_errors(self):
        result = ValidationResult([ValidationFailure(None, None), ValidationFailure(None, None)])
        self.assertFalse(result.is_valid)

    def test_Should_add_errors(self):
        result = ValidationResult([ValidationFailure(None, None), ValidationFailure(None, None)])
        self.assertEqual(len(result.errors), 2)

    def test_Can_serialize_result(self):
        result = ValidationResult([ValidationFailure("Property", "Error")])
        # Python JSON serialization
        serialized = json.dumps({"errors": [{"property_name": f.PropertyName, "error_message": f.ErrorMessage} for f in result.errors], "is_valid": result.is_valid})
        deserialized_data = json.loads(serialized)

        # Reconstruct ValidationResult from JSON
        errors = [ValidationFailure(e["property_name"], e["error_message"]) for e in deserialized_data["errors"]]
        deserialized = ValidationResult(errors)

        self.assertEqual(len(deserialized.errors), 1)
        self.assertEqual(deserialized.errors[0].ErrorMessage, "Error")
        self.assertEqual(deserialized.errors[0].PropertyName, "Property")

    def test_Can_serialize_failure(self):
        failure = ValidationFailure("Property", "Error")
        # Python JSON serialization for ValidationFailure
        serialized = json.dumps({"property_name": failure.PropertyName, "error_message": failure.ErrorMessage})
        deserialized_data = json.loads(serialized)
        deserialized = ValidationFailure(deserialized_data["property_name"], deserialized_data["error_message"])

        self.assertEqual(deserialized.PropertyName, "Property")
        self.assertEqual(deserialized.ErrorMessage, "Error")

    def test_ToString_return_empty_string_when_there_is_no_error(self):
        result = ValidationResult()
        actual_result = result.to_string()
        self.assertEqual(actual_result, "")

    def test_ToString_return_error_messages_with_newline_as_separator(self):
        error_message1 = "expected error message 1"
        error_message2 = "expected error message 2"

        expected_result = f"\n {error_message1}\n {error_message2}"

        result = ValidationResult(
            [
                ValidationFailure("property1", error_message1),
                ValidationFailure("property2", error_message2),
            ]
        )

        actual_result = result.to_string()
        self.assertEqual(actual_result, expected_result)

    def test_ToString_return_error_messages_with_given_separator(self):
        error_message1 = "expected error message 1"
        error_message2 = "expected error message 2"
        separator = "~"
        expected_result = f"{separator} {error_message1}{separator} {error_message2}"

        result = ValidationResult([ValidationFailure("property1", error_message1), ValidationFailure("property2", error_message2)])

        # Assuming ValidationResult has a to_string method that accepts separator
        actual_result = result.to_string(separator)
        self.assertEqual(actual_result, expected_result)


if __name__ == "__main__":
    unittest.main()
