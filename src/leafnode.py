from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.tag:
            return self.value if self.value else ''
        attr_str = super().props_to_html()
        return f'<{self.tag}{attr_str}>{self.value}</{self.tag}>'