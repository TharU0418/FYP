from flask import Flask, request, jsonify
import numpy as np
import pickle
import re
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
import gensim.downloader as api
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained models
with open('Model/svm_model.pkl', 'rb') as file:
    classifier = pickle.load(file)

with open('Model/label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)

with open('Model/scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# GloVe model
glove_vectors = api.load("glove-wiki-gigaword-100")

# Stopwords and custom stopwords
custom_stopwords = set(stopwords.words('english')).union({
    'doctor', 'feel', 'feeling', 'experience', 'experiencing', 'sensation', 'really', 'get', 'got', 'just'
})

# Preprocessing function
# def preprocess_sentence(sentence):
#     sentence = re.sub(r'[^a-zA\s]', '', sentence)
#     tokens = sentence.split()

#     tag_map = defaultdict(lambda: wn.NOUN)
#     tag_map['J'] = wn.ADJ
#     tag_map['V'] = wn.VERB
#     tag_map['R'] = wn.ADV

#     lemmatizer = WordNetLemmatizer()
#     stemmer = PorterStemmer()

#     final_words = []

#     for word, tag in pos_tag(tokens):
#         if word not in custom_stopwords and word.isalpha():
#             word_lemmatized = lemmatizer.lemmatize(word, tag_map[tag[0]])
#             word_stemmed = stemmer.stem(word_lemmatized)
#             final_words.append(word_stemmed)

#     return " ".join(final_words)

# Get word embeddings
def get_word_embeddings(sentence):
    words = sentence.split()
    embeddings = [glove_vectors[word] for word in words if word in glove_vectors]

    if embeddings:
        return np.mean(embeddings, axis=0)
    else:
        return np.zeros(100)

# Endpoint for symptom prediction
@app.route('/predict', methods=['POST'])
def predict_symptom():
    try:
        # Get the sentence from the POST request
        data = request.get_json()
        sentence = data['sentence']
        
        # Preprocess and get embeddings
       # preprocessed_sentence = preprocess_sentence(sentence)

        print('sentence', sentence)

        embeddings = get_word_embeddings(sentence)

        print('embeddings', embeddings)
        
        # Scale embeddings
        embeddings = scaler.transform([embeddings])
        
        print('////////////////////')

        print('embeddings', embeddings)


        # Make prediction
        prediction = classifier.predict(embeddings)
        predicted_label = label_encoder.inverse_transform(prediction)
        
        # Return the predicted symptom
        return jsonify({'symptom': predicted_label[0]})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
