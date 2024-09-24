import unittest

from leafnode import LeafNode
from textnode import TextNode
from constants import *
from main import text_node_to_html_node

class TestMain(unittest.TestCase):
    def test_text_node_to_html_node(self):
        self.setDiff = None

        text_node1 = TextNode("nothing to see here...", "text")
        text_node2 = TextNode("I'm Bold!", "bold")
        text_node3 = TextNode("OOOOH italics!", "italic")
        text_node4 = TextNode("while true do this.", "code")
        text_node5 = TextNode("Some link", "link", "https://www.google.com")
        text_node6 = TextNode("Some image", "image", "c:/Test/intro.png")
        text_node7 = TextNode("This isn't right...", "uhoh")

        actual1 = text_node_to_html_node(text_node1)
        actual2 = text_node_to_html_node(text_node2)
        actual3 = text_node_to_html_node(text_node3)
        actual4 = text_node_to_html_node(text_node4)
        actual5 = text_node_to_html_node(text_node5)
        actual6 = text_node_to_html_node(text_node6)

        expected1 = LeafNode(None, "nothing to see here...")
        expected2 = LeafNode("b", "I'm Bold!")
        expected3 = LeafNode("i", "OOOOH italics!")
        expected4 = LeafNode("code", "while true do this.")
        expected5 = LeafNode("a", "Some link", { "href" : "https://www.google.com" })
        expected6 = LeafNode("img", "Some image", { "src" : "c:/Test/intro.png", "alt" : "" })

        self.assertEqual(actual1, expected1)
        self.assertEqual(actual2, expected2)
        self.assertEqual(actual3, expected3)
        self.assertEqual(actual4, expected4)
        self.assertEqual(actual5, expected5)
        self.assertEqual(actual6, expected6)
        self.assertRaises(Exception, text_node_to_html_node, text_node7)

if(__name__ == "__main__"):
    unittest.main()