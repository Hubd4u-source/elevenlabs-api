"""Token management system with automatic rotation and failover."""

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TokenManager:
    """Manages multiple ElevenLabs tokens with automatic rotation."""

    def __init__(self, tokens_file: str = "tokens.json"):
        self.tokens_file = Path(tokens_file)
        self.tokens: List[Dict] = []
        self.current_index = 0
        self.lock = threading.Lock()
        self._load_tokens()

    def _load_tokens(self) -> None:
        """Load tokens from file or environment."""
        if self.tokens_file.exists():
            with open(self.tokens_file, "r") as f:
                data = json.load(f)
                self.tokens = data.get("tokens", [])
        
        # Fallback to environment variable
        if not self.tokens:
            env_token = os.getenv("XI_BEARER_TOKEN")
            if env_token:
                self.tokens = [{
                    "token": env_token,
                    "name": "Default Token",
                    "enabled": True,
                    "usage_count": 0,
                    "last_used": None,
                    "failed_count": 0
                }]
                self._save_tokens()

    def _save_tokens(self) -> None:
        """Save tokens to file."""
        with open(self.tokens_file, "w") as f:
            json.dump({"tokens": self.tokens}, f, indent=2)

    def get_active_token(self) -> Optional[str]:
        """Get the current active token."""
        with self.lock:
            if not self.tokens:
                return None

            # Find next enabled token
            attempts = 0
            while attempts < len(self.tokens):
                token_data = self.tokens[self.current_index]
                
                if token_data.get("enabled", True):
                    # Update usage stats
                    token_data["usage_count"] = token_data.get("usage_count", 0) + 1
                    token_data["last_used"] = datetime.utcnow().isoformat()
                    self._save_tokens()
                    return token_data["token"]
                
                # Move to next token
                self.current_index = (self.current_index + 1) % len(self.tokens)
                attempts += 1

            return None

    def mark_token_failed(self) -> None:
        """Mark current token as failed and rotate to next."""
        with self.lock:
            if self.tokens:
                token_data = self.tokens[self.current_index]
                token_data["failed_count"] = token_data.get("failed_count", 0) + 1
                
                # Auto-disable after 3 consecutive failures
                if token_data["failed_count"] >= 3:
                    token_data["enabled"] = False
                    print(f"Token '{token_data.get('name', 'Unknown')}' auto-disabled after 3 failures")
                
                self._save_tokens()
                self.rotate_token()

    def rotate_token(self) -> None:
        """Manually rotate to next token."""
        with self.lock:
            if self.tokens:
                self.current_index = (self.current_index + 1) % len(self.tokens)

    def add_token(self, token: str, name: str = "New Token") -> Dict:
        """Add a new token to the pool."""
        with self.lock:
            token_data = {
                "token": token,
                "name": name,
                "enabled": True,
                "usage_count": 0,
                "last_used": None,
                "failed_count": 0,
                "added_at": datetime.utcnow().isoformat()
            }
            self.tokens.append(token_data)
            self._save_tokens()
            return token_data

    def remove_token(self, index: int) -> bool:
        """Remove a token by index."""
        with self.lock:
            if 0 <= index < len(self.tokens):
                removed = self.tokens.pop(index)
                if self.current_index >= len(self.tokens) and self.tokens:
                    self.current_index = 0
                self._save_tokens()
                return True
            return False

    def toggle_token(self, index: int) -> bool:
        """Enable/disable a token."""
        with self.lock:
            if 0 <= index < len(self.tokens):
                self.tokens[index]["enabled"] = not self.tokens[index].get("enabled", True)
                self.tokens[index]["failed_count"] = 0  # Reset failure count
                self._save_tokens()
                return True
            return False

    def get_all_tokens(self) -> List[Dict]:
        """Get all tokens with masked values."""
        with self.lock:
            return [
                {
                    "index": i,
                    "name": t.get("name", "Unknown"),
                    "token_preview": t["token"][:20] + "..." if len(t["token"]) > 20 else t["token"],
                    "enabled": t.get("enabled", True),
                    "usage_count": t.get("usage_count", 0),
                    "last_used": t.get("last_used"),
                    "failed_count": t.get("failed_count", 0),
                    "added_at": t.get("added_at"),
                    "is_current": i == self.current_index
                }
                for i, t in enumerate(self.tokens)
            ]

    def reset_failures(self, index: int) -> bool:
        """Reset failure count for a token."""
        with self.lock:
            if 0 <= index < len(self.tokens):
                self.tokens[index]["failed_count"] = 0
                self._save_tokens()
                return True
            return False


# Global instance
token_manager = TokenManager()
