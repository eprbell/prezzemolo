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

from prezzemolo.graph import Graph
from prezzemolo.vertex import Vertex


# pylint: disable=invalid-name
class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_simple_graph(self) -> None:
        v1 = Vertex[int](name="v1", data=1)
        v2 = Vertex[int](name="v2", data=2)
        v3 = Vertex[int](name="v3", data=3)
        v4 = Vertex[int](name="v4", data=4)
        v5 = Vertex[int](name="v5", data=5)
        v6 = Vertex[int](name="v6", data=6)
        v7 = Vertex[int](name="v7", data=7)

        v1.add_neighbor(v2)
        v1.add_neighbor(v3)

        v2.add_neighbor(v4)

        v3.add_neighbor(v4)

        v4.add_neighbor(v5)

        v5.add_neighbor(v2)
        v5.add_neighbor(v6)

        g1 = Graph[int]([v1, v2, v3, v4, v5, v6, v7])

        self.assertFalse(g1.breadth_first_search(v2, v7))
        self.assertFalse(g1.breadth_first_search(v2, v1))

        self.assertTrue(g1.breadth_first_search(v2, v2))
        self.assertTrue(g1.breadth_first_search(v2, v6))
        self.assertTrue(g1.breadth_first_search(v1, v5))

        path = g1.find_shortest_path(v2, v2)
        assert path
        self.assertEqual(list(path), [v2])

        path = g1.find_shortest_path(v2, v6)
        assert path
        self.assertEqual(list(path), [v6, v5, v4, v2])

        path = g1.find_shortest_path(v1, v5, reverse=False)
        assert path
        self.assertEqual(list(path), [v1, v2, v4, v5])

    def test_complex_graph(self) -> None:
        v1 = Vertex[int](name="v1", data=1)
        v2 = Vertex[int](name="v2", data=2)
        v3 = Vertex[int](name="v3", data=3)
        v4 = Vertex[int](name="v4", data=4)
        v5 = Vertex[int](name="v5", data=5)
        v6 = Vertex[int](name="v6", data=6)
        v7 = Vertex[int](name="v7", data=7)
        v8 = Vertex[int](name="v8", data=8)
        v9 = Vertex[int](name="v9", data=9)
        v10 = Vertex[int](name="v10", data=10)
        v11 = Vertex[int](name="v11", data=11)

        v1.add_neighbor(v2)
        v1.add_neighbor(v3)
        v1.add_neighbor(v4)

        v2.add_neighbor(v3)
        v2.add_neighbor(v5)

        v3.add_neighbor(v5)
        v3.add_neighbor(v6)

        v4.add_neighbor(v3)
        v4.add_neighbor(v8)

        v5.add_neighbor(v7)

        v6.add_neighbor(v5)

        v7.add_neighbor(v8)

        v8.add_neighbor(v6)
        v8.add_neighbor(v9)

        v9.add_neighbor(v11)

        v10.add_neighbor(v8)

        v11.add_neighbor(v10)

        g1 = Graph[int]([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11])

        self.assertFalse(g1.breadth_first_search(v11, v1))

        self.assertTrue(g1.breadth_first_search(v1, v8))

        path = g1.find_shortest_path(v1, v8, reverse=False)
        assert path
        self.assertEqual(list(path), [v1, v4, v8])

        path = g1.find_shortest_path(v4, v7)
        assert path
        self.assertEqual(list(path), [v7, v5, v3, v4])

        path = g1.find_shortest_path(v11, v1)
        self.assertIsNone(path)

    def test_graph_without_all_nodes(self) -> None:
        v1 = Vertex[int](name="v1", data=1)
        v2 = Vertex[int](name="v2", data=2)
        v3 = Vertex[int](name="v3", data=3)

        v1.add_neighbor(v2)
        v2.add_neighbor(v3)
        v3.add_neighbor(v1)

        g1 = Graph[int]([v1, v2])
        with self.assertRaisesRegex(ValueError, "Vertex .* has a neighbor that wasn't added to the graph"):
            g1.breadth_first_search(v1, v3)

        g1 = Graph[int]()
        g1.add_vertex(v1)
        g1.add_vertex(v2)
        with self.assertRaisesRegex(ValueError, "Vertex .* has a neighbor that wasn't added to the graph"):
            g1.breadth_first_search(v1, v3)

    def test_disconnected_graph(self) -> None:
        v1 = Vertex[int](name="v1", data=1)
        v2 = Vertex[int](name="v2", data=2)
        v3 = Vertex[int](name="v3", data=3)

        v1.add_neighbor(v2)

        g1 = Graph[int]([v1, v2, v3])

        self.assertFalse(g1.breadth_first_search(v1, v3))

        path = g1.find_shortest_path(v1, v3)
        self.assertIsNone(path)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("abc").setLevel(logging.DEBUG)
    unittest.main()
