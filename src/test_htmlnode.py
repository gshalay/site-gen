import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_init(self):
        node = HtmlNode("p", "This is paragraph text.", [], {"url": "https://www.testurl.com"})
        node2 = HtmlNode()

        expected1_1 = "p"
        expected1_2 = "This is paragraph text."
        expected1_3 = []
        expected1_4 = {"url": "https://www.testurl.com"}

        expected2_1 = None
        expected2_2 = None
        expected2_3 = None
        expected2_4 = None

        self.assertEqual(node.tag, expected1_1)
        self.assertEqual(node.value, expected1_2)
        self.assertEqual(node.children, expected1_3)
        self.assertEqual(node.props, expected1_4)

        self.assertEqual(node2.tag, expected2_1)
        self.assertEqual(node2.value, expected2_2)
        self.assertEqual(node2.children, expected2_3)
        self.assertEqual(node2.props, expected2_4)

    def test_eq(self):
        node = HtmlNode("p", "text", [])
        node2 = HtmlNode("p", "text", [])
        self.assertEqual(node, node2)

    def test_repr(self):
        actual = HtmlNode("p", "BE", [], {})
        actual2 = HtmlNode("h1", "BE")
        actual3 = HtmlNode("img")

        expected = "HtmlNode(p, BE, [], {})"
        expected2 = "HtmlNode(h1, BE, None, None)"
        expected3 = "HtmlNode(img, N0ne, None, None)" 
        
        self.assertEqual(actual.__repr__(), expected)
        self.assertEqual(actual2.__repr__(), expected2)
        self.assertNotEqual(actual3.__repr__(), expected3)

    # Temporary test. Need to revamp once implemented.
    def test_to_html(self):
        node = HtmlNode()
        self.assertRaises(NotImplementedError, node.to_html)
    
    def test_props_to_html(self):
        props1 = {
            "balony" : "is a type of meat", 
            "lettuce" : "is a plant"
        }

        props2 = {
            "rel" : "stylesheet", 
            "link" : "www.google.com"
        }

        props3 = {
            "style" : "123.css", 
            "alt" : "image alt text"
        }

        node = HtmlNode("p", "text", [], props1)
        node2 = HtmlNode("p", "text", [], props2)
        node3 = HtmlNode("p", "text", [], props3)

        expected1 = "balony=\"is a type of meat\" lettuce=\"is a plant\""
        expected2 = "rel=\"stylesheet\" link=\"www.google.com\""
        expected3 = "style=\"123.css\" alt=\"image alt text\""

        self.assertEqual(node.props_to_html(), expected1)
        self.assertEqual(node2.props_to_html(), expected2)
        self.assertEqual(node3.props_to_html(), expected3)


if(__name__ == "__main__"):
    unittest.main()