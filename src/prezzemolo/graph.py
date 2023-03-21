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
from dataclasses import dataclass
from queue import PriorityQueue
from typing import Deque, Dict, Generic, Iterator, List, Optional, Set

from prezzemolo.utility import ValueType
from prezzemolo.vertex import Vertex


@dataclass(frozen=True)
class _ShortestDistance(Generic[ValueType]):
    distance: float
    vertex: Vertex[ValueType]

    # __lt__ and __gt__ are needed for PriorityQueue
    def __lt__(self, other: object) -> bool:
        if not other:
            return False
        if not isinstance(other, _ShortestDistance):
            raise TypeError(f"Operand is not of class _ShortestDistance: {repr(other)}")
        return self.distance < other.distance

    def __gt__(self, other: object) -> bool:
        return not self.__lt__(other)


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
        if self.__non_validated_vertexes:
            raise ValueError(f"Some vertexes have neighbors that weren't added to the graph: {[v.name for v in self.__non_validated_vertexes]}")
        queue: Deque[Vertex[ValueType]] = deque()
        queue.append(start)
        visited: Set[Vertex[ValueType]] = set()
        visited.add(start)
        if vertex_2_parent is not None:
            vertex_2_parent[start] = None

        while len(queue) > 0:
            current_vertex: Vertex[ValueType] = queue.popleft()
            if current_vertex == end:
                return True
            for neighbor in current_vertex.neighbors:
                if not neighbor in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    if vertex_2_parent is not None:
                        vertex_2_parent[neighbor] = current_vertex

        return False

    def are_connected(self, start: Vertex[ValueType], end: Vertex[ValueType]) -> bool:
        # start and end are type checked inside _breadth_first_search()
        return self._breadth_first_search(start, end, vertex_2_parent=None)

    def _dijkstra(
        self, start: Vertex[ValueType], end: Optional[Vertex[ValueType]], vertex_2_parent: Optional[Dict[Vertex[ValueType], Optional[Vertex[ValueType]]]] = None
    ) -> bool:
        if self.__non_validated_vertexes:
            raise ValueError(f"Some vertexes have neighbors that weren't added to the graph: {[v.name for v in self.__non_validated_vertexes]}")
        distance: Dict[Vertex[ValueType], float] = {v: float("inf") for v in self.__vertexes}
        distance[start] = 0.0
        remaining_vertexes: PriorityQueue[_ShortestDistance[ValueType]] = PriorityQueue()
        remaining_vertexes.put(_ShortestDistance(distance=0.0, vertex=start))
        visited: Set[Vertex[ValueType]] = set()
        if vertex_2_parent is not None:
            vertex_2_parent[start] = None

        while not remaining_vertexes.empty():
            shortest_distance: _ShortestDistance[ValueType] = remaining_vertexes.get()
            current_distance: float = shortest_distance.distance
            current_vertex: Vertex[ValueType] = shortest_distance.vertex

            if current_vertex in visited:
                continue
            if current_vertex == end:
                return True

            visited.add(current_vertex)

            for neighbor in current_vertex.neighbors:
                neighbor_distance = current_distance + current_vertex.get_weight(neighbor)
                if neighbor_distance < distance[neighbor]:
                    distance[neighbor] = neighbor_distance
                    remaining_vertexes.put(_ShortestDistance(distance=neighbor_distance, vertex=neighbor))
                    if vertex_2_parent is not None:
                        vertex_2_parent[neighbor] = current_vertex

        return False

    def breadth_first_search(self, start: Vertex[ValueType], end: Vertex[ValueType], reverse: bool = True) -> Optional[Iterator[Vertex[ValueType]]]:
        # start and end are type checked inside _breadth_first_search()
        vertex_2_parent: Dict[Vertex[ValueType], Optional[Vertex[ValueType]]] = {}
        if self._breadth_first_search(start, end, vertex_2_parent):
            result = self._extract_path_from_parent_dictionary(end, vertex_2_parent)
            if not reverse:
                return reversed(result)
            return iter(result)
        return None

    def dijkstra(self, start: Vertex[ValueType], end: Vertex[ValueType], reverse: bool = True) -> Optional[Iterator[Vertex[ValueType]]]:
        # start and end are type checked inside _dijkstra()
        vertex_2_parent: Dict[Vertex[ValueType], Optional[Vertex[ValueType]]] = {}
        if self._dijkstra(start, end, vertex_2_parent):
            result = self._extract_path_from_parent_dictionary(end, vertex_2_parent)
            if not reverse:
                return reversed(result)
            return iter(result)
        return None
