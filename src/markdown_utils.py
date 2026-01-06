import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_split = markdown.split("\n\n")
    blocks = []
    for item in new_split:
        lines = item.strip().split("\n")
        if lines == "":
            continue
        new_lines = []
        for line in lines:
            sline = line.strip()
            if line != "":
                new_lines.append(sline)
        new_item = "\n".join(new_lines)
        if new_item != "":
            blocks.append(new_item)
        
    return blocks

def block_to_block_type(markdown):
    if markdown.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    lines = markdown.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    pattern = r'^\d+\.'
    if all(re.match(pattern, line) for line in lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH



def markdown_block_strip_header(markdown):
    if markdown.startswith(("#", "##", "###", "####", "#####", "######")):
        header_counter = 0
        for char in markdown:
            if char == "#":
                header_counter += 1
            else:
                break
        return markdown.lstrip("# "), header_counter
    return markdown, 0

def markdown_block_strip_code_tag(markdown):
    stripped_markdown = markdown.strip("```")
    stripped_markdown = stripped_markdown.lstrip("\n")
    return stripped_markdown

def markdown_block_strip_quote_tag(markdown):
    lines = markdown.split("\n")
    if all(line.startswith(">") for line in lines):
        new_lines = []
        for line in lines:
            new_line = line.lstrip("> ")
            new_lines.append(new_line)
        return " ".join(new_lines)
    return markdown

def markdown_block_strip_paragraph(markdown):
    lines = markdown.split("\n")
    return " ".join(lines)


def markdown_block_unordered_list_to_html_tags(markdown):
    lines = markdown.split("\n")
    new_lines = []
    for line in lines:
        new_line = line.lstrip("- ")
        new_lines.append(f"<li>{new_line}</li>")
    return "".join(new_lines)

def markdown_block_ordered_list_to_html_tags(markdown):
    lines = markdown.split("\n")
    new_lines = []
    for line in lines:
        new_line = line.lstrip('0123456789. ')
        new_lines.append(f"<li>{new_line}</li>")
    return "".join(new_lines)

def block_type_to_html_node(block_text, block_type):
    if block_type not in BlockType:
        raise ValueError("invalid block type")

    match block_type:
        case BlockType.PARAGRAPH:
            stripped_text = markdown_block_strip_paragraph(block_text)
            nodes = text_to_children(stripped_text)
            tag = "p"
        case BlockType.HEADING:
            stripped_text, header_counter = markdown_block_strip_header(block_text)
            nodes = text_to_children(stripped_text)
            tag = f"h{header_counter}"
        case BlockType.QUOTE:
            stripped_text = markdown_block_strip_quote_tag(block_text)
            nodes = text_to_children(stripped_text)
            tag = "blockquote"
        case BlockType.UNORDERED_LIST:
            tagged_text = markdown_block_unordered_list_to_html_tags(block_text)
            nodes = text_to_children(tagged_text)
            tag = "ul"
        case BlockType.ORDERED_LIST:
            tagged_text = markdown_block_ordered_list_to_html_tags(block_text)
            nodes = text_to_children(tagged_text)
            tag = "ol"
        case BlockType.CODE:
            stripped_text = markdown_block_strip_code_tag(block_text)
            nodes = [LeafNode(tag="code", value=stripped_text)]
            tag = "pre"
    return ParentNode(tag=tag, children=nodes)


def text_to_children(text):
    if text == "":
        return []
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        new_html_node = text_node_to_html_node(node)
        html_nodes.append(new_html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_parent = block_type_to_html_node(block, block_type)
        parent_nodes.append(html_parent)
    return ParentNode(tag="div", children=parent_nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            title, header_counter = markdown_block_strip_header(block)
            if header_counter == 1:
                if title.strip() == "":
                    raise Exception("Empty title")
                return title
    raise Exception("Title not found")



