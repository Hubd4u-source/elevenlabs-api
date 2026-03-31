"""ElevenLabs API client with token rotation support."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional


class ElevenLabsClient:
    """Client for ElevenLabs API with Bearer token authentication."""

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = "https://api.elevenlabs.io/v1"

    def _build_headers(self, accept: str = "application/json") -> dict:
        """Build request headers."""
        return {
            "Accept": accept,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bearer_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        data: dict = None,
        accept: str = "application/json",
    ) -> tuple[bytes, int]:
        """Make HTTP request and return (response_body, status_code)."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._build_headers(accept=accept)

        request_data = json.dumps(data).encode("utf-8") if data else None
        request = urllib.request.Request(url, data=request_data, method=method, headers=headers)

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read(), response.status
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return body.encode("utf-8"), exc.code
        except urllib.error.URLError as exc:
            error_msg = json.dumps({"error": f"Network error: {exc.reason}"})
            return error_msg.encode("utf-8"), 503

    def text_to_speech(
        self,
        voice_id: str,
        text: str,
        model_id: str = "eleven_turbo_v2_5",
        output_format: str = "mp3_44100_128",
    ) -> tuple[bytes, int, Optional[str]]:
        """Generate speech from text. Returns (audio_bytes, status_code, error_msg)."""
        query = urllib.parse.urlencode({"output_format": output_format})
        safe_voice_id = urllib.parse.quote(voice_id, safe="")
        endpoint = f"/text-to-speech/{safe_voice_id}?{query}"

        response, status = self._request(
            endpoint,
            method="POST",
            data={"text": text, "model_id": model_id},
            accept="audio/mpeg",
        )

        if status == 200:
            return response, status, None
        else:
            try:
                error_data = json.loads(response.decode("utf-8"))
                error_msg = error_data.get("detail", {}).get("message", "Unknown error")
            except:
                error_msg = response.decode("utf-8", errors="replace")
            return b"", status, error_msg

    def get_user(self) -> tuple[dict, int]:
        """Get user info. Returns (data, status_code)."""
        response, status = self._request("/user")
        if status == 200:
            return json.loads(response.decode("utf-8")), status
        return {"error": response.decode("utf-8", errors="replace")}, status

    def list_voices(self) -> tuple[dict, int]:
        """List available voices. Returns (data, status_code)."""
        response, status = self._request("/voices")
        if status == 200:
            return json.loads(response.decode("utf-8")), status
        return {"error": response.decode("utf-8", errors="replace")}, status

    def get_subscription(self) -> tuple[dict, int]:
        """Get subscription info. Returns (data, status_code)."""
        response, status = self._request("/user/subscription")
        if status == 200:
            return json.loads(response.decode("utf-8")), status
        return {"error": response.decode("utf-8", errors="replace")}, status
