from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag must be specified for ParentNode")
        if not self.children:
            raise ValueError("Children must be specified for ParentNode")
        return f'<{self.tag}{super().props_to_html()}>' + ''.join(child.to_html() for child in self.children) + f'</{self.tag}>'