import unittest
from src import mumblebot


class TestMumble(unittest.TestCase):
    def test_finPrompt_withoutUsername(self):
        '''
        Test that it can correctly make the final prompt without username.
        '''
        data = 'How much is 5 and 5?'
        expected = "Below is a conversation between a user and an AI assistant named Phoenix.\nPhoenix was made by Tiven and provides helpful answers.\nUser: " + data + "\nPhoenix:"
        result = mumblebot.finPrompt(data)
        self.assertEqual(result, expected)

    def test_finPrompt_withUsername(self):
        '''
        Test that it can correctly make the final prompt with username.
        '''
        data = 'How much is 5 and 5?'
        expected = "Below is a conversation between a user named Tiven and an AI assistant named Phoenix.\nPhoenix was made by Tiven and provides helpful answers.\nTiven: " + data + "\nPhoenix:"
        result = mumblebot.finPrompt(data, 'Tiven')
        self.assertEqual(result, expected)