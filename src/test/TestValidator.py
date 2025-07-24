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

from typing import Callable, overload
import sys
from pathlib import Path
from person import Person


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())
from fluent_validation.InlineValidator import InlineValidator  # noqa: E402


class TestValidator(InlineValidator[Person]):
    @overload
    def __init__(self): ...

    @overload
    def __init__(self, *actions: Callable[["TestValidator"], None]): ...

    def __init__(self, *actions: Callable[["TestValidator"], None]):
        super().__init__(Person, *actions)
