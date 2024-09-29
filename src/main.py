from textnode import *
from constants import *
from markdown_parser import *

def main():
    node = TextNode("This is a text node with a `code block` word", TEXT_TYPE_TEXT)
    node2 = TextNode("**There once was a man from Peru *He slipped and fell one day and lost his shoe* `which made him quite blue`, now a man with one shoe**", TEXT_TYPE_BOLD)
    node3 = TextNode("There once was a man from Tahiti > He climbed a cliff and watched the sunset. *Then came night `then midnight` then dawn `then morning once more`* C'est Fini.", MARKDOWN_BLOCKQUOTE)

    # print(f"split nodes - {split_nodes_by_delimitter([node])}")
    # print(f"split nodes - {split_nodes_by_delimitter([node2])}")
    # print(f"split nodes - {split_nodes_by_delimitter([node3])}")

if(__name__ == "__main__"):
    main()