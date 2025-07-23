import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "not a TextNode")
        self.assertNotEqual(node, None)
        self.assertNotEqual(node, 42)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        expected = "TextNode(This is a link, link, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_init_plain_text(self):
        node = TextNode("Plain text", TextType.PLAIN)
        self.assertEqual(node.text, "Plain text")
        self.assertEqual(node.text_type, TextType.PLAIN)
        self.assertIsNone(node.url)

    def test_init_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Click here")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    def test_all_text_types(self):
        # Test that all TextType enum values can be used
        text_types = [
            TextType.PLAIN,
            TextType.BOLD,
            TextType.ITALIC,
            TextType.CODE,
            TextType.LINK,
            TextType.IMAGE
        ]
        
        for text_type in text_types:
            node = TextNode("test text", text_type)
            self.assertEqual(node.text_type, text_type)

    def test_empty_text(self):
        node = TextNode("", TextType.PLAIN)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.PLAIN)

    def test_none_url_explicit(self):
        node = TextNode("Test", TextType.BOLD, None)
        self.assertEqual(node.text, "Test")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()