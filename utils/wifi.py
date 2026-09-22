"""
Utilities for building Wi-Fi QR code payloads.

The Wi-Fi QR code format looks like this:

    WIFI:T:<security>;S:<ssid>;P:<password>;H:<hidden>;;

Where:
    T = security type (WPA, WEP, or nopass)
    S = network name (SSID)
    P = password (omitted for open networks)
    H = whether the network is hidden (true/false)

Special characters that have meaning in the payload (\\ ; , : ")
must be escaped with a backslash so they are treated as literal
characters instead of field separators.
"""

# Characters that need to be escaped inside a Wi-Fi QR field.
# Backslash must be escaped first, otherwise it would double-escape
# the backslashes we add for the other characters.
_SPECIAL_CHARS = ["\\", ";", ",", ":", '"']


def escape_wifi_value(value: str) -> str:
    """Escape characters that are special in the Wi-Fi QR payload format."""
    if value is None:
        return ""

    escaped = value
    for char in _SPECIAL_CHARS:
        escaped = escaped.replace(char, "\\" + char)
    return escaped


def build_wifi_payload(ssid: str, password: str, security: str, hidden: bool) -> str:
    """
    Build the standard Wi-Fi QR code payload string.

    security is expected to be one of: "WPA", "WEP", "nopass"
    """
    security = (security or "nopass").upper()
    if security == "NONE":
        security = "nopass"

    ssid_escaped = escape_wifi_value(ssid)
    hidden_value = "true" if hidden else "false"

    if security == "NOPASS":
        payload = f"WIFI:T:nopass;S:{ssid_escaped};P:;H:{hidden_value};;"
    else:
        password_escaped = escape_wifi_value(password)
        payload = f"WIFI:T:{security};S:{ssid_escaped};P:{password_escaped};H:{hidden_value};;"

    return payload
