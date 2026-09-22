"""
QR Code Generator - Flask application.

Generates QR codes for Wi-Fi networks, website URLs, and plain text.
Everything is processed in memory: no QR data, credentials, or
generated images are written to disk or a database.
"""

import io

from flask import Flask, jsonify, render_template, request, send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_M

from utils.validation import validate_text, validate_url, validate_wifi
from utils.wifi import build_wifi_payload

app = Flask(__name__)

# Keep error responses generic so we never leak stack traces or
# other internal details to the browser.
app.config["PROPAGATE_EXCEPTIONS"] = False


def generate_qr_image(data: str) -> io.BytesIO:
    """Build a PNG QR code image for the given data and return it as a buffer."""
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """
    Accept form data for one of the three QR types, validate it,
    and return the generated QR code as a PNG image.

    Wi-Fi passwords are read from the request, used only to build
    the in-memory QR payload, and are never logged or persisted.
    """
    payload = request.get_json(silent=True) or request.form

    qr_type = (payload.get("type") or "").strip().lower()

    if qr_type == "wifi":
        ssid = payload.get("ssid", "")
        password = payload.get("password", "")
        security = payload.get("security", "nopass")
        hidden = str(payload.get("hidden", "false")).lower() in ("true", "1", "on", "yes")

        is_valid, error_message = validate_wifi(ssid, password, security)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        data = build_wifi_payload(ssid, password, security, hidden)

    elif qr_type == "website":
        url = payload.get("url", "")

        is_valid, error_message = validate_url(url)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        data = url.strip()

    elif qr_type == "text":
        text = payload.get("text", "")

        is_valid, error_message = validate_text(text)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        data = text

    else:
        return jsonify({"error": "Please choose a QR code type."}), 400

    try:
        image_buffer = generate_qr_image(data)
    except Exception:
        # Never expose internal error details to the client.
        return jsonify({"error": "Something went wrong while generating the QR code."}), 500

    return send_file(
        image_buffer,
        mimetype="image/png",
        as_attachment=False,
        download_name="qrcode.png",
    )


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Not found."}), 404


@app.errorhandler(500)
def server_error(_error):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(debug=True)
