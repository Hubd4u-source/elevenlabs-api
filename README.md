# ElevenLabs Multi-Token API

Production-ready Flask API for ElevenLabs with automatic token rotation and failover. Deploy to Vercel with zero configuration.

## Features

- ✅ Multi-token pool management
- ✅ Automatic token rotation on exhaustion
- ✅ Failover logic for high availability
- ✅ Admin panel for token management
- ✅ Global API access
- ✅ Vercel-ready deployment
- ✅ CORS enabled
- ✅ Production-ready error handling

## Quick Start

### 1. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and set your ADMIN_KEY

# Run locally
python api/index.py
```

Server runs at `http://localhost:5000`

### 2. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# ADMIN_KEY=your-secret-key
```

## API Endpoints

### Public Endpoints

#### POST /api/tts
Generate text-to-speech audio.

**Request:**
```json
{
  "text": "Hello world",
  "voice_id": "cgSgspJ2msm6clMCkdW9",
  "model_id": "eleven_turbo_v2_5",
  "output_format": "mp3_44100_128"
}
```

**Response:** Audio file (audio/mpeg)

**Example:**
```bash
curl -X POST https://your-api.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world"}' \
  --output speech.mp3
```

#### GET /api/voices
List available voices.

#### GET /api/user
Get user information.

#### GET /api/subscription
Get subscription details.

### Admin Endpoints

All admin endpoints require `X-Admin-Key` header or `admin_key` query parameter.

#### GET /admin?admin_key=YOUR_KEY
Access the admin panel UI.

#### GET /admin/tokens
List all tokens with stats.

**Headers:** `X-Admin-Key: YOUR_KEY`

**Response:**
```json
{
  "tokens": [
    {
      "index": 0,
      "name": "Account 1",
      "token_preview": "eyJhbGciOiJSUzI1NiIs...",
      "enabled": true,
      "usage_count": 42,
      "failed_count": 0,
      "last_used": "2024-01-15T10:30:00",
      "is_current": true
    }
  ],
  "current_index": 0
}
```

#### POST /admin/tokens
Add a new token.

**Headers:** `X-Admin-Key: YOUR_KEY`

**Request:**
```json
{
  "name": "Account 2",
  "token": "eyJhbGciOiJSUzI1NiIs..."
}
```

#### DELETE /admin/tokens/{index}
Remove a token.

**Headers:** `X-Admin-Key: YOUR_KEY`

#### PUT /admin/tokens/{index}/toggle
Enable/disable a token.

**Headers:** `X-Admin-Key: YOUR_KEY`

#### POST /admin/tokens/{index}/reset
Reset failure count for a token.

**Headers:** `X-Admin-Key: YOUR_KEY`

## Token Management

### Automatic Rotation

The API automatically rotates tokens when:
- Current token returns 402 (payment required)
- Current token returns 401 (unauthorized)
- Current token returns 429 (rate limited)

### Auto-Disable

Tokens are automatically disabled after 3 consecutive failures to prevent repeated errors.

### Manual Management

Use the admin panel at `/admin?admin_key=YOUR_KEY` to:
- View all tokens and their stats
- Add new tokens
- Enable/disable tokens
- Reset failure counts
- Delete tokens

## Environment Variables

### Required

- `ADMIN_KEY`: Secret key for admin panel access

### Optional

- `XI_BEARER_TOKEN`: Default token (can be managed via admin panel)

## File Structure

```
.
├── api/
│   ├── __init__.py
│   ├── index.py              # Main Flask app
│   ├── token_manager.py      # Token rotation logic
│   └── elevenlabs_client.py  # ElevenLabs API client
├── tokens.json               # Token storage (auto-created)
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (local)
└── README.md
```

## Usage Examples

### Python

```python
import requests

# Text-to-speech
response = requests.post(
    "https://your-api.vercel.app/api/tts",
    json={
        "text": "Hello from Python",
        "voice_id": "FZkK3TvQ0pjyDmT8fzIW"
    }
)

with open("output.mp3", "wb") as f:
    f.write(response.content)
```

### JavaScript

```javascript
// Text-to-speech
const response = await fetch('https://your-api.vercel.app/api/tts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Hello from JavaScript',
    voice_id: 'FZkK3TvQ0pjyDmT8fzIW'
  })
});

const blob = await response.blob();
const url = URL.createObjectURL(blob);
const audio = new Audio(url);
audio.play();
```

### cURL

```bash
# Generate speech
curl -X POST https://your-api.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","voice_id":"FZkK3TvQ0pjyDmT8fzIW"}' \
  --output speech.mp3

# List voices
curl https://your-api.vercel.app/api/voices

# Admin: Add token
curl -X POST https://your-api.vercel.app/admin/tokens \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: your-secret-key" \
  -d '{"name":"Account 2","token":"eyJhbGci..."}'
```

## Security

- Admin endpoints require authentication via `ADMIN_KEY`
- Tokens are stored with masked previews in responses
- CORS enabled for global access
- Environment variables for sensitive data

## Troubleshooting

### "No active tokens available"
- Add tokens via admin panel
- Check if tokens are enabled
- Verify token validity

### "All tokens exhausted or failed"
- All tokens have been disabled due to failures
- Add new tokens or reset failure counts
- Check token expiration

### Admin panel not accessible
- Verify `ADMIN_KEY` is set correctly
- Use correct query parameter: `?admin_key=YOUR_KEY`
- Check Vercel environment variables

## License

MIT
