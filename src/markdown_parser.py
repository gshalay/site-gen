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

def filter_duplicate_asterisks(italic_list, bold_list):
    unique_italics = []

    for italic_pos in italic_list:
        if(not (italic_pos in bold_list) and not (italic_pos - 1 in italic_list)):
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
                    delim_idxs[delim] = filtered_italics

            else:
                delim_idxs[delim] = delim_positions
    
    # print("Found Delims")
    # for delim, foundIdxs in delim_idxs.items():
    #     print(f"delim {delim} found at idxs: {foundIdxs}")
    
    return delim_idxs

def split_nodes_delimitter(old_nodes, delimitter, text_type):
    new_nodes = []

    if(bool(delimitter) and bool(text_type)):
        for old_node in old_nodes:
            if(bool(old_node.text)):
                delim_poses = dict(sorted(get_delim_postitions(old_node.text).items(), key=lambda item: item[1][0]))

                if(delim_poses != None and len(delim_poses) > 0):
                    is_delim_segment = delim_poses.get(0)[0] == 0
                    last_upper = -1
                    for delim, idxs in delim_poses.items():
                        lower = idxs[0] if(last_upper == -1) else last_upper
                        upper = 

                        if(last_upper != -1): 
                            if(is_delim_segment):
                                segment = old_node.text[idxs[0] - 1:idxs[1]]
                                last_upper = idxs[1]

                    new_nodes.append(TextNode(, markdown_delim_to_text_type(delim)))
                    

                text_segments = old_node.text.split(delimitter)
                delim_proc = len(text_segments) % 2 == 0 or not bool(text_segments[0])

                for segment in text_segments:
                    if(bool(segment)):
                        found_delims = [dlm for dlm in MARKDOWN_DELIMS.values() if dlm in segment]

                        if(len(found_delims) > 0):
                            for currentDlm in found_delims:
                                new_text_type = markdown_delim_to_text_type(currentDlm)
                                new_nodes += split_nodes_delimitter([TextNode(segment, new_text_type)], currentDlm, new_text_type)
                                break
                        else:
                            if(delim_proc):
                                new_nodes.append(TextNode(segment, text_type))
                                delim_proc = False
                            else:
                                new_nodes.append(TextNode(segment, TEXT_TYPE_TEXT))
                                delim_proc = True

    return new_nodes

# def split_nodes_by_delimitter(old_nodes):
#     new_nodes = []
    
#     for old_node in old_nodes:
#         if(old_node.text != None):
#             text_segments = old_node.text.split()

#             # res = get_delim_postitions(old_node.text)
#             # print(f"delims_poses - {res}")
#             for delim in MARKDOWN_DELIMS.values():
#                 if(old_node.text != None and delim in old_node.text 
#                    and ((delim == MARKDOWN_BLOCKQUOTE) or (old_node.text.count(delim) > 1))):
#                     # Only need one of the blockquote delimitter for the blockquote to be valid.       
#                     delim_first = False
#                     text_segments = old_node.text.split(delim)

#                     # Then the matched tag starts with the first array element.
#                     if(old_node.text.startswith(delim)):
#                         delim_first = True
                    
#                     # The order that the delimitters are checked will matter. Check larger ones first. e.g. ###### before ##### (h6 before h5).
#                     for x in range(0, len(text_segments)):
#                         if(x % 2 == 0):
#                             if(delim_first):
#                                 if(text_segments[x].contains(any(MARKDOWN_DELIMS.values()))):
#                                     new_nodes += split_nodes_by_delimitter(new_nodes)
#                                 else:
#                                     new_nodes.append(TextNode(text_segments[x], markdown_delim_to_text_type(delim)))
#                             else:
#                                 new_nodes.append(TextNode(text_segments[x], TEXT_TYPE_TEXT))
#                         else:
#                             if(not delim_first):
#                                 if(text_segments[x].contains(any(MARKDOWN_DELIMS.values()))):
#                                     new_nodes += split_nodes_by_delimitter(new_nodes)
#                                 else:
#                                     new_nodes.append(TextNode(text_segments[x], markdown_delim_to_text_type(delim)))
#                             else:
#                                 new_nodes.append(TextNode(text_segments[x], TEXT_TYPE_TEXT))

#     return new_nodes


# node = TextNode("This is a text node with a `code block` word", TEXT_TYPE_TEXT)
# # node2 = TextNode("**There once was a man from Peru *He slipped and fell one day and lost his shoe* `which made him quite blue`, now a man with one shoe**", TEXT_TYPE_BOLD)
# # node3 = TextNode("There once was a man from Tahiti > He climbed a cliff and watched the sunset. *Then came night `then midnight` then dawn `then morning once more`* C'est Fini.", MARKDOWN_BLOCKQUOTE)

# print(f"res - {split_nodes_delimitter([node], MARKDOWN_CODE, TEXT_TYPE_CODE)}")