import pickle
import re
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

# Define the CustomLabelEncoder class (same as in your training script)
class CustomLabelEncoder:
    def __init__(self, start=0):
        self.start = start
        self.classes_ = []
    
    def fit_transform(self, y):
        self.classes_ = sorted(set(y))  # Get unique classes
        class_map = {class_: i for i, class_ in enumerate(self.classes_)}
        return np.array([class_map[class_] + self.start for class_ in y])

    def inverse_transform(self, y):
        return [self.classes_[i - self.start] for i in y]  # Inverse transformation
    
# Initialize Flask app
app = Flask(__name__)

# Load the saved models and encoders
with open('random_forest_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

with open('label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

with open('mlb_encoder.pkl', 'rb') as mlb_file:
    mlb = pickle.load(mlb_file)

# Helper function to clean and process user input symptoms
def strip_to_basic_tokens(symptoms):
    if isinstance(symptoms, str):
        symptoms = [symptoms]  # Make it a list if it's a single string
    
    symptoms = [symptom.strip().lower().replace(' ', '_').replace('_', ' ') for symptom in symptoms]
    return [re.sub(r'\s+', ' ', symptom) for symptom in symptoms]

@app.route('/')
def home():
    return "Illness Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input (symptoms) from the request
    data = request.get_json()

    if 'symptoms' not in data:
        return jsonify({'error': 'No symptoms provided'}), 400

    user_input = data['symptoms']
    
    # Process and clean user input
    user_input_stripped = strip_to_basic_tokens(user_input)

    # Transform the symptoms using the MultiLabelBinarizer
    user_input_encoded = pd.DataFrame(mlb.transform([user_input_stripped]), columns=mlb.classes_)

    # Prepare the input data (make sure the column order matches the training data)
    final_user_input = pd.concat([pd.DataFrame(columns=mlb.classes_), user_input_encoded], axis=0)
    final_user_input = final_user_input.drop(columns=['Disease'], errors='ignore')

    # Predict the class for the user input
    user_pred = rf_model.predict(final_user_input)
    predicted_class_index = np.argmax(user_pred)
    prediction_encoded = label_encoder.classes_[predicted_class_index]

    # Return the prediction result
    return jsonify({'predicted_illness': prediction_encoded})

if __name__ == '__main__':
    app.run(debug=True)
