from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import pickle
import re
import numpy as np

app = Flask(__name__)
CORS(app)


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
   

# Load the saved models and encoders
with open('Models/random_forest_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

with open('Models/label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

with open('Models/mlb_encoder.pkl', 'rb') as mlb_file:
    mlb = pickle.load(mlb_file)


# Helper function to clean and process user input symptoms
def strip_to_basic_token(symptoms):
    if isinstance(symptoms, str):
        symptoms = [symptoms]
    
    symptoms = [symptom.strip().lower().replace(' ', '_').replace('_', ' ') for symptom in symptoms]
    return [re.sub(r'\s+', ' ', symptom) for symptom in symptoms]



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
        symptoms =  data.get('symptoms', [])

        print('symptoms', symptoms)
        
        false_return = 'Not_Available'
        no_null_count = len([s for s in symptoms if s])

        # If user select less than 1 symptom return 'NO'
        if no_null_count <= 1:
            return jsonify({"predicted_illness" : false_return})

        cleaned_input = strip_to_basic_token(symptoms)

        user_input_encoded = pd.DataFrame(mlb.transform([cleaned_input]), columns=mlb.classes_)


        final_user_input = pd.concat([pd.DataFrame(columns=mlb.classes_), user_input_encoded], axis=0)
        final_user_input = final_user_input.drop(columns=['Disease'], errors='ignore')


        # Predict the class for the user input
        user_pred = rf_model.predict(final_user_input)

        print('user_pred', user_pred)


        predicted_class_index = np.argmax(user_pred)
        prediction_encoded = label_encoder.classes_[predicted_class_index]

        return jsonify({'predicted_illness': prediction_encoded})


    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    

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

if __name__ == '__main__':
    app.run(debug=True)