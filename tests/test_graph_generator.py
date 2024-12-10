import unittest
import os
from graph_generator import generate_plantuml_graph

class TestGraphGenerator(unittest.TestCase):
    def test_generate_graph(self):
        dependencies = {"A": {"B", "C"}, "B": set(), "C": set()}
        output_file = "test.uml"
        generate_plantuml_graph(dependencies, output_file)
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)
