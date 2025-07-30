import unittest

from textnode import TextNode, TextType
from process_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        """Test basic delimiter splitting with bold text"""
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        """Test splitting with multiple delimiter pairs"""
        node = TextNode("This has **bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_italic(self):
        """Test delimiter splitting with italic text"""
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_code(self):
        """Test delimiter splitting with code text"""
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_no_delimiter(self):
        """Test with text that has no delimiter"""
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_only_delimiter(self):
        """Test with text that is only delimited content"""
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_starts_with_delimiter(self):
        """Test with text that starts with delimiter"""
        node = TextNode("**bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_ends_with_delimiter(self):
        """Test with text that ends with delimiter"""
        node = TextNode("text **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_unmatched_raises_error(self):
        """Test that unmatched delimiter raises ValueError"""
        node = TextNode("This has **unmatched bold", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("Unmatched delimiter", str(context.exception))

    def test_split_nodes_delimiter_empty_delimiter_content(self):
        """Test with empty content between delimiters"""
        node = TextNode("Text **** more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode(" more text", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_multiple_nodes(self):
        """Test with multiple input nodes"""
        nodes = [
            TextNode("First **bold** text", TextType.TEXT),
            TextNode("Second **bold** text", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 6)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes are left unchanged"""
        nodes = [
            TextNode("Plain **bold** text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("**Should not change**", TextType.ITALIC)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        # First node should be split
        self.assertEqual(new_nodes[0].text, "Plain ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
        # Second and third nodes should be unchanged
        self.assertEqual(new_nodes[3].text, "Already bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, "**Should not change**")
        self.assertEqual(new_nodes[4].text_type, TextType.ITALIC)

    def test_split_nodes_delimiter_empty_list(self):
        """Test with empty list of nodes"""
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 0)

    def test_split_nodes_delimiter_adjacent_delimiters(self):
        """Test with adjacent delimiters"""
        node = TextNode("**bold****italic**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.BOLD)
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_nodes_delimiter_preserve_whitespace(self):
        """Test that whitespace is preserved correctly"""
        node = TextNode("  **bold**  ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("  ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("  ", TextType.TEXT)
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        """Test extracting multiple images"""
        text = "Here's ![first image](https://example.com/1.jpg) and ![second image](https://example.com/2.png)"
        matches = extract_markdown_images(text)
        expected = [
            ("first image", "https://example.com/1.jpg"),
            ("second image", "https://example.com/2.png")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_empty_alt(self):
        """Test extracting images with empty alt text"""
        text = "![](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.jpg")], matches)

    def test_extract_markdown_images_no_images(self):
        """Test text with no images"""
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_complex_alt(self):
        """Test images with complex alt text"""
        text = "![Image with spaces and symbols!@#](https://example.com/test.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("Image with spaces and symbols!@#", "https://example.com/test.png")], matches)

    def test_extract_markdown_images_nested_brackets(self):
        """Test images with brackets in alt text"""
        text = "![Alt [with] brackets](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        # The regex actually captures the full content including nested brackets
        self.assertListEqual([("Alt [with] brackets", "https://example.com/image.jpg")], matches)

    def test_extract_markdown_images_mixed_with_links(self):
        """Test images mixed with regular links"""
        text = "Here's a [link](https://example.com) and an ![image](https://example.com/pic.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/pic.jpg")], matches)

    def test_extract_markdown_links_basic(self):
        """Test basic link extraction"""
        text = "This is text with a [link](https://www.example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        """Test extracting multiple links"""
        text = "Visit [Google](https://google.com) and [GitHub](https://github.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_empty_text(self):
        """Test extracting links with empty link text"""
        text = "[](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_links_no_links(self):
        """Test text with no links"""
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_complex_text(self):
        """Test links with complex link text"""
        text = "[Link with spaces and symbols!@#](https://example.com/path)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Link with spaces and symbols!@#", "https://example.com/path")], matches)

    def test_extract_markdown_links_with_images(self):
        """Test links mixed with images (should not match images)"""
        text = "Here's an ![image](https://example.com/pic.jpg) and a [link](https://example.com)"
        matches = extract_markdown_links(text)
        # Should match both the image (as a link) and the actual link
        expected = [
            ("link", "https://example.com")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_nested_brackets(self):
        """Test links with brackets in link text"""
        text = "[Link with [brackets]](https://example.com)"
        matches = extract_markdown_links(text)
        # The regex actually captures the full content including nested brackets
        self.assertListEqual([("Link with [brackets]", "https://example.com")], matches)

    def test_extract_markdown_images_special_urls(self):
        """Test images with special characters in URLs"""
        text = "![test](https://example.com/path?param=value&other=123#anchor)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("test", "https://example.com/path?param=value&other=123#anchor")], matches)

    def test_extract_markdown_links_special_urls(self):
        """Test links with special characters in URLs"""
        text = "[Search](https://google.com/search?q=hello+world&source=web)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Search", "https://google.com/search?q=hello+world&source=web")], matches)

    def test_extract_markdown_images_relative_urls(self):
        """Test images with relative URLs"""
        text = "![local image](./images/test.jpg) and ![another](../assets/pic.png)"
        matches = extract_markdown_images(text)
        expected = [
            ("local image", "./images/test.jpg"),
            ("another", "../assets/pic.png")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_relative_urls(self):
        """Test links with relative URLs"""
        text = "[Home](./index.html) and [About](../about.html)"
        matches = extract_markdown_links(text)
        expected = [
            ("Home", "./index.html"),
            ("About", "../about.html")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_multiline(self):
        """Test images across multiple lines"""
        text = """This is a multiline text
        with an ![image](https://example.com/image.jpg) in it
        and some more text"""
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/image.jpg")], matches)

    def test_extract_markdown_links_multiline(self):
        """Test links across multiple lines"""
        text = """This is a multiline text
        with a [link](https://example.com) in it
        and some more text"""
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images_single_image(self):
        node = TextNode("Hello ![img](url.jpg) world", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("Hello ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode(" world", TextType.TEXT)
        ], new_nodes)

    def test_split_images_image_at_start(self):
        node = TextNode("![img](url.jpg) and text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode(" and text", TextType.TEXT)
        ], new_nodes)

    def test_split_images_image_at_end(self):
        node = TextNode("text and ![img](url.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("text and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.jpg")
        ], new_nodes)

    def test_split_images_adjacent_images(self):
        node = TextNode("![a](1.jpg)![b](2.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("a", TextType.IMAGE, "1.jpg"),
            TextNode("b", TextType.IMAGE, "2.jpg")
        ], new_nodes)

    def test_split_images_no_images(self):
        node = TextNode("just text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("just text", TextType.TEXT)
        ], new_nodes)

    def test_split_images_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("foo ![img](url.jpg) bar", TextType.TEXT),
            TextNode("baz", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([
            TextNode("foo ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode(" bar", TextType.TEXT),
            TextNode("baz", TextType.TEXT)
        ], new_nodes)

    def test_split_images_mixed_types(self):
        nodes = [
            TextNode("foo ![img](url.jpg) bar", TextType.TEXT),
            TextNode("baz", TextType.BOLD)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([
            TextNode("foo ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode(" bar", TextType.TEXT),
            TextNode("baz", TextType.BOLD)
        ], new_nodes)

    def test_split_images_empty_alt(self):
        node = TextNode("before ![](url.jpg) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("before ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "url.jpg"),
            TextNode(" after", TextType.TEXT)
        ], new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_single_link(self):
        node = TextNode("Hello [foo](bar.com) world", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Hello ", TextType.TEXT),
            TextNode("foo", TextType.LINK, "bar.com"),
            TextNode(" world", TextType.TEXT)
        ], new_nodes)

    def test_split_links_link_at_start(self):
        node = TextNode("[foo](bar.com) and text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("foo", TextType.LINK, "bar.com"),
            TextNode(" and text", TextType.TEXT)
        ], new_nodes)

    def test_split_links_link_at_end(self):
        node = TextNode("text and [foo](bar.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("text and ", TextType.TEXT),
            TextNode("foo", TextType.LINK, "bar.com")
        ], new_nodes)

    def test_split_links_adjacent_links(self):
        node = TextNode("[a](1.com)[b](2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("a", TextType.LINK, "1.com"),
            TextNode("b", TextType.LINK, "2.com")
        ], new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("just text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("just text", TextType.TEXT)
        ], new_nodes)

    def test_split_links_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("foo [bar](baz.com) qux", TextType.TEXT),
            TextNode("quux", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual([
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.LINK, "baz.com"),
            TextNode(" qux", TextType.TEXT),
            TextNode("quux", TextType.TEXT)
        ], new_nodes)

    def test_split_links_mixed_types(self):
        nodes = [
            TextNode("foo [bar](baz.com) qux", TextType.TEXT),
            TextNode("quux", TextType.BOLD)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual([
            TextNode("foo ", TextType.TEXT),
            TextNode("bar", TextType.LINK, "baz.com"),
            TextNode(" qux", TextType.TEXT),
            TextNode("quux", TextType.BOLD)
        ], new_nodes)

    def test_split_links_empty_text(self):
        node = TextNode("before [](url.com) after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("before ", TextType.TEXT),
            TextNode("", TextType.LINK, "url.com"),
            TextNode(" after", TextType.TEXT)
        ], new_nodes)

    def test_split_links_image_and_link(self):
        node = TextNode("![img](img.jpg) and [foo](bar.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual([
            TextNode("img", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("foo", TextType.LINK, "bar.com")
        ], new_nodes)

    def test_split_links_link_and_image(self):
        node = TextNode("[foo](bar.com) and ![img](img.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual([
            TextNode("foo", TextType.LINK, "bar.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.jpg")
        ], new_nodes)

    
    def test_split_links_link_then_image(self):
        node = TextNode("[foo](bar.com) and ![img](img.jpg)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        # we expect the link to greedily take the image since they only differ by a !
        self.assertListEqual([
            TextNode("foo", TextType.LINK, "bar.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.jpg")
        ], new_nodes)

    def test_split_links_multiple_images_and_links(self):
        node = TextNode("[foo](bar.com) ![img](img.jpg) [baz](qux.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual([
            TextNode("foo", TextType.LINK, "bar.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("baz", TextType.LINK, "qux.com")
        ], new_nodes)

    def test_split_links_multiple_images_and_links_reverse(self):
        node = TextNode("![img](img.jpg) [foo](bar.com) ![baz](baz.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual([
            TextNode("img", TextType.IMAGE, "img.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("foo", TextType.LINK, "bar.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("baz", TextType.IMAGE, "baz.jpg")
        ], new_nodes)

    def test_split_links_no_text_nodes(self):
        nodes = [TextNode("foo", TextType.BOLD), TextNode("bar", TextType.ITALIC)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_images_no_text_nodes(self):
        nodes = [TextNode("foo", TextType.BOLD), TextNode("bar", TextType.ITALIC)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_images_and_links_empty(self):
        new_nodes = split_nodes_image([])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual([], new_nodes)

    def test_split_links_and_images_empty(self):
        new_nodes = split_nodes_link([])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual([], new_nodes)

class TestTextToTextnodes(unittest.TestCase):       
    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], new_nodes)

    def test_text_to_textnodes_empty(self):
        new_nodes = text_to_textnodes("")
        self.assertListEqual([], new_nodes)

    def test_text_to_textnodes_only_text(self):
        new_nodes = text_to_textnodes("Just plain text.")
        self.assertListEqual([
            TextNode("Just plain text.", TextType.TEXT)
        ], new_nodes)

    def test_text_to_textnodes_multiple_bold(self):
        new_nodes = text_to_textnodes("**bold1** and **bold2**")
        self.assertListEqual([
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD)
        ], new_nodes)

    def test_text_to_textnodes_multiple_italic(self):
        new_nodes = text_to_textnodes("_italic1_ and _italic2_")
        self.assertListEqual([
            TextNode("italic1", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic2", TextType.ITALIC)
        ], new_nodes)

    def test_text_to_textnodes_multiple_code(self):
        new_nodes = text_to_textnodes("`code1` and `code2`")
        self.assertListEqual([
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE)
        ], new_nodes)

    def test_text_to_textnodes_multiple_images(self):
        new_nodes = text_to_textnodes("![img1](url1.jpg) and ![img2](url2.png)")
        self.assertListEqual([
            TextNode("img1", TextType.IMAGE, "url1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.png")
        ], new_nodes)

    def test_text_to_textnodes_multiple_links(self):
        new_nodes = text_to_textnodes("[foo](bar.com) and [baz](qux.com)")
        self.assertListEqual([
            TextNode("foo", TextType.LINK, "bar.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("baz", TextType.LINK, "qux.com")
        ], new_nodes)

    def test_text_to_textnodes_adjacent_elements(self):
        new_nodes = text_to_textnodes("**bold**_italic_`code`![img](url.jpg)[link](url.com)")
        self.assertListEqual([
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode("link", TextType.LINK, "url.com")
        ], new_nodes)

    def test_text_to_textnodes_interleaved(self):
        new_nodes = text_to_textnodes("Text **bold** _italic_ [link](url.com) ![img](img.jpg) `code`")
        self.assertListEqual([
            TextNode("Text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ], new_nodes)

    def test_text_to_textnodes_empty_image_and_link(self):
        new_nodes = text_to_textnodes("![](img.jpg) and [](url.com)")
        self.assertListEqual([
            TextNode("", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("", TextType.LINK, "url.com")
        ], new_nodes)

    def test_text_to_textnodes_nested_delimiters(self):
        # Should treat as plain text if delimiters are not matched
        new_nodes = text_to_textnodes("**bold _italic_**")
        self.assertListEqual([
            TextNode("bold _italic_", TextType.BOLD)
        ], new_nodes)

    def test_text_to_textnodes_escaped_delimiters(self):
        # Escaped delimiters should be treated as plain text, preserving backslashes
        new_nodes = text_to_textnodes(r"This is a literal \*asterisk\* and \_underscore\_")
        self.assertListEqual([
            TextNode(r"This is a literal \*asterisk\* and \_underscore\_", TextType.TEXT)
        ], new_nodes)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        """Test with empty string"""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only(self):
        """Test with only whitespace"""
        md = "   \n\n\t  \n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_paragraph(self):
        """Test with a single paragraph"""
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_markdown_to_blocks_single_paragraph_with_whitespace(self):
        """Test single paragraph with leading/trailing whitespace"""
        md = "   This is a paragraph with whitespace.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with whitespace."])

    def test_markdown_to_blocks_multiple_paragraphs(self):
        """Test with multiple paragraphs separated by blank lines"""
        md = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph.", "Third paragraph."])

    def test_markdown_to_blocks_paragraphs_with_extra_newlines(self):
        """Test paragraphs with multiple blank lines between them"""
        md = "First paragraph.\n\n\n\nSecond paragraph.\n\n\n\n\nThird paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph.", "Third paragraph."])

    def test_markdown_to_blocks_multiline_paragraph(self):
        """Test paragraph that spans multiple lines"""
        md = "This is a paragraph\nthat spans multiple\nlines but is still one block."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph\nthat spans multiple\nlines but is still one block."])

    def test_markdown_to_blocks_list_items(self):
        """Test with list items"""
        md = "- First item\n- Second item\n- Third item"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- First item\n- Second item\n- Third item"])

    def test_markdown_to_blocks_ordered_list(self):
        """Test with ordered list"""
        md = "1. First item\n2. Second item\n3. Third item"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["1. First item\n2. Second item\n3. Third item"])

    def test_markdown_to_blocks_code_block(self):
        """Test with code block"""
        md = "```\nprint('Hello, World!')\nprint('This is code')\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["```\nprint('Hello, World!')\nprint('This is code')\n```"])

    def test_markdown_to_blocks_heading(self):
        """Test with headings"""
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading 1", "## Heading 2", "### Heading 3"])

    def test_markdown_to_blocks_blockquote(self):
        """Test with blockquote"""
        md = "> This is a quote\n> that spans multiple lines\n> and should be one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["> This is a quote\n> that spans multiple lines\n> and should be one block"])

    def test_markdown_to_blocks_mixed_content(self):
        """Test with mixed content types"""
        md = """# Title

This is a paragraph.

- List item 1
- List item 2

```
code block
```

> Quote block

Another paragraph."""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Title",
            "This is a paragraph.",
            "- List item 1\n- List item 2",
            "```\ncode block\n```",
            "> Quote block",
            "Another paragraph."
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        """Test with leading and trailing whitespace in the entire markdown"""
        md = "\n\n\nFirst paragraph.\n\nSecond paragraph.\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph."])

    def test_markdown_to_blocks_indented_content(self):
        """Test with indented content"""
        md = "    This is indented\n    And continues here\n\nNormal paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is indented\n    And continues here", "Normal paragraph"])

    def test_markdown_to_blocks_tabs_and_spaces(self):
        """Test with tabs and spaces"""
        md = "   \t  Paragraph with mixed whitespace.  \t  \n\n\t\tAnother paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph with mixed whitespace.", "Another paragraph."])

    def test_markdown_to_blocks_preserve_internal_spacing(self):
        """Test that internal spacing within blocks is preserved"""
        md = "This  has    multiple   spaces.\n\nThis\thas\ttabs."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This  has    multiple   spaces.", "This\thas\ttabs."])

    def test_markdown_to_blocks_complex_list(self):
        """Test with complex list structure"""
        md = """- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3

1. Ordered item 1
2. Ordered item 2"""
        blocks = markdown_to_blocks(md)
        expected = [
            "- Item 1\n- Item 2\n  - Nested item\n  - Another nested item\n- Item 3",
            "1. Ordered item 1\n2. Ordered item 2"
        ]
        self.assertEqual(blocks, expected)

if __name__ == "__main__":
    unittest.main()
