import unittest
from parser import remove_comments, parse_constants, parse_dict

class TestParser(unittest.TestCase):

    def test_remove_comments(self):
        text = """
C This is a comment
{
    key = value(* Multi-line comment *)
}"""
        expected = """
{
    key = value
}"""
        self.assertEqual(remove_comments(text), expected.strip())

    def test_parse_constants(self):
        text = """
        def lives = 3
        def score = 100
        {
            player = John
        }
        """
        expected_constants = {"lives": 3, "score": 100}
        expected_remaining = "{\nplayer = John\n}"
        constants, remaining_text = parse_constants(text)
        self.assertEqual(constants, expected_constants)
        self.assertEqual(remaining_text.strip(), expected_remaining.strip())

    def test_parse_dict_flat(self):
        text = "{ key1 = 123, key2 = value }"
        constants = {}
        expected = {
            "key1": 123,
            "key2": 'value'
        }
        self.assertEqual(parse_dict(text, constants), expected)

    def test_parse_dict_nested(self):
        text = "{ player = John, settings = { difficulty = hard, volume = 80}}"
        constants = {}
        expected = {
            "player": "John",
            "settings": {
                "difficulty": "hard",
                "volume": 80
            }
        }
        self.assertEqual(parse_dict(text, constants), expected)

    def test_parse_dict_with_constants(self):
        text = "{ lives = 3, score = score }"
        constants = {"score": 100}
        expected = {
            "lives": 3,
            "score": 100
        }
        self.assertEqual(parse_dict(text, constants), expected)

if __name__ == "__main__":
    unittest.main()