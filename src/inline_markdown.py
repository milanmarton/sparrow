import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
# doesnt work with mixed italic and bold types in the same text
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if node_not_text_type(old_node):
            new_nodes.append(old_node)
            continue

        split_node = old_node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("Invalid markdown syntax (missing closing delimiter)")

        for i, part in enumerate(split_node):
            if i % 2 == 0:
                if part:  # only if the part is not an empty string
                    new_nodes.append(TextNode(part, text_type_text))
            else:
                if part:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes

def node_not_text_type(node: TextNode) -> bool:
    return node.text_type != text_type_text

def extract_markdown_images(text: str) -> list:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

# text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
# print(extract_markdown_images(text))

def extract_markdown_links(text: str) -> list:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

# text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
# print(extract_markdown_links(text))


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if node_not_text_type(old_node):
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue

        temp_text = old_node.text[:]
        for i, image in enumerate(images):
            new_text = temp_text.split(f'![{image[0]}]({image[1]})', 1)
            new_nodes.append(TextNode(new_text[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            if i == len(images) - 1 and new_text[1]:
                new_nodes.append(TextNode(new_text[1], text_type_text))
            temp_text = new_text[1]

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if node_not_text_type(old_node):
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        temp_text = old_node.text[:]
        for i, link in enumerate(links):
            new_text = temp_text.split(f'[{link[0]}]({link[1]})', 1)
            new_nodes.append(TextNode(new_text[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            if i == len(links) - 1 and new_text[1]:
                new_nodes.append(TextNode(new_text[1], text_type_text))
            temp_text = new_text[1]

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    first_node = TextNode(text, text_type_text)
    nodes = [first_node]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
    nodes = split_nodes_delimiter(nodes, '`', text_type_code)

    return nodes
