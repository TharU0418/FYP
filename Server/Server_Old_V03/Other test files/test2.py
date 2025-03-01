import unittest
import json
from tests import app  # Import your Flask app and CustomLabelEncoder class
import pickle


class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup the test client."""
        cls.client = app.test_client()

    def test_get_diseases_name(self):
        """Test the /get_diseases_name endpoint with valid input."""
        test_data = {
            "symptom_user_input": "headache"
        }
        
        response = self.client.post('/get_diseases_name', json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn('diseases', response_json)


    def test_get_illess_name(self): 
        """Test the /get_illess_name endpoint with valid input."""
        test_data = {
            "diseases_input": "Allergy"
        }
        
        response = self.client.post('/get_illess_name', json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn('symptoms', response_json)
        
        # Expected symptoms list (no leading spaces)
        expected_symptoms = [
            "continuous_sneezing", 
            "shivering", 
            "chills", 
            "watering_from_eyes"
        ]
        
        # Clean up the response symptoms by stripping leading/trailing spaces
        cleaned_response_symptoms = [symptom.strip() for symptom in response_json['symptoms']]
        
        # Verify the symptoms are correct (after cleaning the response)
        self.assertEqual(cleaned_response_symptoms, expected_symptoms)


    def test_predictthediseases_valid(self): 
        """Test the /predictthediseases endpoint with valid input."""
        test_data = {
            "symptoms": "prolonged_cough,chest_pain,fatigue,yellowing_of_eyes,breathlessness,sweating,loss_of_appetite,phlegm,night_sweats,high_fever"
        }

        response = self.client.post('/predictthediseases', json=test_data)
        
        # Print the response content for debugging
        print(response.data)  # This will print the error details in the terminal/logs
        
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn('predicted_disease', response_json)
        
        # Expected predicted disease
        expected_predicted_disease = "Tuberculosis"
        
        # Verify the predicted disease
        self.assertEqual(response_json['predicted_disease'], expected_predicted_disease)

    def test_predictthediseases_no_symptoms(self):
        """Test the /predictthediseases endpoint with no symptoms."""
        test_data = {
            "symptoms": ""
        }
        
        response = self.client.post('/predictthediseases', json=test_data)
        
        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()
        self.assertIn('error', response_json)

    # def test_getpreventions_valid(self): #F
    #     """Test the /getpreventions endpoint with valid input."""
    #     test_data = {
    #         "diseases": "fever"
    #     }
        
    #     response = self.client.post('/getpreventions', json=test_data)
        
    #     self.assertEqual(response.status_code, 200)
    #     response_json = response.get_json()
    #     self.assertIn('description', response_json)
    #     self.assertIn('prevntion_list', response_json)

    def test_getpreventions_missing_disease(self): #F
        """Test the /getpreventions endpoint with missing disease."""
        test_data = {}
        
        response = self.client.post('/getpreventions', json=test_data)
        
        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()
        self.assertIn('error', response_json)

if __name__ == '__main__':
    unittest.main()
