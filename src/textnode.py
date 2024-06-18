text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other) -> bool:
        if self.text == other.text and self.text_type == other.text_type \
            and self.url == other.url:
            return True
        return False
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


# doesnt work with mixed italic and bold types in the same text
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if node_not_text_type(old_node):
            new_nodes.append(old_node)
            continue

        splitted_node = old_node.text.split(delimiter)
        if len(splitted_node) % 2 == 0:
            raise ValueError("Invalid markdown syntax (missing closing delimiter)")

        for i, part in enumerate(splitted_node):
            if i % 2 == 0:
                if part:  # only if the part is not an empty string
                    new_nodes.append(TextNode(part, text_type_text))
            else:
                if part:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes

def node_not_text_type(node: TextNode) -> bool:
    return node.text_type != text_type_text
