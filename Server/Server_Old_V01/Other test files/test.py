from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import pickle

from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

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

model = TFBertForSequenceClassification.from_pretrained('./sen_models')
tokenizer = BertTokenizer.from_pretrained('./sen_models')

with open('sen_models/label_mapping.pkl', 'rb') as f:
    label_mapping = pickle.load(f)


# setence model functions
# Function to predict illness
def predict_illness(text):

   
    # Tokenize the input text
    encoding = tokenizer(text, truncation=True, padding=True, max_length=128, return_tensors="tf")
    
    # Get model output
    outputs = model(encoding)
    logits = outputs.logits
    
    # Get the predicted class index
    predicted_class = tf.argmax(logits, axis=1).numpy()[0]
    
    # Map the predicted class index to the illness (intent)
    predicted_illness = label_mapping[predicted_class]
    
    return predicted_illness






@app.route('/get_sentence', methods= ['POST'])
def get_sentence():
    try:

        data = request.json
        sentence = data.get('sentence')

         # Check if the input is a string
        if not isinstance(sentence, str):
            return jsonify({"error": "Invalid sentence"}), 400
        
        # Check if the input string is empty
        if sentence.strip() == "":
            return jsonify({"error": "Please enter your sentence"}), 400
    

        # Predict the illness
        predicted_illness = predict_illness(sentence)
        
        # Return the result as a JSON response
        return jsonify({"symptom": predicted_illness})

        
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)