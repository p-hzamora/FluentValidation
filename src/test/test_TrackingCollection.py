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

#!/usr/bin/env python3
"""
Copyright (c) .NET Foundation and contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Translated from C# to Python for fluent_validation library.
"""

import sys
import unittest
from pathlib import Path

# Add the src directory to the path so we can import fluent_validation modules
sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.internal.TrackingCollection import TrackingCollection


class TrackingCollectionTests(unittest.TestCase):
    """Test suite for TrackingCollection translated from C# Xunit tests."""

    def test_Add_AddsItem(self):
        """Test that Add method adds an item to the collection."""
        items = TrackingCollection[str]()
        items.append("foo")

        # Verify the item was added
        self.assertEqual(len(items), 1)
        self.assertEqual(list(items)[0], "foo")

    def test_When_Item_Added_Raises_ItemAdded(self):
        """Test that adding an item raises the ItemAdded event."""
        added_item = None
        items = TrackingCollection[str]()

        def capture_added_item(item: str):
            nonlocal added_item
            added_item = item

        with items.OnItemAdded(capture_added_item):
            items.append("foo")

        self.assertEqual(added_item, "foo")

    def test_Should_not_raise_event_once_handler_detached(self):
        """Test that events are not raised after the handler is detached."""
        added_items = []
        items = TrackingCollection[str]()

        with items.OnItemAdded(added_items.append):
            items.append("foo")

        # Add another item after the handler is detached
        items.append("bar")

        # Only the first item should have been captured
        self.assertEqual(len(added_items), 1)
        self.assertEqual(added_items[0], "foo")

    # region Custom tests not derived from the original C# test suite
    def test_multiple_handlers_work_correctly(self):
        """Test that multiple event handlers can be attached and work correctly."""
        first_handler_items = []
        second_handler_items = []
        items = TrackingCollection[str]()

        with items.OnItemAdded(first_handler_items.append):
            with items.OnItemAdded(second_handler_items.append):
                items.append("test")

        # Both handlers should have captured the item
        self.assertEqual(len(first_handler_items), 1)
        self.assertEqual(len(second_handler_items), 1)
        self.assertEqual(first_handler_items[0], "test")
        self.assertEqual(second_handler_items[0], "test")

    def test_collection_behaves_like_list(self):
        """Test that the collection behaves like a standard list."""
        items = TrackingCollection[int]()

        # Add some items
        items.append(1)
        items.append(2)
        items.append(3)

        # Test length
        self.assertEqual(len(items), 3)

        # Test indexing
        self.assertEqual(items[0], 1)
        self.assertEqual(items[1], 2)
        self.assertEqual(items[2], 3)

        # Test iteration
        result = list(items)
        self.assertEqual(result, [1, 2, 3])

    def test_nested_event_handlers(self):
        """Test that nested event handlers work correctly."""
        outer_items = []
        inner_items = []
        items = TrackingCollection[str]()

        with items.OnItemAdded(outer_items.append):
            items.append("outer1")

            with items.OnItemAdded(inner_items.append):
                items.append("both")

            items.append("outer2")

        # Outer handler should capture all items
        self.assertEqual(len(outer_items), 3)
        self.assertEqual(outer_items, ["outer1", "both", "outer2"])

        # Inner handler should only capture the middle item
        self.assertEqual(len(inner_items), 1)
        self.assertEqual(inner_items[0], "both")

    def test_empty_collection_properties(self):
        """Test properties of an empty collection."""
        items = TrackingCollection[str]()

        self.assertEqual(len(items), 0)
        self.assertEqual(list(items), [])

    # endregion


if __name__ == "__main__":
    unittest.main()
