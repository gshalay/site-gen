import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_init(self):
        node = TextNode("this is a test node", "bold")
        node2 = TextNode("this is a test node", "bold", "https://www.google.com")

        expected1_1 = "this is a test node"
        expected1_2 = "bold"
        expected1_3 = None

        expected2_1 = "this is a test node"
        expected2_2 = "bold"
        expected2_3 = "https://www.google.com"

        self.assertEqual(node.text, expected1_1)
        self.assertEqual(node.text_type, expected1_2)
        self.assertEqual(node.url, expected1_3)

        self.assertEqual(node2.text, expected2_1)
        self.assertEqual(node2.text_type, expected2_2)
        self.assertEqual(node2.url, expected2_3)

    def test_eq(self):
        node = TextNode("this is a test node", "bold")
        node2 = TextNode("this is a test node", "bold")
        self.assertEqual(node, node2)

    def test_repr(self):
        actual = TextNode("I WANNA", "BE", "THE VERY BEST")
        actual2 = TextNode("I WANNA", "BE", "THE VERY B3ST")
        actual3 = TextNode("I W4NNA", "BE")

        expected = "TextNode(I WANNA, BE, THE VERY BEST)"
        expected2 = "TextNode(I WANNA, BE, THE VERY BEST)"
        expected3 = "TextNode(I WANNA, BE, None)" 
        
        self.assertEqual(actual.__repr__(), expected)
        self.assertNotEqual(actual2.__repr__(), expected2)
        self.assertNotEqual(actual3.__repr__(), expected3)

if(__name__ == "__main__"):
    unittest.main()