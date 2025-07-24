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

import inspect
import re


def nameof(_, full_name=False) -> str:
    """
    Return the name of the variable passed as argument

    >>> class C:
    ...     member = 5
    >>> my_var = C()
    >>> nameof(my_var)
    'my_var'
    >>> nameof(my_var.member)
    'member'
    >>> nameof(my_var.member, full_name=True)
    'my_var.member'

    >>> nameof(4 + (my_var.member) + 11)
    Traceback (most recent call last):
      ...
    RuntimeError: Invalid nameof invocation: nameof(4 + (my_var.member) + 11)
    >>> nameof(4)
    Traceback (most recent call last):
      ...
    RuntimeError: Invalid nameof invocation: nameof(4)
    """
    s = inspect.stack()
    func_name = s[0].frame.f_code.co_name
    call = s[1].code_context[0].strip()
    # Simple search for first closing bracket or comma
    arg = re.search(rf"{func_name}\(([^,)]+)[,)]", call)
    if arg is not None:
        var_parts = arg.group(1).split(".")
    if arg is None or not all(map(str.isidentifier, var_parts)):
        raise RuntimeError(f"Invalid {func_name} invocation: {call}")

    if full_name:
        return arg.group(1)
    else:
        return var_parts[-1]
