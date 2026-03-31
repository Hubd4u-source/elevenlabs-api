"""Simple test to check API status."""

import requests
import time

BASE_URL = "http://localhost:5000"

print("Testing API endpoints...\n")

# Test 1: API Info
print("[1] Testing API Info...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"✓ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API: {data['name']}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Check if token is loaded
print("\n[2] Testing User Info (checks token)...")
try:
    response = requests.get(f"{BASE_URL}/api/user", timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ User ID: {data.get('user_id')}")
        print(f"✓ Token is valid!")
    elif response.status_code == 401:
        print("✗ Token is invalid or expired")
        print(f"Response: {response.text}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Quick TTS test
print("\n[3] Testing TTS (small text)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/tts",
        json={"text": "Hello", "voice_id": "cgSgspJ2msm6clMCkdW9"},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Generated {len(response.content)} bytes")
        with open("quick_test.mp3", "wb") as f:
            f.write(response.content)
        print("✓ Saved to quick_test.mp3")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("Test complete!")
