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


from typing import Callable, Dict, Generic, Iterator, List, Optional
from prezzemolo.utility import ValueType

from prezzemolo.utility import to_string


class Vertex(Generic[ValueType]):
    def __init__(self, name: str, data: Optional[ValueType] = None) -> None:
        self.__name: str = name
        self.__data: Optional[ValueType] = data
        self.__neighbors: Dict[Vertex[ValueType], Vertex[ValueType]] = {}
        self.__edge_weights: Dict[Vertex[ValueType], float] = {}

    def to_string(self, indent: int = 0, repr_format: bool = True, extra_data: Optional[List[str]] = None) -> str:
        class_specific_data: List[str] = []
        stringify: Callable[[object], str] = repr if repr_format else str  # type: ignore[assignment]
        if repr_format:
            class_specific_data.append(f"{type(self).__name__}(name={stringify(self.name)}")
        else:
            class_specific_data.append(f"{type(self).__name__}:")
            class_specific_data.append(f"name={stringify(self.name)}")
        class_specific_data.append(f"data={stringify(self.data)}")
        class_specific_data.append(f"neighbors=[{stringify(', '.join([neighbor.name for neighbor in self.neighbors]))}]")
        class_specific_data.append(f"weights={stringify({neighbor.name:weight for neighbor, weight in self.__edge_weights.items()})}")

        if extra_data:
            class_specific_data.extend(extra_data)

        return to_string(indent=indent, repr_format=repr_format, data=class_specific_data)

    def __str__(self) -> str:
        return self.to_string(indent=0, repr_format=False)

    def __repr__(self) -> str:
        return self.to_string(indent=0, repr_format=True)

    def __eq__(self, other: object) -> bool:
        if not other:
            return False
        if not isinstance(other, Vertex):
            raise TypeError(f"Operand has non-Vertex value: {repr(other)}")
        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def data(self) -> Optional[ValueType]:
        return self.__data

    @property
    def neighbors(self) -> Iterator["Vertex[ValueType]"]:
        return iter(self.__neighbors.keys())

    def add_neighbor(self, vertex: "Vertex[ValueType]", weight: float = 0.0) -> None:
        if vertex in self.__neighbors:
            raise ValueError(f"Vertex '{vertex.name}' has already been added to vertex '{self.name}'")
        self.__neighbors[vertex] = vertex
        if weight != 0.0:
            self.__edge_weights[vertex] = weight

    def add_neighbor_bidirectional(self, vertex: "Vertex[ValueType]", weight: float = 0.0) -> None:
        self.add_neighbor(vertex, weight)
        vertex.add_neighbor(self, weight)

    def get_weight(self, neighbor: "Vertex[ValueType]") -> float:
        return self.__edge_weights[neighbor] if neighbor in self.__edge_weights else 0.0
