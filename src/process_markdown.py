from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Splits a list of nodes into sublists based on a delimiter."""
    new_nodes = []

    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            if delimiter in node.text:
                # Split on delimiter not preceded by a backslash (i.e., ignore escaped delimiters)
                # Replace escaped delimiters with the delimiter itself
                special_regex_chars = ".^$*+?{}[]\\|()"
                if delimiter and delimiter[0] in special_regex_chars:
                    escaped_delim = re.escape(delimiter)
                else:
                    escaped_delim = delimiter
                parts = re.split(rf'(?<!\\){escaped_delim}', node.text)
                if len(parts) % 2 == 0:  # Even number of parts means unmatched delimiter
                    raise ValueError("Unmatched delimiter in text node")
                for i, part in enumerate(parts):
                    if part:  # Only add non-empty parts
                        new_node_type = TextType.TEXT
                        new_text = part #.replace(f"\\{delimiter}", delimiter)
                        if i % 2 == 1:  # Odd indices are inside delimiters
                            new_node_type = text_type
                        new_nodes.append(TextNode(new_text, new_node_type))         
            else:
                # No delimiter found, add the original node
                new_nodes.append(node)
        else:
            # Not a TEXT node, add as-is
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(markdown_text):
    """Extracts image URLs from markdown text."""
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(image_pattern, markdown_text)
    return [(alt, url) for alt, url in matches]

def extract_markdown_links(markdown_text):
    """Extracts link URLs from markdown text."""
    link_pattern = r'(?<!\!)\[(.*?)\]\((.*?)\)'
    matches = re.findall(link_pattern, markdown_text)
    return [(alt, url) for alt, url in matches]

def split_nodes_image(old_nodes):
    """Splits nodes that are images into TextNodes."""
    new_nodes = []

    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            image_links = extract_markdown_images(node.text)
            text = node.text
            for alt, url in image_links:
                text_nodes = text.split(f"![{alt}]({url})", 1)
                if len(text_nodes) > 0:
                    if text_nodes[0] != "":
                        new_nodes.append(TextNode(text_nodes[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    text = text_nodes[1] if len(text_nodes) > 1 else ""
                    if len(text_nodes) > 1 and text_nodes[1] != "":
                        text = text_nodes[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    """Splits nodes that are links into TextNodes."""
    new_nodes = []

    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            web_links = extract_markdown_links(node.text)
            text = node.text
            for alt, url in web_links:
                text_nodes = text.split(f"[{alt}]({url})", 1)
                if len(text_nodes) > 0:
                    if text_nodes[0] != "":
                        new_nodes.append(TextNode(text_nodes[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.LINK, url))
                    text = text_nodes[1] if len(text_nodes) > 1 else ""
                    if len(text_nodes) > 1 and text_nodes[1] != "":
                        text = text_nodes[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    """Converts a string to TextNodes."""
    new_nodes = []
    new_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], delimiter="**", text_type=TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, delimiter="_", text_type=TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, delimiter="`", text_type=TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    """Converts markdown text to a list of TextNodes."""
    if not markdown:
        return []

    # Split by newlines to handle paragraphs
    lines = markdown.split('\n\n')
    blocks = []
    
    for line in lines:
        if line.strip():  # Ignore empty lines
            blocks.append(line.strip())
    
    return blocks