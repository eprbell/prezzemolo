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

import logging
import sys
import unittest
from typing import Dict, Iterator, List, Optional, Tuple

from prezzemolo.graph import Graph
from prezzemolo.utility import ValueType
from prezzemolo.vertex import Vertex


# pylint: disable=invalid-name
class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_simple_unweighted_graph(self) -> None:
        graph: Graph[int] = TestGraph._generate_graph(
            [
                (1, 2, 0),
                (1, 3, 0),
                (2, 4, 0),
                (3, 4, 0),
                (4, 5, 0),
                (5, 2, 0),
                (5, 6, 0),
            ]
        )
        graph.add_vertex(Vertex[int](name="7", data=7))
        vertexes: Dict[int, Vertex[int]] = {int(v.name):v for v in graph.vertexes}

        self.assertFalse(graph.are_connected(vertexes[2], vertexes[7]))
        self.assertFalse(graph.are_connected(vertexes[2], vertexes[1]))
        self.assertFalse(graph.are_connected(vertexes[5], vertexes[1]))

        self.assertTrue(graph.are_connected(vertexes[2], vertexes[2]))
        self.assertTrue(graph.are_connected(vertexes[2], vertexes[6]))
        self.assertTrue(graph.are_connected(vertexes[1], vertexes[5]))

        path = graph.breadth_first_search(vertexes[2], vertexes[2])
        assert path
        self.assertEqual(list(path), [vertexes[2]])

        path = graph.breadth_first_search(vertexes[2], vertexes[6])
        assert path
        self.assertEqual(list(path), [vertexes[6], vertexes[5], vertexes[4], vertexes[2]])

        path = graph.breadth_first_search(vertexes[1], vertexes[5], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[1], vertexes[2], vertexes[4], vertexes[5]])

    def test_complex_unweighted_graph(self) -> None:
        graph: Graph[int] = TestGraph._generate_graph(
            [
                (1, 2, 0),
                (1, 3, 0),
                (1, 4, 0),
                (2, 3, 0),
                (2, 5, 0),
                (3, 5, 0),
                (3, 6, 0),
                (4, 3, 0),
                (4, 8, 0),
                (5, 7, 0),
                (6, 5, 0),
                (7, 8, 0),
                (8, 6, 0),
                (8, 9, 0),
                (9, 11, 0),
                (10, 8, 0),
                (11, 10, 0),
            ]
        )
        vertexes: Dict[int, Vertex[int]] = {int(v.name):v for v in graph.vertexes}

        self.assertFalse(graph.are_connected(vertexes[11], vertexes[1]))
        self.assertTrue(graph.are_connected(vertexes[1], vertexes[8]))

        path = graph.breadth_first_search(vertexes[1], vertexes[8], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[1], vertexes[4], vertexes[8]])

        path = graph.breadth_first_search(vertexes[4], vertexes[7])
        assert path
        self.assertEqual(list(path), [vertexes[7], vertexes[5], vertexes[3], vertexes[4]])

        path = graph.breadth_first_search(vertexes[11], vertexes[1])
        self.assertIsNone(path)

    def test_graph_without_all_nodes(self) -> None:
        v1 = Vertex[int](name="v1", data=1)
        v2 = Vertex[int](name="v2", data=2)
        v3 = Vertex[int](name="v3", data=3)

        v1.add_neighbor(v2)
        v2.add_neighbor(v3)
        v3.add_neighbor(v1)

        graph = Graph[int]([v1, v2])
        with self.assertRaisesRegex(ValueError, "Some vertexes have neighbors that weren't added to the graph"):
            graph.are_connected(v1, v3)

        graph = Graph[int]([v1, v2])
        with self.assertRaisesRegex(ValueError, "Some vertexes have neighbors that weren't added to the graph"):
            graph.breadth_first_search(v1, v3)

        graph = Graph[int]([v1, v2])
        with self.assertRaisesRegex(ValueError, "Some vertexes have neighbors that weren't added to the graph"):
            graph.dijkstra(v1, v3)

        graph = Graph[int]()
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        with self.assertRaisesRegex(ValueError, "Some vertexes have neighbors that weren't added to the graph"):
            graph.are_connected(v1, v3)

    def test_simple_weighted_graph(self) -> None:
        graph: Graph[int] = TestGraph._generate_graph(
            [
                (0, 1, 5),
                (0, 2, 2),
                (1, 3, 4),
                (1, 4, 1),
                (2, 1, 1),
                (2, 3, 7),
                (3, 4, 3),
            ]
        )
        vertexes: List[Vertex[int]] = list(graph.vertexes)
        path = graph.dijkstra(vertexes[0], vertexes[4], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[2], vertexes[1], vertexes[4]])

    def test_graph_with_one_vertex(self) -> None:
        v1 = Vertex[int](name="1")

        graph = Graph[int]([v1])
        self.assertTrue(graph.are_connected(v1, v1))

        graph = Graph[int]([v1])
        path = graph.breadth_first_search(v1, v1)
        assert path
        self.assertEqual(list(path), [v1])

        graph = Graph[int]([v1])
        path = graph.dijkstra(v1, v1)
        assert path
        self.assertEqual(list(path), [v1])

    # 0->1, 1->2 weighs less than 0->2
    def test_weighted_triangle_graph_1(self) -> None:
        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 2), (0, 2, 4)])
        vertexes = list(graph.vertexes)
        path = graph.breadth_first_search(vertexes[0], vertexes[2], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[2]])

        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 2), (0, 2, 4)])
        vertexes = list(graph.vertexes)
        path = graph.dijkstra(vertexes[0], vertexes[2], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[1], vertexes[2]])

    # 0->1, 1->2 weighs more than 0->2
    def test_weighted_triangle_graph_2(self) -> None:
        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 2), (0, 2, 2)])
        vertexes = list(graph.vertexes)
        path = graph.breadth_first_search(vertexes[0], vertexes[2], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[2]])

        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 2), (0, 2, 2)])
        vertexes = list(graph.vertexes)
        path = graph.dijkstra(vertexes[0], vertexes[2], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[2]])

    # 0->1, 1->2 weighs same as 0->2
    def test_weighted_triangle_graph_3(self) -> None:
        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 2), (0, 2, 3)])
        vertexes = list(graph.vertexes)
        path = graph.breadth_first_search(vertexes[0], vertexes[2], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[2]])

        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 2), (0, 2, 3)])
        vertexes = list(graph.vertexes)
        path = graph.dijkstra(vertexes[0], vertexes[2], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[2]])

    def test_weighted_cycle_graph(self) -> None:
        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1), (1, 5, 1)])
        vertexes = list(graph.vertexes)
        path = graph.breadth_first_search(vertexes[1], vertexes[1], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[1]])
        path = graph.breadth_first_search(vertexes[0], vertexes[4], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[1], vertexes[2], vertexes[3], vertexes[4]])
        path = graph.breadth_first_search(vertexes[0], vertexes[5], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[1], vertexes[5]])

        graph = TestGraph._generate_graph([(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1), (1, 5, 1)])
        vertexes = list(graph.vertexes)
        path = graph.dijkstra(vertexes[1], vertexes[1], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[1]])
        path = graph.dijkstra(vertexes[0], vertexes[4], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[1], vertexes[2], vertexes[3], vertexes[4]])
        path = graph.dijkstra(vertexes[0], vertexes[5], reverse=False)
        assert path
        self.assertEqual(list(path), [vertexes[0], vertexes[1], vertexes[5]])

    def test_disconnected_graph_1(self) -> None:
        v1 = Vertex[int](name="v1", data=1)
        v2 = Vertex[int](name="v2", data=2)
        v3 = Vertex[int](name="v3", data=3)

        v1.add_neighbor(v2)

        graph = Graph[int]([v1, v2, v3])
        self.assertFalse(graph.are_connected(v1, v3))

        graph = Graph[int]([v1, v2, v3])
        path = graph.breadth_first_search(v1, v3)
        self.assertIsNone(path)

        graph = Graph[int]([v1, v2, v3])
        path = graph.dijkstra(v1, v3)
        self.assertIsNone(path)

    def test_disconnected_graph_2(self) -> None:
        graph: Graph[int] = TestGraph._generate_graph([(0, 1, 1), (1, 2, 1), (2, 0, 1), (3, 4, 2), (4, 5, 2), (5, 3, 2)])
        vertexes: List[Vertex[int]] = list(graph.vertexes)

        self.assertFalse(graph.are_connected(vertexes[0], vertexes[3]))

        path = graph.breadth_first_search(vertexes[0], vertexes[3])
        self.assertIsNone(path)

        path = graph.dijkstra(vertexes[0], vertexes[3])
        self.assertIsNone(path)

    def test_dijkstra_search_two_zones(self) -> None:
        graph: Graph[int] = TestGraph._generate_graph(
            [(0, 1, 1), (0, 2, 2), (0, 3, 3), (1, 4, 1), (2, 4, 1), (3, 4, 1), (4, 5, 1), (4, 6, 2), (4, 7, 3), (5, 8, 1), (6, 8, 1), (7, 8, 1)]
        )

        vertexes: List[Vertex[int]] = list(graph.vertexes)
        path = graph.dijkstra(vertexes[0], vertexes[8])

        assert path
        self.assertEqual(list(path), [vertexes[8], vertexes[5], vertexes[4], vertexes[1], vertexes[0]])

    # This is the graph from "Cracking the Coding Interview by Gayle Laakmann" (XI, Advanced Topics)
    def test_cracking_the_coding_interview_graph(self) -> None:
        graph: Graph[str] = TestGraph._generate_graph(
            [
                ("a", "b", 5),
                ("a", "c", 3),
                ("a", "e", 2),
                ("b", "d", 2),
                ("c", "b", 1),
                ("c", "d", 1),
                ("d", "a", 1),
                ("d", "g", 2),
                ("d", "h", 1),
                ("e", "a", 1),
                ("e", "h", 4),
                ("e", "i", 7),
                ("f", "b", 3),
                ("f", "g", 1),
                ("g", "c", 3),
                ("g", "i", 2),
                ("h", "c", 2),
                ("h", "f", 2),
                ("h", "g", 2),
            ]
        )
        vertexes: Dict[str, Vertex[str]] = {v.name:v for v in graph.vertexes}

        self.assertTrue(graph.are_connected(vertexes["a"], vertexes["i"]))
        path = graph.dijkstra(vertexes["a"], vertexes["i"], reverse=False)
        assert path
        path_as_list = list(path)
        self.assertEqual(path_as_list, [vertexes["a"], vertexes["c"], vertexes["d"], vertexes["g"], vertexes["i"]])
        self.assertEqual(TestGraph._get_path_total_weight(iter(path_as_list)), 8)

        self.assertTrue(graph.are_connected(vertexes["g"], vertexes["f"]))
        path = graph.dijkstra(vertexes["g"], vertexes["f"], reverse=False)
        assert path
        path_as_list = list(path)
        self.assertEqual(list(path_as_list), [vertexes["g"], vertexes["c"], vertexes["d"], vertexes["h"], vertexes["f"]])

        self.assertFalse(graph.are_connected(vertexes["i"], vertexes["b"]))
        path = graph.dijkstra(vertexes["i"], vertexes["b"], reverse=False)
        self.assertIsNone(path)

    @classmethod
    def _get_path_total_weight(cls, path: Iterator["Vertex[ValueType]"]) -> float:
        result: float = 0.0
        previous_vertex: Optional[Vertex[ValueType]] = None
        for current_vertex in path:
            if not previous_vertex:
                previous_vertex = current_vertex
                continue
            result += previous_vertex.get_weight(current_vertex)
            previous_vertex = current_vertex

        return result

    @classmethod
    def _generate_graph(cls, edges: List[Tuple[ValueType, ValueType, int]]) -> Graph[ValueType]:
        vertexes: Dict[ValueType, Vertex[ValueType]] = {}
        current_vertex: Vertex[ValueType]

        for edge in edges:
            current_vertex = vertexes.setdefault(edge[0], Vertex[ValueType](name=str(edge[0]), data=edge[0]))
            neighbor = vertexes.setdefault(edge[1], Vertex[ValueType](name=str(edge[1]), data=edge[1]))
            current_vertex.add_neighbor(neighbor, edge[2])

        return Graph(sorted(vertexes.values()))


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("abc").setLevel(logging.DEBUG)
    unittest.main()
