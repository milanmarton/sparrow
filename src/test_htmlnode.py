import unittest
from htmlnode import (HTMLNode, LeafNode, ParentNode)

class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode("p", "this is a html node", None,\
                {"href": "https://www.google.com", "target": "_blank"})
        # python uses '' as the default string representation
        node_as_str = "HTMLNode(p, this is a html node, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node_as_str, repr(node))

    def test_props_to_html(self):
        props1 = {"href": "https://www.google.com", "target": "_blank"}
        props2 = {"href": "https://www.kagi.com", "target": "_blank"}
        node1 = HTMLNode(None, None, None, props1)
        node2 = HTMLNode(None, None, None, props2)
        props_to_str_1 = ' href="https://www.google.com" target="_blank"'
        props_to_str_2 = ' href="https://www.kagi.com" target="_blank"'

        self.assertEqual(
            props_to_str_1, node1.props_to_html()
        )
        self.assertEqual(
            props_to_str_2, node2.props_to_html()
        )

class TestLeafNode(unittest.TestCase):
    def test_render(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html_rendered1 = '<p>This is a paragraph of text.</p>'
        html_rendered2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(
            html_rendered1, node1.to_html()
        )
        self.assertEqual(
            html_rendered2, node2.to_html()
        )

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
        html_rendered = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

        self.assertEqual(
            html_rendered, node.to_html()
        )

    def test_nested_parent_nodes(self):
        child1 = LeafNode("span", "Child 1")
        child2 = LeafNode("span", "Child 2")
        inner_parent = ParentNode("div", [child1, child2], {"class": "inner-parent"})

        child3 = LeafNode("p", "Outer child 1")
        outer_parent = ParentNode("section", [inner_parent, child3], {"class": "outer-parent"})

        html_rendered = '<section class="outer-parent"><div class="inner-parent"><span>Child 1</span><span>Child 2</span></div><p>Outer child 1</p></section>'
        self.assertEqual(html_rendered, outer_parent.to_html())

    def test_deeply_nested_parent_nodes(self):
        child1 = LeafNode("span", "Child 1")
        child2 = LeafNode("span", "Child 2")
        inner_parent1 = ParentNode("div", [child1, child2], {"class": "inner-parent-1"})

        child3 = LeafNode("span", "Child 3")
        child4 = LeafNode("span", "Child 4")
        inner_parent2 = ParentNode("div", [child3, child4], {"class": "inner-parent-2"})

        middle_parent = ParentNode("article", [inner_parent1, inner_parent2], {"class": "middle-parent"})

        outer_child = LeafNode("p", "Outer child")
        outer_parent = ParentNode("section", [middle_parent, outer_child], {"class": "outer-parent"})

        html_rendered = (
            '<section class="outer-parent">'
            '<article class="middle-parent">'
            '<div class="inner-parent-1"><span>Child 1</span><span>Child 2</span></div>'
            '<div class="inner-parent-2"><span>Child 3</span><span>Child 4</span></div>'
            '</article>'
            '<p>Outer child</p>'
            '</section>'
        )
        self.assertEqual(html_rendered, outer_parent.to_html())

if __name__ == "__main__":
    unittest.main()
