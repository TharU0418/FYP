from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import re

app = Flask(__name__)

from sklearn.preprocessing import LabelEncoder

class CustomLabelEncoder(LabelEncoder):
    def __init__(self, start=0):
        self.start = start
        super().__init__()

    def fit_transform(self, y):
        encoded = super().fit_transform(y)
        encoded += self.start
        return encoded



# Load the saved models and encoders
with open("Models/rf_model.pkl", "rb") as model_file:
    rf_model = pickle.load(model_file)

with open("Models/label_encoder.pkl", "rb") as le_file:
    encoder = pickle.load(le_file)

with open("Models/mlb.pkl", "rb") as mlb_file:
    mlb = pickle.load(mlb_file)

# Function to preprocess symptoms
def strip_to_basic_tokens(text):
    # Remove double spaces and underscores, then split by commas and lowercase the tokens
    text = re.sub(r'[_\s]+', ' ', text)
    tokens = [token.strip().lower() for token in text.split(',')]
    return tokens



# API endpoint for illness prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the symptoms from the request
        data = request.json
        symptoms = data.get("symptoms", "")

        if not symptoms:
            return jsonify({"error": "No symptoms provided."}), 400

        # Preprocess the symptoms
        basic_tokens = strip_to_basic_tokens(symptoms)

        # One-hot encode the symptoms using the loaded MultiLabelBinarizer
        one_hot_encoded_sample = mlb.transform([basic_tokens])

        # Create a DataFrame for prediction
        one_hot_df = pd.DataFrame(one_hot_encoded_sample, columns=mlb.classes_)

        # Ensure all columns from training are present
        missing_columns = set(mlb.classes_) - set(one_hot_df.columns)
        for col in missing_columns:
            one_hot_df[col] = 0

        # Reorder columns to match the original training DataFrame
        one_hot_df = one_hot_df[mlb.classes_]

        # Make the prediction
        y_pred = rf_model.predict(one_hot_df)

        # Check if all values in `y_pred` are `False`
        if not y_pred.any():
            return jsonify({"predicted_disease": "No_Matching"}), 200

        # Decode the prediction
        predicted_class_index = np.argmax(y_pred)
        predicted_disease = encoder.inverse_transform([predicted_class_index])[0]

        return jsonify({"predicted_disease": predicted_disease}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
