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

from typing import Type, Optional


class AsyncValidatorInvokedSynchronouslyException(RuntimeError):
    def __init__(self, validatorType: Optional[Type] = None, wasInvokedByAspNet: bool = False, message: Optional[str] = None):
        self.validatorType = validatorType if validatorType else type(None).__class__
        self.message = message if message else self.BuildMessage(validatorType, wasInvokedByAspNet)

    @staticmethod
    def BuildMessage(validatorType: Type, wasInvokedByAspNet: bool) -> str:
        if wasInvokedByAspNet:
            return f"Validator \"{validatorType.__name__}\" can't be used with ASP.NET automatic validation as it contains asynchronous rules. ASP.NET's validation pipeline is not asynchronous and can't invoke asynchronous rules. Remove the asynchronous rules in order for this validator to run."
        return f'Validator "{validatorType.__name__}" contains asynchronous rules but was invoked synchronously. Please call ValidateAsync rather than validate.'

    def __str__(self) -> str:
        return self.message
