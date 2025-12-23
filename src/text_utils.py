import re

from textnode import TextNode, TextType, text_node_to_html_node

from htmlnode import HTMLNode,LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiter_list = []

    for old_node in old_nodes:
        text_to_delimiter = old_node.text
        if old_node.text_type != TextType.TEXT or delimiter == "" or delimiter is None or old_node.text.count(delimiter) == 0:
            delimiter_list.extend([old_node])
        else:
            if old_node.text.count(delimiter) % 2 != 0:
                raise Exception("Invalid Markdown syntax, closing delimiter not found")
            text_split = text_to_delimiter.split(delimiter)
            text_node_start = TextNode(text_split[0], TextType.TEXT)
            text_node_end = TextNode(text_split[-1], TextType.TEXT)
            if text_node_start.text != "":
                delimiter_list.extend([text_node_start])
            for i in range(1, len(text_split) -1):
                if i == 1:
                    delimiter_list.extend([TextNode(text_split[i], text_type)])
                elif i % 2 == 0:
                    if text_split[i] != "":
                        delimiter_list.extend([TextNode(text_split[i], TextType.TEXT)])
                else:
                    match_node = TextNode(text_split[i], text_type)
                    if match_node.text != "":
                        delimiter_list.extend([match_node])
            if text_node_end.text != "":
                delimiter_list.extend([text_node_end])
    return delimiter_list


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_to_nodes = node.text
        link_matches = extract_markdown_images(text_to_nodes)
        if link_matches == [] and text_to_nodes != "":
            new_nodes.append(TextNode(text_to_nodes, TextType.TEXT))
        else:
            for match in link_matches:
                alt_text = match[0]
                image_link = match[1]
                sections = text_to_nodes.split(f"![{alt_text}]({image_link})", maxsplit=1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                text_to_nodes = sections[1]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_link))
            if text_to_nodes != "":
                new_nodes.append(TextNode(text_to_nodes, TextType.TEXT))
                
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_to_nodes = node.text
        link_matches = extract_markdown_links(text_to_nodes)
        if link_matches == [] and text_to_nodes != "":
            new_nodes.append(TextNode(text_to_nodes, TextType.TEXT))
        else:
            for match in link_matches:
                anchor_text = match[0]
                link_url = match[1]
                sections = text_to_nodes.split(f"[{anchor_text}]({link_url})", maxsplit=1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                text_to_nodes = sections[1]
                new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))
            if text_to_nodes != "":
                new_nodes.append(TextNode(text_to_nodes, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes_b = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes_bu = split_nodes_delimiter(new_nodes_b, "_", TextType.ITALIC)
    new_nodes_buc = split_nodes_delimiter(new_nodes_bu, "`", TextType.CODE)
    new_nodes_bucl = split_nodes_link(new_nodes_buc)
    new_nodes_bucli = split_nodes_image(new_nodes_bucl)
    return new_nodes_bucli




