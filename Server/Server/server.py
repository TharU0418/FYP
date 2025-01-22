from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pickle
import re
import pandas as pd
import numpy as np
import random
    
app = Flask(__name__)
CORS(app)

data = pd.read_json('DB/intense.json')

def getSymptomCSV():
    global df_symptoms
    df_symptoms = pd.read_csv('DB/Symptoms.csv')

def getIllnessCSV():
    global df_illness
    df_illness = pd.read_csv('DB/Illness.csv')
def getIllnessDesription():
    global df_diseases_list
    df_diseases_list = pd.read_csv('DB/symptom_Description.csv')

def getPreventionDetails():
    global df_preventions
    df_preventions = pd.read_csv('DB/symptom_precaution.csv',  encoding='ISO-8859-1')

def getTreatmentDetails():
    global df_treatments
    df_treatments = pd.read_csv('DB/symptom_treatments.csv', encoding='ISO-8859-1')


with open('Models/sentence_models/model.pkl', 'rb') as f:
    model = joblib.load(f)
with open('Models/sentence_models/vectorizer.pkl', 'rb') as f:
    vectorizer = joblib.load(f)
with open('Models/sentence_models/intent_labels.pkl', 'rb') as f:
    intent_labels = joblib.load(f)


# Load the saved models and encoders **after** defining the class
with open("Models/random_forest_model.pkl", "rb") as model_file:
    rf_model = pickle.load(model_file)

with open("Models/multilabel_binarizer.pkl", "rb") as mlb:
    mlb = pickle.load(mlb)

with open("Models/label_encoder.pkl", "rb") as encoder:
    encoder = pickle.load(encoder)

with open("Models/df_encoded.pkl", "rb") as df_encoded:
    df_encoded = pickle.load(df_encoded)

with open("Models/offset.pkl", "rb") as offset:
    offset = pickle.load(offset)


def strip_to_basic_tokens(text):
    # Remove double spaces and underscores, then split by commas and lowercase the tokens
    text = re.sub(r'[_\s]+', ' ', text)
    tokens = [token.strip().lower() for token in text.split(',')]
    return tokens


def predict_symptom(text):
    # Vectorize the input text
    text_vec = vectorizer.transform([text])
    
    # Make the prediction (predicting the index of the intent)
    intent_pred_index = model.predict(text_vec)[0]
    
    # Map the predicted index back to the actual intent and get a random response
    predicted_responses = data['intents'][intent_pred_index]['responses']
    if isinstance(predicted_responses, list):
        predicted_response = random.choice(predicted_responses)
    else:
        predicted_response = predicted_responses  # In case it's a string
    
    return predicted_response

# def predict_symptom(text):
#     text_vec = vectorizer.transform([text])  # Transform input sentence into a vector
#     intent_pred = model.predict(text_vec)[0]  # Get predicted value (likely a string)

#     # Check if the prediction is a string (as model may return a string label)
#     if isinstance(intent_pred, str):
#         # Convert the predicted string to its corresponding label using intent_labels
#         if intent_pred in intent_labels:
#             predict_int = intent_pred  # If it's already in intent_labels, return it directly
#             return predict_int
#         else:
#             raise ValueError(f"Prediction '{intent_pred}' not found in intent_labels.")
#     else:
#         raise ValueError(f"Unexpected prediction type: {type(intent_pred)}")


def predict_illness(symptoms):

    # Apply the tokenization process to the sample symptoms
    basic_tokens = strip_to_basic_tokens(symptoms)

    # Step 2: One-hot encode the tokens using the MultiLabelBinarizer (mlb) used during training
    one_hot_encoded_sample = mlb.transform([basic_tokens])
    
     # Create a DataFrame from the one-hot encoded sample
    one_hot_df = pd.DataFrame(one_hot_encoded_sample, columns=mlb.classes_)
    
    # Ensure that all columns (features) from training data are present (fill with 0 for missing columns)
    missing_columns = set(df_encoded.columns) - set(one_hot_df.columns)
    for col in missing_columns:
        one_hot_df[col] = 0
    
    # Reorder columns to match the original training DataFrame's order
    one_hot_df = one_hot_df[df_encoded.columns.difference(['Disease'])]

    # Step 3: Make prediction
    y_pred = rf_model.predict(one_hot_df)

    # Check if all values in `y_pred` are `False`
    if not y_pred.any():
        return "No_Matching"
    
    # Step 4: Decode the prediction (back to the disease label)
    predicted_class_index = np.argmax(y_pred)
    
    # Get the original encoded value
    predicted_encoded_value = encoder.transform(encoder.classes_)[predicted_class_index]
    
    # Apply the offset to get the final encoded value
    predicted_encoded_value_with_offset = predicted_encoded_value + offset

    # Create the mapping for later
    label_mapping = {v + offset: k for k, v in zip(encoder.classes_, range(len(encoder.classes_)))}
    
    # Get the original class name based on the offset value
    predicted_disease_name = label_mapping[predicted_encoded_value_with_offset]

    return predicted_disease_name



