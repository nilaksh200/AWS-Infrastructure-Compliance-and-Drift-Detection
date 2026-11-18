/**
 * IDPS Infrastructure Compliance & Drift Detection Dashboard
 * Client-Side Application Logic (Vanilla JavaScript ES6)
 */

(function () {
  "use strict";

  // Application State
  const state = {
    currentTab: "live", // "live" | "sim" | "compare"
    isScanning: false,
    alertTimeout: null,
  };

  // DOM Elements
  const elements = {
    // Header Metadata
    metaTarget: document.getElementById("meta-target"),
    metaRegion: document.getElementById("meta-region"),
    metaStatus: document.getElementById("meta-status"),

    // Controls
    btnScanLive: document.getElementById("btn-scan-live"),
    scanSpinner: document.getElementById("scan-spinner"),
    btnRefresh: document.getElementById("btn-refresh"),
    btnDownloadLive: document.getElementById("btn-download-live"),
    btnDownloadSim: document.getElementById("btn-download-sim"),

    // Alert
    alertContainer: document.getElementById("alert-container"),
    alertMessage: document.getElementById("alert-message"),
    btnAlertDismiss: document.getElementById("btn-alert-dismiss"),

    // Tabs
    tabLive: document.getElementById("tab-live"),
    tabSim: document.getElementById("tab-sim"),
    tabCompare: document.getElementById("tab-compare"),

    // Banner
    modeBanner: document.getElementById("mode-banner"),
    bannerIcon: document.getElementById("banner-icon"),
    bannerTitle: document.getElementById("banner-title"),
    bannerDesc: document.getElementById("banner-desc"),

    // Views
    viewSingle: document.getElementById("view-single"),
    viewCompare: document.getElementById("view-compare"),

    // Single Report Cards
    cardTotal: document.getElementById("card-total"),
    cardCompliant: document.getElementById("card-compliant"),
    cardNonCompliant: document.getElementById("card-non-compliant"),
    cardErrors: document.getElementById("card-errors"),
    cardPosture: document.getElementById("card-posture"),
    cardPostureSub: document.getElementById("card-posture-sub"),
    reportTimestamp: document.getElementById("report-timestamp"),
    reportResource: document.getElementById("report-resource"),
    checksTbody: document.getElementById("checks-tbody"),

    // Compare View Cards & Table
    cmpTotal: document.getElementById("cmp-total"),
    cmpMatching: document.getElementById("cmp-matching"),
    cmpDrifted: document.getElementById("cmp-drifted"),
    cmpLiveTime: document.getElementById("cmp-live-time"),
    cmpSimTime: document.getElementById("cmp-sim-time"),
    compareTbody: document.getElementById("compare-tbody"),
  };

  /**
   * Helper: Formats arbitrary values for readable tabular display.
   */
  function formatValue(val) {
    if (val === null || val === undefined) return "N/A";
    if (typeof val === "boolean") return val ? "True" : "False";
    if (typeof val === "object") {
      try {
        return JSON.stringify(val);
      } catch (_) {
        return String(val);
      }
    }
    return String(val);
  }

  /**
   * Helper: Formats ISO date string to localized display string.
   */
  function formatDate(isoStr) {
    if (!isoStr || isoStr === "--") return "--";
    try {
      const d = new Date(isoStr);
      return d.toLocaleString() + " (" + isoStr + ")";
    } catch (_) {
      return isoStr;
    }
  }

  /**
   * Displays an alert notification at the top of the dashboard.
   */
  function showAlert(message, type = "info") {
    if (state.alertTimeout) {
      clearTimeout(state.alertTimeout);
    }
    elements.alertContainer.className = `alert-container alert-${type}`;
    elements.alertMessage.textContent = message;
    elements.alertContainer.classList.remove("hidden");

    // Auto-dismiss after 7 seconds for non-error alerts
    if (type !== "error") {
      state.alertTimeout = setTimeout(() => {
        hideAlert();
      }, 7000);
    }
  }

  function hideAlert() {
    elements.alertContainer.classList.add("hidden");
  }

  /**
   * Toggles scanning button UI during active scans.
   */
  function setScanningState(scanning) {
    state.isScanning = scanning;
    if (scanning) {
      elements.btnScanLive.disabled = true;
      elements.btnRefresh.disabled = true;
      elements.scanSpinner.classList.remove("hidden");
      elements.btnScanLive.querySelector(".btn-text").textContent = "Scanning AWS (Read-Only)...";
    } else {
      elements.btnScanLive.disabled = false;
      elements.btnRefresh.disabled = false;
      elements.scanSpinner.classList.add("hidden");
      elements.btnScanLive.querySelector(".btn-text").textContent = "Run Live AWS Scan";
    }
  }

  /**
   * Fetches safe system metadata from /api/status.
   */
  async function fetchStatus() {
    try {
      const res = await fetch("/api/status");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (data.resource_id) {
        elements.metaTarget.textContent = data.resource_id;
        elements.metaTarget.title = data.resource_id;
      }
      if (data.aws_region) {
        elements.metaRegion.textContent = data.aws_region;
      }
      if (data.scan_in_progress) {
        setScanningState(true);
      }
    } catch (err) {
      console.warn("Status fetch failed:", err);
      elements.metaTarget.textContent = "Offline / Error";
    }
  }

  /**
   * Fetches and renders the live AWS compliance report.
   */
  async function fetchLiveReport() {
    renderLoading(elements.checksTbody, "Querying latest live AWS compliance report...");
    try {
      const res = await fetch("/api/reports/latest-live");
      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server returned HTTP ${res.status}`);
      }
      const report = await res.json();
      renderSingleReport(report, true);
    } catch (err) {
      renderError(elements.checksTbody, `Failed to load live report: ${err.message}`);
      showAlert(`Error loading live compliance report: ${err.message}`, "error");
    }
  }

  /**
   * Fetches and renders the simulated drift report.
   */
  async function fetchSimulatedReport() {
    renderLoading(elements.checksTbody, "Loading simulated drift testbench report...");
    try {
      const res = await fetch("/api/reports/simulated");
      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server returned HTTP ${res.status}`);
      }
      const report = await res.json();
      renderSingleReport(report, false);
    } catch (err) {
      renderError(elements.checksTbody, `Failed to load simulated drift report: ${err.message}`);
      showAlert(`Error loading simulated drift report: ${err.message}`, "error");
    }
  }

  /**
   * Fetches and renders the comparison matrix.
   */
  async function fetchComparison() {
    renderLoading(elements.compareTbody, "Calculating side-by-side compliance delta...");
    try {
      const res = await fetch("/api/reports/compare");
      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server returned HTTP ${res.status}`);
      }
      const data = await res.json();
      renderComparison(data);
    } catch (err) {
      renderError(elements.compareTbody, `Failed to load comparison data: ${err.message}`);
      showAlert(`Error comparing reports: ${err.message}`, "error");
    }
  }

  /**
   * Renders the single report view (Live AWS or Simulated Drift).
   */
  function renderSingleReport(report, isLive) {
    const summary = report.summary || {};
    elements.cardTotal.textContent = summary.total ?? 7;
    elements.cardCompliant.textContent = summary.compliant ?? 0;
    elements.cardNonCompliant.textContent = summary.non_compliant ?? 0;
    elements.cardErrors.textContent = summary.errors ?? 0;

    // Posture Badge
    if (summary.is_fully_compliant) {
      elements.cardPosture.className = "posture-badge posture-pass";
      elements.cardPosture.textContent = "COMPLIANT";
      elements.cardPostureSub.textContent = isLive ? "All live AWS baselines match" : "All policies compliant";
    } else if ((summary.errors || 0) > 0) {
      elements.cardPosture.className = "posture-badge posture-warn";
      elements.cardPosture.textContent = "OPERATIONAL ERRORS";
      elements.cardPostureSub.textContent = "API or permission exceptions";
    } else {
      elements.cardPosture.className = "posture-badge posture-fail";
      elements.cardPosture.textContent = "DRIFT DETECTED";
      elements.cardPostureSub.textContent = isLive
        ? "Deviations detected in live state"
        : "Simulated policy violations flagged";
    }

    elements.reportTimestamp.textContent = formatDate(report.timestamp);
    elements.reportResource.textContent = report.resource_id || "--";

    // Populate Table
    const tbody = elements.checksTbody;
    tbody.innerHTML = "";

    const results = report.results || [];
    if (results.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4">No policy evaluation results found.</td></tr>`;
      return;
    }

    results.forEach((check) => {
      const tr = document.createElement("tr");

      // Status Badge
      let statusBadge = "";
      if (check.status === "COMPLIANT") {
        statusBadge = `<span class="status-tag status-tag-compliant" aria-label="Compliant">&#10003; COMPLIANT</span>`;
      } else if (check.status === "NON_COMPLIANT") {
        statusBadge = `<span class="status-tag status-tag-noncompliant" aria-label="Non-Compliant">&#10007; NON_COMPLIANT</span>`;
      } else {
        statusBadge = `<span class="status-tag status-tag-error" aria-label="Error">&#9888; ERROR</span>`;
      }

      const expectedFormatted = formatValue(check.expected_value);
      const observedFormatted = formatValue(check.observed_value);

      tr.innerHTML = `
        <td class="code-font"><strong>${escapeHtml(check.check_id)}</strong></td>
        <td><code>${escapeHtml(check.property_name || "--")}</code></td>
        <td class="code-font">${escapeHtml(expectedFormatted)}</td>
        <td class="code-font ${check.status === "NON_COMPLIANT" ? "val-mismatch" : "val-match"}">${escapeHtml(observedFormatted)}</td>
        <td>${statusBadge}</td>
        <td>${escapeHtml(check.explanation || "--")}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  /**
   * Renders the comparison view.
   */
  function renderComparison(data) {
    const summary = data.summary || {};
    elements.cmpTotal.textContent = summary.total_checks ?? 7;
    elements.cmpMatching.textContent = summary.matching_checks ?? 0;
    elements.cmpDrifted.textContent = summary.drifted_checks ?? 0;

    elements.cmpLiveTime.textContent = formatDate(data.live_timestamp);
    elements.cmpSimTime.textContent = formatDate(data.simulated_timestamp);

    const tbody = elements.compareTbody;
    tbody.innerHTML = "";

    const checks = data.checks || [];
    if (checks.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4">No comparison checks found.</td></tr>`;
      return;
    }

    checks.forEach((item) => {
      const tr = document.createElement("tr");
      if (item.differs) {
        tr.className = "row-drift";
      }

      const diffBadge = item.differs
        ? `<span class="status-tag status-tag-noncompliant">&#9888; DRIFT DETECTED</span>`
        : `<span class="status-tag status-tag-compliant">&#10003; IDENTICAL</span>`;

      tr.innerHTML = `
        <td class="code-font"><strong>${escapeHtml(item.check_id)}</strong><br><small class="text-dim"><code>${escapeHtml(item.property_name)}</code></small></td>
        <td class="code-font">${escapeHtml(formatValue(item.expected_value))}</td>
        <td class="code-font val-match">${escapeHtml(formatValue(item.live_value))}</td>
        <td class="code-font ${item.differs ? "val-mismatch" : "val-match"}">${escapeHtml(formatValue(item.simulated_value))}</td>
        <td>${diffBadge}</td>
        <td>${escapeHtml(item.explanation || "No deviation observed.")}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  /**
   * Triggers a live AWS scan via POST /api/scan/live.
   */
  async function triggerLiveScan() {
    if (state.isScanning) return;
    setScanningState(true);
    showAlert("Initiating live read-only AWS scan in ap-south-1. Please wait...", "info");

    try {
      const res = await fetch("/api/scan/live", { method: "POST" });
      if (res.status === 409) {
        showAlert("A live scan is already in progress on the server.", "warning");
        return;
      }
      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server returned HTTP ${res.status}`);
      }
      const freshReport = await res.json();
      showAlert("Live AWS scan completed successfully. Compliance report updated.", "success");

      // If user is currently on live or compare tab, reload view
      if (state.currentTab === "live") {
        renderSingleReport(freshReport, true);
      } else if (state.currentTab === "compare") {
        fetchComparison();
      }
    } catch (err) {
      showAlert(`Live scan failed: ${err.message}`, "error");
    } finally {
      setScanningState(false);
    }
  }

  /**
   * Switches the active view tab.
   */
  function switchTab(tabId) {
    state.currentTab = tabId;

    // Reset tab active classes
    elements.tabLive.classList.remove("active");
    elements.tabSim.classList.remove("active");
    elements.tabCompare.classList.remove("active");
    elements.tabLive.setAttribute("aria-selected", "false");
    elements.tabSim.setAttribute("aria-selected", "false");
    elements.tabCompare.setAttribute("aria-selected", "false");

    if (tabId === "live") {
      elements.tabLive.classList.add("active");
      elements.tabLive.setAttribute("aria-selected", "true");
      elements.viewSingle.classList.remove("hidden");
      elements.viewCompare.classList.add("hidden");

      elements.modeBanner.className = "mode-banner mode-live";
      elements.bannerIcon.textContent = "📡";
      elements.bannerTitle.textContent = "Live AWS Infrastructure Scan";
      elements.bannerDesc.textContent =
        "Verified production telemetry collected directly from deployed AWS S3 bucket in ap-south-1 using read-only APIs.";

      fetchLiveReport();
    } else if (tabId === "sim") {
      elements.tabSim.classList.add("active");
      elements.tabSim.setAttribute("aria-selected", "true");
      elements.viewSingle.classList.remove("hidden");
      elements.viewCompare.classList.add("hidden");

      elements.modeBanner.className = "mode-banner mode-sim";
      elements.bannerIcon.textContent = "⚠️";
      elements.bannerTitle.textContent = "SIMULATED DRIFT SCENARIO (OFFLINE TESTBENCH)";
      elements.bannerDesc.textContent =
        "Synthetic telemetry simulating 4 unauthorized configuration drifts to demonstrate IDPS policy violations. Actual AWS infrastructure is untouched.";

      fetchSimulatedReport();
    } else if (tabId === "compare") {
      elements.tabCompare.classList.add("active");
      elements.tabCompare.setAttribute("aria-selected", "true");
      elements.viewSingle.classList.add("hidden");
      elements.viewCompare.classList.remove("hidden");

      elements.modeBanner.className = "mode-banner mode-compare";
      elements.bannerIcon.textContent = "⚖️";
      elements.bannerTitle.textContent = "Policy Drift Delta Matrix (Live AWS vs. Simulated Drift)";
      elements.bannerDesc.textContent =
        "Side-by-side analysis contrasting verified production AWS state against the simulated drift testbench across all 7 policies.";

      fetchComparison();
    }
  }

  function renderLoading(tbody, msg) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted"><span class="spinner" style="display:inline-block; vertical-align:middle; margin-right:8px;"></span> ${escapeHtml(msg)}</td></tr>`;
  }

  function renderError(tbody, msg) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-danger">&#9888; ${escapeHtml(msg)}</td></tr>`;
  }

  function escapeHtml(str) {
    if (typeof str !== "string") return String(str);
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  /**
   * Initializes event listeners and loads default view.
   */
  function init() {
    // Tab switching
    elements.tabLive.addEventListener("click", () => switchTab("live"));
    elements.tabSim.addEventListener("click", () => switchTab("sim"));
    elements.tabCompare.addEventListener("click", () => switchTab("compare"));

    // Actions
    elements.btnScanLive.addEventListener("click", triggerLiveScan);
    elements.btnRefresh.addEventListener("click", () => switchTab(state.currentTab));
    elements.btnAlertDismiss.addEventListener("click", hideAlert);

    // Downloads
    elements.btnDownloadLive.addEventListener("click", () => {
      window.location.href = "/api/reports/download/live";
    });
    elements.btnDownloadSim.addEventListener("click", () => {
      window.location.href = "/api/reports/download/simulated";
    });

    // Keyboard support for tabs
    const tabs = [elements.tabLive, elements.tabSim, elements.tabCompare];
    tabs.forEach((tab, idx) => {
      tab.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight") {
          tabs[(idx + 1) % tabs.length].focus();
        } else if (e.key === "ArrowLeft") {
          tabs[(idx - 1 + tabs.length) % tabs.length].focus();
        }
      });
    });

    // Initial load
    fetchStatus();
    switchTab("live");
  }

  // Initialize on DOM load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
