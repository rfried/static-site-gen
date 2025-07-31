from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

markdown_patterns = {
    BlockType.HEADING: r"^#{1,6} .*$",
    BlockType.CODE: r"^```[^`]+```$",
    BlockType.QUOTE: r"^>.*(?:\n>.*)*$",
    BlockType.UNORDERED_LIST: r"\A([-*]) .*?$(?:\n\1 .*?$)*\Z",
    BlockType.ORDERED_LIST: r"\A1\. .*?$(?:\n\d+\. .*?$)*\Z",
    BlockType.PARAGRAPH: r".*"
}

def block_to_block_type(markdown_text:str) -> BlockType:
    """Converts a markdown text block to a BlockType."""
    text = markdown_text.strip()
    markdown_len = len(text)
    matches = None
    for block_type, pattern in markdown_patterns.items():
        matches = re.match(pattern, text, re.MULTILINE)
        if matches and len(matches.group(0)) == markdown_len:
            return block_type
    return BlockType.PARAGRAPH  # Default to paragraph if no other type matches