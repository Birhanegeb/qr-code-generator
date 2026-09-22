from utils.wifi import build_wifi_payload, escape_wifi_value


def test_escape_wifi_value_escapes_special_characters():
    raw = 'a\\b;c,d:e"f'
    escaped = escape_wifi_value(raw)
    assert escaped == 'a\\\\b\\;c\\,d\\:e\\"f'


def test_escape_wifi_value_handles_empty_string():
    assert escape_wifi_value("") == ""


def test_build_wifi_payload_wpa():
    payload = build_wifi_payload("MyNetwork", "MyPassword", "WPA", False)
    assert payload == "WIFI:T:WPA;S:MyNetwork;P:MyPassword;H:false;;"


def test_build_wifi_payload_hidden_network():
    payload = build_wifi_payload("MyNetwork", "MyPassword", "WPA", True)
    assert payload == "WIFI:T:WPA;S:MyNetwork;P:MyPassword;H:true;;"


def test_build_wifi_payload_open_network_has_no_password():
    payload = build_wifi_payload("OpenNet", "", "nopass", False)
    assert payload == "WIFI:T:nopass;S:OpenNet;P:;H:false;;"


def test_build_wifi_payload_escapes_special_characters_in_fields():
    payload = build_wifi_payload("My;Net", "Pa:ss", "WPA", False)
    assert payload == "WIFI:T:WPA;S:My\\;Net;P:Pa\\:ss;H:false;;"


def test_build_wifi_payload_wep():
    payload = build_wifi_payload("OldNet", "12345", "WEP", False)
    assert payload == "WIFI:T:WEP;S:OldNet;P:12345;H:false;;"
