from constants import *
from leafnode import LeafNode
from textnode import TextNode
import itertools as it
import collections as ct
import more_itertools as mit
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
    elif(delim == MARKDOWN_ITALIC or delim == MARKDOWN_ITALIC2):
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

def in_collection(list_of_lists, search_item):
    for a_list in list_of_lists:
        if(search_item in a_list):
            return True
    
    return False
        

def filter_duplicate_asterisks(italic_lists, bold_lists):
    unique_italics = []
    flat_italic_list = list(it.chain(*italic_lists)) if(isinstance(italic_lists[0], list)) else italic_lists
    flat_bold_list = flat_italic_list = list(it.chain(*bold_lists)) if(isinstance(bold_lists[0], list)) else bold_lists

    for italic_pos in italic_lists:
        if(not (italic_pos in flat_bold_list) and not (italic_pos - 1 in flat_italic_list)):
            unique_italics.append(italic_pos)

    return unique_italics

def get_delim_postitions(text):
    delim_idxs = {}

    for delim in MARKDOWN_DELIMS.values():
        delim_cpy = re.escape(delim)
        delim_positions = [m.start() for m in re.finditer(delim_cpy, text)]

        if(delim_positions != None and delim_positions != []):
            if(delim == MARKDOWN_ITALIC and delim_idxs.get(MARKDOWN_BOLD) != None):
                filtered_italics = filter_duplicate_asterisks(delim_positions, delim_idxs[MARKDOWN_BOLD])
                if(filtered_italics != []):
                    delim_idxs[delim] = list(mit.chunked(filtered_italics, 2))

            else:
                delim_idxs[delim] = list(mit.chunked(delim_positions, 2))
    
    return delim_idxs

def get_min_delim_pos(dict_items):
    current_min = float('inf')
    for key, value in dict_items:
        for l in value:
            if(min(l) < current_min):
                current_min = min(l)
    
    return current_min

def split_nodes_delimitter(old_nodes, delimitter, text_type):
    new_nodes = []

    if(bool(delimitter) and bool(text_type)):
        for old_node in old_nodes:
            if(bool(old_node.text)):
                delim_poses = dict(sorted(get_delim_postitions(old_node.text).items(), key=lambda item: item[1][0]))

                if(delim_poses != None and len(delim_poses) > 0):
                    last_upper = -1

                    min_delim_pos = get_min_delim_pos(delim_poses.items())

                    if(min_delim_pos > 0):
                        new_nodes.append(TextNode(old_node.text[:min_delim_pos], TEXT_TYPE_TEXT))

                    for delim, idxs in delim_poses.items():
                        for pos_pair in idxs:
                            delim_offset = 2 if(delim == MARKDOWN_BOLD) else 1
                            if(last_upper != -1):
                                new_nodes.append(TextNode(old_node.text[last_upper:pos_pair[0]], TEXT_TYPE_TEXT))

                            new_nodes.append(TextNode(old_node.text[(pos_pair[0] + delim_offset):pos_pair[1]], markdown_delim_to_text_type(delim)))                            
                            last_upper = pos_pair[1] + delim_offset
                    
                    if(last_upper < len(old_node.text)):
                        new_nodes.append(TextNode(old_node.text[last_upper:], TEXT_TYPE_TEXT))

    return new_nodes

def extract_markdown_images(text):
    # Return a list of tuples (alt text, url)
    image_tuples = []
    image_matches = re.findall(MARKDOWN_IMAGE, text)

    for match in image_matches:
        alt_text = match.substring(match.find("[") + 1, match.find("]"))
        url_text = match.substring(match.find("(") + 1, match.find(")"))
        image_tuples.append(tuple(alt_text, url_text))

    return image_tuples

def extract_markdown_links(text):
    # Return a list of tuples (anchor text, url)
    link_tuples = []
    link_matches = re.findall(MARKDOWN_LINK, text)

    for match in link_matches:
        anchor_text = match.substring(match.find("[") + 1, match.find("]"))
        url_text = match.substring(match.find("(") + 1, match.find(")"))
        link_tuples.append(tuple(anchor_text, url_text))

    return link_tuples