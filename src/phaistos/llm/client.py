"""Local Ollama client for research synthesis and Skeptic reviews."""

import json
from typing import Dict, List, Optional
import urllib.request
import urllib.error


class OllamaClient:
    """Client for local Ollama HTTP API (Mac or Fedora PC)."""

    def __init__(self, host: str = "http://localhost:11434", default_model: str = "qwen2.5:3b"):
        self.host = host.rstrip("/")
        self.default_model = default_model

    def is_available(self) -> bool:
        """Check if local Ollama daemon is reachable."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """List available local model tags."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    def generate_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        """Send chat completion request to local Ollama."""
        selected_model = model or self.default_model
        payload = {
            "model": selected_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=180.0) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res.get("message", {}).get("content", "")
        except TimeoutError:
            raise ConnectionError(f"Ollama inference timed out after 180s on {self.host}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to connect to local Ollama at {self.host}: {e}")
