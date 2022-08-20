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


from datetime import datetime
from decimal import Decimal
from typing import Callable, Generic, List, Optional, TypeVar

from prezzemolo.utility import to_string


KeyType = TypeVar("KeyType", int, datetime, Decimal, float, str)  # pylint: disable=invalid-name
ValueType = TypeVar("ValueType")  # pylint: disable=invalid-name


class Node(Generic[KeyType, ValueType]):
    def __init__(self, key: KeyType, value: ValueType):
        self.__key: KeyType = key
        self.__value: ValueType = value
        self.__left: Optional[Node[KeyType, ValueType]] = None
        self.__right: Optional[Node[KeyType, ValueType]] = None

    def to_string(self, indent: int = 0, repr_format: bool = True, extra_data: Optional[List[str]] = None) -> str:
        class_specific_data: List[str] = []
        stringify: Callable[[object], str] = repr if repr_format else str  # type: ignore[assignment]
        if repr_format:
            class_specific_data.append(f"{type(self).__name__}(key={stringify(self.key)}")
        else:
            class_specific_data.append(f"{type(self).__name__}:")
            class_specific_data.append(f"key={stringify(self.key)}")
        class_specific_data.append(f"value={stringify(self.value)}")
        class_specific_data.append(f"left={stringify(self.left)}")
        class_specific_data.append(f"right={stringify(self.right)}")

        if extra_data:
            class_specific_data.extend(extra_data)

        return to_string(indent=indent, repr_format=repr_format, data=class_specific_data)

    def __str__(self) -> str:
        return self.to_string(indent=0, repr_format=False)

    def __repr__(self) -> str:
        return self.to_string(indent=0, repr_format=True)

    @property
    def key(self) -> KeyType:
        return self.__key

    @property
    def value(self) -> ValueType:
        return self.__value

    @property
    def left(self) -> "Optional[Node[KeyType, ValueType]]":
        return self.__left

    @left.setter
    def left(self, node: "Optional[Node[KeyType, ValueType]]") -> None:
        self.__left = node

    @property
    def right(self) -> "Optional[Node[KeyType, ValueType]]":
        return self.__right

    @right.setter
    def right(self, node: "Optional[Node[KeyType, ValueType]]") -> None:
        self.__right = node
