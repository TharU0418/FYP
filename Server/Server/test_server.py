from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import pickle
import re
import numpy as np
from transformers import BertTokenizer, TFBertForSequenceClassification, TFAutoModelForSequenceClassification
from transformers import AutoModel, AutoTokenizer
import tensorflow as tf


app = Flask(__name__)
CORS(app)


# Load the saved models for sentences
# Load the trained model, tokenizer, and label mapping
model = TFBertForSequenceClassification.from_pretrained('./sen_models')
#tokenizer = BertTokenizer.from_pretrained('./sen_models')

model_name = "tharu0418/sentence-model"

# Load the model and tokenizer (with TensorFlow)
model = AutoModel.from_pretrained(model_name, from_tf=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# model_name = 'bert-base-uncased'  # Or any other model you are using
# model = TFBertForSequenceClassification.from_pretrained(model_name)
# tokenizer = BertTokenizer.from_pretrained(model_name)


with open('sen_models/label_mapping.pkl', 'rb') as f:
    label_mapping = pickle.load(f)

def predict_illness(text):
    # Tokenize the input text
    encoding = tokenizer(text, truncation=True, padding=True, max_length=128, return_tensors="tf")
    
    # Get model output
    outputs = model(encoding)
    
    # Print outputs to debug structure
    print("Model outputs:", outputs)
    
    # If the output is a tuple, the logits should be the first element
    logits = outputs[0] if isinstance(outputs, tuple) else outputs
    
    # Check if logits are correctly extracted
    print("Logits:", logits)
    
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