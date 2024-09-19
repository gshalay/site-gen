import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "this is a paragraph.", { "html" : "yes", "css": "no" })
        node2 = LeafNode("h1", "Header 1", { "hello" : "world", "tiny": "large" })
        node3 = LeafNode("h6", "Header 6", { "rel" : "stylesheet", "cool": "no" })
        node4 = LeafNode("p", None, { "html" : "yes", "css": "no" })

        expected = "<p html=\"yes\" css=\"no\">this is a paragraph.</p>"
        expected2 = "<h1 hello=\"world\" tiny=\"large\">Header 1</h1>"
        expected3 = "<h6 rel=\"stylesheet\" cool=\"no\">Header 6</h6>"

        self.assertEqual(node.to_html(), expected)
        self.assertEqual(node2.to_html(), expected2)
        self.assertEqual(node3.to_html(), expected3)
        self.assertRaises(ValueError, node4.to_html)

if(__name__ == "__main__"):
    unittest.main()