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

if __name__ == "__main__":
    unittest.main()
