#!/usr/bin/env python3
"""Add token to local server."""

import requests

API_URL = "http://localhost:5000"
ADMIN_KEY = "my-secret-admin-key-2024"

NEW_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM3MzAwNzY5YTA3ZTA1MTE2ZjdlNTEzOGZhOTA5MzY4NWVlYmMyNDAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTW9oYW1tYWQgRmFpemFuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGNPeDNTTC15TldkYVdzeHBFM3BCN1lxWGtfRjVYMnJ5SGVJTWp6RVU5Sj1zOTYtYyIsIndvcmtzcGFjZV9pZCI6IjU3YzE0ODNhNDUxMTQxYzY4OGVjNWM4ZTUyMDIzNDljIiwid29ya3NwYWNlX3VzZXJfaWQiOiJVbW5saUxYMHdNWURNeGZNVllEbUdkOE9YYWwxIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3hpLWxhYnMiLCJhdWQiOiJ4aS1sYWJzIiwiYXV0aF90aW1lIjoxNzc0OTU5NzM5LCJ1c2VyX2lkIjoiVW1ubGlMWDB3TVlETXhmTVZZRG1HZDhPWGFsMSIsInN1YiI6IlVtbmxpTFgwd01ZRE14Zk1WWURtR2Q4T1hhbDEiLCJpYXQiOjE3NzQ5NTk3MzksImV4cCI6MTc3NDk2MzMzOSwiZW1haWwiOiJtZGZhaXphbnNpd2FuQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTAwNzMzNTk0MDQyMTgzMjc5MzcxIl0sImVtYWlsIjpbIm1kZmFpemFuc2l3YW5AZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.W_M1pMloN4o2ocIVUG7tKHDt203lejQzV4kqBvtAXpzgi84O4QCnJOIQRbpShX27bbB-lCR9xNtlk2Q6MutZMVL1mYgesGlZWGtEz3EEi4E969B_h1IG0ESLmp6XQB-t3GCUGhjIesAJTt-Aa7MMEW_S3_b60lDg7Bw8e7KE7kMZxixrIt-MB_uW8byMUdDEmFERxet-rXYuElXszRxW28cNqk6CiZJ9NKMnjavE87QIKYvZMIqhWuzv-jnM9C4FNH61wPv1yvq9PayizXRzPfyxegjjeQs3_SFnfncNvTA7_7uGQry9YWt9F9XR4Ze-mgYQTqlLRmLVDJmXZRHuA"

print("Adding token to local server...")
print(f"API: {API_URL}")

try:
    response = requests.post(
        f"{API_URL}/admin/tokens",
        headers={
            "Content-Type": "application/json",
            "X-Admin-Key": ADMIN_KEY
        },
        json={
            "name": "Mohammad Faizan Account",
            "token": NEW_TOKEN
        },
        timeout=10
    )
    
    if response.status_code in [200, 201]:
        print("✅ Token added successfully!")
        
        # Show current tokens
        response = requests.get(
            f"{API_URL}/admin/tokens",
            headers={"X-Admin-Key": ADMIN_KEY}
        )
        
        if response.status_code == 200:
            data = response.json()
            tokens = data.get("tokens", [])
            print(f"\nTotal tokens: {len(tokens)}")
            for token in tokens:
                status = "✓" if token["enabled"] else "✗"
                current = " 👈" if token["is_current"] else ""
                print(f"  {status} {token['name']} (Used: {token['usage_count']}){current}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
