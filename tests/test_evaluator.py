import unittest
from evaluator import evaluate_postfix

class TestEvaluator(unittest.TestCase):

    def test_simple_addition(self):
        tokens = ["2", "3", "+"]
        constants = {}
        self.assertEqual(evaluate_postfix(tokens, constants), 5)

    def test_with_constants(self):
        tokens = ["score", "1", "+"]
        constants = {"score": 100}
        self.assertEqual(evaluate_postfix(tokens, constants), 101)

    def test_nested_operations(self):
        tokens = ["5", "1", "+", "2", "*"]
        constants = {}
        self.assertEqual(evaluate_postfix(tokens, constants), 12)

    def test_max_function(self):
        tokens = ["[", "3", "5", "2", "]", "max"]
        constants = {}
        self.assertEqual(evaluate_postfix(tokens, constants), 5)

    def test_invalid_expression(self):
        tokens = ["1", "+"]
        constants = {}
        with self.assertRaises(ValueError):
            evaluate_postfix(tokens, constants)

if __name__ == "__main__":
    unittest.main()