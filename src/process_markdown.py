from textnode import TextNode, TextType, text_node_to_html_node
from blocknode import BlockType, block_to_block_type
from parentnode import ParentNode
from leafnode import LeafNode
import re
import os

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

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def markdown_to_html_node(markdown):
    """Converts markdown text to a list of HTMLNodes."""
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                # Join lines in paragraph block with spaces
                paragraph_text = ' '.join(line.strip() for line in block.split('\n'))
                paragraph_nodes = text_to_children(paragraph_text)
                paragraph_node = ParentNode("p", paragraph_nodes)
                block_nodes.append(paragraph_node)
            case BlockType.HEADING:
                header_level = len(block.strip().split(" ")[0])
                header_nodes = text_to_children(block.lstrip('#').strip())
                header_node = ParentNode(f"h{header_level}", header_nodes)
                block_nodes.append(header_node)
            case BlockType.CODE:
                # Remove triple backticks and wrap in <pre><code>
                code_content = block
                if code_content.startswith('```') and code_content.endswith('```'):
                    code_content = code_content[3:-3].strip('\n')
                    code_content += '\n'
                code_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])])
                block_nodes.append(code_node)
            case BlockType.QUOTE:
                # Remove '>' from the beginning of every line
                quote_text = '\n'.join(line.lstrip('>').strip() for line in block.split('\n'))
                quote_nodes = text_to_children(quote_text)
                quote_node = ParentNode("blockquote", quote_nodes)
                block_nodes.append(quote_node)
            case BlockType.ORDERED_LIST:
                list_items = []
                lines = block.split("\n")
                for line in lines:
                    html_nodes = text_to_children(line[3:])
                    if len(html_nodes) > 0:
                        list_items.append(ParentNode("li", html_nodes))
                list_node = ParentNode("ol", list_items)
                block_nodes.append(list_node)
            case BlockType.UNORDERED_LIST:
                list_items = []
                lines = block.split("\n")
                for line in lines:
                    html_nodes = text_to_children(line[2:])
                    if len(html_nodes) > 0:
                        list_items.append(ParentNode("li", html_nodes))
                list_node = ParentNode("ul", list_items)
                block_nodes.append(list_node)
            case _:
                pass  # Handle unknown block type
    html_node = ParentNode("div", block_nodes)
    return html_node

def extract_title(markdown):
    """Extracts the title from markdown text."""
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()  # Return the title without the '# '
    raise ValueError("No title found in markdown text")  # No title found

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    """Generates a page from markdown text."""
    with open(from_path, 'r') as f:
        markdown_text = f.read()
    
    title = extract_title(markdown_text)
    html_node = markdown_to_html_node(markdown_text)

    # Load template and replace placeholders
    with open(template_path, 'r') as f:
        template = f.read()
    
    html_content = template.replace('{{ Title }}', title).replace('{{ Content }}', html_node.to_html())

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    # Write to destination path
    with open(dest_path, 'w') as f:
        f.write(html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Generates pages recursively from markdown files in a directory."""
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            # Recursively generate pages in subdirectories
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item))
        elif item.endswith('.md'):
            # Generate page for markdown file
            dest_file_name = item.replace('.md', '.html')
            dest_file_path = os.path.join(dest_dir_path, dest_file_name)
            generate_page(item_path, template_path, dest_file_path)