import unittest

from leafnode import LeafNode
from textnode import TextNode
from constants import *
from markdown_parser import text_node_to_html_node
from markdown_parser import split_nodes_delimitter
from markdown_parser import get_delim_postitions
from markdown_parser import extract_markdown_images
from markdown_parser import extract_markdown_links
from markdown_parser import split_nodes_image
from markdown_parser import split_nodes_link
from markdown_parser import text_to_textnodes
from markdown_parser import markdown_to_blocks
from markdown_parser import block_to_block_type

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

          self.assertEqual(actual1, expected1)
          self.assertEqual(actual2, expected2)

     def test_extract_markdown_links(self):
          self.maxDiff = None
          text1 = "This is text with a ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
          text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

          actual1 = extract_markdown_links(text1)
          actual2 = extract_markdown_links(text2)

          expected1 = []
          expected2 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

          self.assertEqual(actual1, expected1)
          self.assertEqual(actual2, expected2)

     def test_split_link_nodes(self):
          self.maxDiff = None
          link_nodes1 = [
               TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                    TEXT_TYPE_TEXT)
          ]

          link_nodes2 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site [tellmeaboutit](https://tellmeaboutit.org) nah maybe later. [haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          link_nodes3 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site [tellmeaboutit](https://tellmeaboutit.org) nah maybe later. [haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          link_nodes4 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site [tellmeaboutit](https://tellmeaboutit.org) nah maybe later. ![haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          link_nodes5 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site [tellmeaboutit](https://tellmeaboutit.org) nah maybe later. ![haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          link_nodes6 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site [tellmeaboutit](https://tellmeaboutit.org) nah maybe later. [haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          link_nodes7 = [
               TextNode("[hello there](www.mynamejeff.com)[tellmeaboutit](https://tellmeaboutit.org)[haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          expected1 = [
               TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ", TEXT_TYPE_TEXT),
               TextNode("to youtube", TEXT_TYPE_LINK, "https://www.youtube.com/@bootdotdev"),
          ]

          expected2 = [
               TextNode("hello there", TEXT_TYPE_LINK, "www.mynamejeff.com"),
               TextNode(" what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_LINK, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. ", TEXT_TYPE_TEXT),
               TextNode("haveityourway", TEXT_TYPE_LINK, "https://www.burgerking.ca"),
          ]

          expected3 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_LINK, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. ", TEXT_TYPE_TEXT),
               TextNode("haveityourway", TEXT_TYPE_LINK, "https://www.burgerking.ca"),
          ]

          expected4 = [
               TextNode("hello there", TEXT_TYPE_LINK, "www.mynamejeff.com"),
               TextNode(" what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_LINK, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. ![haveityourway](https://www.burgerking.ca)", TEXT_TYPE_TEXT),
          ]

          expected5 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_LINK, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. ![haveityourway](https://www.burgerking.ca)", TEXT_TYPE_TEXT),
          ]

          expected6 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site ", TEXT_TYPE_TEXT), 
               TextNode("tellmeaboutit", TEXT_TYPE_LINK, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. ", TEXT_TYPE_TEXT),
               TextNode("haveityourway", TEXT_TYPE_LINK, "https://www.burgerking.ca"),
          ]

          expected7 = [
               TextNode("hello there", TEXT_TYPE_LINK, "www.mynamejeff.com"),
               TextNode("tellmeaboutit", TEXT_TYPE_LINK, "https://tellmeaboutit.org"),
               TextNode("haveityourway", TEXT_TYPE_LINK, "https://www.burgerking.ca")
          ]

          self.assertEqual(split_nodes_link(link_nodes1), expected1)
          self.assertEqual(split_nodes_link(link_nodes2), expected2)
          self.assertEqual(split_nodes_link(link_nodes3), expected3)
          self.assertEqual(split_nodes_link(link_nodes4), expected4)
          self.assertEqual(split_nodes_link(link_nodes5), expected5)
          self.assertEqual(split_nodes_link(link_nodes6), expected6)
          self.assertEqual(split_nodes_link(link_nodes7), expected7)

     def test_split_image_nodes(self):
          self.maxDiff = None

          image_nodes1 = [
               TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
                    TEXT_TYPE_TEXT)
          ]

          image_nodes2 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site ![tellmeaboutit](https://tellmeaboutit.org) nah maybe later. ![haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          image_nodes3 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site ![tellmeaboutit](https://tellmeaboutit.org) nah maybe later. ![haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          image_nodes4 = [
               TextNode("![hello there](www.mynamejeff.com) what a weird name for a site ![tellmeaboutit](https://tellmeaboutit.org) nah maybe later. [haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          image_nodes5 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site ![tellmeaboutit](https://tellmeaboutit.org) nah maybe later. [haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          image_nodes6 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site [tellmeaboutit](https://tellmeaboutit.org) nah maybe later. ![haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          image_nodes7 = [
               TextNode("![hello there](www.mynamejeff.com)![tellmeaboutit](https://tellmeaboutit.org)![haveityourway](https://www.burgerking.ca)",
                    TEXT_TYPE_TEXT)
          ]

          expected1 = [
               TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ", TEXT_TYPE_TEXT),
               TextNode("to youtube", TEXT_TYPE_IMAGE, "https://www.youtube.com/@bootdotdev"),
          ]

          expected2 = [
               TextNode("hello there", TEXT_TYPE_IMAGE, "www.mynamejeff.com"),
               TextNode(" what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_IMAGE, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. ", TEXT_TYPE_TEXT),
               TextNode("haveityourway", TEXT_TYPE_IMAGE, "https://www.burgerking.ca"),
          ]

          expected3 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_IMAGE, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. ", TEXT_TYPE_TEXT),
               TextNode("haveityourway", TEXT_TYPE_IMAGE, "https://www.burgerking.ca"),
          ]

          expected4 = [
               TextNode("hello there", TEXT_TYPE_IMAGE, "www.mynamejeff.com"),
               TextNode(" what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_IMAGE, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. [haveityourway](https://www.burgerking.ca)", TEXT_TYPE_TEXT)
          ]

          expected5 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site ", TEXT_TYPE_TEXT),
               TextNode("tellmeaboutit", TEXT_TYPE_IMAGE, "https://tellmeaboutit.org"),
               TextNode(" nah maybe later. [haveityourway](https://www.burgerking.ca)", TEXT_TYPE_TEXT)
          ]

          expected6 = [
               TextNode("[hello there](www.mynamejeff.com) what a weird name for a site [tellmeaboutit](https://tellmeaboutit.org) nah maybe later. ", TEXT_TYPE_TEXT),
               TextNode("haveityourway", TEXT_TYPE_IMAGE, "https://www.burgerking.ca")
          ]

          expected7 = [
               TextNode("hello there", TEXT_TYPE_IMAGE, "www.mynamejeff.com"),
               TextNode("tellmeaboutit", TEXT_TYPE_IMAGE, "https://tellmeaboutit.org"),
               TextNode("haveityourway", TEXT_TYPE_IMAGE, "https://www.burgerking.ca")
          ]

          self.assertEqual(split_nodes_image(image_nodes1), expected1)
          self.assertEqual(split_nodes_image(image_nodes2), expected2)
          self.assertEqual(split_nodes_image(image_nodes3), expected3)
          self.assertEqual(split_nodes_image(image_nodes4), expected4)
          self.assertEqual(split_nodes_image(image_nodes5), expected5)
          self.assertEqual(split_nodes_image(image_nodes6), expected6)
          self.assertEqual(split_nodes_image(image_nodes7), expected7)

     def test_text_to_textnodes(self):
          actual1 = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
          actual2 = text_to_textnodes("This is and a [link](https://boot.dev)![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)")
          actual3 = text_to_textnodes("and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and This is **text** with an *italic* word and a `code block` a [link](https://boot.dev)")

          expected1 = [
               TextNode("This is ", TEXT_TYPE_TEXT),
               TextNode("text", TEXT_TYPE_BOLD),
               TextNode(" with an ", TEXT_TYPE_TEXT),
               TextNode("italic", TEXT_TYPE_ITALIC),
               TextNode(" word and a ", TEXT_TYPE_TEXT),
               TextNode("code block", TEXT_TYPE_CODE),
               TextNode(" and an ", TEXT_TYPE_TEXT),
               TextNode("obi wan image", TEXT_TYPE_IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
               TextNode(" and a ", TEXT_TYPE_TEXT),
               TextNode("link", TEXT_TYPE_LINK, "https://boot.dev"),
          ]

          expected2 = [
               TextNode("This is and a ", TEXT_TYPE_TEXT),
               TextNode("link", TEXT_TYPE_LINK, "https://boot.dev"),
               TextNode("obi wan image", TEXT_TYPE_IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
          ]

          expected3 = [
               TextNode("and an ", TEXT_TYPE_TEXT),
               TextNode("obi wan image", TEXT_TYPE_IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
               TextNode(" and This is ", TEXT_TYPE_TEXT),
               TextNode("text", TEXT_TYPE_BOLD),
               TextNode(" with an ", TEXT_TYPE_TEXT),
               TextNode("italic", TEXT_TYPE_ITALIC),
               TextNode(" word and a ", TEXT_TYPE_TEXT),
               TextNode("code block", TEXT_TYPE_CODE),
               TextNode(" a ", TEXT_TYPE_TEXT),
               TextNode("link", TEXT_TYPE_LINK, "https://boot.dev"),
               
          ]

          self.assertEqual(actual1, expected1)
          self.assertEqual(actual2, expected2)
          self.assertEqual(actual3, expected3)

     def test_markdown_to_blocks(self):
          actual1 = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
          actual2 = "wallan\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nallen\n\nallenjackson420"
          actual3 = "    happy    \n\n tastes\n\n  gucci"

          expected1 = [ 
               "# This is a heading", 
               "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
               "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
          ]

          expected2 = [
               "wallan", 
               "allen",
               "allenjackson420"
          ]

          expected3 = [
               "happy", 
               "tastes",
               "gucci"
          ]

          self.assertEqual(markdown_to_blocks(actual1), expected1)
          self.assertEqual(markdown_to_blocks(actual2), expected2)
          self.assertEqual(markdown_to_blocks(actual3), expected3)

     def test_block_to_block_type(self):
          actual1 = block_to_block_type("# HEADING 1")
          actual2 = block_to_block_type("## HEADING 2")
          actual3 = block_to_block_type("### HEADING 3")
          actual4 = block_to_block_type("#### HEADING 4")
          actual5 = block_to_block_type("##### HEADING 5")
          actual6 = block_to_block_type("###### HEADING 6")

          actual7 = block_to_block_type("* item1\n* item2\n* item3\n* item4\n* item5")
          actual8 = block_to_block_type("- item1\n- item2\n- item3\n- item4\n- item5")
          actual9 = block_to_block_type("* item1\n* item2\n- item3\n* item4\n- item5")
          actual10 = block_to_block_type("- item1\n* item2\n- item3\n- item4\n* item5")

          actual11 = block_to_block_type("1. this is item 1\n2. this is item 1\n3. this is item 1\n4. this is item 1\n5. this is item 1\n6. this is item 1")
          actual12 = block_to_block_type("1. this is item 1\n2. this is item 1\n3. this is item 1\n4. this is item 1\n5. this is item 1\n8. this is item 1")

          actual13 = block_to_block_type("> this is a line\n> this is a line\n> this is a line\n> this is a line\n> this is a line")
          actual14 = block_to_block_type(">this is a line\n>this is a line\n>this is a line\n>this is a line\n>this is a line")
          actual15 = block_to_block_type("> this is a line\n> this is a line\n+ this is a line\n> this is a line\np this is a line")

          actual16 = block_to_block_type("```this is a line\n> this is a line\n+ this is a line\n> this is a line\np this is a line\n```")
          actual17 = block_to_block_type("```> this is a line\n> this is a line\n+ this is a line\n> this is a line\np this is a line\n``")
          actual18 = block_to_block_type("``> this is a line\n> this is a line\n+ this is a line\n> this is a line\np this is a line\n```")

          actual19 = block_to_block_type("uhhhhhh... paragraph maybe???")
          actual20 = block_to_block_type("multiline paragraph\nmultiline paragraph\nmultiline paragraph\nmultiline paragraph\nmultiline paragraph\nmultiline paragraph")
          
          expected1 = BLOCK_TYPE_HEADING
          expected2 = BLOCK_TYPE_HEADING
          expected3 = BLOCK_TYPE_HEADING
          expected4 = BLOCK_TYPE_HEADING
          expected5 = BLOCK_TYPE_HEADING
          expected6 = BLOCK_TYPE_HEADING
          expected7 = BLOCK_TYPE_UL
          expected8 = BLOCK_TYPE_UL
          expected9 = BLOCK_TYPE_UL
          expected10 = BLOCK_TYPE_UL
          expected11 = BLOCK_TYPE_OL
          expected12 = BLOCK_TYPE_PARAGRAPH
          expected13 = BLOCK_TYPE_QUOTE
          expected14 = BLOCK_TYPE_QUOTE
          expected15 = BLOCK_TYPE_PARAGRAPH
          expected16 = BLOCK_TYPE_CODE
          expected17 = BLOCK_TYPE_PARAGRAPH
          expected18 = BLOCK_TYPE_PARAGRAPH
          expected19 = BLOCK_TYPE_PARAGRAPH
          expected20 = BLOCK_TYPE_PARAGRAPH

          self.assertEqual(actual1, expected1)
          self.assertEqual(actual2, expected2)
          self.assertEqual(actual3, expected3)
          self.assertEqual(actual4, expected4)
          self.assertEqual(actual5, expected5)
          self.assertEqual(actual6, expected6)
          self.assertEqual(actual7, expected7)
          self.assertEqual(actual8, expected8)
          self.assertEqual(actual9, expected9)
          self.assertEqual(actual10, expected10)
          self.assertEqual(actual11, expected11)
          self.assertEqual(actual12, expected12)
          self.assertEqual(actual13, expected13)
          self.assertEqual(actual14, expected14)
          self.assertEqual(actual15, expected15)
          self.assertEqual(actual16, expected16)
          self.assertEqual(actual17, expected17)
          self.assertEqual(actual18, expected18)
          self.assertEqual(actual19, expected19)
          self.assertEqual(actual20, expected20)


if(__name__ == "__main__"):
    unittest.main()
