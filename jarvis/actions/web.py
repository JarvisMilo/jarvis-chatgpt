from __future__ import annotations
import webbrowser
from urllib.parse import urlparse
from jarvis.tools import RiskLevel, Tool, ToolError

def _open_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ToolError("Only absolute http/https URLs are allowed")
    webbrowser.open(url)
    return {"opened": url}

TOOL = Tool(
    name="open_url",
    description="Open an approved HTTP(S) URL in the default browser.",
    handler=_open_url,
    parameters={"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
    risk=RiskLevel.EXTERNAL_SIDE_EFFECT,
    requires_confirmation=True,
    category="browser",
)
