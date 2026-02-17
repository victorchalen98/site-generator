import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextType, TextNode, TextNodeDelimiter

class TestNodeSplit(unittest.TestCase):
    def test_two_word_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], TextNodeDelimiter.CODE, TextType.CODE)

        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(result, expected_result)
