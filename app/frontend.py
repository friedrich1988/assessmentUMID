from __future__ import annotations


def render_frontend() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Galderma MVP Console</title>
  <style>
    :root {
      --bg: #f6efe7;
      --panel: rgba(255, 252, 247, 0.9);
      --ink: #1e1b18;
      --muted: #6e655d;
      --accent: #d4542a;
      --accent-dark: #a33c1a;
      --line: rgba(30, 27, 24, 0.12);
      --card: #fffaf4;
      --ok: #256f4b;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(212, 84, 42, 0.18), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(39, 111, 75, 0.16), transparent 24%),
        linear-gradient(180deg, #fff8f1 0%, var(--bg) 58%, #efe0cf 100%);
      min-height: 100vh;
    }

    .shell {
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 20px 56px;
    }

    .hero {
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(255,255,255,0.88), rgba(255,244,233,0.92));
      box-shadow: 0 28px 60px rgba(56, 36, 17, 0.12);
    }

    .eyebrow {
      margin: 0 0 12px;
      color: var(--accent-dark);
      text-transform: uppercase;
      letter-spacing: 0.22em;
      font-size: 12px;
      font-weight: 700;
    }

    h1 {
      margin: 0;
      font-size: clamp(40px, 6vw, 76px);
      line-height: 0.95;
      letter-spacing: -0.04em;
      max-width: 760px;
    }

    .hero p {
      max-width: 760px;
      margin: 18px 0 0;
      font-size: 18px;
      line-height: 1.6;
      color: var(--muted);
    }

    .grid {
      display: grid;
      grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
      gap: 22px;
      margin-top: 22px;
    }

    .panel {
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--panel);
      box-shadow: 0 22px 50px rgba(56, 36, 17, 0.08);
      overflow: hidden;
    }

    .panel-head {
      padding: 22px 24px 12px;
      border-bottom: 1px solid var(--line);
    }

    .panel-head h2 {
      margin: 0;
      font-size: 24px;
      letter-spacing: -0.03em;
    }

    .panel-head p {
      margin: 8px 0 0;
      color: var(--muted);
      line-height: 1.5;
    }

    .controls {
      padding: 24px;
      display: grid;
      gap: 16px;
    }

    label {
      display: grid;
      gap: 8px;
      font-size: 14px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    input, textarea {
      width: 100%;
      border: 1px solid rgba(30, 27, 24, 0.18);
      border-radius: 16px;
      padding: 14px 16px;
      font: inherit;
      font-size: 16px;
      color: var(--ink);
      background: rgba(255,255,255,0.92);
    }

    textarea {
      min-height: 140px;
      resize: vertical;
      line-height: 1.5;
    }

    .actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    button {
      border: 0;
      border-radius: 999px;
      padding: 14px 18px;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
      transition: transform 140ms ease, opacity 140ms ease, background 140ms ease;
    }

    button:hover {
      transform: translateY(-1px);
    }

    button.primary {
      background: var(--accent);
      color: #fff8f2;
    }

    button.secondary {
      background: rgba(30, 27, 24, 0.08);
      color: var(--ink);
    }

    button:disabled {
      opacity: 0.55;
      cursor: wait;
      transform: none;
    }

    .status {
      padding: 0 24px 24px;
      color: var(--ok);
      min-height: 24px;
      font-size: 15px;
    }

    .output {
      padding: 24px;
      display: grid;
      gap: 18px;
    }

    .meta {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }

    .stat {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 16px;
    }

    .stat strong {
      display: block;
      font-size: 13px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }

    .stat span {
      font-size: 24px;
      letter-spacing: -0.03em;
    }

    .download {
      display: none;
      width: fit-content;
      padding: 12px 18px;
      border-radius: 999px;
      background: #1e1b18;
      color: #fff8f2;
      text-decoration: none;
      font-weight: 700;
    }

    .download.show {
      display: inline-flex;
    }

    pre {
      margin: 0;
      padding: 18px;
      border-radius: 18px;
      background: #1b1714;
      color: #f8efe7;
      overflow: auto;
      line-height: 1.5;
      font-size: 14px;
      min-height: 360px;
    }

    @media (max-width: 900px) {
      .grid {
        grid-template-columns: 1fr;
      }

      .actions,
      .meta {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Galderma Interview MVP</p>
      <h1>From business question to deck in one page.</h1>
      <p>
        This frontend sits directly on top of the MVP API. It lets you inspect KPI data,
        run the forecast, trigger the prompt-driven workflow, and download the generated
        PowerPoint without touching the command line.
      </p>
    </section>

    <section class="grid">
      <div class="panel">
        <div class="panel-head">
          <h2>Control Panel</h2>
          <p>Use the direct buttons for API checks or run the full prompt-based presentation flow.</p>
        </div>
        <div class="controls">
          <label>
            Brand
            <input id="brand" value="BrandA" />
          </label>
          <label>
            Product
            <input id="product" value="ProductA1" />
          </label>
          <label>
            Business Question
            <textarea id="question">Create a presentation for BrandA with forecast for the next quarter and include product ProductA1</textarea>
          </label>
          <div class="actions">
            <button class="secondary" id="kpiBtn">Load KPI</button>
            <button class="secondary" id="forecastBtn">Load Forecast</button>
            <button class="primary" id="askBtn">Generate Deck</button>
            <button class="secondary" id="healthBtn">Check Health</button>
          </div>
        </div>
        <div class="status" id="status">Ready.</div>
      </div>

      <div class="panel">
        <div class="panel-head">
          <h2>Response Viewer</h2>
          <p>Latest API response plus shortcut metrics for the current brand and product.</p>
        </div>
        <div class="output">
          <div class="meta">
            <div class="stat">
              <strong>Brand</strong>
              <span id="brandStat">BrandA</span>
            </div>
            <div class="stat">
              <strong>Product</strong>
              <span id="productStat">ProductA1</span>
            </div>
            <div class="stat">
              <strong>Deck</strong>
              <span id="deckStat">Not generated</span>
            </div>
          </div>
          <a id="downloadLink" class="download" href="#">Download Latest Deck</a>
          <pre id="output">Run a request to see the JSON response here.</pre>
        </div>
      </div>
    </section>
  </main>

  <script>
    const brandInput = document.getElementById("brand");
    const productInput = document.getElementById("product");
    const questionInput = document.getElementById("question");
    const statusNode = document.getElementById("status");
    const outputNode = document.getElementById("output");
    const brandStat = document.getElementById("brandStat");
    const productStat = document.getElementById("productStat");
    const deckStat = document.getElementById("deckStat");
    const downloadLink = document.getElementById("downloadLink");
    const buttons = Array.from(document.querySelectorAll("button"));

    function setBusy(isBusy, message) {
      buttons.forEach((button) => {
        button.disabled = isBusy;
      });
      statusNode.textContent = message;
    }

    function renderResponse(data) {
      outputNode.textContent = JSON.stringify(data, null, 2);
      if (data.brand) {
        brandStat.textContent = data.brand;
      }
      if (data.product) {
        productStat.textContent = data.product;
      }
      if (data.presentation_file) {
        deckStat.textContent = "Generated";
        downloadLink.href = `/presentation/${encodeURIComponent(data.brand)}`;
        downloadLink.classList.add("show");
      }
    }

    function renderError(errorText) {
      outputNode.textContent = errorText;
      statusNode.textContent = "Request failed.";
    }

    async function requestJson(url, options = {}) {
      const response = await fetch(url, options);
      const contentType = response.headers.get("content-type") || "";
      const payload = contentType.includes("application/json")
        ? await response.json()
        : await response.text();
      if (!response.ok) {
        throw new Error(typeof payload === "string" ? payload : JSON.stringify(payload, null, 2));
      }
      return payload;
    }

    document.getElementById("healthBtn").addEventListener("click", async () => {
      setBusy(true, "Checking API health...");
      try {
        const payload = await requestJson("/health");
        renderResponse(payload);
        statusNode.textContent = "Health check passed.";
      } catch (error) {
        renderError(String(error));
      } finally {
        setBusy(false, statusNode.textContent);
      }
    });

    document.getElementById("kpiBtn").addEventListener("click", async () => {
      setBusy(true, "Loading KPI snapshot...");
      try {
        const brand = brandInput.value.trim();
        const payload = await requestJson(`/kpi?brand=${encodeURIComponent(brand)}`);
        renderResponse(payload);
        statusNode.textContent = "KPI loaded.";
      } catch (error) {
        renderError(String(error));
      } finally {
        setBusy(false, statusNode.textContent);
      }
    });

    document.getElementById("forecastBtn").addEventListener("click", async () => {
      setBusy(true, "Running forecast...");
      try {
        const product = productInput.value.trim();
        const payload = await requestJson(`/forecast?product=${encodeURIComponent(product)}`);
        renderResponse(payload);
        statusNode.textContent = "Forecast loaded.";
      } catch (error) {
        renderError(String(error));
      } finally {
        setBusy(false, statusNode.textContent);
      }
    });

    document.getElementById("askBtn").addEventListener("click", async () => {
      setBusy(true, "Generating presentation...");
      try {
        const payload = await requestJson("/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: questionInput.value.trim() })
        });
        renderResponse(payload);
        statusNode.textContent = "Presentation flow completed.";
      } catch (error) {
        renderError(String(error));
      } finally {
        setBusy(false, statusNode.textContent);
      }
    });
  </script>
</body>
</html>
"""
