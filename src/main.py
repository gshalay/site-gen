from os import getcwd
from textnode import *
from constants import *
from markdown_parser import *

def main():
    # Get file contents.
    print(getcwd())
    sample1_text = "".join(open(MARKDOWN_SAMPLE_DIR + "paired_down.md").readlines())
    sample2_text = "".join(open(MARKDOWN_SAMPLE_DIR + "sample2.md").readlines())

    # Drive the main parse method.
    sample1_html = markdown_to_html_node(sample1_text)
    # sample2_html = markdown_to_html_node(sample2_text)

    print("Finished Processing.")

if(__name__ == "__main__"):
    main()