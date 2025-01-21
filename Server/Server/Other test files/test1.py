import unittest
#from flask import Flask, jsonify, request

from test import app



class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup the test client."""
        cls.client = app.test_client()

    def test_get_sentence_valid(self):
        """Test the /get_sentence endpoint with valid input."""
        test_data = {
            "sentence": "I have a fever."
        }
        
        response = self.client.post('/get_sentence', json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn('symptom', response_json)
        self.assertEqual(response_json['symptom'], "fever")

    def test_get_sentence_invalid_input(self):
        """Test the /get_sentence endpoint with invalid input format."""
        test_data = {
            "sentence": 123456  # Invalid input, not a string
        }
        
        response = self.client.post('/get_sentence', json=test_data)
        
        self.assertEqual(response.status_code, 400)

    def test_get_sentence_missing_sentence(self):
        """Test the /get_sentence endpoint with missing 'sentence' field."""
        test_data = {}
        
        response = self.client.post('/get_sentence', json=test_data)
        
        self.assertEqual(response.status_code, 400)

    # def test_get_sentence_server_error(self):
    #     """Test the /get_sentence endpoint with invalid data that causes server error."""
    #     test_data = {
    #         "sentence": "I have something that breaks the model."
    #     }
        
    #     response = self.client.post('/get_sentence', json=test_data)
        
    #     self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
