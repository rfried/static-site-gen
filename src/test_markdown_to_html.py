import unittest
from process_markdown import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs_and_inline(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_code_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()    
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        from process_markdown import extract_title
        md = """# My Title\n\nSome content here."""
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_first_heading(self):
        from process_markdown import extract_title
        md = """Some intro\n\n# First Heading\n\n## Second Heading"""
        self.assertEqual(extract_title(md), "First Heading")

    def test_extract_title_multiple_headings(self):
        from process_markdown import extract_title
        md = """# First\n\n# Second\n\n# Third"""
        self.assertEqual(extract_title(md), "First")

    def test_extract_title_heading_with_formatting(self):
        from process_markdown import extract_title
        md = """# **Bold Title**\n\nSome text."""
        self.assertEqual(extract_title(md), "**Bold Title**")

    def test_extract_title_heading_with_extra_spaces(self):
        from process_markdown import extract_title
        md = """#    Title With Spaces   \nContent."""
        self.assertEqual(extract_title(md), "Title With Spaces")

    def test_extract_title_heading_not_first_line(self):
        from process_markdown import extract_title
        md = "Intro\n\n# Title After Intro\nMore text."
        self.assertEqual(extract_title(md), "Title After Intro")

    def test_extract_title_malformed_heading_raises(self):
        from process_markdown import extract_title
        md = "#\nNo title after hash"
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
