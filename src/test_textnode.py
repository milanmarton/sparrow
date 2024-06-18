import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "kagi.com")
        node2 = TextNode(
            "This is a text node", text_type_italic, "kagi.com"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "kagi.com")
        self.assertEqual(
            "TextNode(This is a text node, text, kagi.com)", repr(node)
        )

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_single_italic_text(self):
        node = TextNode("This is *italic* text.", "text")
        expected_output = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text.", "text")
        ]
        result = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(result, expected_output)

    def test_no_delimiters(self):
        node = TextNode("This is plain text.", "text")
        expected_output = [node]
        result = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(result, expected_output)

    # def test_mixed_text(self):
    #     node = TextNode("This is *italic* and **bold** text.", "text")
    #     expected_output = [
    #         TextNode("This is ", "text"),
    #         TextNode("italic", "italic"),
    #         TextNode(" and **bold** text.", "text")
    #     ]
    #     result = split_nodes_delimiter([node], "*", "italic")
    #     self.assertEqual(result, expected_output)

    def test_multiple_italic_segments(self):
        node = TextNode("This is *italic1* and *italic2* text.", "text")
        expected_output = [
            TextNode("This is ", "text"),
            TextNode("italic1", "italic"),
            TextNode(" and ", "text"),
            TextNode("italic2", "italic"),
            TextNode(" text.", "text")
        ]
        result = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(result, expected_output)

    def test_invalid_syntax(self):
        node = TextNode("This is *italic text.", "text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", "italic")

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png) and another ![second image](https://example.com/second.png)",
            text_type_text,
        )
        expected_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/image.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://example.com/second.png"),
        ]

        result_nodes = split_nodes_image([node])

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)
            self.assertEqual(result_node.url, expected_node.url)

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is plain text without any images.", text_type_text)
        expected_nodes = [node]

        result_nodes = split_nodes_image([node])

        self.assertEqual(result_nodes, expected_nodes)

    def test_split_nodes_image_mixed_types(self):
        node1 = TextNode("This is text with an ![image](https://example.com/image.png)", text_type_text)
        node2 = TextNode("This is a bold node", text_type_link, "https://example.com")
        expected_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/image.png"),
            node2
        ]

        result_nodes = split_nodes_image([node1, node2])

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)
            self.assertEqual(result_node.url, expected_node.url)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.com/second)",
            text_type_text,
        )
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://example.com/second"),
        ]

        result_nodes = split_nodes_link([node])

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)
            self.assertEqual(result_node.url, expected_node.url)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is plain text without any links.", text_type_text)
        expected_nodes = [node]

        result_nodes = split_nodes_link([node])

        self.assertEqual(result_nodes, expected_nodes)

    def test_split_nodes_link_mixed_types(self):
        node1 = TextNode("This is text with a [link](https://example.com)", text_type_text)
        node2 = TextNode("This is an image node", text_type_image, "https://example.com/image.png")
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            node2
        ]

        result_nodes = split_nodes_link([node1, node2])

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)
            self.assertEqual(result_node.url, expected_node.url)


if __name__ == "__main__":
    unittest.main()
