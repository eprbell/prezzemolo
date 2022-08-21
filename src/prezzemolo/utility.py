# Copyright 2022 eprbell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Parametrized and extensible method to generate string representation from classes
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TypeVar

KeyType = TypeVar("KeyType", int, datetime, Decimal, float, str)  # pylint: disable=invalid-name
ValueType = TypeVar("ValueType")  # pylint: disable=invalid-name


def to_string(indent: int = 0, repr_format: bool = True, data: Optional[List[str]] = None) -> str:
    padding: str
    output: List[str] = []
    separator: str
    if not data:
        return ""

    if repr_format:
        padding = ""
        separator = ", "
        data[0] = f"{'  ' * indent}{data[0]}"
    else:
        padding = "  " * indent
        separator = "\n  "

    if data:
        for line in data:
            output.append(f"{padding}{line}")

    if repr_format:
        output[-1] += ")"

    # Joining by separator adds one level of indentation to internal fields (like id) in str mode, which is correct.
    return separator.join(output)
