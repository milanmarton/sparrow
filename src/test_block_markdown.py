import unittest
from block_markdown import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()
