TEXT_TYPE_TEXT : str = "text"
TEXT_TYPE_BOLD : str = "bold"
TEXT_TYPE_ITALIC : str = "italic"
TEXT_TYPE_CODE : str = "code"
TEXT_TYPE_LINK : str = "link"
TEXT_TYPE_IMAGE : str = "image"

MARKDOWN_H1 = "#"
MARKDOWN_H2 = "##"
MARKDOWN_H3 = "###"
MARKDOWN_H4 = "####"
MARKDOWN_H5 = "#####"
MARKDOWN_H6 = "######"
MARKDOWN_BOLD = "**"
MARKDOWN_ITALIC = "*"
MARKDOWN_ITALIC2 = "_"
MARKDOWN_BLOCKQUOTE = ">"
MARKDOWN_CODE = "`" # one or more I guess.

MARKDOWN_IMAGE = "^\[.*\]\(.*\)$"

MARKDOWN_DELIMS = { 
        "h6" : MARKDOWN_H6,
        "h6" : MARKDOWN_H5,
        "h6" : MARKDOWN_H1, 
        "h6" : MARKDOWN_H4,
        "h6" : MARKDOWN_H3,
        "h6" : MARKDOWN_H2,
        "h6" : MARKDOWN_H1,
        "h6" : MARKDOWN_BOLD, 
        "h6" : MARKDOWN_ITALIC,
        "h6" : MARKDOWN_ITALIC2,
        "h6" : MARKDOWN_BLOCKQUOTE,
        "h6" : MARKDOWN_CODE 
}

