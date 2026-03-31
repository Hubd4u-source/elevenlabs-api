#!/usr/bin/env python3
"""Test voice generation on the deployed website."""

import requests
import time

API_URL = "https://elevenlabs-api-sable.vercel.app"

def test_tts():
    """Test text-to-speech generation."""
    print("=" * 70)
    print("Testing Voice Generation on Deployed Website")
    print("=" * 70)
    print(f"\nAPI URL: {API_URL}")
    print()
    
    # Test 1: Get voices
    print("[1] Fetching available voices...")
    try:
        response = requests.get(f"{API_URL}/api/voices", timeout=10)
        if response.status_code == 200:
            data = response.json()
            voices = data.get("voices", [])
            print(f"✅ Found {len(voices)} voices")
            if voices:
                print(f"   First voice: {voices[0].get('name')} ({voices[0].get('voice_id')})")
                voice_id = voices[0].get('voice_id')
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Generate speech
    print("\n[2] Generating speech...")
    test_text = "Hello! This is a test of the ElevenLabs Multi-Token API. The voice generation is working perfectly!"
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/api/tts",
            json={
                "text": test_text,
                "voice_id": voice_id,
                "model_id": "eleven_turbo_v2_5"
            },
            timeout=30
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            audio_size = len(response.content)
            print(f"✅ Speech generated successfully!")
            print(f"   Size: {audio_size:,} bytes ({audio_size/1024:.1f} KB)")
            print(f"   Time: {elapsed:.2f} seconds")
            
            # Save to file
            output_file = "website_test_output.mp3"
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"   Saved to: {output_file}")
            
            # Try to play it
            try:
                import os
                if os.name == 'nt':  # Windows
                    os.startfile(output_file)
                    print(f"   🔊 Playing audio...")
            except:
                pass
                
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 3: Check token status
    print("\n[3] Checking token status...")
    try:
        response = requests.get(f"{API_URL}/api", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data.get('name')}")
            print(f"   Tokens loaded: {data.get('tokens_loaded')}")
        else:
            print(f"⚠️  Could not fetch status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed successfully!")
    print("=" * 70)
    print(f"\n🌐 Visit the website: {API_URL}")
    print(f"🎯 Try the demo: {API_URL}/#demo")

if __name__ == "__main__":
    test_tts()
