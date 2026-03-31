# Vercel Environment Variables Setup

## Step 1: Go to Vercel Dashboard

1. Visit: https://vercel.com/dashboard
2. Click on your project: **elevenlabs-api**
3. Go to **Settings** tab
4. Click **Environment Variables** in the left sidebar

## Step 2: Add Required Variables

### Variable 1: ADMIN_KEY

- **Name:** `ADMIN_KEY`
- **Value:** `my-secret-admin-key-2024`
- **Environment:** Select all (Production, Preview, Development)
- Click **Save**

### Variable 2: XI_BEARER_TOKEN

- **Name:** `XI_BEARER_TOKEN`
- **Value:** 
```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjM3MzAwNzY5YTA3ZTA1MTE2ZjdlNTEzOGZhOTA5MzY4NWVlYmMyNDAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTW9oYW1tYWQgRmFpemFuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGNPeDNTTC15TldkYVdzeHBFM3BCN1lxWGtfRjVYMnJ5SGVJTWp6RVU5Sj1zOTYtYyIsIndvcmtzcGFjZV9pZCI6IjU3YzE0ODNhNDUxMTQxYzY4OGVjNWM4ZTUyMDIzNDljIiwid29ya3NwYWNlX3VzZXJfaWQiOiJVbW5saUxYMHdNWURNeGZNVllEbUdkOE9YYWwxIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3hpLWxhYnMiLCJhdWQiOiJ4aS1sYWJzIiwiYXV0aF90aW1lIjoxNzc0OTU5NzM5LCJ1c2VyX2lkIjoiVW1ubGlMWDB3TVlETXhmTVZZRG1HZDhPWGFsMSIsInN1YiI6IlVtbmxpTFgwd01ZRE14Zk1WWURtR2Q4T1hhbDEiLCJpYXQiOjE3NzQ5NTk3MzksImV4cCI6MTc3NDk2MzMzOSwiZW1haWwiOiJtZGZhaXphbnNpd2FuQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTAwNzMzNTk0MDQyMTgzMjc5MzcxIl0sImVtYWlsIjpbIm1kZmFpemFuc2l3YW5AZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.W_M1pMloN4o2ocIVUG7tKHDt203lejQzV4kqBvtAXpzgi84O4QCnJOIQRbpShX27bbB-lCR9xNtlk2Q6MutZMVL1mYgesGlZWGtEz3EEi4E969B_h1IG0ESLmp6XQB-t3GCUGhjIesAJTt-Aa7MMEW_S3_b60lDg7Bw8e7KE7kMZxixrIt-MB_uW8byMUdDEmFERxet-rXYuElXszRxW28cNqk6CiZJ9NKMnjavE87QIKYvZMIqhWuzv-jnM9C4FNH61wPv1yvq9PayizXRzPfyxegjjeQs3_jSFnfncNvTA7_7uGQry9YWt9F9XR4Ze-mgYQTqlLRmLVDJmXZRHuA
```
- **Environment:** Select all (Production, Preview, Development)
- Click **Save**

## Step 3: Redeploy

After adding environment variables, you need to redeploy:

### Option A: Via Vercel Dashboard
1. Go to **Deployments** tab
2. Click the three dots (...) on the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete (~1-2 minutes)

### Option B: Via Git Push
```bash
git commit --allow-empty -m "Trigger redeploy with env vars"
git push
```

## Step 4: Test the API

Once redeployed, test it:

```bash
# Test API info
curl https://elevenlabs-api-sable.vercel.app/api

# Test TTS
curl -X POST https://elevenlabs-api-sable.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world"}' \
  --output test.mp3
```

## Step 5: Add More Tokens (Optional)

You can add more tokens via the admin panel or API:

### Via Admin Panel
Visit: https://elevenlabs-api-sable.vercel.app/admin?admin_key=my-secret-admin-key-2024

### Via API Script
```bash
python add_token_to_vercel.py
```

## Troubleshooting

### "No active tokens available"
- Environment variables not set
- Redeploy after setting variables
- Check Vercel deployment logs

### "Unauthorized" on admin endpoints
- ADMIN_KEY not set correctly
- Check spelling and value
- Redeploy after fixing

### Token expires quickly
- Bearer tokens expire after ~1 hour
- Add multiple tokens for redundancy
- Use admin panel to add fresh tokens

## Quick Reference

**Your Deployment:** https://elevenlabs-api-sable.vercel.app
**Admin Panel:** https://elevenlabs-api-sable.vercel.app/admin?admin_key=my-secret-admin-key-2024
**API Docs:** https://elevenlabs-api-sable.vercel.app/#docs
