#!/usr/bin/env python3
"""
Quick test script for the Phishing Detection API
"""

def test_feature_extraction():
    """Test the feature extraction function"""
    print("🔧 Testing Feature Extraction...")
    
    try:
        from app import extract_features_from_url
        
        # Test with a simple URL
        url = "https://www.google.com"
        features = extract_features_from_url(url)
        
        print(f"✅ Features extracted: {len(features)}")
        print(f"✅ First 10 features: {features[:10]}")
        print(f"✅ All features sum: {sum(features)}")
        
        if len(features) == 49:
            print("✅ Feature extraction working correctly!")
            return True
        else:
            print(f"❌ Expected 49 features, got {len(features)}")
            return False
            
    except Exception as e:
        print(f"❌ Error in feature extraction: {e}")
        return False

def test_model_loading():
    """Test if the model can be loaded"""
    print("\n🤖 Testing Model Loading...")
    
    try:
        import pickle
        import numpy as np
        
        # Load the model
        with open("phishing_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Test prediction
        dummy_features = [0] * 49
        prediction = model.predict([dummy_features])[0]
        
        print(f"✅ Model loaded successfully")
        print(f"✅ Test prediction: {prediction}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        from app import app
        import requests
        
        # Test health check
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Health check endpoint working")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        
        # Test prediction endpoint
        test_data = {"url": "https://www.google.com"}
        with app.test_client() as client:
            response = client.post('/predict', json=test_data)
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Prediction endpoint working")
                print(f"✅ Prediction: {data.get('prediction')}")
                print(f"✅ Features extracted: {data.get('features_extracted')}")
                return True
            else:
                print(f"❌ Prediction endpoint failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def main():
    """Run all tests"""
    print("🛡️ Phishing Detection System - Quick Test")
    print("=" * 50)
    
    tests = [
        test_feature_extraction,
        test_model_loading,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main() 