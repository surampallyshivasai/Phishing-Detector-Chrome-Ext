from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
import re
import urllib.parse
import ssl
import socket
import requests
from urllib.parse import urlparse
import tldextract
import whois
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)  # Allow frontend/browser extension requests

# Global variable for model
model = None

def load_model():
    """Load the trained ML model"""
    global model
    try:
        with open("phishing_model.pkl", "rb") as f:
            model = pickle.load(f)
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def extract_features_from_url(url):
    """
    Extract 49 features from URL for phishing detection
    Based on the dataset features we analyzed
    """
    features = []
    
    try:
        # Parse URL
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query
        
        # Basic URL features
        features.append(len(url))  # URLLength
        features.append(len(domain))  # DomainLength
        
        # Check if domain is IP
        is_ip = bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain))
        features.append(1 if is_ip else 0)  # IsDomainIP
        
        # URL similarity (simplified)
        features.append(100)  # URLSimilarityIndex (placeholder)
        
        # Character continuation rate
        features.append(1.0)  # CharContinuationRate (placeholder)
        
        # TLD legitimate probability
        tld = domain.split('.')[-1] if '.' in domain else ''
        legitimate_tlds = ['com', 'org', 'net', 'edu', 'gov', 'mil']
        features.append(0.8 if tld in legitimate_tlds else 0.2)  # TLDLegitimateProb
        
        # URL character probability
        features.append(0.5)  # URLCharProb (placeholder)
        
        # TLD analysis
        features.append(len(tld))  # TLDLength
        
        # Subdomain count
        subdomain_count = len(domain.split('.')) - 1
        features.append(subdomain_count)  # NoOfSubDomain
        
        # Obfuscation detection
        obfuscated_chars = len(re.findall(r'%[0-9A-Fa-f]{2}', url))
        features.append(1 if obfuscated_chars > 0 else 0)  # HasObfuscation
        features.append(obfuscated_chars)  # NoOfObfuscatedChar
        features.append(round(obfuscated_chars / len(url), 3) if len(url) > 0 else 0)  # ObfuscationRatio
        
        # Character analysis
        letters = len(re.findall(r'[a-zA-Z]', url))
        digits = len(re.findall(r'\d', url))
        special_chars = len(re.findall(r'[^a-zA-Z0-9]', url))
        
        features.append(letters)  # NoOfLettersInURL
        features.append(round(letters / len(url), 3) if len(url) > 0 else 0)  # LetterRatioInURL
        features.append(digits)  # NoOfDegitsInURL
        features.append(round(digits / len(url), 3) if len(url) > 0 else 0)  # DegitRatioInURL
        
        # Special characters
        features.append(url.count('='))  # NoOfEqualsInURL
        features.append(url.count('?'))  # NoOfQMarkInURL
        features.append(url.count('&'))  # NoOfAmpersandInURL
        features.append(special_chars)  # NoOfOtherSpecialCharsInURL
        features.append(round(special_chars / len(url), 3) if len(url) > 0 else 0)  # SpacialCharRatioInURL
        
        # HTTPS check
        features.append(1 if parsed.scheme == 'https' else 0)  # IsHTTPS
        
        # Content analysis (simplified)
        features.append(100)  # LineOfCode (placeholder)
        features.append(len(url))  # LargestLineLength (placeholder)
        features.append(1)  # HasTitle (placeholder)
        features.append(0.5)  # DomainTitleMatchScore (placeholder)
        features.append(0.5)  # URLTitleMatchScore (placeholder)
        features.append(1)  # HasFavicon (placeholder)
        features.append(1)  # IsResponsive (placeholder)
        features.append(0)  # NoOfURLRedirect (placeholder)
        features.append(0)  # NoOfSelfRedirect (placeholder)
        features.append(1)  # HasDescription (placeholder)
        features.append(0)  # NoOfPopup (placeholder)
        features.append(0)  # NoOfiFrame (placeholder)
        features.append(0)  # HasExternalFormSubmit (placeholder)
        features.append(0)  # HasSocialNet (placeholder)
        features.append(0)  # HasSubmitButton (placeholder)
        features.append(0)  # HasHiddenFields (placeholder)
        features.append(0)  # HasPasswordField (placeholder)
        features.append(0)  # Bank (placeholder)
        features.append(0)  # Pay (placeholder)
        features.append(0)  # Crypto (placeholder)
        features.append(1)  # HasCopyrightInfo (placeholder)
        features.append(5)  # NoOfImage (placeholder)
        features.append(3)  # NoOfCSS (placeholder)
        features.append(2)  # NoOfJS (placeholder)
        features.append(1)  # NoOfSelfRef (placeholder)
        features.append(0)  # NoOfEmptyRef (placeholder)
        features.append(0)  # NoOfExternalRef (placeholder)
        
    except Exception as e:
        # If any error occurs, return 49 zeros
        print(f"Error extracting features: {e}")
        features = [0] * 49
    
    # Ensure we have exactly 49 features
    while len(features) < 49:
        features.append(0)
    
    return features[:49]

@app.route('/')
def home():
    return jsonify({"message": "Phishing detection API is running ✅"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Load model if not already loaded
        if model is None:
            if not load_model():
                return jsonify({'error': "Failed to load ML model"}), 500
        
        data = request.get_json()

        # Check if 'url' is provided
        if 'url' not in data:
            return jsonify({'error': "Missing 'url' in request"}), 400

        url = data['url']

        # Extract features from the URL
        features = extract_features_from_url(url)

        # Validate feature length
        if len(features) != 49:
            return jsonify({'error': f"Expected 49 features, got {len(features)}"}), 400

        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)[0]
        
        # Get prediction probability
        prediction_proba = model.predict_proba(features)[0]
        phishing_probability = prediction_proba[1] if len(prediction_proba) > 1 else 0

        return jsonify({
            'prediction': int(prediction),
            'phishing_probability': round(float(phishing_probability), 3),
            'safe_probability': round(float(prediction_proba[0]), 3),
            'features_extracted': len(features[0])
        })
    except Exception as e:
        return jsonify({'error': f"Something went wrong: {str(e)}"}), 500

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        print("✅ Model loaded successfully")
    else:
        print("❌ Failed to load model")
    
    app.run(debug=True)
