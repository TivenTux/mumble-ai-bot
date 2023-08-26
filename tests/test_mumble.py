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

    def test_generate_key(self):
        '''
        Test that it can generate private key file.
        '''
        expected = 1
        result = mumblebot.generate_private_key("./src/cert/private.pem")
        print(result)
        self.assertEqual(result, expected)
        action = mumblebot.remove_key_cert_files("./src/cert/private.pem", "./src/cert/public.pem")
        print(action)

    def test_generate_certificate(self):
        '''
        Test that it can generate self signed certificate.
        '''
        expected = 1
        makekeyfile = mumblebot.generate_private_key("./src/cert/private.pem")
        result = mumblebot.generate_certificate("./src/cert/private.pem", "./src/cert/public.pem")
        print(makekeyfile, result)
        self.assertEqual(result, expected)
        #clean up
        action = mumblebot.remove_key_cert_files("./src/cert/private.pem", "./src/cert/public.pem")
        print(action)