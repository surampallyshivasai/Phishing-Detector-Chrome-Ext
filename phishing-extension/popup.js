document.addEventListener("DOMContentLoaded", function () {
  const statusDiv = document.getElementById("status");
  const urlDisplayDiv = document.getElementById("url-display");
  const probabilityDiv = document.getElementById("probability");

  // Show loading state
  statusDiv.innerHTML = "🔍 Analyzing URL...";
  statusDiv.className = "loading";

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentUrl = tabs[0].url;
    
    // Display the URL being analyzed
    urlDisplayDiv.textContent = currentUrl;

    // Make API request
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: currentUrl })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        throw new Error(data.error);
      }

      const prediction = data.prediction;
      const phishingProb = data.phishing_probability || 0;
      const safeProb = data.safe_probability || 0;

      if (prediction === 1) {
        statusDiv.innerHTML = "⚠️ <b>PHISHING DETECTED!</b>";
        statusDiv.className = "danger";
        probabilityDiv.innerHTML = `Phishing Probability: ${(phishingProb * 100).toFixed(1)}%`;
      } else if (prediction === 0) {
        statusDiv.innerHTML = "✅ <b>SAFE</b>";
        statusDiv.className = "safe";
        probabilityDiv.innerHTML = `Safe Probability: ${(safeProb * 100).toFixed(1)}%`;
      } else {
        statusDiv.innerHTML = "❓ <b>UNCERTAIN</b>";
        statusDiv.className = "error";
        probabilityDiv.innerHTML = "Unable to determine";
      }
    })
    .catch(error => {
      console.error("Error:", error);
      statusDiv.innerHTML = "❌ <b>ERROR</b><br>Check if API is running";
      statusDiv.className = "error";
      probabilityDiv.innerHTML = "Make sure the ML API is running on localhost:5000";
    });
  });
});
