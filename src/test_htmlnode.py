import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        """Test that HTMLNode initializes with None defaults"""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_all_parameters(self):
        """Test HTMLNode initialization with all parameters"""
        children = [HTMLNode("span", "child1"), HTMLNode("span", "child2")]
        props = {"class": "container", "id": "main"}
        node = HTMLNode("div", "Hello World", children, props)
        
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_empty(self):
        """Test props_to_html with no props"""
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        """Test props_to_html with explicitly None props"""
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        """Test props_to_html with empty dictionary"""
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        """Test props_to_html with single property"""
        node = HTMLNode(props={"href": "https://www.google.com"})
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple_props(self):
        """Test props_to_html with multiple properties"""
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
        })
        result = node.props_to_html()
        
        # Should start with a space
        self.assertTrue(result.startswith(' '))
        # Should contain both attributes
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)

    def test_props_to_html_special_characters(self):
        """Test props_to_html with special characters in values"""
        node = HTMLNode(props={
            "title": "Hello & Welcome",
            "data-value": "test<script>"
        })
        result = node.props_to_html()
        self.assertIn('title="Hello & Welcome"', result)
        self.assertIn('data-value="test<script>"', result)

    def test_to_html_raises_not_implemented(self):
        """Test that to_html raises NotImplementedError"""
        node = HTMLNode("p", "test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_html_raises_with_message(self):
        """Test that to_html raises NotImplementedError with correct message"""
        node = HTMLNode("div")
        with self.assertRaises(NotImplementedError) as context:
            node.to_html()
        self.assertIn("Subclasses should implement this method", str(context.exception))

    def test_repr_all_none(self):
        """Test __repr__ with all None values"""
        node = HTMLNode()
        expected = "HTMLNode(None, None, None, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_values(self):
        """Test __repr__ with actual values"""
        node = HTMLNode("p", "Hello", None, {"class": "text"})
        expected = "HTMLNode(p, Hello, None, {'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_repr_with_children(self):
        """Test __repr__ with children"""
        child = HTMLNode("span", "child")
        node = HTMLNode("div", None, [child], None)
        result = repr(node)
        self.assertIn("HTMLNode(div, None,", result)
        self.assertIn("HTMLNode(span, child, None, None)", result)

    def test_tag_only(self):
        """Test HTMLNode with only tag specified"""
        node = HTMLNode(tag="p")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_value_only(self):
        """Test HTMLNode with only value specified"""
        node = HTMLNode(value="Just text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Just text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_children_only(self):
        """Test HTMLNode with only children specified"""
        children = [HTMLNode("span", "test")]
        node = HTMLNode(children=children)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)

    def test_props_only(self):
        """Test HTMLNode with only props specified"""
        props = {"id": "test"}
        node = HTMLNode(props=props)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, props)


if __name__ == "__main__":
    unittest.main()
