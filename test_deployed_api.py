"""Test the deployed Vercel API."""

import requests

BASE_URL = "https://elevenlabs-api-sable.vercel.app"

def test_api_info():
    """Test API info endpoint."""
    print("\n[TEST] API Info")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API Name: {data['name']}")
        print(f"✓ Version: {data['version']}")
        print(f"✓ Endpoints: {len(data['endpoints'])} available")
    else:
        print(f"✗ Failed: {response.text}")

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
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        with open("deployed_api_output.mp3", "wb") as f:
            f.write(response.content)
        print(f"✓ Success! Saved {len(response.content)} bytes to deployed_api_output.mp3")
    else:
        print(f"✗ Failed: {response.text}")

def test_voices():
    """Test list voices endpoint."""
    print("\n[TEST] List Voices")
    response = requests.get(f"{BASE_URL}/api/voices")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        voices = data.get("voices", [])
        print(f"✓ Found {len(voices)} voices")
        if voices:
            print(f"  First 3 voices:")
            for voice in voices[:3]:
                print(f"  - {voice.get('name')} ({voice.get('voice_id')})")
    else:
        print(f"✗ Failed: {response.text}")

def test_user():
    """Test user info endpoint."""
    print("\n[TEST] User Info")
    response = requests.get(f"{BASE_URL}/api/user")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ User ID: {data.get('user_id')}")
        sub = data.get('subscription', {})
        print(f"✓ Tier: {sub.get('tier')}")
        print(f"✓ Characters: {sub.get('character_count')}/{sub.get('character_limit')}")
    else:
        print(f"✗ Failed: {response.text}")

if __name__ == "__main__":
    print("=" * 70)
    print("Testing Deployed API: elevenlabs-api-sable.vercel.app")
    print("=" * 70)
    
    test_api_info()
    test_voices()
    test_user()
    test_tts()
    
    print("\n" + "=" * 70)
    print("Tests Complete!")
    print("=" * 70)
    print(f"\n🌐 Your API is live at: {BASE_URL}")
    print(f"📊 Admin Panel: {BASE_URL}/admin?admin_key=YOUR_KEY")
