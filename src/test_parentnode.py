import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_simple(self):
        """Test ParentNode with simple children"""
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode("i", "Italic text")
        parent = ParentNode("p", [child1, child2])
        expected = "<p><b>Bold text</b><i>Italic text</i></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_to_html_with_props(self):
        """Test ParentNode with properties"""
        child = LeafNode("span", "Content")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        result = parent.to_html()
        self.assertTrue(result.startswith('<div '))
        self.assertTrue(result.endswith('<span>Content</span></div>'))
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)

    def test_parent_to_html_nested_parents(self):
        """Test ParentNode with nested ParentNodes"""
        inner_child = LeafNode("strong", "Bold")
        inner_parent = ParentNode("p", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        expected = "<div><p><strong>Bold</strong></p></div>"
        self.assertEqual(outer_parent.to_html(), expected)

    def test_parent_to_html_mixed_children(self):
        """Test ParentNode with mixed LeafNode and ParentNode children"""
        leaf1 = LeafNode("span", "Start")
        leaf2 = LeafNode("b", "Bold")
        nested_parent = ParentNode("p", [leaf2])
        leaf3 = LeafNode("span", "End")
        parent = ParentNode("div", [leaf1, nested_parent, leaf3])
        expected = "<div><span>Start</span><p><b>Bold</b></p><span>End</span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_to_html_no_tag_raises_error(self):
        """Test ParentNode raises ValueError when tag is None"""
        child = LeafNode("span", "Content")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Tag must be specified for ParentNode")

    def test_parent_to_html_empty_children_raises_error(self):
        """Test ParentNode raises ValueError when children is empty list"""
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Children must be specified for ParentNode")

    def test_parent_to_html_none_children_raises_error(self):
        """Test ParentNode raises ValueError when children is None"""
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Children must be specified for ParentNode")

    def test_parent_init_parameters(self):
        """Test ParentNode initialization sets correct parameters"""
        children = [LeafNode("span", "test")]
        props = {"class": "test"}
        parent = ParentNode("div", children, props)
        
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, children)
        self.assertEqual(parent.props, props)
        self.assertIsNone(parent.value)  # ParentNode should have no value

    def test_parent_init_defaults(self):
        """Test ParentNode initialization with defaults"""
        children = [LeafNode("span", "test")]
        parent = ParentNode("div", children)
        
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, children)
        self.assertIsNone(parent.props)
        self.assertIsNone(parent.value)

    def test_parent_to_html_single_child(self):
        """Test ParentNode with single child"""
        child = LeafNode("span", "Single child")
        parent = ParentNode("div", [child])
        expected = "<div><span>Single child</span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_to_html_text_only_child(self):
        """Test ParentNode with text-only LeafNode child"""
        child = LeafNode(None, "Just text")
        parent = ParentNode("p", [child])
        expected = "<p>Just text</p>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_to_html_complex_nesting(self):
        """Test ParentNode with complex nesting structure"""
        # Create a structure like: <div><p><b>Bold</b> and <i>Italic</i></p></div>
        bold_leaf = LeafNode("b", "Bold")
        text_leaf = LeafNode(None, " and ")
        italic_leaf = LeafNode("i", "Italic")
        paragraph = ParentNode("p", [bold_leaf, text_leaf, italic_leaf])
        div = ParentNode("div", [paragraph])
        
        expected = "<div><p><b>Bold</b> and <i>Italic</i></p></div>"
        self.assertEqual(div.to_html(), expected)

    def test_parent_to_html_with_link_children(self):
        """Test ParentNode with link children"""
        link1 = LeafNode("a", "Google", {"href": "https://google.com"})
        text = LeafNode(None, " and ")
        link2 = LeafNode("a", "GitHub", {"href": "https://github.com"})
        parent = ParentNode("p", [link1, text, link2])
        
        result = parent.to_html()
        self.assertTrue(result.startswith("<p>"))
        self.assertTrue(result.endswith("</p>"))
        self.assertIn('<a href="https://google.com">Google</a>', result)
        self.assertIn('<a href="https://github.com">GitHub</a>', result)
        self.assertIn(" and ", result)

    def test_parent_to_html_empty_tag_string_raises_error(self):
        """Test ParentNode raises ValueError when tag is empty string"""
        child = LeafNode("span", "Content")
        parent = ParentNode("", [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Tag must be specified for ParentNode")

    def test_parent_to_html_multiple_levels_deep(self):
        """Test ParentNode with multiple levels of nesting"""
        # <div><section><article><p><strong>Text</strong></p></article></section></div>
        strong = LeafNode("strong", "Text")
        p = ParentNode("p", [strong])
        article = ParentNode("article", [p])
        section = ParentNode("section", [article])
        div = ParentNode("div", [section])
        
        expected = "<div><section><article><p><strong>Text</strong></p></article></section></div>"
        self.assertEqual(div.to_html(), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
