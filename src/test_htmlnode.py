import unittest
import htmlnode

class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = htmlnode.HTMLNode("p", "this is a html node", None,\
                {"href": "https://www.google.com", "target": "_blank"})
        # python uses '' as the default string representation
        node_as_str = "HTMLNode(p, this is a html node, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node_as_str, repr(node))

    def test_props_to_html(self):
        props1 = {"href": "https://www.google.com", "target": "_blank"}
        props2 = {"href": "https://www.kagi.com", "target": "_blank"}
        node1 = htmlnode.HTMLNode(None, None, None, props1)
        node2 = htmlnode.HTMLNode(None, None, None, props2)
        props_to_str_1 = ' href="https://www.google.com" target="_blank"'
        props_to_str_2 = ' href="https://www.kagi.com" target="_blank"'

        self.assertEqual(
            props_to_str_1, node1.props_to_html()
        )
        self.assertEqual(
            props_to_str_2, node2.props_to_html()
        )

class TestLeafNode(unittest.TestCase):
    def test_constructor_error(self):
        with self.assertRaises(ValueError):
            node = htmlnode.LeafNode("p")

    def test_render(self):
        node1 = htmlnode.LeafNode("p", "This is a paragraph of text.")
        node2 = htmlnode.LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html_rendered1 = '<p>This is a paragraph of text.</p>'
        html_rendered2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(
            html_rendered1, node1.to_html()
        )
        self.assertEqual(
            html_rendered2, node2.to_html()
        )

if __name__ == "__main__":
    unittest.main()
