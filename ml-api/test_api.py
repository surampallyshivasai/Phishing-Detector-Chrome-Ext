#!/usr/bin/env python3
"""
Test script for the Phishing Detection API
"""

import requests
import json
import time

def test_api():
    """Test the phishing detection API"""
    
    base_url = "http://127.0.0.1:5000"
    
    # Test URLs
    test_urls = [
        "https://www.google.com",  # Safe
        "https://www.paypal.com",  # Safe
        "https://paypal-secure-login.xyz",  # Suspicious
        "https://login-facebook.secure-account.xyz",  # Very suspicious
        "https://192.168.1.1",  # IP address
        "https://example.com/login?redirect=http://evil.com",  # Suspicious redirect
    ]
    
    print("🛡️ Phishing Detection API Test")
    print("=" * 50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on localhost:5000")
        return
    
    print("\n🔍 Testing URL Analysis:")
    print("-" * 50)
    
    for url in test_urls:
        try:
            response = requests.post(
                f"{base_url}/predict",
                json={"url": url},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = "🟢 SAFE" if data['prediction'] == 0 else "🔴 PHISHING"
                prob = data.get('phishing_probability', 0)
                
                print(f"URL: {url}")
                print(f"Result: {prediction}")
                print(f"Phishing Probability: {prob:.1%}")
                print(f"Features Extracted: {data.get('features_extracted', 0)}")
                print("-" * 30)
            else:
                print(f"❌ Error testing {url}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception testing {url}: {e}")
        
        time.sleep(1)  # Rate limiting
    
    print("\n✅ Test completed!")

def test_feature_extraction():
    """Test feature extraction specifically"""
    
    print("\n🔧 Testing Feature Extraction:")
    print("-" * 50)
    
    # Import the feature extraction function
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from app import extract_features_from_url
    
    test_url = "https://www.google.com"
    features = extract_features_from_url(test_url)
    
    print(f"URL: {test_url}")
    print(f"Features extracted: {len(features)}")
    print(f"First 10 features: {features[:10]}")
    print(f"All features sum: {sum(features)}")
    
    if len(features) == 50:
        print("✅ Feature extraction working correctly")
    else:
        print(f"❌ Expected 50 features, got {len(features)}")

if __name__ == "__main__":
    test_api()
    test_feature_extraction() 