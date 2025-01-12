from flask import Flask, request, jsonify
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the trained model, tokenizer, and label mapping
model = TFBertForSequenceClassification.from_pretrained('./saved_model')
tokenizer = BertTokenizer.from_pretrained('./saved_model')

with open('label_mapping.pkl', 'rb') as f:
    label_mapping = pickle.load(f)

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

# Define the prediction endpoint
@app.route('/get_sentence', methods=['POST'])
def predict():
    # Get the data from the request
    data = request.get_json()

    # Check if the sentence is provided in the request
    if 'sentence' not in data:
        return jsonify({"error": "No sentence provided"}), 400

    # Get the sentence from the request
    sentence = data['sentence']
    
    # Predict the illness
    predicted_illness = predict_illness(sentence)
    
    # Return the result as a JSON response
    return jsonify({"predicted_illness": predicted_illness})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
