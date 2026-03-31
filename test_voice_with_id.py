#!/usr/bin/env python3
"""Test using a specific voice ID and demonstrate voice creation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from elevenlabs_browser_client import ElevenLabsClient


def test_voice_tts(client: ElevenLabsClient, voice_id: str, text: str) -> None:
    """Test text-to-speech with a specific voice ID."""
    print(f"\n[TEST] Using voice ID: {voice_id}")
    
    try:
        # Try to get voice details first
        voice_info = client.get_voice(voice_id)
        print(f"✓ Voice found: {voice_info.get('name', 'Unknown')}")
        print(f"  Category: {voice_info.get('category', 'Unknown')}")
        
    except RuntimeError as exc:
        print(f"⚠ Could not fetch voice details: {exc}")
        print("  Attempting TTS anyway...")

    try:
        # Generate speech
        audio = client.text_to_speech(voice_id=voice_id, text=text)
        
        # Save output
        output_file = Path(f"voice_{voice_id}.mp3")
        output_file.write_bytes(audio)
        
        print(f"✓ Generated {len(audio)} bytes")
        print(f"✓ Saved to: {output_file.resolve()}")
        
    except RuntimeError as exc:
        error_msg = str(exc)
        
        if "paid_plan_required" in error_msg or "not available" in error_msg:
            print(f"\n✗ API Restriction: {exc}")
            print("\n💡 Solution: Use browser session authentication!")
            print("   1. Login to elevenlabs.io in your browser")
            print("   2. Open DevTools (F12) → Application → Cookies")
            print("   3. Copy 'xi-session' cookie value")
            print("   4. Add to .env: XI_SESSION=\"your_token\"")
            print("   5. Run this script again")
        else:
            print(f"✗ Error: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Test specific voice ID")
    parser.add_argument(
        "--voice-id",
        default="FZkK3TvQ0pjyDmT8fzIW",
        help="Voice ID to test (default: FZkK3TvQ0pjyDmT8fzIW)",
    )
    parser.add_argument(
        "--text",
        default="sun bhai aaj kal tu mujhse milne nhi aa rha ha?",
        help="Text to speak",
    )
    args = parser.parse_args()

    try:
        client = ElevenLabsClient.from_env(Path(__file__).with_name(".env"))
        print(f"Authentication: {client.auth_method.upper()}")
        
        test_voice_tts(client, args.voice_id, args.text)
        return 0
        
    except ValueError as exc:
        print(f"✗ Authentication error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
