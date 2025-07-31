import unittest
from blocknode import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Not heading"), BlockType.HEADING)

    def test_code_block(self):
        code = """```
print('Hello')
print('World')
```"""
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        not_code = "``not a code block``"
        self.assertNotEqual(block_to_block_type(not_code), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type("This is not a quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("* item 1\n* item 2"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("+ item 1"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("10. Tenth\n11. Eleventh"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1) Not a list"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Another paragraph\nwith multiple lines."), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type("- list"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
