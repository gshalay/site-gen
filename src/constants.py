TEXT_TYPE_TEXT : str = "text"
TEXT_TYPE_BOLD : str = "bold"
TEXT_TYPE_ITALIC : str = "italic"
TEXT_TYPE_CODE : str = "code"
TEXT_TYPE_LINK : str = "link"
TEXT_TYPE_IMAGE : str = "image"

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
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

BLOCK_CODE = "```"

MARKDOWN_IMAGE_OR_LINK = "\[.*?\]\(.*?\)"

MARKDOWN_HEADINGS = [
        MARKDOWN_H6,
        MARKDOWN_H5, 
        MARKDOWN_H4,
        MARKDOWN_H3,
        MARKDOWN_H2,
        MARKDOWN_H1
]

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

