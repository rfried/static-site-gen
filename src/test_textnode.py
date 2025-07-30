import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


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
        node = TextNode("Plain text", TextType.TEXT)
        self.assertEqual(node.text, "Plain text")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_init_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Click here")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    def test_all_text_types(self):
        # Test that all TextType enum values can be used
        text_types = [
            TextType.TEXT,
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
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.TEXT)

    def test_none_url_explicit(self):
        node = TextNode("Test", TextType.BOLD, None)
        self.assertEqual(node.text, "Test")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertIsNone(node.url)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        """Test converting TEXT TextNode to LeafNode"""
        text_node = TextNode("Just plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Just plain text")
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "Just plain text")

    def test_text_node_to_html_node_bold(self):
        """Test converting BOLD TextNode to LeafNode"""
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_html_node_italic(self):
        """Test converting ITALIC TextNode to LeafNode"""
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_to_html_node_code(self):
        """Test converting CODE TextNode to LeafNode"""
        text_node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_text_node_to_html_node_link(self):
        """Test converting LINK TextNode to LeafNode"""
        text_node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Click here</a>')

    def test_text_node_to_html_node_image(self):
        """Test converting IMAGE TextNode to LeafNode"""
        text_node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})
        result = html_node.to_html()
        self.assertIn('src="https://example.com/image.jpg"', result)
        self.assertIn('alt="Alt text"', result)
        self.assertTrue(result.startswith('<img '))
        self.assertTrue(result.endswith('></img>'))

    def test_text_node_to_html_node_link_no_url_raises_error(self):
        """Test that LINK TextNode without URL raises ValueError"""
        text_node = TextNode("Click here", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertIn("Unsupported TextType", str(context.exception))

    def test_text_node_to_html_node_image_no_url_raises_error(self):
        """Test that IMAGE TextNode without URL raises ValueError"""
        text_node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertIn("Unsupported TextType", str(context.exception))

    def test_text_node_to_html_node_link_empty_url_raises_error(self):
        """Test that LINK TextNode with empty URL raises ValueError"""
        text_node = TextNode("Click here", TextType.LINK, "")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertIn("Unsupported TextType", str(context.exception))

    def test_text_node_to_html_node_image_empty_url_raises_error(self):
        """Test that IMAGE TextNode with empty URL raises ValueError"""
        text_node = TextNode("Alt text", TextType.IMAGE, "")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertIn("Unsupported TextType", str(context.exception))

    def test_text_node_to_html_node_empty_text(self):
        """Test converting TextNode with empty text"""
        text_node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), "<b></b>")

    def test_text_node_to_html_node_special_characters(self):
        """Test converting TextNode with special characters"""
        text_node = TextNode("Hello & <world>", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.value, "Hello & <world>")
        self.assertEqual(html_node.to_html(), "<b>Hello & <world></b>")

    def test_text_node_to_html_node_link_with_special_chars_in_url(self):
        """Test converting LINK TextNode with special characters in URL"""
        text_node = TextNode("Search", TextType.LINK, "https://google.com/search?q=hello&world")
        html_node = text_node_to_html_node(text_node)
        
        expected_props = {"href": "https://google.com/search?q=hello&world"}
        self.assertEqual(html_node.props, expected_props)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()