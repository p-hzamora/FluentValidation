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
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.internal.PropertyChain import PropertyChain
from fluent_validation.MemberInfo import MemberInfo
from person import Person


class Parent:
    def __init__(self):
        self.Child = None


class Child:
    def __init__(self):
        self.GrandChild = None


class Grandchild:
    pass


class PropertyChainTests(unittest.TestCase):
    def setUp(self):
        self.chain = PropertyChain()

    def test_Calling_ToString_should_construct_string_representation_of_chain(self):
        # Create MemberInfo objects for the properties

        self.chain.Add(MemberInfo(lambda x: Parent.Child))
        self.chain.Add(MemberInfo(lambda x: Child.GrandChild))
        expected = "Child.GrandChild"

        self.assertEqual(self.chain.ToString(), expected)

    def test_Calling_ToString_should_construct_string_representation_of_chain_with_indexers(self):
        self.chain.Add(MemberInfo(lambda x: Parent.Child))
        self.chain.AddIndexer(0)
        self.chain.Add(MemberInfo(lambda x: Child.GrandChild))
        expected = "Child[0].GrandChild"

        self.assertEqual(self.chain.ToString(), expected)

    def test_AddIndexer_throws_when_nothing_added(self):
        with self.assertRaises(AttributeError):
            self.chain.AddIndexer(0)

    def test_Should_be_subchain(self):
        self.chain.Add("Parent")
        self.chain.Add("Child")

        child_chain = PropertyChain(self.chain)
        child_chain.Add("Grandchild")

        self.assertTrue(child_chain.ToString().startswith(self.chain.ToString()))

    def test_Should_not_be_subchain(self):
        self.chain.Add("Foo")

        other_chain = PropertyChain()
        other_chain.Add("Bar")

        self.assertFalse(other_chain.ToString().startswith(self.chain.ToString()))

    def test_Creates_from_expression(self):
        chain = PropertyChain.FromExpression(lambda x: x.Address.Id)
        self.assertEqual(chain.ToString(), "Address.Id")

    def test_Should_ignore_blanks(self):
        self.chain.Add("")
        self.chain.Add("Foo")

        self.assertEqual(self.chain.ToString(), "Foo")


if __name__ == "__main__":
    unittest.main()
