"""
Test script for Agent Utility API
Verifies all endpoints work correctly
"""

import requests
import json
from typing import Dict

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your deployed URL
BYPASS_PAYMENT = True  # Set to False to test with x402 payment

def print_test_result(name: str, success: bool, response: Dict = None):
    """Print formatted test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} - {name}")
    if response:
        print(json.dumps(response, indent=2, ensure_ascii=False))

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200 and response.json()["status"] == "healthy"
        print_test_result("Health Check", success, response.json())
        return success
    except Exception as e:
        print_test_result("Health Check", False, {"error": str(e)})
        return False

def test_slug_generate():
    """Test slug generation"""
    try:
        payload = {
            "text": "Building AI Agents with Claude 🚀",
            "max_length": 50,
            "separator": "-",
            "lowercase": True
        }
        response = requests.post(f"{BASE_URL}/api/slug/generate", json=payload)
        data = response.json()
        success = (
            response.status_code == 200 and
            data.get("slug") == "building-ai-agents-with-claude" and
            data.get("valid") == True
        )
        print_test_result("Slug Generation", success, data)
        return success
    except Exception as e:
        print_test_result("Slug Generation", False, {"error": str(e)})
        return False

def test_slug_validate():
    """Test slug validation"""
    try:
        # Test valid slug
        payload = {"slug": "hello-world", "strict": True}
        response = requests.post(f"{BASE_URL}/api/slug/validate", json=payload)
        data = response.json()
        success = response.status_code == 200 and data.get("valid") == True
        print_test_result("Slug Validation (Valid)", success, data)
        
        # Test invalid slug
        payload = {"slug": "Hello World!", "strict": True}
        response = requests.post(f"{BASE_URL}/api/slug/validate", json=payload)
        data = response.json()
        success = response.status_code == 200 and data.get("valid") == False
        print_test_result("Slug Validation (Invalid)", success, data)
        
        return success
    except Exception as e:
        print_test_result("Slug Validation", False, {"error": str(e)})
        return False

def test_slug_similarity():
    """Test slug similarity"""
    try:
        payload = {
            "slug1": "machine-learning-basics",
            "slug2": "machine-learning-advanced"
        }
        response = requests.post(f"{BASE_URL}/api/slug/similarity", json=payload)
        data = response.json()
        success = (
            response.status_code == 200 and
            data.get("similarity") > 0.6 and
            data.get("common_prefix") == "machine-learning-"
        )
        print_test_result("Slug Similarity", success, data)
        return success
    except Exception as e:
        print_test_result("Slug Similarity", False, {"error": str(e)})
        return False

def test_transliteration():
    """Test transliteration"""
    try:
        # Roman to Devanagari
        payload = {
            "text": "namaste",
            "from_script": "roman",
            "to_script": "devanagari"
        }
        response = requests.post(f"{BASE_URL}/api/transliterate", json=payload)
        data = response.json()
        success = response.status_code == 200 and len(data.get("transliterated", "")) > 0
        print_test_result("Transliteration (Roman→Devanagari)", success, data)
        
        # Roman to Telugu
        payload = {
            "text": "hello",
            "from_script": "roman",
            "to_script": "telugu"
        }
        response = requests.post(f"{BASE_URL}/api/transliterate", json=payload)
        data = response.json()
        success = response.status_code == 200 and len(data.get("transliterated", "")) > 0
        print_test_result("Transliteration (Roman→Telugu)", success, data)
        
        return success
    except Exception as e:
        print_test_result("Transliteration", False, {"error": str(e)})
        return False

def test_ifsc_lookup():
    """Test IFSC lookup"""
    try:
        payload = {"ifsc": "SBIN0000001"}
        response = requests.post(f"{BASE_URL}/api/ifsc/lookup", json=payload)
        data = response.json()
        success = (
            response.status_code == 200 and
            data.get("valid_format") == True and
            "State Bank of India" in data.get("bank", "")
        )
        print_test_result("IFSC Lookup", success, data)
        return success
    except Exception as e:
        print_test_result("IFSC Lookup", False, {"error": str(e)})
        return False

def test_ifsc_validate():
    """Test IFSC validation"""
    try:
        # Valid format
        response = requests.get(f"{BASE_URL}/api/ifsc/validate/SBIN0000001")
        data = response.json()
        success = response.status_code == 200 and data.get("valid_format") == True
        print_test_result("IFSC Validation (Valid)", success, data)
        
        # Invalid format
        response = requests.get(f"{BASE_URL}/api/ifsc/validate/INVALID123")
        data = response.json()
        success = response.status_code == 200 and data.get("valid_format") == False
        print_test_result("IFSC Validation (Invalid)", success, data)
        
        return success
    except Exception as e:
        print_test_result("IFSC Validation", False, {"error": str(e)})
        return False

def test_timezone_lookup():
    """Test timezone lookup"""
    try:
        # Mumbai coordinates
        payload = {
            "latitude": 19.0760,
            "longitude": 72.8777
        }
        response = requests.post(f"{BASE_URL}/api/timezone/lookup", json=payload)
        data = response.json()
        success = (
            response.status_code == 200 and
            "Asia/Kolkata" in data.get("timezone", "")
        )
        print_test_result("Timezone Lookup (Mumbai)", success, data)
        
        # New York coordinates
        payload = {
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        response = requests.post(f"{BASE_URL}/api/timezone/lookup", json=payload)
        data = response.json()
        success = (
            response.status_code == 200 and
            "America/New_York" in data.get("timezone", "")
        )
        print_test_result("Timezone Lookup (New York)", success, data)
        
        return success
    except Exception as e:
        print_test_result("Timezone Lookup", False, {"error": str(e)})
        return False

def test_phone_validate():
    """Test phone validation"""
    try:
        # Valid Indian mobile
        payload = {
            "phone": "+919876543210",
            "country_code": "IN"
        }
        response = requests.post(f"{BASE_URL}/api/phone/validate", json=payload)
        data = response.json()
        success = (
            response.status_code == 200 and
            data.get("valid") == True and
            data.get("type") == "mobile"
        )
        print_test_result("Phone Validation (Valid)", success, data)
        
        # Invalid phone
        payload = {
            "phone": "123",
            "country_code": "IN"
        }
        response = requests.post(f"{BASE_URL}/api/phone/validate", json=payload)
        data = response.json()
        success = response.status_code == 200 and data.get("valid") == False
        print_test_result("Phone Validation (Invalid)", success, data)
        
        return success
    except Exception as e:
        print_test_result("Phone Validation", False, {"error": str(e)})
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("🧪 Agent Utility API - Comprehensive Test Suite")
    print("=" * 70)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Payment Bypass: {BYPASS_PAYMENT}\n")
    
    tests = [
        ("Health Check", test_health),
        ("Slug Generation", test_slug_generate),
        ("Slug Validation", test_slug_validate),
        ("Slug Similarity", test_slug_similarity),
        ("Transliteration", test_transliteration),
        ("IFSC Lookup", test_ifsc_lookup),
        ("IFSC Validation", test_ifsc_validate),
        ("Timezone Lookup", test_timezone_lookup),
        ("Phone Validation", test_phone_validate)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ {name} - Exception: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! API is ready for production.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
    
    return passed == total

if __name__ == "__main__":
    import sys
    
    # Allow URL override via command line
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
