"""Test the Flask API locally."""

import requests
import json

BASE_URL = "http://localhost:5000"
ADMIN_KEY = "my-secret-admin-key-2024"

def test_tts():
    """Test text-to-speech endpoint."""
    print("\n[TEST] Text-to-Speech")
    response = requests.post(
        f"{BASE_URL}/api/tts",
        json={
            "text": "sun bhai aaj kal tu mujhse milne nhi aa rha ha?",
            "voice_id": "FZkK3TvQ0pjyDmT8fzIW"
        }
    )
    
    if response.status_code == 200:
        with open("api_test_output.mp3", "wb") as f:
            f.write(response.content)
        print(f"✓ Success! Saved {len(response.content)} bytes to api_test_output.mp3")
    else:
        print(f"✗ Failed: {response.status_code}")
        print(response.text)

def test_voices():
    """Test list voices endpoint."""
    print("\n[TEST] List Voices")
    response = requests.get(f"{BASE_URL}/api/voices")
    
    if response.status_code == 200:
        data = response.json()
        voices = data.get("voices", [])
        print(f"✓ Found {len(voices)} voices")
        if voices:
            print(f"  Example: {voices[0].get('name')} ({voices[0].get('voice_id')})")
    else:
        print(f"✗ Failed: {response.status_code}")

def test_admin_tokens():
    """Test admin token management."""
    print("\n[TEST] Admin - List Tokens")
    response = requests.get(
        f"{BASE_URL}/admin/tokens",
        headers={"X-Admin-Key": ADMIN_KEY}
    )
    
    if response.status_code == 200:
        data = response.json()
        tokens = data.get("tokens", [])
        print(f"✓ Found {len(tokens)} tokens")
        for token in tokens:
            status = "✓ Enabled" if token["enabled"] else "✗ Disabled"
            current = " 👈 CURRENT" if token["is_current"] else ""
            print(f"  - {token['name']}: {status} (Used: {token['usage_count']}){current}")
    else:
        print(f"✗ Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("=" * 60)
    print("Testing ElevenLabs Multi-Token API")
    print("=" * 60)
    
    test_tts()
    test_voices()
    test_admin_tokens()
    
    print("\n" + "=" * 60)
    print("Tests Complete!")
    print("=" * 60)
