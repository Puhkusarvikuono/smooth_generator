import unittest

from textnode import TextNode, TextType, text_node_to_html_node

from htmlnode import HTMLNode,LeafNode

from text_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_only_text(self):
        node = TextNode(
            "No images here, only plain text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("No images here, only plain text.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_links_multiple_adjacent(self):
        node = TextNode(
            "[one](https://a.com)[two](https://b.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://a.com"),
                TextNode("two", TextType.LINK, "https://b.com"),
            ],
            new_nodes,
        )

    def test_split_links_single_middle(self):
        node = TextNode(
            "Start [link](https://example.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_two_links_with_trailing_text(self):
        node = TextNode(
            "A [one](https://a.com) B [two](https://b.com) C",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://a.com"),
                TextNode(" B ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://b.com"),
                TextNode(" C", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_entire_string_is_link(self):
        node = TextNode(
            "[only](https://only.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only", TextType.LINK, "https://only.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links_returns_same_text(self):
        node = TextNode(
            "No links here at all.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("No links here at all.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_ignores_non_text_nodes(self):
        text_node = TextNode(
            "Check [this](https://example.com)",
            TextType.TEXT,
        )
        img_node = TextNode(
            "alt",
            TextType.IMAGE,
            "https://img.com/pic.png",
        )
        new_nodes = split_nodes_link([text_node, img_node])
        # Last node should still be the image node unchanged
        self.assertEqual(new_nodes[-1], img_node)

    def test_split_links_with_monster(self):
        node = TextNode(
            "A [one](1) B [two](2) C",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("one", TextType.LINK, "1"),
                TextNode(" B ", TextType.TEXT),
                TextNode("two", TextType.LINK, "2"),
                TextNode(" C", TextType.TEXT),
            ], 
            new_nodes,
        )
