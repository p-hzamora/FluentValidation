from datetime import datetime, date, time, timezone, timedelta
import sys
import unittest
from pathlib import Path
from typing import Callable, Optional
from decimal import Decimal
from parameterized import parameterized
from pydantic import BaseModel

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation import InlineValidator


class DefaultTypesModel(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    # Numeric types
    int_field: int = 0
    float_field: float = 0.0
    complex_field: complex = 0j
    decimal_field: Decimal = Decimal("0")

    # Date/time types
    datetime_field: datetime = datetime.min
    date_field: date = date.min
    time_field: time = time.min
    timezone_field: timezone = timezone.min
    timedelta_field: timedelta = timedelta()

    # String and bytes
    str_field: str = ""
    bytes_field: bytes = b""
    bytearray_field: bytearray = bytearray()

    # None type
    none_field: Optional[str] = None


class DefaultTypesTest(unittest.TestCase):
    @parameterized.expand(
        [
            (lambda x: x.int_field, "int_field"),
            (lambda x: x.float_field, "float_field"),
            (lambda x: x.complex_field, "complex_field"),
            (lambda x: x.decimal_field, "decimal_field"),
            (lambda x: x.datetime_field, "datetime_field"),
            (lambda x: x.date_field, "date_field"),
            (lambda x: x.time_field, "time_field"),
            (lambda x: x.timezone_field, "timezone_field"),
            (lambda x: x.timedelta_field, "timedelta_field"),
            (lambda x: x.str_field, "str_field"),
            (lambda x: x.bytes_field, "bytes_field"),
            (lambda x: x.bytearray_field, "bytearray_field"),
            (lambda x: x.none_field, "none_field"),
        ]
    )
    def test_default_values_should_fail_validation[T](self, property: Callable[[DefaultTypesModel], T], property_name: str):
        """Test that all default values fail not_empty validation"""
        validator = InlineValidator(DefaultTypesModel)
        model = DefaultTypesModel()  # All fields will have default values

        validator.rule_for(property).not_empty()

        result = validator.validate(model, lambda v: v.IncludeProperties(property))

        # Should have validation errors for all fields
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].PropertyName, property_name)  # 13 fields with default values

    def test_non_default_values_should_pass_validation(self):
        """Test that non-default values pass not_empty validation"""
        validator = InlineValidator(DefaultTypesModel)

        model = DefaultTypesModel(
            int_field=1,
            float_field=1.5,
            complex_field=1 + 2j,
            decimal_field=Decimal("10"),
            datetime_field=datetime.now(),
            date_field=date.today(),
            time_field=time(12, 30),
            timezone_field=timezone.utc,
            timedelta_field=timedelta(days=1),
            str_field="hello",
            bytes_field=b"hello",
            bytearray_field=bytearray(b"hello"),
            none_field="not none",
        )

        validator.rule_for(lambda x: x.int_field).not_empty()
        validator.rule_for(lambda x: x.float_field).not_empty()
        validator.rule_for(lambda x: x.complex_field).not_empty()
        validator.rule_for(lambda x: x.decimal_field).not_empty()
        validator.rule_for(lambda x: x.datetime_field).not_empty()
        validator.rule_for(lambda x: x.date_field).not_empty()
        validator.rule_for(lambda x: x.time_field).not_empty()
        validator.rule_for(lambda x: x.timezone_field).not_empty()
        validator.rule_for(lambda x: x.timedelta_field).not_empty()
        validator.rule_for(lambda x: x.str_field).not_empty()
        validator.rule_for(lambda x: x.bytes_field).not_empty()
        validator.rule_for(lambda x: x.bytearray_field).not_empty()
        validator.rule_for(lambda x: x.none_field).not_empty()

        result = validator.validate(model)

        # Should pass validation
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)


if __name__ == "__main__":
    unittest.main()
