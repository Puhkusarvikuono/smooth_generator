import re

from textnode import TextNode, TextType, text_node_to_html_node

from htmlnode import HTMLNode,LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiter_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or delimiter == "" or delimiter is None:
            delimiter_list.extend([old_node])
        else:
            if old_node.text.count(delimiter) % 2 != 0:
                raise Exception("Invalid Markdown syntax, closing delimiter not found")
            old_node_split = old_node.text.split(delimiter)
            text_node_start = TextNode(old_node_split[0], TextType.TEXT)
            text_nodes = []
            for i in range(1, len(old_node_split) -1):
                text_nodes.extend([TextNode(old_node_split[i], text_type)])
            text_node_end = TextNode(old_node_split[-1], TextType.TEXT)

            delimiter_list.extend([text_node_start])
            delimiter_list.extend(text_nodes)
            delimiter_list.extend([text_node_end])

    return delimiter_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

