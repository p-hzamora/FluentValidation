from datetime import datetime
import sys
import unittest
from pathlib import Path
from typing import Optional, cast
from ormlambda import Table, Column, DATETIME, VARCHAR, CHAR
from parameterized import parameterized

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation import AbstractValidator


class Client(Table):
    __table_name__ = "client"

    pk: Column[CHAR] = Column(CHAR(2), is_primary_key=True)
    name: Column[VARCHAR] = Column(VARCHAR(30), is_not_null=True)
    lname1: Column[VARCHAR] = Column(VARCHAR(30), is_not_null=True)
    name2: Optional[Column[VARCHAR]] = Column(VARCHAR(30))
    last_update: Column[DATETIME] = Column(DATETIME())


class ClientValidator(AbstractValidator[Client]):
    def __init__(self):
        super().__init__(Client)

        self.rule_for(lambda x: cast(str, x.pk)).not_null()
        self.rule_for(lambda x: cast(str, x.name)).not_null()
        self.rule_for(lambda x: cast(str, x.lname1)).not_null()
        self.rule_for(lambda x: cast(str, x.name2)).not_null()
        self.rule_for(lambda x: cast(datetime, x.last_update)).not_null()


class CastTypingTest(unittest.TestCase):
    @parameterized.expand(
        [
            "pk",
            "name",
            "lname1",
            "name2",
            "last_update",
        ]
    )
    def test_get_correct_property_name_using_cast(self, attribute: str) -> None:
        validator = ClientValidator()
        client = Client()
        result = validator.validate(client, lambda opt: opt.IncludeProperties(attribute))
        self.assertEqual(result.is_valid, False)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, attribute)


if __name__ == "__main__":
    unittest.main()
