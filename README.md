# 🛡️ Phishing URL Detection System

A machine learning-based phishing detection system with a Flask API backend and Chrome browser extension frontend.

## 🚀 Features

- **Real-time URL Analysis**: Analyzes URLs for phishing indicators
- **Machine Learning Model**: Random Forest classifier trained on phishing dataset
- **Browser Extension**: Chrome extension for instant phishing detection
- **REST API**: Flask API for programmatic access
- **Feature Extraction**: 50+ features extracted from URLs including:
  - URL length and structure analysis
  - Domain age and SSL certificate validation
  - Character frequency analysis
  - Suspicious keyword detection
  - Obfuscation detection

## 📁 Project Structure

```
PhishingMLProject/
├── ml-api/                    # Backend API
│   ├── app.py                # Flask API server
│   ├── train_model.py        # Model training script
│   ├── requirements.txt      # Python dependencies
│   ├── phishing_dataset.csv  # Training dataset
│   └── phishing_model.pkl   # Trained model
└── phishing-extension/       # Browser extension
    ├── manifest.json         # Extension manifest
    ├── popup.html           # Extension UI
    ├── popup.js             # Extension logic
    └── icons/               # Extension icons
```

## 🛠️ Setup Instructions

### 1. Backend API Setup

```bash
# Navigate to API directory
cd ml-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the model (if needed)
python train_model.py

# Start the API server
python app.py
```

The API will be available at `http://127.0.0.1:5000`

### 2. Browser Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the `phishing-extension` folder
5. The extension will appear in your toolbar

## 🔧 API Endpoints

### Health Check
```
GET http://127.0.0.1:5000/
```
Response:
```json
{
  "message": "Phishing detection API is running ✅"
}
```

### Predict Phishing
```
POST http://127.0.0.1:5000/predict
Content-Type: application/json

{
  "url": "https://example.com"
}
```

Response:
```json
{
  "prediction": 0,
  "phishing_probability": 0.123,
  "safe_probability": 0.877,
  "features_extracted": 50
}
```

- `prediction`: 0 = Safe, 1 = Phishing
- `phishing_probability`: Probability of being phishing (0-1)
- `safe_probability`: Probability of being safe (0-1)

## 🧪 Testing with Postman

### Test Cases:

1. **Safe URL:**
```json
{
  "url": "https://www.google.com"
}
```

2. **Suspicious URL:**
```json
{
  "url": "https://paypal-secure-login.xyz"
}
```

3. **Invalid Request:**
```json
{
  "wrong_field": "https://example.com"
}
```

## 🔍 Features Extracted

The system extracts 50 features from URLs:

1. **URL Structure Features:**
   - URL length
   - Domain length
   - TLD length
   - Subdomain count
   - IP vs domain usage

2. **Character Analysis:**
   - Letter count and ratio
   - Digit count and ratio
   - Special character analysis
   - Character continuation rate

3. **Security Features:**
   - HTTPS usage
   - SSL certificate validation
   - Domain age
   - Obfuscation detection

4. **Content Analysis:**
   - Suspicious keywords
   - TLD legitimacy
   - URL similarity index

## 🎯 Usage

### Browser Extension:
1. Navigate to any website
2. Click the extension icon
3. View the phishing analysis result

### API Usage:
```python
import requests

response = requests.post('http://127.0.0.1:5000/predict', 
                        json={'url': 'https://example.com'})
result = response.json()
print(f"Prediction: {'Phishing' if result['prediction'] else 'Safe'}")
```

## 📊 Model Performance

The Random Forest classifier is trained on a comprehensive phishing dataset with features including:
- URL characteristics
- Domain information
- SSL certificate data
- Content analysis
- Behavioral patterns

## 🔧 Troubleshooting

### Common Issues:

1. **API not starting:**
   - Check if port 5000 is available
   - Ensure all dependencies are installed
   - Verify the model file exists

2. **Extension not working:**
   - Ensure API is running on localhost:5000
   - Check browser console for errors
   - Verify CORS is enabled

3. **Model prediction errors:**
   - Check if the model file is corrupted
   - Retrain the model if needed
   - Verify feature extraction is working

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational and research purposes.

## ⚠️ Disclaimer

This tool is for educational purposes. Always use multiple security measures and don't rely solely on automated detection for critical security decisions. 