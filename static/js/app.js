(function () {
  "use strict";

  const tabs = document.querySelectorAll(".tab");
  const forms = {
    wifi: document.getElementById("wifi-form"),
    website: document.getElementById("website-form"),
    text: document.getElementById("text-form"),
  };
  const errorBox = document.getElementById("form-error");
  const resultSection = document.getElementById("qr-result");
  const qrImage = document.getElementById("qr-image");
  const downloadBtn = document.getElementById("download-btn");
  const generateAgainBtn = document.getElementById("generate-again-btn");
  const clearBtn = document.getElementById("clear-btn");

  let currentType = "wifi";
  let currentObjectUrl = null;

  function showTab(type) {
    currentType = type;

    tabs.forEach((tab) => {
      const isActive = tab.dataset.type === type;
      tab.classList.toggle("active", isActive);
      tab.setAttribute("aria-selected", isActive ? "true" : "false");
    });

    Object.entries(forms).forEach(([key, form]) => {
      form.hidden = key !== type;
    });

    hideError();
  }

  function showError(message) {
    errorBox.textContent = message;
    errorBox.hidden = false;
  }

  function hideError() {
    errorBox.textContent = "";
    errorBox.hidden = true;
  }

  function revokeCurrentObjectUrl() {
    if (currentObjectUrl) {
      URL.revokeObjectURL(currentObjectUrl);
      currentObjectUrl = null;
    }
  }

  function buildPayload(type) {
    if (type === "wifi") {
      const form = forms.wifi;
      return {
        type: "wifi",
        ssid: form.ssid.value,
        password: form.password.value,
        security: form.security.value,
        hidden: form.hidden.checked,
      };
    }

    if (type === "website") {
      return {
        type: "website",
        url: forms.website.url.value,
      };
    }

    return {
      type: "text",
      text: forms.text.text.value,
    };
  }

  async function generateQrCode(type) {
    hideError();

    const payload = buildPayload(type);

    let response;
    try {
      response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    } catch (networkError) {
      showError("Could not reach the server. Please try again.");
      return;
    }

    if (!response.ok) {
      let message = "Something went wrong. Please check your input.";
      try {
        const data = await response.json();
        if (data && data.error) {
          message = data.error;
        }
      } catch (parseError) {
        // Keep the default message if the response body isn't JSON.
      }
      showError(message);
      return;
    }

    const blob = await response.blob();
    revokeCurrentObjectUrl();
    currentObjectUrl = URL.createObjectURL(blob);

    qrImage.src = currentObjectUrl;
    resultSection.hidden = false;
    resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => showTab(tab.dataset.type));
  });

  Object.entries(forms).forEach(([type, form]) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      generateQrCode(type);
    });
  });

  downloadBtn.addEventListener("click", () => {
    if (!currentObjectUrl) {
      return;
    }
    const link = document.createElement("a");
    link.href = currentObjectUrl;
    link.download = "qrcode.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  generateAgainBtn.addEventListener("click", () => {
    generateQrCode(currentType);
  });

  clearBtn.addEventListener("click", () => {
    forms[currentType].reset();
    resultSection.hidden = true;
    revokeCurrentObjectUrl();
    qrImage.src = "";
    hideError();
  });

  showTab("wifi");
})();
