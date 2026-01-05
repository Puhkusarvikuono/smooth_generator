import unittest

from markdown_utils import (
    markdown_to_blocks, 
    block_to_block_type, 
    BlockType, 
    markdown_block_strip_header, 
    markdown_block_strip_code_tag, 
    markdown_block_strip_quote_tag,
    markdown_block_unordered_list_to_html_tags, 
    markdown_block_ordered_list_to_html_tags,
    text_to_children,
    markdown_to_html_node,
)
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class TestMarkDownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
```
Code.
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "```\nCode.\n```"
            ],
        )


    def test_markdown_to_blocks_extra_empty_blocks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_paragraph(self):
        md = """
This is **bolded** paragraph.
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
#This is a header
"""

        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

class TestBlockStrips(unittest.TestCase):

    def test_block_strip_header(self):
        md = """
###This is header paragraph with 3 hashtags.
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            if block != "\n":
                stripped_text, header_count = markdown_block_strip_header(block)
                self.assertEqual(stripped_text, "This is header paragraph with 3 hashtags.")
                self.assertEqual(header_count, 3)

    def test_block_strip_code(self):
        md = """
```
This is four lines of code.
Another paragraph of code.
Third paragraph of code.
Last line of code.
```
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            if block != "\n":
                stripped_text = markdown_block_strip_code_tag(block)
                self.assertEqual(stripped_text, "This is four lines of code.\nAnother paragraph of code.\nThird paragraph of code.\nLast line of code.\n")
    
    def test_block_strip_quote(self):
        md = """
>Some quotes.
>In separate lines.
>Third line.
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            if block != "\n":
                stripped_text = markdown_block_strip_quote_tag(block)
                self.assertEqual(stripped_text, "Some quotes. In separate lines. Third line.")
 
    def test_block_unordered_list_to_html_tags(self):
        md = """
- Unordered list item one.
- Item two.
- Item three.
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            if block != "\n":
                stripped_text = markdown_block_unordered_list_to_html_tags(block)
                self.assertEqual(stripped_text, "<li>Unordered list item one.</li><li>Item two.</li><li>Item three.</li>")

    def test_block_ordered_list_to_html_tags(self):
        md = """
1. Ordered list item one.
2. Item two.
3. Item three.
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            if block != "\n":
                stripped_text = markdown_block_ordered_list_to_html_tags(block)
                self.assertEqual(stripped_text, "<li>Ordered list item one.</li><li>Item two.</li><li>Item three.</li>")

class TestTextToHTMLNodes(unittest.TestCase):

    def test_text_to_children(self):
        text = "Test."
        html_nodes = text_to_children(text)
        self.assertEqual(html_nodes[0].value, text)

    def test_text_to_children_more_complicated(self):
        text = "Test. And something **bold**."
        html_nodes = text_to_children(text)
        self.assertEqual(html_nodes[1].value, "bold")
        self.assertEqual(html_nodes[1].tag, "b")

class TestMarkDownToHTMLNodes(unittest.TestCase):

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


        def test_unordered_list(self):
            md = """
        - First item
        - Second item
        - Third item
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
            )

    def test_unordered_list(self):
        md = """
    - First item
    - Second item
    - Third item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. First step
    2. Second step
    3. Third step
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First step</li><li>Second step</li><li>Third step</li></ol></div>",
        )

    def test_list_with_inline_markdown(self):
        md = """
    - This item has **bold** text
    - This one has _italic_ text
    - And this has `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This item has <b>bold</b> text</li><li>This one has <i>italic</i> text</li><li>And this has <code>code</code></li></ul></div>",
        )
