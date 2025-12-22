import unittest

from textnode import TextNode, TextType, text_node_to_html_node

from htmlnode import HTMLNode,LeafNode

from text_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestDelimiter(unittest.TestCase):
    def test_multiple_code_segments(self):

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ], new_nodes)

    def test_no_delimiters(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.CODE)
        self.assertEqual([node], new_nodes)

    def test_leaves_non_text_nodes_unchanged(self):
        text_node = TextNode("Before `code` after", TextType.TEXT)
        bold_node = TextNode("already bold", TextType.BOLD)

        new_nodes = split_nodes_delimiter(
            [text_node, bold_node],
            "`",
            TextType.CODE,
        )

        self.assertEqual([
            TextNode("Before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.TEXT),
            bold_node,  # unchanged
        ], new_nodes)

    def test_raises_on_unmatched_delimiter(self):
        node = TextNode("This has `no end", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_italic_with_underscore(self):
        node = TextNode("This is _italic text_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ], new_nodes)


class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple_matches(self):

        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)



    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple_matches(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


