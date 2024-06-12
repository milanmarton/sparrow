class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

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
    def __init__(self, tag=None, value=None, props=None) -> None:
        if value is None:
            raise ValueError
        super().__init__(tag, value, None, props)

    def props_to_html(self) -> str:
        return super().props_to_html()

    def to_html(self) -> str:
        if self.tag is None and self.value is not None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
