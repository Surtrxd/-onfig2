import unittest
from analyzer import analyze_dependencies

class TestAnalyzer(unittest.TestCase):
    def test_analyze_dependencies(self):
        dependencies = analyze_dependencies("com.example.main")
        self.assertIn("com.example.main", dependencies)
        self.assertIn("com.example.utils", dependencies["com.example.main"])
