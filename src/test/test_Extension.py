import sys
from typing import Callable
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from person import Person
from fluent_validation.internal.ExtensionInternal import ExtensionsInternal
from fluent_validation.MemberInfo import MemberInfo


class ExtensionTester(unittest.TestCase):
    def test_Should_extract_member_from_member_expression(self):
        expression: Callable[[Person], str] = lambda person: person.Surname  # noqa: E731
        member: MemberInfo = MemberInfo(expression)
        self.assertEqual(member.Name, "Surname")

    def test_Should_return_null_for_non_member_expressions(self):
        expression: Callable[[Person], str] = lambda person: "Foo"  # noqa: E731
        self.assertIsNone(MemberInfo(expression).Name)

    def test_Should_split_pascal_cased_member_name(self):
        cases: dict[str, str] = {
            "DateOfBirth": "Date Of Birth",
            "DATEOFBIRTH": "DATEOFBIRTH",
            "dateOfBirth": "date Of Birth",
            "dateofbirth": "dateofbirth",
            "Date_Of_Birth": "Date_ Of_ Birth",
            "Name2": "Name2",
            "ProductID": "Product ID",
            "MyTVRemote": "My TV Remote",
            "TVRemote": "TV Remote",
            "XCopy": "X Copy",
            "ThisXCopy": "This X Copy",
            "Address.Line1": "Address Line1",
            "Address..Line1": "Address. Line1",
            "address.Line1": "address Line1",
            "addressLine1": "address Line1",
            "address.line1": "address.line1",
            "address.line1.": "address.line1.",
        }

        for key, value in cases.items():
            name: str = ExtensionsInternal.split_pascal_case(key)
            self.assertEqual(name, value)

    def test_SplitPascalCase_should_return_null_when_input_is_null(self):
        self.assertIsNone(ExtensionsInternal.split_pascal_case(None))


if __name__ == "__main__":
    unittest.main()
