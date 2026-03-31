# Vercel Environment Variables Setup

## Your API is deployed but needs environment variables!

Your API URL: **https://elevenlabs-api-sable.vercel.app**

## Step 1: Add Environment Variables

Go to your Vercel dashboard:
1. Visit: https://vercel.com/dashboard
2. Click on your project: **elevenlabs-api**
3. Go to **Settings** → **Environment Variables**

## Step 2: Add These Variables

### Required Variables:

**1. ADMIN_KEY**
- Name: `ADMIN_KEY`
- Value: `my-secret-admin-key-2024` (or create your own)
- Environment: Production, Preview, Development (select all)

**2. XI_BEARER_TOKEN**
- Name: `XI_BEARER_TOKEN`
- Value: Your bearer token (the long JWT token you extracted)
- Environment: Production, Preview, Development (select all)

Example token value:
```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjM3MzAwNzY5YTA3ZTA1MTE2ZjdlNTEzOGZhOTA5MzY4NWVlYmMyNDAiLCJ0eXAiOiJKV1QifQ...
```

## Step 3: Redeploy

After adding environment variables:
1. Go to **Deployments** tab
2. Click the three dots (...) on the latest deployment
3. Click **Redeploy**

OR just push a new commit:
```bash
git commit --allow-empty -m "Trigger redeploy"
git push
```

## Step 4: Test Your API

Once redeployed, test it:

```bash
# Test TTS
curl -X POST https://elevenlabs-api-sable.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","voice_id":"FZkK3TvQ0pjyDmT8fzIW"}' \
  --output test.mp3

# Access admin panel
# Open in browser:
https://elevenlabs-api-sable.vercel.app/admin?admin_key=my-secret-admin-key-2024
```

## Quick Test Script

Run this after setting environment variables:

```bash
python test_deployed_api.py
```

## Getting a Fresh Bearer Token

Your current token might have expired. To get a new one:

1. Login to https://elevenlabs.io
2. Open DevTools (F12) → Network tab
3. Click any voice or generate speech
4. Find request to `api.elevenlabs.io`
5. Copy the `Authorization: Bearer ...` header value
6. Update in Vercel environment variables

## Admin Panel Access

Once environment variables are set:

**URL:** https://elevenlabs-api-sable.vercel.app/admin?admin_key=my-secret-admin-key-2024

From the admin panel you can:
- Add multiple tokens
- View token usage statistics
- Enable/disable tokens
- Reset failure counts
- Monitor token health

## Troubleshooting

### "invalid_authorization_header"
- Environment variable `XI_BEARER_TOKEN` is not set
- Token has expired (get a new one)
- Token format is incorrect

### "No active tokens available"
- No tokens configured
- All tokens are disabled
- Add tokens via admin panel

### Admin panel shows "Unauthorized"
- `ADMIN_KEY` environment variable not set
- Wrong admin key in URL parameter

## Next Steps

1. ✅ Set environment variables in Vercel
2. ✅ Redeploy the application
3. ✅ Test the API endpoints
4. ✅ Access admin panel
5. ✅ Add multiple tokens for redundancy
