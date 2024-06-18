import unittest
from block_markdown import (
    is_code_block,
    is_heading_block,
    is_ordered_list_block,
    is_quote_block,
    is_unordered_list_block,
    markdown_to_blocks,
    block_to_block,
    block_type    
)
class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_line(self):
        markdown = "This is a single line."
        expected_blocks = ["This is a single line."]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)

    def test_multiple_lines(self):
        markdown = "This is the first line.\nThis is the second line."
        expected_blocks = ["This is the first line.\nThis is the second line."]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)

    def test_empty_lines(self):
        markdown = "\n\nThis is a line.\n\n"
        expected_blocks = ["This is a line."]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)

    def test_multiple_blocks(self):
        markdown = "This is the first block.\n\nThis is the second block.\n\nThis is the third block."
        expected_blocks = ["This is the first block.", "This is the second block.", "This is the third block."]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)

    def test_trailing_newlines(self):
        markdown = "This is a block.\n\n\n"
        expected_blocks = ["This is a block."]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)

    def test_empty_string(self):
        markdown = ""
        expected_blocks = []
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)

class TestBlockToBlock(unittest.TestCase):
    def test_heading_block(self):
        block = "## This is a heading"
        result = block_to_block(block)
        self.assertEqual(result, block_type.HEADING)

    def test_code_block(self):
        block = "```\nprint('Hello, World!')\n```"
        result = block_to_block(block)
        self.assertEqual(result, block_type.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Spanning multiple lines"
        result = block_to_block(block)
        self.assertEqual(result, block_type.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block(block)
        self.assertEqual(result, block_type.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block(block)
        self.assertEqual(result, block_type.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a regular paragraph."
        result = block_to_block(block)
        self.assertEqual(result, block_type.PARAGRAPH)

class TestIsHeadingBlock(unittest.TestCase):
    def test_valid_heading(self):
        block = "## This is a heading"
        result = is_heading_block(block)
        self.assertTrue(result)

    def test_invalid_heading(self):
        block = "Not a heading"
        result = is_heading_block(block)
        self.assertFalse(result)

    def test_too_many_hashes(self):
        block = "#######This is not a heading"
        result = is_heading_block(block)
        self.assertFalse(result)

class TestIsCodeBlock(unittest.TestCase):
    def test_valid_code_block(self):
        block = "```\nprint('Hello, World!')\n```"
        result = is_code_block(block)
        self.assertTrue(result)

    def test_invalid_code_block(self):
        block = "This is not a code block"
        result = is_code_block(block)
        self.assertFalse(result)

class TestIsQuoteBlock(unittest.TestCase):
    def test_valid_quote_block(self):
        block = "> This is a quote\n> Spanning multiple lines"
        result = is_quote_block(block)
        self.assertTrue(result)

    def test_invalid_quote_block(self):
        block = "This is not a quote block"
        result = is_quote_block(block)
        self.assertFalse(result)

    def test_mixed_quote_block(self):
        block = "> This is a quote\nThis line is not a quote"
        result = is_quote_block(block)
        self.assertFalse(result)

class TestIsUnorderedListBlock(unittest.TestCase):
    def test_valid_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = is_unordered_list_block(block)
        self.assertTrue(result)

    def test_invalid_unordered_list_block(self):
        block = "1. This is not an unordered list"
        result = is_unordered_list_block(block)
        self.assertFalse(result)

    def test_mixed_unordered_list_block(self):
        block = "- Item 1\n- Item 2\nThis line is not a list item"
        result = is_unordered_list_block(block)
        self.assertFalse(result)

class TestIsOrderedListBlock(unittest.TestCase):
    def test_valid_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = is_ordered_list_block(block)
        self.assertTrue(result)

    def test_invalid_ordered_list_block(self):
        block = "- This is not an ordered list"
        result = is_ordered_list_block(block)
        self.assertFalse(result)

    def test_mixed_ordered_list_block(self):
        block = "1. First item\n2. Second item\nThis line is not a list item"
        result = is_ordered_list_block(block)
        self.assertFalse(result)

    def test_missing_number(self):
        block = "1. First item\n2. Second item\n. Third item"
        result = is_ordered_list_block(block)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
