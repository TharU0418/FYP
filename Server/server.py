from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import pickle
import re
import numpy as np
import gensim.downloader as api
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)

glove_vectors = api.load("glove-wiki-gigaword-100")


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
    df_preventions = pd.read_csv('DB/symptom_precaution.csv')


# Define the CustomLabelEncoder class (same as in your training script)
# class CustomLabelEncoder:
#     def __init__(self, start=0):
#         self.start = start
#         self.classes_ = []
    
#     def fit_transform(self, y):
#         self.classes_ = sorted(set(y))  # Get unique classes
#         class_map = {class_: i for i, class_ in enumerate(self.classes_)}
#         return np.array([class_map[class_] + self.start for class_ in y])
class CustomLabelEncoder(LabelEncoder):
    def __init__(self, start=0):
        self.start = start
        super().__init__()

    def fit_transform(self, y):
        encoded = super().fit_transform(y)
        encoded += self.start
        return encoded
    
    #def inverse_transform(self, y):
     #   return [self.classes_[i - self.start] for i in y]  # Inverse transformation
   

# Load the saved models and encoders
with open("Models/rf_model.pkl", "rb") as model_file:
    rf_model = pickle.load(model_file)

with open("Models/label_encoder.pkl", "rb") as le_file:
    encoder = pickle.load(le_file)

with open("Models/mlb.pkl", "rb") as mlb_file:
    mlb = pickle.load(mlb_file)


# Load the saved models for sentences

with open('Models/sentence/svm_model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

with open('Models/sentence/scaler.pkl', 'rb') as sca_file:
    scale_sen = pickle.load(sca_file)

with open('Models/sentence/label_encoder.pkl', 'rb') as le_file:
    label_encoder2 = pickle.load(le_file)


# setence model functions

def get_word_embeddings(sentence):
    words = sentence.split()
    embeddings = [glove_vectors[word] for word in words if word in glove_vectors]

    if embeddings:
        return np.mean(embeddings, axis=0)
    else:
        return np.zeros(100)


# Helper function to clean and process user input symptoms
# # def strip_to_basic_token(symptoms):
# #     if isinstance(symptoms, str):
# #         symptoms = [symptoms]
    
# #     symptoms = [symptom.strip().lower().replace(' ', '_').replace('_', ' ') for symptom in symptoms]
# #     return [re.sub(r'\s+', ' ', symptom) for symptom in symptoms]

def strip_to_basic_tokens(text):
    # Remove double spaces and underscores, then split by commas and lowercase the tokens
    text = re.sub(r'[_\s]+', ' ', text)
    tokens = [token.strip().lower() for token in text.split(',')]
    return tokens


# Get diseases names based on symptoms
@app.route('/get_diseases_name', methods= ['POST'])
def get_diseases_name():
    try:
        getSymptomCSV();
        data = request.json
        symptom_input = data['symptom_user_input']

        print('symptom_input', symptom_input)
        print('df_symptoms', df_symptoms)

        matching_diseases = df_symptoms[df_symptoms['symptom'] == symptom_input]
        print('matching_diseases', matching_diseases)

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
        symptoms =  data.get('symptoms', "")

        print('symptoms', symptoms)
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided."}), 400


        false_return = 'Not_Available'
        no_null_count = len([s for s in symptoms if s])

        # If user select less than 1 symptom return 'NO'
        if no_null_count <= 1:
            return jsonify({"predicted_illness" : false_return})

        basic_tokens = strip_to_basic_tokens(symptoms)

        one_hot_encoded_sample = mlb.transform([basic_tokens])

        one_hot_df = pd.DataFrame(one_hot_encoded_sample, columns=mlb.classes_)

        missing_columns = set(mlb.classes_) - set(one_hot_df.columns)
        for col in missing_columns:
            one_hot_df[col] = 0

        one_hot_df = one_hot_df[mlb.classes_]

        y_pred = rf_model.predict(one_hot_df)

        if not y_pred.any():
            return jsonify({"predicted_disease": "No_Matching"}), 200

        predicted_class_index = np.argmax(y_pred)
        predicted_disease = encoder.inverse_transform([predicted_class_index])[0]

        return jsonify({"predicted_disease": predicted_disease}), 200


    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    
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

# Get illness preventions and treatments
@app.route('/getpreventions', methods=['POST'])
def getPreventions():
    try:
        getIllnessDesription()
        getPreventionDetails()

        data = request.json
        diseases = data.get('diseases')

        discription = df_diseases_list[df_diseases_list['Disease'] == diseases]
        discription = discription.values[0][1]

        print('discription', discription)

        prevention_list = []

        prevention_row = df_preventions[df_preventions['Disease'] == diseases]

        if not prevention_row.empty:
            for i in range(1, len(prevention_row.columns)):
                prevention = prevention_row.iloc[0, i]
                if pd.notna(prevention):
                    prevention_list.append(prevention)

        return jsonify({"description" : discription, "prevntion_list" : prevention_list})


    except Exception as e:
        return jsonify({"error" : str(e)}), 500    



@app.route('/get_sentence', methods= ['POST'])
def get_sentence():
    try:

        data = request.json
        sentence = data.get('sentence')

        embeddings = get_word_embeddings(sentence)

        embeddings = scale_sen.transform([embeddings])

        prediction = svm_model.predict(embeddings)
        predicted_label = label_encoder2.inverse_transform(prediction)


        return jsonify({'symptom' : predicted_label[0]})
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)