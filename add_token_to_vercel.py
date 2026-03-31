#!/usr/bin/env python3
"""Add token to Vercel deployment via admin API."""

import requests

# Vercel deployment URL
API_URL = "https://elevenlabs-api-sable.vercel.app"

# Admin key (you need to set this in Vercel environment variables)
ADMIN_KEY = "my-secret-admin-key-2024"

# New token to add
NEW_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM3MzAwNzY5YTA3ZTA1MTE2ZjdlNTEzOGZhOTA5MzY4NWVlYmMyNDAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTW9oYW1tYWQgRmFpemFuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGNPeDNTTC15TldkYVdzeHBFM3BCN1lxWGtfRjVYMnJ5SGVJTWp6RVU5Sj1zOTYtYyIsIndvcmtzcGFjZV9pZCI6IjU3YzE0ODNhNDUxMTQxYzY4OGVjNWM4ZTUyMDIzNDljIiwid29ya3NwYWNlX3VzZXJfaWQiOiJVbW5saUxYMHdNWURNeGZNVllEbUdkOE9YYWwxIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3hpLWxhYnMiLCJhdWQiOiJ4aS1sYWJzIiwiYXV0aF90aW1lIjoxNzc0OTU5NzM5LCJ1c2VyX2lkIjoiVW1ubGlMWDB3TVlETXhmTVZZRG1HZDhPWGFsMSIsInN1YiI6IlVtbmxpTFgwd01ZRE14Zk1WWURtR2Q4T1hhbDEiLCJpYXQiOjE3NzQ5NTk3MzksImV4cCI6MTc3NDk2MzMzOSwiZW1haWwiOiJtZGZhaXphbnNpd2FuQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTAwNzMzNTk0MDQyMTgzMjc5MzcxIl0sImVtYWlsIjpbIm1kZmFpemFuc2l3YW5AZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.W_M1pMloN4o2ocIVUG7tKHDt203lejQzV4kqBvtAXpzgi84O4QCnJOIQRbpShX27bbB-lCR9xNtlk2Q6MutZMVL1mYgesGlZWGtEz3EEi4E969B_h1IG0ESLmp6XQB-t3GCUGhjIesAJTt-Aa7MMEW_S3_b60lDg7Bw8e7KE7kMZxixrIt-MB_uW8byMUdDEmFERxet-rXYuElXszRxW28cNqk6CiZJ9NKMnjavE87QIKYvZMIqhWuzv-jnM9C4FNH61wPv1yvq9PayizXRzPfyxegjjeQs3_jSFnfncNvTA7_7uGQry9YWt9F9XR4Ze-mgYQTqlLRmLVDJmXZRHuA"

TOKEN_NAME = "Mohammad Faizan Account"

def add_token():
    """Add token to the API."""
    print("=" * 70)
    print("Adding Token to Vercel Deployment")
    print("=" * 70)
    print(f"\nAPI URL: {API_URL}")
    print(f"Token Name: {TOKEN_NAME}")
    print(f"Token Preview: {NEW_TOKEN[:50]}...")
    print()
    
    try:
        # Add token via admin API
        response = requests.post(
            f"{API_URL}/admin/tokens",
            headers={
                "Content-Type": "application/json",
                "X-Admin-Key": ADMIN_KEY
            },
            json={
                "name": TOKEN_NAME,
                "token": NEW_TOKEN
            },
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ Token added successfully!")
            print("\nToken Details:")
            data = response.json()
            if "token" in data:
                token_info = data["token"]
                print(f"  Name: {token_info.get('name')}")
                print(f"  Enabled: {token_info.get('enabled')}")
                print(f"  Added At: {token_info.get('added_at')}")
        else:
            print(f"❌ Failed to add token")
            print(f"Response: {response.text}")
            
            if response.status_code == 401:
                print("\n⚠️  Authentication failed!")
                print("Make sure ADMIN_KEY is set correctly in Vercel environment variables.")
            elif response.status_code == 503:
                print("\n⚠️  API might not have environment variables set!")
                print("Please set XI_BEARER_TOKEN and ADMIN_KEY in Vercel dashboard.")
        
        # Check current tokens
        print("\n" + "=" * 70)
        print("Current Token Status")
        print("=" * 70)
        
        response = requests.get(
            f"{API_URL}/admin/tokens",
            headers={"X-Admin-Key": ADMIN_KEY},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            tokens = data.get("tokens", [])
            print(f"\nTotal Tokens: {len(tokens)}")
            for token in tokens:
                status = "✓ Active" if token["enabled"] else "✗ Disabled"
                current = " 👈 CURRENT" if token["is_current"] else ""
                print(f"  - {token['name']}: {status} (Used: {token['usage_count']}){current}")
        else:
            print(f"Could not fetch token status: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API")
        print("Make sure the Vercel deployment is live and accessible")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_token()
