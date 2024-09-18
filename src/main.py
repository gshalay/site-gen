from textnode import *

def main():
    test_node = TextNode("someText", "someType", "https://wallawashington.ca")
    none_node = TextNode("Nope", "Nah fam")

    print(test_node)
    print(none_node)

if(__name__ == "__main__"):
    main()
    print("hello world")