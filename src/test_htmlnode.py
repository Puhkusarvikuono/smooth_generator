import unittest

from htmlnode import HTMLNode,LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_requires_value_or_children(self):
        with self.assertRaises(ValueError):
            HTMLNode(tag="p", value=None, children=None)

    def test_props_normalized_to_empty_dict(self):
        n1 = HTMLNode("p", "hi", props=None)
        n2 = HTMLNode("p", "hi", props={})
        self.assertEqual(n1.props, {})
        self.assertEqual(n2.props, {})

    def test_props_to_html_not_equal(self):
        node = HTMLNode("p", "This is the text inside the paragraph")
        node2 = HTMLNode("p", "This is the text inside the paragraph", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_to_html_notimplemented(self):
        node = HTMLNode(tag="p", value="This is a paragraph")
        with self.assertRaises(NotImplementedError):
            node.to_html()
   
    def test_tag_must_be_str_or_none(self):
        with self.assertRaises(TypeError):
            HTMLNode(tag=123, value="x")

    def test_value_must_be_str_or_none(self):
        with self.assertRaises(TypeError):
            HTMLNode(tag="p", value=object())

    def test_children_must_be_list_of_htmlnode(self):
        with self.assertRaises(TypeError):
            HTMLNode(tag="p", children="not a list")
        with self.assertRaises(TypeError):
            HTMLNode(tag="p", children=[HTMLNode("span", "x"), "bad"])

    def test_props_normalized(self):
        self.assertEqual(HTMLNode("p", "x", props=None).props, {})
        self.assertEqual(HTMLNode("p", "x", props={}).props, {})

    def test_props_must_be_dict(self):
        with self.assertRaises(TypeError):
            HTMLNode("p", "x", props=42)

    def test_require_exactly_one_of_value_or_children(self):
        with self.assertRaises(ValueError):
            HTMLNode("p", value=None, children=None)
        with self.assertRaises(ValueError):
            HTMLNode("p", value="x", children=[HTMLNode("span", "y")])

    def test_props_to_html_formats(self):
        n = HTMLNode("a", "x", props={"href": "https://x", "target": "_blank"})
        s = n.props_to_html()
        self.assertIn(' href="https://x"', s)
        self.assertIn(' target="_blank"', s)

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_raw_text_renders_value_only(self):
        node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_tag_with_single_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_tag_with_multiple_prop(self):
        node = LeafNode("a", "Docs", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Docs</a>')

    def test_leaf_to_html_raises_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            LeafNode(None, None)

    def test_leaf_rejects_non_string_value(self):
        with self.assertRaises(TypeError):
            LeafNode(tag="p", value=123)
        with self.assertRaises(TypeError):
            LeafNode(tag="p", value=True)

if __name__ == "__main__":
    unittest.main()

