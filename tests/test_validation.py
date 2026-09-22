from utils.validation import validate_text, validate_url, validate_wifi


def test_validate_wifi_requires_ssid():
    is_valid, message = validate_wifi("", "password", "WPA")
    assert is_valid is False
    assert message == "Network name is required."


def test_validate_wifi_requires_password_for_wpa():
    is_valid, message = validate_wifi("MyNetwork", "", "WPA")
    assert is_valid is False
    assert message == "Password is required for WPA/WPA2 networks."


def test_validate_wifi_requires_password_for_wep():
    is_valid, message = validate_wifi("MyNetwork", "", "WEP")
    assert is_valid is False
    assert message == "Password is required for WEP networks."


def test_validate_wifi_allows_open_network_without_password():
    is_valid, message = validate_wifi("MyNetwork", "", "nopass")
    assert is_valid is True
    assert message == ""


def test_validate_wifi_accepts_valid_wpa_input():
    is_valid, message = validate_wifi("MyNetwork", "secret123", "WPA")
    assert is_valid is True
    assert message == ""


def test_validate_wifi_rejects_unknown_security_type():
    is_valid, message = validate_wifi("MyNetwork", "secret123", "BOGUS")
    assert is_valid is False


def test_validate_url_accepts_https():
    is_valid, message = validate_url("https://example.com")
    assert is_valid is True
    assert message == ""


def test_validate_url_accepts_http():
    is_valid, message = validate_url("http://example.com")
    assert is_valid is True
    assert message == ""


def test_validate_url_rejects_empty_string():
    is_valid, message = validate_url("")
    assert is_valid is False
    assert message == "Please enter a valid website URL."


def test_validate_url_rejects_missing_scheme():
    is_valid, message = validate_url("example.com")
    assert is_valid is False


def test_validate_text_rejects_empty_string():
    is_valid, message = validate_text("")
    assert is_valid is False
    assert message == "Please enter some text."


def test_validate_text_rejects_whitespace_only():
    is_valid, message = validate_text("   ")
    assert is_valid is False


def test_validate_text_accepts_normal_text():
    is_valid, message = validate_text("Hello, world!")
    assert is_valid is True
    assert message == ""
