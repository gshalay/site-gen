import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        self.maxDiff = None

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        )

        node2 = ParentNode("html", 
            [
                ParentNode("body", 
                    [
                        LeafNode("h2", "An Unordered HTML List"),
                        ParentNode("ul", 
                            [
                                LeafNode("li", "Coffee"),
                                LeafNode("li", "Tea"),           
                                LeafNode("li", "Milk"),
                                LeafNode("li", "Muffins")
                            ]
                        ),
                        LeafNode("h2", "An Ordered HTML List"),
                        ParentNode("ol", 
                            [
                                LeafNode("li", "Coffee"),
                                LeafNode("li", "Tea"),           
                                LeafNode("li", "Milk"),
                                LeafNode("li", "Muffins")
                            ]
                        ),
                    ]
                )
            ]
        )

        node3 = ParentNode("html",
            [
                ParentNode("body", 
                    [
                        LeafNode(None, "Normal text"),
                        ParentNode("ul", 
                            [
                                LeafNode("li", "tape glue runner")
                            ]
                        ),
                        LeafNode(None, "Normal text"),
                        ParentNode("ol", 
                            [
                                LeafNode("li", "dye ink pad")
                            ]
                        ),
                        LeafNode(None, "Normal text"),
                        ParentNode("p",
                            [
                                LeafNode(None, "One two three "), 
                                LeafNode("i", "italic"),
                                LeafNode(None, " four five six")
                            ]
                        ),
                        LeafNode(None, "Normal text"),
                    ]
                ),
            ]
        )

        node4 = ParentNode("html",
            [
                ParentNode("body", 
                    [
                        LeafNode(None, "Normal text"),
                        ParentNode("ul", None),
                        LeafNode(None, "Normal text"),
                        LeafNode("ol", None),
                        LeafNode(None, "Normal text"),
                        ParentNode("p",
                            [
                                LeafNode(None, "One two three "), 
                                LeafNode("i", "italic"),
                                LeafNode(None, " four five six")
                            ]
                        ),
                        LeafNode(None, "Normal text"),
                    ]
                ),
            ]
        )

        node5 = ParentNode("html",
            [
                ParentNode("body",
                    [
                        ParentNode("div", 
                            [
                                ParentNode("p", 
                                    [
                                        ParentNode("a", 
                                            [
                                                LeafNode(None, "Some text.")
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        node6 = ParentNode("html", 
            [
                LeafNode(None, "Some text."),
                LeafNode("i", "italic text", {"l": "link"}),
                LeafNode("i", "italic text", {"num": "twelve"}),
                ParentNode("parent", 
                    [
                        ParentNode("inner", 
                            [
                                LeafNode("p", "paragraph", {"test" : "1", "debug" : "0"})
                            ],
                            {"innerProp1" : "prop1", "innerProp2" : "prop2"}
                        )
                        
                    ],
                    {"prop1" : "p1", "prop2" : "p2"}
                )
            ]
        )

        node7 = ParentNode("html", 
            [
                LeafNode("body")
            ], 
            {})

        node8 = ParentNode("html", 
            [
                LeafNode("body", "some val", {})
            ], 
            {})

        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        expected2 = "<html><body><h2>An Unordered HTML List</h2><ul><li>Coffee</li><li>Tea</li><li>Milk</li><li>Muffins</li></ul><h2>An Ordered HTML List</h2><ol><li>Coffee</li><li>Tea</li><li>Milk</li><li>Muffins</li></ol></body></html>"
        expected3 = "<html><body>Normal text<ul><li>tape glue runner</li></ul>Normal text<ol><li>dye ink pad</li></ol>Normal text<p>One two three <i>italic</i> four five six</p>Normal text</body></html>"
        expected5 = "<html><body><div><p><a>Some text.</a></p></div></body></html>"
        expected6 = "<html>Some text.<i l=\"link\">italic text</i><i num=\"twelve\">italic text</i><parent prop1=\"p1\" prop2=\"p2\"><inner innerProp1=\"prop1\" innerProp2=\"prop2\"><p test=\"1\" debug=\"0\">paragraph</p></inner></parent></html>"
        expected8 = "<html><body>some val</body></html>"

        self.assertEqual(node.to_html(), expected)
        self.assertEqual(node2.to_html(), expected2)
        self.assertEqual(node3.to_html(), expected3)
        self.assertRaises(ValueError, node4.to_html)
        self.assertEqual(node5.to_html(), expected5)
        self.assertEqual(node6.to_html(), expected6)
        self.assertRaises(ValueError, node7.to_html)
        self.assertEqual(node8.to_html(), expected8)

if(__name__ == "__main__"):
    unittest.main()