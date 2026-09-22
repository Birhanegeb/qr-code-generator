# QR Code Generator

## Overview

QR Code Generator is a simple, modern, and responsive web application built
with Python and Flask. It lets you generate QR codes for Wi-Fi networks,
website URLs, and plain text, preview the result, and download it as a PNG
image. Everything runs locally - there is no database, no external QR
generation API, and no third-party services involved.

## Features

- Wi-Fi QR codes (SSID, password, security type, hidden network support)
- Website QR codes with URL validation
- Text QR codes for any plain text
- PNG download of the generated QR code
- Responsive, mobile-friendly interface
- Runs as a local Flask application
- Privacy-focused: input is never logged or stored
- No database
- No external QR generation API

## Tech Stack

- **Python** - core application language
- **Flask** - lightweight web framework serving the app and API route
- **qrcode** - generates the QR code matrix
- **Pillow** - renders the QR code as a PNG image
- **HTML / CSS / vanilla JavaScript** - frontend, no build step required
- **pytest** - test suite for validation and Wi-Fi payload logic
- **venv** - isolates project dependencies

## Project Structure

```
qr-code-generator/
├── app.py                  Flask application and /generate route
├── requirements.txt        Python dependencies
├── README.md
├── .gitignore
├── LICENSE
│
├── templates/
│   └── index.html          Main page (type selector, forms, preview)
│
├── static/
│   ├── css/style.css        Styling
│   └── js/app.js            Form handling, fetch calls, download logic
│
├── utils/
│   ├── wifi.py               Wi-Fi QR payload builder and escaping
│   └── validation.py         Input validation for all three QR types
│
└── tests/
    ├── test_wifi.py
    └── test_validation.py
```

## Installation

### Linux / macOS

Clone the repository:

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd qr-code-generator
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Keep the virtual environment active while running the application or the
tests. You will see `(.venv)` at the start of your shell prompt when it is
active.

## Windows Installation

### PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

With the virtual environment active:

```bash
python app.py
```

Then open your browser to:

```
http://127.0.0.1:5000
```

## Testing

With the virtual environment active, run:

```bash
pytest
```

or, if `pytest` is not on your PATH:

```bash
python -m pytest
```

Tests cover Wi-Fi QR payload generation, special-character escaping, and
validation for SSID, password, URL, and text input.

## Deactivating the Virtual Environment

When you are done, deactivate the virtual environment with:

```bash
deactivate
```

## How Wi-Fi QR Codes Work

Wi-Fi QR codes use a standard text payload that phones and QR scanners
recognize automatically. It looks like this:

```
WIFI:T:WPA;S:NetworkName;P:Password;H:false;;
```

- **T** - security type: `WPA` (covers WPA/WPA2), `WEP`, or `nopass` for open
  networks
- **S** - the network name (SSID)
- **P** - the network password (left empty for open networks)
- **H** - whether the network is hidden (`true` or `false`)

Characters that have special meaning in the payload format - backslash (`\`),
semicolon (`;`), comma (`,`), colon (`:`), and double quote (`"`) - are
escaped with a backslash so they are treated as literal characters inside the
SSID or password rather than as field separators.

## Privacy

This application processes all QR code information locally, inside the
Flask application running on your own machine. Wi-Fi passwords and other
form input are used only to build the QR code image in memory and are never
logged, written to a file, saved to a database, or sent to any third-party
service. When you run the app locally, the form data submitted from your
browser to the Flask server stays on your own computer.

## Future Improvements

The following features are not implemented but could be added later:

- SVG export
- PDF export
- vCard QR codes
- Email QR codes
- SMS QR codes
- Custom QR colors
- Logo support
- Dark mode
- Docker deployment

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
