from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
import os
import re
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

def load_and_predict(symptoms, model_dir="Models"):
    """
    Loads the saved model, binarizer, encoder, df_encoded and offset from the 'Models' folder
    and predicts the disease based on input symptoms.

    Args:
        symptoms (str): A comma-separated string of symptoms (e.g., "cough, fever, headache").
        model_dir (str, optional): The path to the directory containing the saved model files.
            Defaults to "Models"

    Returns:
        str: The predicted disease or "No_Matching" if no match found.
    """
    
    # Construct full paths to the saved components
    model_path = os.path.join(model_dir, 'random_forest_model.pkl')
    mlb_path = os.path.join(model_dir, 'multilabel_binarizer.pkl')
    encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
    df_encoded_path = os.path.join(model_dir, 'df_encoded.pkl')
    offset_path = os.path.join(model_dir, 'offset.pkl')

    # Load the saved components
    with open(model_path, 'rb') as file:
        rf_model = pickle.load(file)
    with open(mlb_path, 'rb') as file:
        mlb = pickle.load(file)
    with open(encoder_path, 'rb') as file:
        encoder = pickle.load(file)
    with open(df_encoded_path, 'rb') as file:
        df_encoded = pickle.load(file)
    with open(offset_path, 'rb') as file:
        offset = pickle.load(file)
        

    # Step 1: Preprocess the symptoms
    def strip_to_basic_tokens(text):
        # Remove double spaces and underscores, then split by commas and lowercase the tokens
        text = re.sub(r'[_\s]+', ' ', text)
        tokens = [token.strip().lower() for token in text.split(',')]
        return tokens
    
    # Apply the tokenization process to the sample symptoms
    basic_tokens = strip_to_basic_tokens(symptoms)
    print('basic_tokens', basic_tokens)

    # Step 2: One-hot encode the tokens using the MultiLabelBinarizer (mlb) used during training
    one_hot_encoded_sample = mlb.transform([basic_tokens])
    print('one_hot_encoded_sample', one_hot_encoded_sample)


    # Create a DataFrame from the one-hot encoded sample
    one_hot_df = pd.DataFrame(one_hot_encoded_sample, columns=mlb.classes_)
    print('one_hot_df', one_hot_df)


    # Ensure that all columns (features) from training data are present (fill with 0 for missing columns)
    missing_columns = set(df_encoded.columns) - set(one_hot_df.columns)
    for col in missing_columns:
        one_hot_df[col] = 0
    
    # Reorder columns to match the original training DataFrame's order
    one_hot_df = one_hot_df[df_encoded.columns.difference(['Disease'])]
    print('one_hot_df', one_hot_df)


    # Step 3: Make prediction
    y_pred = rf_model.predict(one_hot_df)
    print('y_pred', y_pred)

    # Check if all values in `y_pred` are `False`
    if not y_pred.any():
        return "No_Matching"
    
    # Step 4: Decode the prediction (back to the disease label)
    predicted_class_index = np.argmax(y_pred)
    print('predicted_class_index', predicted_class_index)

    
    # Get the original encoded value
    predicted_encoded_value = encoder.transform(encoder.classes_)[predicted_class_index]
    print('predicted_encoded_value', predicted_encoded_value)


    # Apply the offset to get the final encoded value
    predicted_encoded_value_with_offset = predicted_encoded_value + offset
    print('predicted_encoded_value_with_offset', predicted_encoded_value_with_offset)


    # Create the mapping for later
    label_mapping = {v + offset: k for k, v in zip(encoder.classes_, range(len(encoder.classes_)))}
    print('label_mapping', label_mapping)

    
    # Get the original class name based on the offset value
    predicted_disease_name = label_mapping[predicted_encoded_value_with_offset]

    return predicted_disease_name

@app.route('/predictthediseases', methods=['POST'])
def predict():
    """
    Handles POST requests to the '/predict' endpoint.
    Accepts symptoms as a string in the JSON request body
    and returns the predicted disease.
    """
    try:
        data = request.get_json()
        if not data or 'symptoms' not in data:
            return jsonify({'error': 'No symptoms provided in the request'}), 400
        symptoms = data['symptoms']
        prediction = load_and_predict(symptoms)
        return jsonify({'predicted_disease': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)