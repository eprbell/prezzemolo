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


from collections import deque
from typing import Deque, Dict, Generic, Iterator, List, Optional, Set

from prezzemolo.utility import ValueType
from prezzemolo.vertex import Vertex


class Graph(Generic[ValueType]):
    def __init__(self, vertexes: Optional[List["Vertex[ValueType]"]] = None) -> None:
        self.__vertexes: Dict[Vertex[ValueType], Vertex[ValueType]] = {vertex: vertex for vertex in vertexes} if vertexes else {}
        self.__non_validated_vertexes: Set[Vertex[ValueType]] = set(vertexes) if vertexes else set()
        for vertex in self.vertexes:
            self._validate_vertex(vertex)

    def _validate_vertex(self, vertex: Vertex[ValueType]) -> bool:
        if vertex not in self.__non_validated_vertexes:
            return True
        for neighbor in vertex.neighbors:
            if neighbor not in self.__vertexes:
                return False
        self.__non_validated_vertexes.remove(vertex)
        return True

    @property
    def vertexes(self) -> Iterator[Vertex[ValueType]]:
        return iter(self.__vertexes.keys())

    def add_vertex(self, vertex: Vertex[ValueType]) -> None:
        self.__vertexes[vertex] = vertex
        self.__non_validated_vertexes.add(vertex)
        self._validate_vertex(vertex)

    def _extract_path_from_parent_dictionary(
        self, last: Vertex[ValueType], vertex_2_parent: Dict[Vertex[ValueType], Optional[Vertex[ValueType]]]
    ) -> List[Vertex[ValueType]]:
        result: List[Vertex[ValueType]] = []
        current_vertex: Optional[Vertex[ValueType]] = last
        while current_vertex:
            result.append(current_vertex)
            current_vertex = vertex_2_parent[current_vertex]
        return result

    def _breadth_first_search(
        self,
        start: Vertex[ValueType],
        end: Optional[Vertex[ValueType]],
        vertex_2_parent: Optional[Dict[Vertex[ValueType], Optional[Vertex[ValueType]]]] = None,
    ) -> bool:
        marked_set: Set[Vertex[ValueType]] = set()
        queue: Deque[Vertex[ValueType]] = deque()
        queue.append(start)
        marked_set.add(start)
        if vertex_2_parent is not None:
            vertex_2_parent[start] = None

        while len(queue) > 0:
            vertex: Vertex[ValueType] = queue.popleft()
            if vertex in self.__non_validated_vertexes and not self._validate_vertex(vertex):
                raise ValueError(f"Vertex '{vertex.name}' has a neighbor that wasn't added to the graph")
            for neighbor in vertex.neighbors:
                if not neighbor in marked_set:
                    queue.append(neighbor)
                    marked_set.add(neighbor)
                    if vertex_2_parent is not None:
                        vertex_2_parent[neighbor] = vertex
                if neighbor == end:
                    return True

        return False

    def breadth_first_search(self, start: Vertex[ValueType], end: Vertex[ValueType]) -> bool:
        # start and end are type checked inside _breadth_first_search()
        return self._breadth_first_search(start, end, vertex_2_parent=None)

    def find_shortest_path(self, start: Vertex[ValueType], end: Vertex[ValueType], reverse: bool = True) -> Optional[Iterator[Vertex[ValueType]]]:
        # start and end are type checked inside _breadth_first_search()
        vertex_2_parent: Dict[Vertex[ValueType], Optional[Vertex[ValueType]]] = {}
        if self._breadth_first_search(start, end, vertex_2_parent):
            result = self._extract_path_from_parent_dictionary(end, vertex_2_parent)
            if not reverse:
                return reversed(result)
            return iter(result)
        return None
