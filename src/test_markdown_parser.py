import unittest

from leafnode import LeafNode
from textnode import TextNode
from constants import *
from markdown_parser import text_node_to_html_node
from markdown_parser import split_nodes_delimitter
from markdown_parser import get_delim_postitions
from markdown_parser import extract_markdown_images
from markdown_parser import extract_markdown_links

class TestMarkdownParser(unittest.TestCase):
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


    def test_get_delim_postitions(self):
          self.setDiff = None
          
          actual1 = get_delim_postitions("`first and last`")
          actual2 = get_delim_postitions("to a*n*d fro")
          actual3 = get_delim_postitions("**only** start")
          actual4 = get_delim_postitions("only *end*")
          actual5 = get_delim_postitions("*nothing* **to see** `here...`")

          expected1 = { "`"  : [[0, 15]] }
          expected2 = { "*"  : [[4, 6]] }
          expected3 = { "**" : [[0, 6]] }
          expected4 = { "*"  : [[5, 9]] }
          expected5 = { "*"  : [[0, 8]],
                        "**" : [[10, 18]],
                        "`"  : [[21, 29]] }

          self.assertEqual(actual1, expected1)
          self.assertEqual(actual2, expected2)
          self.assertEqual(actual3, expected3)
          self.assertEqual(actual4, expected4)
          self.assertEqual(actual5, expected5)

    
    def test_split_nodes_delimitter(self):
        self.setDiff = None

        # Text nodes with delims at start of string
        text_node1 = split_nodes_delimitter([TextNode("nothing to see here...", "text")], None, TEXT_TYPE_TEXT)
        text_node2 = split_nodes_delimitter([TextNode("**I'm Bold!** but I'm not!", "bold")], MARKDOWN_BOLD, TEXT_TYPE_BOLD)
        text_node3 = split_nodes_delimitter([TextNode("*OOOOH italics!*aww... I'm normal", "italic")], MARKDOWN_ITALIC, TEXT_TYPE_ITALIC)
        text_node4 = split_nodes_delimitter([TextNode("`spaghetti code` what is going on here?", "code")], MARKDOWN_CODE, TEXT_TYPE_CODE)
        
        # # delims in the middle
        text_node5 = split_nodes_delimitter([TextNode("nothing **to** see here...", "bold")], MARKDOWN_BOLD, TEXT_TYPE_BOLD)
        text_node6 = split_nodes_delimitter([TextNode("nothing *to* see here...", "italic")], MARKDOWN_ITALIC, TEXT_TYPE_ITALIC)
        text_node7 = split_nodes_delimitter([TextNode("nothing `to` see here...", "code")], MARKDOWN_CODE, TEXT_TYPE_CODE)

        # # delims at the end
        text_node8 = split_nodes_delimitter([TextNode("nothing to **see here...**", "bold")], MARKDOWN_BOLD, TEXT_TYPE_BOLD)
        text_node9 = split_nodes_delimitter([TextNode("nothing to see *here...*", "italic")], MARKDOWN_ITALIC, TEXT_TYPE_ITALIC)
        text_node10 = split_nodes_delimitter([TextNode("nothing to see `here...`", "code")], MARKDOWN_CODE, TEXT_TYPE_CODE)

        # # multiple delims
        text_node11 = split_nodes_delimitter([TextNode("**nothing** *to see* `here...`", "bold")], MARKDOWN_BOLD, TEXT_TYPE_BOLD)
        text_node12 = split_nodes_delimitter([TextNode("*nothing* **to see** `here...`", "italic")], MARKDOWN_ITALIC, TEXT_TYPE_ITALIC)
        text_node13 = split_nodes_delimitter([TextNode("`nothing` *to see* **here...**", "code")], MARKDOWN_CODE, TEXT_TYPE_CODE)
        text_node14 = split_nodes_delimitter([TextNode("**nothing** `to see` `here...`", "bold")], MARKDOWN_BOLD, TEXT_TYPE_BOLD)
        text_node15 = split_nodes_delimitter([TextNode("let me write some code... `while true do this` oh no! an **infinite** loop! NOT THE MEMORY!!!", "code")], MARKDOWN_CODE, TEXT_TYPE_CODE)

        # Expected results
        expected_1  = [] # [TextNode("nothing to see here...", "text")]
        expected_2  = [TextNode("I'm Bold!", "bold"), TextNode(" but I'm not!", "text")]
        expected_3  = [TextNode("OOOOH italics!", "italic"), TextNode("aww... I'm normal", "text")]
        expected_4  = [TextNode("spaghetti code", "code"), TextNode(" what is going on here?", "text")]
        expected_5  = [TextNode("nothing ", "text"), TextNode("to", "bold"), TextNode(" see here...", "text")]
        expected_6  = [TextNode("nothing ", "text"), TextNode("to", "italic"), TextNode(" see here...", "text")]
        expected_7  = [TextNode("nothing ", "text"), TextNode("to", "code"), TextNode(" see here...", "text")]
        expected_8  = [TextNode("nothing to ", "text"), TextNode("see here...", "bold")]
        expected_9  = [TextNode("nothing to see ", "text"), TextNode("here...", "italic")]
        expected_10 = [TextNode("nothing to see ", "text"), TextNode("here...", "code")]

        expected_11 = [
             TextNode("nothing", "bold"),
             TextNode(" ", "text"),
             TextNode("to see", "italic"),
             TextNode(" ", "text"),
             TextNode("here...", "code")
        ]

        expected_12 = [
             TextNode("nothing", "italic"),
             TextNode(" ", "text"),
             TextNode("to see", "bold"),
             TextNode(" ", "text"),
             TextNode("here...", "code")
        ]

        expected_13 = [
             TextNode("nothing", "code"),
             TextNode(" ", "text"),
             TextNode("to see", "italic"),
             TextNode(" ", "text"),
             TextNode("here...", "bold")
        ]

        expected_14 = [
             TextNode("nothing", "bold"),
             TextNode(" ", "text"),
             TextNode("to see", "code"),
             TextNode(" ", "text"),
             TextNode("here...", "code")
        ]

        expected_15 = [
             TextNode("let me write some code... ", "text"), 
             TextNode("while true do this", "code"), 
             TextNode(" oh no! an ", "text"), 
             TextNode("infinite", "bold"), 
             TextNode(" loop! NOT THE MEMORY!!!", "text")
        ]

        # Assertions
        self.assertEqual(text_node1, expected_1)
        self.assertEqual(text_node2, expected_2)
        self.assertEqual(text_node3, expected_3)
        self.assertEqual(text_node4, expected_4)
        self.assertEqual(text_node5, expected_5)
        self.assertEqual(text_node6, expected_6)
        self.assertEqual(text_node7, expected_7)
        self.assertEqual(text_node8, expected_8)
        self.assertEqual(text_node9, expected_9)
        self.assertEqual(text_node10, expected_10)
        self.assertEqual(text_node11, expected_11)
        self.assertEqual(text_node12, expected_12)
        self.assertEqual(text_node13, expected_13)
        self.assertEqual(text_node14, expected_14)
        self.assertEqual(text_node15, expected_15)

def test_extract_markdown_images(self):
     text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
     text2 = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

     actual1 = extract_markdown_images(text1)
     actual2 = extract_markdown_images(text2)

     expected1 = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
     expected2 = [("to boot dev", "https://www.boot.dev")]

     self.assertEquals(actual1, expected1)
     self.assertEquals(actual2, expected2)

def test_extract_markdown_links(self):
     text1 = "This is text with a ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
     text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

     actual1 = extract_markdown_links(text1)
     actual2 = extract_markdown_links(text2)

     expected1 = []
     expected2 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

     self.assertEquals(actual1, expected1)
     self.assertEquals(actual2, expected2)


if(__name__ == "__main__"):
    unittest.main()