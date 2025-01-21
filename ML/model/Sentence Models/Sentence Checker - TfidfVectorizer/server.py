from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

with open('Models/model.pkl', 'rb') as f:
    model = joblib.load(f)
with open('Models/vectorizer.pkl', 'rb') as f:
    vectorizer = joblib.load(f)
with open('Models/intent_labels.pkl', 'rb') as f:
    intent_labels = joblib.load(f)


def predict_symptom(text):
    text_vec = vectorizer.transform([text])
    intent_pred = model.predict(text_vec)[0]
    predict_int = intent_labels[intent_pred]
    return predict_int

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


if __name__ == '__main__':
    app.run(debug=True)