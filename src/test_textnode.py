import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()
