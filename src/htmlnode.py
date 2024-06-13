from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
    

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        in_html = ""
        if self.props is not None:
            for key, value in self.props.items():
                in_html = f'{in_html} {key}="{value}"'
        return in_html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def props_to_html(self) -> str:
        return super().props_to_html()

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode without tag error")
        if self.children is None:
            raise ValueError("ParentNode without children error")

        children_html = ''
        for child in self.children:
            children_html = children_html + ''.join(child.to_html())
      
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    # match text_node.text_type:
    #     case text_type_text:
    #         return LeafNode(None, text_node.text)
    #     case text_type_bold:
    #         return LeafNode('b', text_node.text)
    #     case text_type_italic:
    #         return LeafNode('i', text_node.text)
    #     case text_type_code:
    #         return LeafNode('code', text_node.text)
    #     case text_type_link:
    #         return LeafNode('a', text_node.text, {'href': text_node.url})
    #     case text_type_image:
    #         return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    #     case _:
    #         raise NotImplementedError

    # for some reason the switch case doesn't work with the imported text_types
            
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    else:
        raise ValueError(f'Invalid text type {text_node.text_type}')
