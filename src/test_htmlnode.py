import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_same(self):
        node = HTMLNode("<h1>", "abc", "<p>")
        self.assertEqual((node.tag, node.value, node.children), ("<h1>", "abc", "<p>"))

    def test_props_diff(self):
        node = HTMLNode("<a>", "Google", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"') # See how to use props_to_html again, with actual properties.

class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError)
                         
    def test_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")
        
    def test_whole_node(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me.", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), '<p>This is a paragraph of text.</p>')
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me.</a>')
    
class TestParentNode(unittest.TestCase):
    def parent_in_parent(self):
        node = ParentNode(
            "h1",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Normal text"),
                    ])
            ]
        )
        self.assertEqual(node.to_html(), "<h1><p>Normal text</p></h1>")

    def multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>Italic text</i></p>")
    
    def no_children(self):
        node = ParentNode(
            "p",
            None
        )
        self.assertRaises(ValueError)
        
        
if __name__ == "__main__":
    unittest.main()
