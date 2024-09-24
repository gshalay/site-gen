from constants import *
from leafnode import LeafNode
from textnode import TextNode
import re

def text_node_to_html_node(text_node):
        html_node = None

        match(str(text_node.text_type)):
            case "text":
                html_node = LeafNode(None, text_node.text)
            case "bold":
                html_node = LeafNode("b", text_node.text)
            case "italic":
                html_node = LeafNode("i", text_node.text)
            case "code":
                html_node = LeafNode("code", text_node.text)
            case "link":
                html_node = LeafNode("a", text_node.text, { "href" : text_node.url})
            case "image":
                html_node = LeafNode("img", text_node.text, {"src" : text_node.url, "alt" : ""})
            case _:
                raise Exception(f"Tag '{text_node.text_type}' is unknown.")
            
        return html_node

def markdown_delim_to_text_type(delim : str):
    if(delim == MARKDOWN_CODE):
        return TEXT_TYPE_CODE
    elif(delim == MARKDOWN_BOLD):
        return TEXT_TYPE_BOLD
    elif(delim == TEXT_TYPE_ITALIC):
        return TEXT_TYPE_ITALIC
    elif(delim == TEXT_TYPE_TEXT):
        return TEXT_TYPE_TEXT
    else:
        raise ValueError(f"Unknown markdown delimitter '{delim}'.")


def convert_image_to_text_token(image_text):
    bracket_text = image_text.substring(image_text.find("[") + 1, image_text.find("]"))
    paren_text = image_text.substring(image_text.find("(") + 1, image_text.find(")"))
    tag_type = TEXT_TYPE_IMAGE if(image_text.startswith("!")) else TEXT_TYPE_LINK

    return TextNode(bracket_text, tag_type, paren_text)


def split_nodes_by_delimitter(old_nodes, delimitter):
    new_nodes = []
    
    for old_node in old_nodes:
        if(old_node.text != None and delimitter in old_node.text):
            # Only need one of the blockquote delimitter for the blockquote to be valid.
            if((delimitter == MARKDOWN_BLOCKQUOTE) or (old_node.text.count(delimitter) > 1)):        
                delim_first = False
                text_segments = old_node.text.split(delimitter)

                # Then the matched tag starts with the first array element.
                if(old_node.text.startswith(delimitter)):
                    delim_first = True

                # The order that the delimitters are checked will matter. Check larger ones first. e.g. ###### before ##### (h6 before h5).
                for x in range(0, len(text_segments)):
                    if(x % 2 == 0):
                        if(delim_first):
                            if(any(MARKDOWN_DELIMS, text_segments[x])):
                            # May need to make a helper that checks which delim is next and trim that off, then continue with the next.
                            # Something like get_next_delim which takes text, and finds the next closest delims by using find. Lowest index is the next delim.
                            new_nodes.append(TextNode(text_segments[x], markdown_delim_to_text_type(delimitter)))
                        else:
                            new_nodes.append(TextNode(text_segments[x], TEXT_TYPE_TEXT))
                    else:
                        if(not delim_first):
                            new_nodes.append(TextNode(text_segments[x], markdown_delim_to_text_type(delimitter)))
                        else:
                            new_nodes.append(TextNode(text_segments[x], TEXT_TYPE_TEXT))
    
    return new_nodes

                