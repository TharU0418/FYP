import unittest

from server import app


class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup the test client"""
        cls.client = app.test_client()

    def test_get_sentence_valid(self):
        """Test the /get_sentence endpoint with valid input."""
        test_data = {
            "sentence" : "The thought of food makes me feel nauseous"
        }

        response = self.client.post('/get_sentence', json = test_data)

        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn('symptom', response_json)
        self.assertEqual(response_json['symptom'], "loss_of_appetite")

    def test_get_sentence_valid_input(self):
        """Test the /get_sentence endpoint with invalid input format."""
        test_data = {
            "sentence": 123456
        }

        response = self.client.post('/get_sentence', json = test_data)

        self.assertEqual(response.status_code, 400)

    def test_get_sentence_missing_sentence(self):
        """Test the /get_sentence endpoint with missing 'sentence' field."""
        test_data = {}
        
        response = self.client.post('/get_sentence', json=test_data)
        
        self.assertEqual(response.status_code, 400)

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

    # def test_predictthediseases_valid(self): 
    #     """Test the /predictthediseases endpoint with valid input."""
    #     test_data = {
    #         "symptoms": "prolonged_cough,chest_pain,fatigue,yellowing_of_eyes,breathlessness,sweating,loss_of_appetite,phlegm,night_sweats,high_fever"
    #     }

    #     response = self.client.post('/predictthediseases', json=test_data)
        
    #     # Print the response content for debugging
    #     print(response.data)  # This will print the error details in the terminal/logs
        
    #     self.assertEqual(response.status_code, 200)
    #     response_json = response.get_json()
    #     self.assertIn('predicted_disease', response_json)
        
    #     # Expected predicted disease
    #     expected_predicted_disease = "Tuberculosis"
        
    #     # Verify the predicted disease
    #     self.assertEqual(response_json['predicted_disease'], expected_predicted_disease)


    def test_getpreventions_valid(self): #F
        """Test the /getpreventions endpoint with valid input."""
        test_data = {
            "diseases": "Chicken pox"
        }
            
        response = self.client.post('/getpreventions', json=test_data)
            
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        # Verify that the response contains the expected keys
        self.assertIn('description', response_json)
        self.assertIn('prevntion_list', response_json)
        self.assertIn('treatment_list', response_json)

        # Check if the description contains the expected text
        self.assertEqual(response_json['description'], "Chickenpox (known medically as varicella) is caused by a virus called the varicella-zoster virus. It’s spread quickly and easily from someone who is infected. Chickenpox is most common in children under the age of 10. Children usually catch chickenpox in winter and spring, particularly between March and May.")
        
        # Check if the prevention list matches the expected list
        expected_prevention_list = [
            "You'll need to stay away from school, nursery or work until all the spots have formed a scab. This is usually 5 days after the spots appeared.",
            "Drink plenty of fluid (try ice lollies if your child is not drinking) to avoid dehydration.",
            "Use cooling creams or gels from a pharmacy.",
            "Bathe in cool water and pat the skin dry (do not rub).",
            "Dress in loose clothes."
        ]
        self.assertEqual(response_json['prevntion_list'], expected_prevention_list)

        # Check if the treatment list matches the expected list
        self.assertEqual(response_json['treatment_list'], ["vaccine"])



if __name__ == '__main__':
    unittest.main()