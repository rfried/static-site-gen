import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        """Test LeafNode with paragraph tag"""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        """Test LeafNode without tag returns raw text"""
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_empty_value_no_tag(self):
        """Test LeafNode with empty value and no tag"""
        node = LeafNode(None, "")
        self.assertEqual(node.to_html(), "")

    def test_leaf_to_html_none_value_no_tag(self):
        """Test LeafNode with None value and no tag"""
        node = LeafNode(None, None)
        self.assertEqual(node.to_html(), "")

    def test_leaf_to_html_with_props(self):
        """Test LeafNode with properties"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_multiple_props(self):
        """Test LeafNode with multiple properties"""
        node = LeafNode("a", "Click me!", {
            "href": "https://www.google.com",
            "target": "_blank"
        })
        result = node.to_html()
        # Check that it starts and ends correctly
        self.assertTrue(result.startswith('<a '))
        self.assertTrue(result.endswith('>Click me!</a>'))
        # Check that both attributes are present
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)

    def test_leaf_to_html_bold(self):
        """Test LeafNode with bold tag"""
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_italic(self):
        """Test LeafNode with italic tag"""
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_leaf_to_html_code(self):
        """Test LeafNode with code tag"""
        node = LeafNode("code", "print('hello')")
        self.assertEqual(node.to_html(), "<code>print('hello')</code>")

    def test_leaf_to_html_img_with_props(self):
        """Test LeafNode with img tag and properties"""
        node = LeafNode("img", "", {
            "src": "image.jpg",
            "alt": "A beautiful image"
        })
        result = node.to_html()
        self.assertTrue(result.startswith('<img '))
        self.assertTrue(result.endswith('></img>'))
        self.assertIn('src="image.jpg"', result)
        self.assertIn('alt="A beautiful image"', result)

    def test_leaf_to_html_span_with_class(self):
        """Test LeafNode with span tag and class"""
        node = LeafNode("span", "Highlighted text", {"class": "highlight"})
        expected = '<span class="highlight">Highlighted text</span>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_div_with_id(self):
        """Test LeafNode with div tag and id"""
        node = LeafNode("div", "Content", {"id": "main-content"})
        expected = '<div id="main-content">Content</div>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_init_parameters(self):
        """Test LeafNode initialization sets correct parameters"""
        node = LeafNode("p", "Test value", {"class": "test"})
        self.assertEqual(node.value, "Test value")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.props, {"class": "test"})
        self.assertIsNone(node.children)  # LeafNode should have no children

    def test_leaf_init_defaults(self):
        """Test LeafNode initialization with defaults"""
        node = LeafNode(None, "Just text")
        self.assertEqual(node.value, "Just text")
        self.assertIsNone(node.tag)
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_leaf_to_html_special_characters(self):
        """Test LeafNode with special characters in value"""
        node = LeafNode("p", "Hello & goodbye <script>")
        expected = "<p>Hello & goodbye <script></p>"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_empty_string_with_tag(self):
        """Test LeafNode with empty string value and tag"""
        node = LeafNode("p", "")
        expected = "<p></p>"
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
