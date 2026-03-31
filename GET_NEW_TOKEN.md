# Your Bearer Token Has Expired!

Bearer tokens expire after about 1 hour. You need to get a fresh one.

## Quick Steps to Get New Token:

### 1. Open ElevenLabs
Go to: https://elevenlabs.io (make sure you're logged in)

### 2. Open DevTools
Press `F12` or `Ctrl+Shift+I`

### 3. Go to Network Tab
Click the **"Network"** tab in DevTools

### 4. Trigger a Request
Do ANY of these:
- Click on any voice to hear a preview
- Type some text and click "Generate"
- Click on "History"
- Click on "Voices"

### 5. Find the Request
In the Network tab, look for a request to:
- `api.elevenlabs.io/v1/user`
- `api.elevenlabs.io/v1/voices`
- `api.elevenlabs.io/v1/text-to-speech`

Click on it!

### 6. Copy the Token
- Click on the **"Headers"** tab (on the right)
- Scroll down to **"Request Headers"**
- Find: `Authorization: Bearer eyJhbGci...`
- Copy EVERYTHING after "Bearer " (the long token)

### 7. Update .env File
Open `.env` and replace the old token:

```env
XI_BEARER_TOKEN=PASTE_YOUR_NEW_TOKEN_HERE
```

### 8. Restart Server
Stop the server (Ctrl+C) and start again:
```bash
python api/index.py
```

### 9. Test Again
```bash
python test_simple.py
```

## Example Token Format:

Your token should look like this (very long):
```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjM3MzAwNzY5YTA3ZTA1MTE2ZjdlNTEzOGZhOTA5MzY4NWVlYmMyNDAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiRmFpemFuY2hlYXQ0IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0ljYzdxaDhIY3I5TmtrLTVSU1B5QXctNTVLTjdycEMzdG44U0pOOEhlbUxQbUw9czk2LWMiLCJ3b3Jrc3BhY2VfaWQiOiIxYTQyYjIxZjdmYjI0OWIyYTRiNGRjMGFhODE3OGJhYyIsIndvcmtzcGFjZV91c2VyX2lkIjoidXNlcl81NzAxa24xcG5iMG5mamNicmg1MTV0YWhzazVkIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3hpLWxhYnMiLCJhdWQiOiJ4aS1sYWJzIiwiYXV0aF90aW1lIjoxNzc0OTUyNTYwLCJ1c2VyX2lkIjoicDI2N09wVHVMT2hkTUtoc2txSk83WmJGM293MiIsInN1YiI6InAyNjdPcFR1TE9oZE1LaHNrcUpPN1piRjNvdzIiLCJpYXQiOjE3NzQ5NTI1NjAsImV4cCI6MTc3NDk1NjE2MCwiZW1haWwiOiJmYWl6YW5jaGVhdDRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTE2Mzk4NDEyNzE0MTc2Mzg0NjMiXSwiZW1haWwiOlsiZmFpemFuY2hlYXQ0QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.LQM2_jgwXhQHNNaO-kFFRjmhtCbI_5nnJ9SoW2CMFjqD6jSXkATUc2gDNkp_y7W5hH0YNeuwpyRQk3n6MWS_FlAuTyE6fSKJZKGdlFZJFQIXUiW6To_Q5t9v4NXkBxHT28BrjtX_cF3tRbhxUaFoLakjSoIVnSUK9_-IwC77zynAHoZ0i_de-z_orzMRG5wwlxWE5bh-y6Tc7xzNpcB-3ZaDyT19PgOFSGa1_8QG0ral5ZPTDCFCIOtfYAqfXCZ0q7T5m6txXBKVbq-f4kAitMHhYoUhYJMgKruc1eQs0NBR9MjgK-PJMFCIUo9feJcRYcvf9lW_E4JnaV3y7FofDw
```

## Why Tokens Expire

Bearer tokens are JWT (JSON Web Tokens) with an expiration time built in. ElevenLabs tokens typically expire after 1 hour for security reasons.

## Solution for Production

For production, you should:
1. Add multiple tokens to the admin panel
2. Tokens will auto-rotate when one expires
3. Get fresh tokens regularly and add them via admin panel

This way, your API stays online even when individual tokens expire!
