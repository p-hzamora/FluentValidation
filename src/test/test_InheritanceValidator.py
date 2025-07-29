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
from typing import Optional

from pydantic import BaseModel, Field


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.validators.PolymorphicValidator import PolymorphicValidator
from fluent_validation.InlineValidator import InlineValidator
# from CultureScope import CultureScope


class IFoo(BaseModel):
    """Interface for Foo implementations"""

    ...


class FooImpl1(IFoo):
    Name: Optional[str] = None


class FooImpl2(IFoo):
    Number: int = 0


class Root(BaseModel):
    Foo: Optional[IFoo] = None
    Foos: list[IFoo] = Field(default_factory=list)


class TypeUnsafePolymorphicValidator[T, TProperty](PolymorphicValidator[T, TProperty]):
    """Custom polymorphic validator for testing"""

    def __init__(self):
        self.impl1Validator = InlineValidator(FooImpl1)
        self.impl1Validator.rule_for(lambda x: x.Name).not_null()

        self.add(FooImpl1, self.impl1Validator)


class InheritanceValidatorTest(unittest.TestCase):
    def test_Validates_inheritance_hierarchy(self):
        validator = InlineValidator(Root)
        impl1Validator = InlineValidator(FooImpl1)
        impl2_validator = InlineValidator(FooImpl2)

        impl1Validator.rule_for(lambda x: x.Name).not_null()
        impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

        # fmt: off
        validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (
            v.add(impl1Validator)
                .add(impl2_validator)
        ))
        # fmt: on

        # Test with FooImpl1
        result = validator.validate(Root(Foo=FooImpl1()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

        # Test with FooImpl2
        result = validator.validate(Root(Foo=FooImpl2()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    # async def test_Validates_inheritance_async(self):
    #     """Test async validation of inheritance hierarchy"""
    #     validator = InlineValidator(Root)
    #     impl1Validator = InlineValidator(FooImpl1)
    #     impl2_validator = InlineValidator(FooImpl2)

    #     # Note: MustAsync needs to be implemented - using regular validators for now
    #     impl1Validator.rule_for(lambda x: x.Name).not_null()
    #     impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

    #     validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (v.add(impl1Validator).add(impl2_validator)))

    #     # Test with FooImpl1
    #     result = await validator.validate_async(Root(Foo=FooImpl1()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

    #     # Test with FooImpl2
    #     result = await validator.validate_async(Root(Foo=FooImpl2()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    def test_Validates_collection(self):
        """Test validation of collection with inheritance"""
        validator = InlineValidator(Root)
        impl1Validator = InlineValidator(FooImpl1)
        impl2_validator = InlineValidator(FooImpl2)

        impl1Validator.rule_for(lambda x: x.Name).not_null()
        impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

        # fmt: off
        validator.rule_for_each(lambda x: x.Foos).set_inheritance_validator(lambda v: (
            v.add(impl1Validator)
                .add(impl2_validator)))
        # fmt: on

        # Test with FooImpl1 in collection
        result = validator.validate(Root(Foos=[FooImpl1()]))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foos[0].Name")

        # Test with FooImpl2 in collection
        result = validator.validate(Root(Foos=[FooImpl2()]))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foos[0].Number")

    # async def test_Validates_collection_async(self):
    #     """Test async validation of collection with inheritance"""
    #     validator = InlineValidator(Root)
    #     impl1Validator = InlineValidator(FooImpl1)
    #     impl2_validator = InlineValidator(FooImpl2)

    #     # Note: MustAsync needs to be implemented - using regular validators for now
    #     impl1Validator.rule_for(lambda x: x.Name).not_null()
    #     impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

    #     # Note: RuleForEach needs to be implemented - testing collection validation manually for now
    #     validator.rule_for(lambda x: x.Foos).set_inheritance_validator(lambda v: (v.add(impl1Validator).add(impl2_validator)))

    #     # Test with FooImpl1 in collection
    #     result = await validator.validate_async(Root(Foos=[FooImpl1()]))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foos.Name")

    #     # Test with FooImpl2 in collection
    #     result = await validator.validate_async(Root(Foos=[FooImpl2()]))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foos.Number")

    def test_Validates_with_callback(self):
        """Test validation with callback"""
        validator = InlineValidator(Root)
        impl1Validator = InlineValidator(FooImpl1)
        impl2_validator = InlineValidator(FooImpl2)

        impl1Validator.rule_for(lambda x: x.Name).not_null()
        impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

        # fmt:off
        validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (
            v.add(lambda x: impl1Validator)
                .add(lambda x: impl2_validator)
        ))
        # fmt:on

        # Test with FooImpl1
        result = validator.validate(Root(Foo=FooImpl1()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

        # Test with FooImpl2
        result = validator.validate(Root(Foo=FooImpl2()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    # async def test_Validates_with_callback_async(self):
    #     """Test async validation with callback"""
    #     validator = InlineValidator(Root)
    #     impl1Validator = InlineValidator(FooImpl1)
    #     impl2_validator = InlineValidator(FooImpl2)

    #     # Note: MustAsync needs to be implemented - using regular validators for now
    #     impl1Validator.rule_for(lambda x: x.Name).not_null()
    #     impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

    #     validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (v.add(lambda x: impl1Validator).add(lambda x: impl2_validator)))

    #     # Test with FooImpl1
    #     result = await validator.validate_async(Root(Foo=FooImpl1()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

    #     # Test with FooImpl2
    #     result = await validator.validate_async(Root(Foo=FooImpl2()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    def test_Validates_with_callback_accepting_derived(self):
        """Test validation with callback accepting derived types"""
        validator = InlineValidator(Root)
        impl1Validator = InlineValidator(FooImpl1)
        impl2_validator = InlineValidator(FooImpl2)

        impl1Validator.rule_for(lambda x: x.Name).not_null()
        impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

        # fmt: off
        validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (
            v.add(lambda x, impl1: (
                self.assertIsNotNone(impl1), impl1Validator)[1])
                
                    .add(lambda x, impl2: (self.assertIsNotNone(impl2), impl2_validator)[1]))
        )
        # fmt: on

        # Test with FooImpl1
        result = validator.validate(Root(Foo=FooImpl1()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

        # Test with FooImpl2
        result = validator.validate(Root(Foo=FooImpl2()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    # async def test_Validates_with_callback_accepting_derived_async(self):
    #     """Test async validation with callback accepting derived types"""
    #     validator = InlineValidator(Root)
    #     impl1Validator = InlineValidator(FooImpl1)
    #     impl2_validator = InlineValidator(FooImpl2)

    #     # Note: MustAsync needs to be implemented - using regular validators for now
    #     impl1Validator.rule_for(lambda x: x.Name).not_null()
    #     impl2_validator.rule_for(lambda x: x.Number).greater_than(0)

    #     # Note: Generic type constraints need to be implemented - using basic Add for now
    #     validator.rule_for(lambda x: x.Foo).set_inheritance_validator(
    #         lambda v: (v.add(lambda x, impl1: (self.assertIsNotNone(impl1), impl1Validator)[1]).add(lambda x, impl2: (self.assertIsNotNone(impl2), impl2_validator)[1]))
    #     )

    #     # Test with FooImpl1
    #     result = await validator.validate_async(Root(Foo=FooImpl1()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

    #     # Test with FooImpl2
    #     result = await validator.validate_async(Root(Foo=FooImpl2()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    def test_Validates_ruleset(self):
        """Test validation with rulesets"""
        validator = InlineValidator(Root)
        impl1Validator = InlineValidator(FooImpl1)
        impl2_validator = InlineValidator(FooImpl2)

        # fmt: off
        impl1Validator.rule_for(lambda x: x.Name).equal("Foo")
        impl1Validator.rule_set("RuleSet1", lambda: (
            impl1Validator.rule_for(lambda x: x.Name).not_null()
        ))

        impl2_validator.rule_for(lambda x: x.Number).equal(42)
        impl2_validator.rule_set("RuleSet2", lambda: (
            impl2_validator.rule_for(lambda x: x.Number).greater_than(0)
        ))

        validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (
            v.add(impl1Validator, "RuleSet1")   
                .add(impl2_validator, "RuleSet2")
        ))
        # fmt: on

        # Test with FooImpl1
        result = validator.validate(Root(Foo=FooImpl1()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

        # Test with FooImpl2
        result = validator.validate(Root(Foo=FooImpl2()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    # async def test_Validates_ruleset_async(self):
    #     """Test async validation with rulesets"""
    #     validator = InlineValidator(Root)
    #     impl1Validator = InlineValidator(FooImpl1)
    #     impl2_validator = InlineValidator(FooImpl2)

    #     impl1Validator.rule_for(lambda x: x.Name).equal("Foo")
    #     impl1Validator.rule_set(
    #         "RuleSet1",
    #         lambda: (
    #             # Note: MustAsync needs to be implemented - using regular validators for now
    #             impl1Validator.rule_for(lambda x: x.Name).not_null(),
    #         ),
    #     )

    #     impl2_validator.rule_for(lambda x: x.Number).equal(42)
    #     impl2_validator.rule_set(
    #         "RuleSet2",
    #         lambda: (
    #             # Note: MustAsync needs to be implemented - using regular validators for now
    #             impl2_validator.rule_for(lambda x: x.Number).greater_than(0),
    #         ),
    #     )

    #     validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (v.add(impl1Validator, "RuleSet1").add(impl2_validator, "RuleSet2")))

    #     # Test with FooImpl1
    #     result = await validator.validate_async(Root(Foo=FooImpl1()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

    #     # Test with FooImpl2
    #     result = await validator.validate_async(Root(Foo=FooImpl2()))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo.Number")

    def test_Can_use_custom_subclass_with_nongeneric_overload(self):
        """Test using custom subclass with non-generic overload"""
        validator = InlineValidator(Root)
        validator.rule_for(lambda x: x.Foo).set_validator(TypeUnsafePolymorphicValidator())
        result = validator.validate(Root(Foo=FooImpl1()))
        self.assertEqual(result.errors[0].PropertyName, "Foo.Name")

    def test_Rulesets_cascade_properly_with_polymorphic_validators(self):
        """Test that rulesets cascade properly with polymorphic validators"""
        foo_validator = InlineValidator(FooImpl1)
        foo_validator.rule_set("test", lambda: (foo_validator.rule_for(lambda x: x.Name).not_null(),))

        validator = InlineValidator(Root)
        # fmt:off
        validator.rule_set("test",lambda: (
            validator.rule_for(lambda x: x.Foo).set_inheritance_validator(lambda v: (
                v.add(foo_validator)
            ))
        ))
        # fmt:on

        model = Root(Foo=FooImpl1())

        # fmt:off
        result = validator.validate(model,lambda options:(
            options.IncludeRuleSets("test").IncludeRulesNotInRuleSet()
        ))
        # fmt:on

        # This test may need adjustment based on how rule sets are implemented
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
