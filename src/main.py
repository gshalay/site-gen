from textnode import *
from constants import *
from markdown_parser import *

def main():
    node = TextNode("This is a text node with a `code block` word", TEXT_TYPE_TEXT)
    print(node)
    print(f"split nodes - {split_nodes_by_delimitter([node], MARKDOWN_CODE)}")

if(__name__ == "__main__"):
    main()