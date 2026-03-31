# Deployment Guide

## Project Structure

```
elevenlabs-api/
├── api/
│   ├── __init__.py
│   ├── index.py              # Main Flask app (Vercel entry point)
│   ├── token_manager.py      # Multi-token rotation system
│   └── elevenlabs_client.py  # ElevenLabs API client
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── .env                     # Local environment variables
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── README.md               # Documentation
├── test_api.py             # Local API tests
└── test_voice_with_id.py   # Voice testing script
```

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
ADMIN_KEY=your-secret-admin-key-change-this
XI_BEARER_TOKEN=your_bearer_token_here
```

### 3. Run Locally

```bash
python api/index.py
```

Server runs at `http://localhost:5000`

### 4. Test API

```bash
# Test TTS
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","voice_id":"FZkK3TvQ0pjyDmT8fzIW"}' \
  --output test.mp3

# Access admin panel
# Open browser: http://localhost:5000/admin?admin_key=your-secret-admin-key-change-this
```

## Deploy to Vercel

### Method 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Set environment variables
vercel env add ADMIN_KEY
vercel env add XI_BEARER_TOKEN

# Deploy to production
vercel --prod
```

### Method 2: GitHub Integration

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Add environment variables:
   - `ADMIN_KEY`: Your admin secret key
   - `XI_BEARER_TOKEN`: Your ElevenLabs bearer token (optional)
6. Deploy!

## Environment Variables

### Required

- `ADMIN_KEY`: Secret key for admin panel access
  - Example: `my-super-secret-key-2024`
  - Used to protect admin endpoints

### Optional

- `XI_BEARER_TOKEN`: Default ElevenLabs bearer token
  - Can be managed via admin panel after deployment
  - Useful for initial setup

## Post-Deployment Setup

### 1. Access Admin Panel

```
https://your-api.vercel.app/admin?admin_key=YOUR_ADMIN_KEY
```

### 2. Add Tokens

- Click "Add New Token"
- Enter token name (e.g., "Account 1")
- Paste bearer token
- Click "Add Token"

### 3. Test API

```bash
curl -X POST https://your-api.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from Vercel!"}' \
  --output speech.mp3
```

## Token Management

### Getting Bearer Tokens

1. Login to elevenlabs.io
2. Open DevTools (F12) → Network tab
3. Perform any action (play voice, generate speech)
4. Find request to `api.elevenlabs.io`
5. Copy `Authorization: Bearer ...` header value

### Adding Multiple Tokens

Add multiple accounts for:
- Load balancing
- Automatic failover
- Higher usage limits
- Redundancy

### Token Rotation

Tokens automatically rotate when:
- 402 Payment Required (balance exhausted)
- 401 Unauthorized (token expired)
- 429 Too Many Requests (rate limited)

### Auto-Disable

Tokens are auto-disabled after 3 consecutive failures.
Reset via admin panel to re-enable.

## API Usage

### Text-to-Speech

```bash
curl -X POST https://your-api.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here",
    "voice_id": "FZkK3TvQ0pjyDmT8fzIW",
    "model_id": "eleven_turbo_v2_5",
    "output_format": "mp3_44100_128"
  }' \
  --output speech.mp3
```

### List Voices

```bash
curl https://your-api.vercel.app/api/voices
```

### Get User Info

```bash
curl https://your-api.vercel.app/api/user
```

### Admin: List Tokens

```bash
curl https://your-api.vercel.app/admin/tokens \
  -H "X-Admin-Key: YOUR_ADMIN_KEY"
```

### Admin: Add Token

```bash
curl -X POST https://your-api.vercel.app/admin/tokens \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: YOUR_ADMIN_KEY" \
  -d '{"name":"Account 2","token":"eyJhbGci..."}'
```

## Security Best Practices

1. **Change Default Admin Key**
   - Use a strong, random key
   - Never commit to Git

2. **Use Environment Variables**
   - Store tokens in Vercel environment variables
   - Never hardcode in source code

3. **Rotate Tokens Regularly**
   - Bearer tokens expire after ~1 hour
   - Add multiple accounts for redundancy

4. **Monitor Usage**
   - Check admin panel regularly
   - Monitor token failure rates

5. **Enable HTTPS Only**
   - Vercel provides HTTPS by default
   - Never use HTTP in production

## Troubleshooting

### "No active tokens available"

**Solution:**
- Add tokens via admin panel
- Check if tokens are enabled
- Verify token validity

### "All tokens exhausted or failed"

**Solution:**
- All tokens have been disabled
- Add new tokens
- Reset failure counts
- Check token expiration

### Admin panel not accessible

**Solution:**
- Verify `ADMIN_KEY` environment variable
- Use correct query parameter: `?admin_key=YOUR_KEY`
- Check Vercel deployment logs

### Token expires quickly

**Solution:**
- Bearer tokens expire after ~1 hour
- Add multiple accounts
- Tokens auto-rotate on expiration

### API returns 401 Unauthorized

**Solution:**
- Token has expired
- Get new token from browser
- Add via admin panel

## Monitoring

### Check Token Status

Visit admin panel to see:
- Total tokens
- Active tokens
- Usage counts
- Failure rates
- Last used timestamps

### Logs

View Vercel deployment logs:
```bash
vercel logs
```

## Scaling

### Add More Tokens

- Support unlimited tokens
- Automatic load balancing
- Seamless failover

### Rate Limiting

Each token has its own rate limit:
- Free: 10,000 characters/month
- Paid: Higher limits

### Performance

- Vercel Edge Network
- Global CDN
- Auto-scaling
- Zero cold starts

## Support

For issues or questions:
1. Check README.md
2. Review Vercel logs
3. Test locally first
4. Verify token validity
