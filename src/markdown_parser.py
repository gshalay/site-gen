from constants import *
from leafnode import LeafNode
from textnode import TextNode
import itertools as it
import collections as ct
import more_itertools as mit
import re

def text_node_to_leaf_node(text_node):
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
    elif(delim == MARKDOWN_H1):
        return TEXT_TYPE_H1
    elif(delim == MARKDOWN_H2):
        return TEXT_TYPE_H2
    elif(delim == MARKDOWN_H3):
        return TEXT_TYPE_H3
    elif(delim == MARKDOWN_H4):
        return TEXT_TYPE_H4
    elif(delim == MARKDOWN_H5):
        return TEXT_TYPE_H5
    elif(delim == MARKDOWN_H6):
        return TEXT_TYPE_H6
    elif(delim == TEXT_TYPE_TEXT):
        return TEXT_TYPE_TEXT
    else:
        raise ValueError(f"Unknown markdown delimitter '{delim}'.")

def image_or_link_to_textnode(image_text, is_link=True):
    tag_type = TEXT_TYPE_IMAGE if(image_text.startswith("!")) else TEXT_TYPE_LINK
    prefix = ("" if(is_link) else "\!") + "["
    bracket_text = image_text[image_text.find(prefix) + len(prefix):image_text.find("]")]
    paren_text = image_text[image_text.find("(") + 1:image_text.find(")")]

    return TextNode(bracket_text, tag_type, paren_text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if(old_node.text):
            splits = re.split("(" + ("\!" + MARKDOWN_IMAGE_OR_LINK) + ")", old_node.text)
            proc_image = bool((len(splits) > 0 and splits[0] and re.search("\!" + MARKDOWN_IMAGE_OR_LINK, splits[0]) != None))

            for split in splits:
                if(split):
                    if(re.search("\!" + MARKDOWN_IMAGE_OR_LINK, split) != None and proc_image):
                        new_nodes.append(image_or_link_to_textnode(split, False))
                    else:
                        new_nodes.append(TextNode(split, TEXT_TYPE_TEXT))

                proc_image = not proc_image      

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if(old_node.text):
            splits = re.split("((?<!\!)" + MARKDOWN_IMAGE_OR_LINK + ")", old_node.text)
            proc_image = bool(len(splits) > 0 and splits[0] and re.search("((?<!\!)" + MARKDOWN_IMAGE_OR_LINK + ")", splits[0]) != None)

            for split in splits:
                if(split):
                    if(re.search("(?<!\!)" + MARKDOWN_IMAGE_OR_LINK, split) != None and proc_image):
                        new_nodes.append(image_or_link_to_textnode(split))
                    else:
                        new_nodes.append(TextNode(split, TEXT_TYPE_TEXT))

                proc_image = not proc_image        

    return new_nodes


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
                            if(len(pos_pair) > 1):
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
    image_matches = re.findall("\!" + MARKDOWN_IMAGE_OR_LINK, text)

    for match in image_matches:
        alt_text = match[int(match.index("[")) + 1 : int(match.index("]"))]
        url_text = match[int(match.index("(")) + 1 : int(match.index(")"))]
        image_tuples.append(tuple([alt_text, url_text]))

    return image_tuples

def extract_markdown_links(text):
    # Return a list of tuples (anchor text, url)
    link_tuples = []

    if(re.search("!" + MARKDOWN_IMAGE_OR_LINK, text) == None):
        link_matches = re.findall(MARKDOWN_IMAGE_OR_LINK, text)

        for match in link_matches:
            anchor_text = match[int(match.index("[")) + 1 : int(match.index("]"))]
            url_text = match[int(match.index("(")) + 1 : int(match.index(")"))]
            link_tuples.append(tuple([anchor_text, url_text]))

    return link_tuples

def insert_items_at_idx(master_list, list_to_insert, insert_idx):
    master_copy = master_list.copy()

    if(not bool(list_to_insert)):
        return list_to_insert

    current_insert_idx = insert_idx
    
    for insert_item in list_to_insert:
        master_copy.insert(current_insert_idx, insert_item)
        current_insert_idx += 1
    
    return master_copy

def text_to_textnodes(text):
    first_inline_delim = list(get_delim_postitions(text).keys())
    input_node = [TextNode(text, TEXT_TYPE_TEXT)]
    new_nodes = []

    if(len(first_inline_delim) > 0 ):
        text_type = markdown_delim_to_text_type(first_inline_delim[0])

        if(first_inline_delim[0] in MARKDOWN_HEADINGS):
            new_nodes = [TextNode(text[len(first_inline_delim[0]):], text_type)]
        else:
            new_nodes = split_nodes_delimitter(input_node, first_inline_delim[0], text_type)
    else:
        new_nodes = input_node

    upper_bound = len(new_nodes)
    node_idx = 0

    while(node_idx < upper_bound):
        if(re.search("!" + MARKDOWN_IMAGE_OR_LINK, new_nodes[node_idx].text) != None):
            popped_node = new_nodes.pop(node_idx)
            new_nodes = insert_items_at_idx(new_nodes, split_nodes_image([popped_node]), node_idx)
            
            if(node_idx > 0):
                node_idx = node_idx - 1
            
            upper_bound = len(new_nodes)

        if(re.search(MARKDOWN_IMAGE_OR_LINK, new_nodes[node_idx].text) != None):
            popped_node = new_nodes.pop(node_idx)
            new_nodes = insert_items_at_idx(new_nodes, split_nodes_link([popped_node]), node_idx)
            
            if(node_idx > 0):
                node_idx = node_idx - 1
            
            upper_bound = len(new_nodes)
        
        node_idx += 1

    return new_nodes

def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    valid_blocks = []

    for block in markdown_blocks:
        block = block.strip()
        
        if(block):
            valid_blocks.append(block)
    
    return valid_blocks

def starts_with_heading(text):
    for heading_type in MARKDOWN_HEADINGS:
        if(text.startswith(heading_type)):
            return True
    
    return False

def is_quote_block(text):
    if(text):
        splits = text.split("\n")

        for split in splits:
            if(not split.startswith(MARKDOWN_BLOCKQUOTE)):
                return False
        
        return True
    
    return False

def is_unordered_list_block(text):
    if(text):
        splits = text.split("\n")

        for split in splits:
            if(not split.startswith(MARKDOWN_UL_PREFIX_1) and not split.startswith(MARKDOWN_UL_PREFIX_2)):
                return False
        
        return True
    
    return False

def is_ordered_list_block(text):
    if(text):
        splits = text.split("\n")
        expected_num = 1

        for split in splits:
            if("." in split and re.search(MARKDOWN_OL_PREFIX, text) != None):
                inner_splits = split.split(".")

                if(inner_splits[0] and inner_splits[0] == str(expected_num)):
                    expected_num += 1
                    
                else: 
                    return False
            else:
                return False
            
        return True
    
    return False

def block_to_block_type(markdown_block):
    if(starts_with_heading(markdown_block)):
        return BLOCK_TYPE_HEADING
    elif(markdown_block.startswith(BLOCK_CODE) and markdown_block.endswith(BLOCK_CODE)):
        return BLOCK_TYPE_CODE
    elif(is_quote_block(markdown_block)):
        return BLOCK_TYPE_QUOTE
    elif(is_unordered_list_block(markdown_block)):
        return BLOCK_TYPE_UL
    elif(is_ordered_list_block(markdown_block)):
        return BLOCK_TYPE_OL
    else:
        return BLOCK_TYPE_PARAGRAPH

def paragraph_block_to_html_node(block):
        raise NotImplementedError

def code_block_to_html_node(block):
        raise NotImplementedError
    
def quote_block_to_html_node(block):
        raise NotImplementedError

def ordered_list_block_to_html_node(block):
        raise NotImplementedError

def unordered_list_block_to_html_node(block):
        raise NotImplementedError

def heading_block_to_html_node(block):
    heading_prefix = block.split(" ")[0] + " "
    heading_type = None

    for key, value in MARKDOWN_DELIMS.items():
        if(value == heading_prefix):
            heading_type = key
            heading_value = block[heading_prefix + 1:]
            
            

            return LeafNode(heading_type, heading_value)
    
    return None
    
    # find inline nodes until none exist. Parents should be ParentNodes, child nodes with no children should be LeafNodes.

def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    parent_html_node = None

    text_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        # Text to TextNodes
        text_nodes.append(text_to_textnodes(block))


    print("Hang on there partner.")


        # TextNodes to HtmlNodes
