import unittest

from textnode import TextNode, TextType, text_node_to_html_node

from htmlnode import HTMLNode,LeafNode



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://bogie.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://bogie.com")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_noteq_2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is something else", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_noteq_with_url(self):
        node = TextNode("This is an image node", TextType.ITALIC, "https://www.thisisnotmysite.com")
        node2 = TextNode("This is an image node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

class TestTextNodeToHtml(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
 
    def test_invalid_text_type_raises(self):
        class FakeType:
            pass

        fake_type = FakeType()
        with self.assertRaises(ValueError):
            TextNode("This is a text node", fake_type)
    
    def test_text_type_text(self):
        node = TextNode("plain text", TextType.TEXT)
        html = text_node_to_html_node(node)
        self.assertIsNone(html.tag)
        self.assertEqual(html.value, "plain text")
     
        self.assertEqual(html.props, {})

    def test_text_type_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "bold text")
        self.assertEqual(html.props, {})

    def test_text_type_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "italic text")
        self.assertEqual(html.props, {})

    def test_text_type_code(self):
        node = TextNode("code text", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "code text")
        self.assertEqual(html.props, {})

    def test_text_type_link(self):
        node = TextNode("click me", TextType.LINK, "https://example.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "click me")
        self.assertEqual(html.props, {"href": "https://example.com"})

    def test_text_type_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(
            html.props,
            {
                "src": "https://example.com/image.png",
                "alt": "alt text",
            },
        )


if __name__ == "__main__":
    unittest.main()