@app.route('/get_sentence', methods = ['POST'])
def get_sentence():
    try:

        data = request.json
        sentence = data.get('sentence')

        # Check if the input is a string
        if not isinstance(sentence, str):
            return jsonify({"error" : " Invalid sentence"}), 400
        
        # Check if the input string is empty
        if sentence.strip() == "":
            return jsonify({"error": "Please enter your sentence"}), 400

        predicted_symptom = predict_symptom(sentence)

        return jsonify({"symptom" : predicted_symptom})

    except Exception as e:
        return jsonify({"error" : str(e)}), 500 
    

########################################


# Get diseases names based on symptoms
@app.route('/get_diseases_name', methods= ['POST'])
def get_diseases_name():
    try:
        getSymptomCSV()

        data = request.json
        symptom_input = data['symptom_user_input']

        matching_diseases = df_symptoms[df_symptoms['symptom'] == symptom_input]

        # Check if matching_diseases is empty
        if matching_diseases.empty:
            return jsonify({"message": "Enter correct symptom"}), 400


        matching_diseases = matching_diseases.iloc[0, 1:].dropna().unique()

        return jsonify({"diseases" : matching_diseases.tolist()})


    except Exception as e:
        return jsonify({"error" : str(e)}), 500

# Get all symptoms names based on diseases
@app.route('/get_illess_name', methods = ['POST'])
def get_illess_name():
    try:
        getIllnessCSV()
        data = request.json
        diseases_input = data['diseases_input']

        print('diseases_input', diseases_input)

        matching_symptoms = df_illness[df_illness['Disease'] == diseases_input]
        matching_symptoms = matching_symptoms.iloc[0, 1:].dropna().unique()

        return jsonify({"symptoms" : matching_symptoms.tolist()})

    except Exception as e:
        return jsonify({"error" : str(e)}), 500



# Predict user's diseases
@app.route('/predictthediseases', methods = ['POST'])
def predictthediseases():
    try:

        data = request.json

        if not data or 'symptoms' not in data:
            return jsonify({'error': 'No symptoms provided in the request'}), 400
        
        symptoms =  data.get('symptoms', "")

        print('symptoms', symptoms)
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided."}), 400


        false_return = 'Not_Available'
        no_null_count = len([s for s in symptoms if s])

        # If user select less than 1 symptom return 'NO'
        if no_null_count <= 1:
            return jsonify({"predicted_illness" : false_return})

        prediction = predict_illness(symptoms)

        
        # if not y_pred.any():
        #     return jsonify({"predicted_disease": "No_Matching"}), 200

        # predicted_class_index = np.argmax(y_pred)
        # predicted_disease = encoder.inverse_transform([predicted_class_index])[0]

        return jsonify({"predicted_disease": prediction}), 200


    except Exception as e:
        return jsonify({"error" : str(e)}), 500
 

# Get illness preventions and treatments
@app.route('/getpreventions', methods=['POST'])
def getPreventions():
    try:
        getIllnessDesription()
        getPreventionDetails()
        getTreatmentDetails()

        data = request.json
        diseases = data.get('diseases')

        discription = df_diseases_list[df_diseases_list['Disease'] == diseases]
        discription = discription.values[0][1]

        print('discription', discription)

        prevention_list = []
        treatment_list = []

        prevention_row = df_preventions[df_preventions['Disease'] == diseases]

        treatment_row = df_treatments[df_treatments['Disease'] == diseases]


        if not prevention_row.empty:
            for i in range(1, len(prevention_row.columns)):
                prevention = prevention_row.iloc[0, i]
                if pd.notna(prevention):
                    prevention_list.append(prevention)


        if not treatment_row.empty:
            for i in range(1, len(treatment_row.columns)):
                treatment = treatment_row.iloc[0, i]
                if pd.notna(treatment):
                    treatment_list.append(treatment)

        


        return jsonify({"description" : discription, "prevntion_list" : prevention_list, "treatment_list" : treatment_list})


    except Exception as e:
        return jsonify({"error" : str(e)}), 500    



if __name__ == '__main__':
    app.run(debug=True)