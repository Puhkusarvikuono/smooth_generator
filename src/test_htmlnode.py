import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode()
        node1 = HTMLNode("p")
        node2 = HTMLNode("p", "This is the text inside the paragraph")
        node3 = HTMLNode("p", "This is the text inside the paragraph", node)
        node4 = HTMLNode("p", "This is the text inside the paragraph", node, {"href": "https://www.google.com", "target": "_blank"})
        print(node)
        print(node2)
        print(node3)
        print(node4)
        self.assertNotEqual(node, node4)

    def test_props_to_html(self):
        test = True
        node = HTMLNode("p", "This is the text inside the paragraph")
        node1 = HTMLNode("p", "This is the text inside the paragraph", node, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "This is the text inside the paragraph", node, "not a valid dictionary")
        print(node.props_to_html())
        print(node1.props_to_html())
        print(node2.props_to_html())
        self.assertNotEqual(node1, node2)
        


    def test_to_html(self):
        node = HTMLNode("p", "This is the text inside the paragraph", None, {"href": "https://www.google.com"})
        try:
            node.to_html()
            print("No error.")
            return
        except NotImplementedError as e:
            print(e)
            return 

if __name__ == "__main__":
    unittest.main()

