"""Local Ollama client for research synthesis and Skeptic reviews."""

import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error
from urllib.parse import urlparse

_local_models_src = Path(__file__).resolve().parents[4] / "local-models" / "src"
if _local_models_src.exists() and str(_local_models_src) not in sys.path:
    sys.path.insert(0, str(_local_models_src))
try:
    from local_models.admission import LocalAdmission, ResourceDeferredError, stop_ollama_model, timed_out
    from local_models.telemetry import TelemetryLogger, UsageEvent
except ImportError:  # The research tools remain standalone without the sibling checkout.
    LocalAdmission = None  # type: ignore[assignment,misc]
    ResourceDeferredError = RuntimeError  # type: ignore[assignment,misc]
    TelemetryLogger = None  # type: ignore[assignment,misc]
    UsageEvent = None  # type: ignore[assignment,misc]

    def timed_out(error: BaseException) -> bool:
        return isinstance(error, TimeoutError) or "timed out" in str(error).casefold()

    def stop_ollama_model(model: str) -> bool:
        return False


class OllamaClient:
    """Client for local Ollama HTTP API (Mac or Fedora PC)."""

    def __init__(self, host: Optional[str] = None, default_model: str = "qwen2.5:3b"):
        self.candidate_hosts = [
            host.rstrip("/") if host else None,
            os.getenv("OLLAMA_HOST"),
            "http://localhost:11434",
            "http://127.0.0.1:11434",
        ]
        self.candidate_hosts = [h for h in self.candidate_hosts if h]
        self.host = self._find_active_host()
        self.default_model = default_model
        self.telemetry = TelemetryLogger() if TelemetryLogger else None

    def _find_active_host(self) -> str:
        for candidate in self.candidate_hosts:
            try:
                req = urllib.request.Request(f"{candidate}/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    if resp.status == 200:
                        return candidate
            except Exception:
                continue
        return self.candidate_hosts[0]

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
        timeout: float = 15.0,
        task: str = "research_synthesis",
    ) -> str:
        """Send chat completion while safely accounting for the selected endpoint."""
        selected_model = model or self.default_model
        request_id = str(uuid.uuid4())
        prompt_chars = sum(len(message.get("content", "")) for message in messages)
        if self.telemetry:
            self.telemetry.start_request(request_id, "phaistos-disk", task, prompt_chars=prompt_chars)
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

        is_local_mac_ollama = self._is_local_mac_ollama()
        execution = "local" if is_local_mac_ollama else "remote"
        started = time.perf_counter()
        snapshot: Optional[Dict[str, Any]] = None
        try:
            if is_local_mac_ollama and LocalAdmission:
                with LocalAdmission() as host_snapshot:
                    snapshot = host_snapshot.to_dict()
                    with urllib.request.urlopen(req, timeout=timeout) as resp:
                        res = json.loads(resp.read().decode("utf-8"))
            else:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
            elapsed = (time.perf_counter() - started) * 1000
            self._record(request_id, task, selected_model, execution, "success", elapsed, host=snapshot)
            return res.get("message", {}).get("content", "")
        except Exception as exc:
            elapsed = (time.perf_counter() - started) * 1000
            status = "deferred" if isinstance(exc, ResourceDeferredError) else "failure"
            error: BaseException | str = exc
            if is_local_mac_ollama and timed_out(exc):
                # urllib timeouts leave Ollama computing; stop only the selected model.
                stop_ollama_model(selected_model)
                error = "cancelled_timeout"
            self._record(request_id, task, selected_model, execution, status, elapsed, error, snapshot)
            if isinstance(exc, ResourceDeferredError):
                raise ConnectionError(str(exc)) from exc
            if isinstance(exc, TimeoutError):
                raise ConnectionError(f"Ollama inference timed out after {timeout}s on {self.host}") from exc
            if isinstance(exc, urllib.error.URLError):
                raise ConnectionError(f"Failed to connect to local Ollama at {self.host}: {exc}") from exc
            raise

    def _is_local_mac_ollama(self) -> bool:
        """Only the Mac's loopback Ollama daemon may be guarded or cancelled."""
        parsed = urlparse(self.host)
        return parsed.hostname in {"localhost", "127.0.0.1", "::1"} and parsed.port in {None, 11434}

    def _record(
        self,
        request_id: str,
        task: str,
        model: str,
        execution: str,
        status: str,
        latency_ms: float,
        error: Optional[BaseException | str] = None,
        host: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Write content-free diagnostics; failures never alter scholarly workflows."""
        if not self.telemetry or not UsageEvent:
            return
        self.telemetry.log_attempt(
            request_id,
            1,
            provider="ollama",
            model=model,
            execution=execution,
            status=status,
            latency_ms=latency_ms,
            error=error,
            host=host,
        )
        self.telemetry.log(
            UsageEvent(
                project="phaistos-disk",
                task=task,
                provider="ollama",
                model=model,
                execution=execution,
                latency_ms=latency_ms,
                status=status,
                error=type(error).__name__ if isinstance(error, BaseException) else error,
                request_id=request_id,
            )
        )
