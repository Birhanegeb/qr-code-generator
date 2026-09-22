"""
Simple input validation helpers for the QR code generator.

Each function returns an (is_valid, error_message) tuple so callers
can decide what to do with the result without relying on exceptions
for normal validation flow.
"""

import re

_URL_PATTERN = re.compile(
    r"^(https?://)"                      # http:// or https://
    r"([a-zA-Z0-9\-._~%]+"               # domain / host
    r"(:[0-9]+)?)"                       # optional port
    r"(/[^\s]*)?$",                      # optional path/query
    re.IGNORECASE,
)

VALID_SECURITY_TYPES = {"WPA", "WEP", "nopass"}


def validate_wifi(ssid: str, password: str, security: str) -> tuple[bool, str]:
    """Validate Wi-Fi form input."""
    if not ssid or not ssid.strip():
        return False, "Network name is required."

    security_normalized = (security or "").strip()
    if security_normalized not in VALID_SECURITY_TYPES:
        return False, "Please choose a valid security type."

    if security_normalized in ("WPA", "WEP") and not (password or "").strip():
        if security_normalized == "WPA":
            return False, "Password is required for WPA/WPA2 networks."
        return False, "Password is required for WEP networks."

    return True, ""


def validate_url(url: str) -> tuple[bool, str]:
    """Validate a website URL. Both http and https are accepted."""
    if not url or not url.strip():
        return False, "Please enter a valid website URL."

    url = url.strip()
    if not _URL_PATTERN.match(url):
        return False, "Please enter a valid website URL."

    return True, ""


def validate_text(text: str) -> tuple[bool, str]:
    """Validate plain text input."""
    if not text or not text.strip():
        return False, "Please enter some text."

    return True, ""
