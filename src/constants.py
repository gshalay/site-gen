from os import getcwd

TEXT_TYPE_TEXT : str = "text"
TEXT_TYPE_BOLD : str = "bold"
TEXT_TYPE_ITALIC : str = "italic"
TEXT_TYPE_CODE : str = "code"
TEXT_TYPE_LINK : str = "link"
TEXT_TYPE_IMAGE : str = "image"
TEXT_TYPE_H1 : str = "h1"
TEXT_TYPE_H2 : str = "h2"
TEXT_TYPE_H3 : str = "h3"
TEXT_TYPE_H4 : str = "h4"
TEXT_TYPE_H5 : str = "h5"
TEXT_TYPE_H6 : str = "h6"

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code_block"
BLOCK_TYPE_QUOTE = "blockquote"
BLOCK_TYPE_UL = "unordered_list"
BLOCK_TYPE_OL = "ordered_list"

MARKDOWN_H1 = "# "
MARKDOWN_H2 = "## "
MARKDOWN_H3 = "### "
MARKDOWN_H4 = "#### "
MARKDOWN_H5 = "##### "
MARKDOWN_H6 = "###### "
MARKDOWN_BOLD = "**"
MARKDOWN_ITALIC = "*"
MARKDOWN_ITALIC2 = "_"
MARKDOWN_BLOCKQUOTE = ">"
MARKDOWN_CODE = "`"

MARKDOWN_UL_PREFIX_1 = "* "
MARKDOWN_UL_PREFIX_2 = "- "

MARKDOWN_OL_PREFIX = "^\d+\.\s+.*"

MARKDOWN_BLOCK_CODE = "```"

MARKDOWN_IMAGE_OR_LINK = "\[.*?\]\(.*?\)"

MARKDOWN_HEADINGS = [
        MARKDOWN_H6,
        MARKDOWN_H5, 
        MARKDOWN_H4,
        MARKDOWN_H3,
        MARKDOWN_H2,
        MARKDOWN_H1
]

BLOCK_TYPE_DELIMS = { 
        "heading6" : MARKDOWN_H6,
        "heading5" : MARKDOWN_H5, 
        "heading4" : MARKDOWN_H4,
        "heading3" : MARKDOWN_H3,
        "heading2" : MARKDOWN_H2,
        "heading1" : MARKDOWN_H1,
        "ul_1" : MARKDOWN_UL_PREFIX_1,
        "ul_2" : MARKDOWN_UL_PREFIX_2, 
        "ol" : MARKDOWN_OL_PREFIX,
        "blockquote" : MARKDOWN_BLOCKQUOTE,
        "block_code" : MARKDOWN_BLOCK_CODE 
}

MARKDOWN_DELIMS = { 
        "h6" : MARKDOWN_H6,
        "h5" : MARKDOWN_H5, 
        "h4" : MARKDOWN_H4,
        "h3" : MARKDOWN_H3,
        "h2" : MARKDOWN_H2,
        "h1" : MARKDOWN_H1,
        "bold" : MARKDOWN_BOLD, 
        "italic" : MARKDOWN_ITALIC,
        "italic2" : MARKDOWN_ITALIC2,
        "blockquote" : MARKDOWN_BLOCKQUOTE,
        "code" : MARKDOWN_CODE 
}

HTML_TAG_TYPES = {
    "ordered_list" : "ol",
    "unordered_list" : "ul",
    "heading1" : "h1",
    "heading2" : "h2",
    "heading3" : "h3",
    "heading4" : "h4",
    "heading5" : "h5",
    "heading6" : "h6",
    "code_block" : "code",
    "bold" : "b",
    "italic" : "i",
    "image" : "img",
    "link" : "a", 
    "division" : "div", 
    "paragraph" : "p",
    "list_item" : "li",
    "blockquote" : "blockquote"
}

MARKDOWN_SAMPLE_DIR = getcwd() + "/src/markdown_sample_files/"