/**
 * VeritasAI — Frontend Application Logic
 * Interactive real-time verification, XAI attention heatmap,
 * Chart.js benchmark dashboards, and history management.
 */

document.addEventListener("DOMContentLoaded", () => {
    // State
    let currentMode = "text"; // "text" or "url"
    let currentScanId = null;
    let benchmarkChart = null;
    let lossChart = null;

    // Elements - Navigation
    const navTabs = document.querySelectorAll(".nav-tab");
    const tabContents = document.querySelectorAll(".tab-content");

    // Elements - Mode Toggle
    const modeTextBtn = document.getElementById("mode-text-btn");
    const modeUrlBtn = document.getElementById("mode-url-btn");
    const formTextMode = document.getElementById("form-text-mode");
    const formUrlMode = document.getElementById("form-url-mode");

    // Elements - Inputs
    const inputHeadline = document.getElementById("input-headline");
    const inputBody = document.getElementById("input-body");
    const inputDomain = document.getElementById("input-source-domain");
    const inputUrl = document.getElementById("input-url");
    const textCharCount = document.getElementById("text-char-count");
    const btnClearInput = document.getElementById("btn-clear-input");
    const btnRunAnalysis = document.getElementById("btn-run-analysis");
    const btnSpinner = document.getElementById("btn-spinner");
    const btnActionText = document.getElementById("btn-action-text");
    const btnPasteUrl = document.getElementById("btn-paste-url");

    // Elements - Quick Chips
    const chipRealScience = document.getElementById("chip-real-science");
    const chipFakeHealth = document.getElementById("chip-fake-health");
    const chipFake5g = document.getElementById("chip-fake-5g");
    const chipSatireOnion = document.getElementById("chip-satire-onion");

    const chipUrlReuters = document.getElementById("chip-url-reuters");
    const chipUrlBbc = document.getElementById("chip-url-bbc");
    const chipUrlOnion = document.getElementById("chip-url-onion");

    // Elements - Results State
    const emptyState = document.getElementById("empty-state");
    const loadingState = document.getElementById("loading-state");
    const verdictContent = document.getElementById("verdict-content");

    // Elements - Verdict Displays
    const verdictBanner = document.getElementById("verdict-banner");
    const verdictIcon = document.getElementById("verdict-icon");
    const verdictTitle = document.getElementById("verdict-title");
    const verdictModelUsed = document.getElementById("verdict-model-used");
    const verdictScanId = document.getElementById("verdict-scan-id");

    const scrapedMetaBox = document.getElementById("scraped-meta-box");
    const scrapedMetaTitle = document.getElementById("scraped-meta-title");
    const scrapedMetaDomain = document.getElementById("scraped-meta-domain");
    const scrapedMetaAuthor = document.getElementById("scraped-meta-author");
    const scrapedMetaDate = document.getElementById("scraped-meta-date");
    const scrapedMetaWords = document.getElementById("scraped-meta-words");

    const gaugeProgressBar = document.getElementById("gauge-progress-bar");
    const confidencePercentage = document.getElementById("confidence-percentage");
    const realProbBar = document.getElementById("real-prob-bar");
    const fakeProbBar = document.getElementById("fake-prob-bar");

    const metricClickbait = document.getElementById("metric-clickbait");
    const barClickbait = document.getElementById("bar-clickbait");
    const metricSubjectivity = document.getElementById("metric-subjectivity");
    const barSubjectivity = document.getElementById("bar-subjectivity");
    const metricCaps = document.getElementById("metric-caps");
    const barCaps = document.getElementById("bar-caps");
    const metricDomainTrust = document.getElementById("metric-domain-trust");
    const barDomainTrust = document.getElementById("bar-domain-trust");

    const xaiTokensContainer = document.getElementById("xai-tokens-container");
    const reasonsList = document.getElementById("reasons-list");

    const btnFbAgree = document.getElementById("btn-fb-agree");
    const btnFbDisagree = document.getElementById("btn-fb-disagree");
    const feedbackAcknowledgement = document.getElementById("feedback-acknowledgement");

    // Elements - Other Views
    const casesGridContainer = document.getElementById("cases-grid-container");
    const historyTableBody = document.getElementById("history-table-body");
    const historyFilter = document.getElementById("history-filter");
    const btnExportCsv = document.getElementById("btn-export-csv");

    // -------------------------------------------------------------
    // 1. Navigation & Tab Switching
    // -------------------------------------------------------------
    navTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const targetId = tab.getAttribute("data-tab");
            navTabs.forEach(t => t.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            tab.classList.add("active");
            const targetContent = document.getElementById(targetId);
            if (targetContent) targetContent.classList.add("active");

            // Lazy load view contents
            if (targetId === "social-radar-view") loadSocialRadar();
            if (targetId === "cases-view") loadCaseStudies();
            if (targetId === "benchmark-view") loadBenchmarks();
            if (targetId === "history-view") loadHistory();
        });
    });

    // -------------------------------------------------------------
    // 2. Input Mode Switching
    // -------------------------------------------------------------
    modeTextBtn.addEventListener("click", () => {
        currentMode = "text";
        modeTextBtn.classList.add("active");
        modeUrlBtn.classList.remove("active");
        formTextMode.style.display = "flex";
        formUrlMode.style.display = "none";
        btnActionText.textContent = "Run Neural Verification";
    });

    modeUrlBtn.addEventListener("click", () => {
        currentMode = "url";
        modeUrlBtn.classList.add("active");
        modeTextBtn.classList.remove("active");
        formTextMode.style.display = "none";
        formUrlMode.style.display = "flex";
        btnActionText.textContent = "Scrape & Verify Article";
    });

    // Textarea Char Counter
    inputBody.addEventListener("input", () => {
        textCharCount.textContent = `${inputBody.value.length} characters`;
    });

    // Clear Button
    btnClearInput.addEventListener("click", () => {
        inputHeadline.value = "";
        inputBody.value = "";
        inputDomain.value = "";
        inputUrl.value = "";
        textCharCount.textContent = "0 characters";
    });

    // Paste URL Button
    btnPasteUrl.addEventListener("click", async () => {
        try {
            const text = await navigator.clipboard.readText();
            if (text) inputUrl.value = text.trim();
        } catch (err) {
            alert("Clipboard access was blocked by the browser. Please paste with Ctrl+V.");
        }
    });

    // -------------------------------------------------------------
    // 3. Quick Test Chips Injector
    // -------------------------------------------------------------
    chipRealScience.addEventListener("click", () => {
        inputHeadline.value = "NASA Perseverance Rover Detects Organic Molecules in Ancient Martian Lakebed";
        inputBody.value = "NASA scientists confirmed that the Perseverance rover has discovered diverse organic carbon compounds in sedimentary rock cores collected from the Jezero Crater delta. According to research published in the peer-reviewed journal Nature, the findings offer compelling insights into the geochemical environment that existed on Mars more than three billion years ago. Investigators noted that while organic molecules can form through non-biological processes, their presence provides critical data for future sample return missions.";
        inputDomain.value = "reuters.com";
        textCharCount.textContent = `${inputBody.value.length} characters`;
    });

    chipFakeHealth.addEventListener("click", () => {
        inputHeadline.value = "SHOCKING TRUTH: Common Lemon Peels 100% Cure Cancer In 24 Hours Suppressed By Big Pharma!";
        inputBody.value = "SHOCKING TRUTH EXPOSED: Mainstream media is completely silent as whistleblowers leak classified medical research proving that boiled lemon water with baking soda destroys 100% of cancer cells in just 24 hours! Corrupt pharmaceutical conglomerates have banned this miraculous cure to preserve chemotherapy revenue! Share this post immediately before it is censored and deleted from the internet forever!";
        inputDomain.value = "naturalnews-miracle.com";
        textCharCount.textContent = `${inputBody.value.length} characters`;
    });

    chipFake5g.addEventListener("click", () => {
        inputHeadline.value = "BOMBSHELL LEAK: 5G Towers Emitting Frequencies to Alter DNA and Trigger Blackout";
        inputBody.value = "DEEP STATE AGENDA REVEALED: Rogue engineers have declassified secret Pentagon documents proving that new high-frequency 5G cellular antennas are emitting pulsed electromagnetic radiation specifically calibrated to alter human DNA and monitor citizens! A total nationwide blackout is scheduled for this weekend to wipe bank account balances to zero! Wake up people and withdraw all your cash!";
        inputDomain.value = "beforeitsnews-unfiltered.com";
        textCharCount.textContent = `${inputBody.value.length} characters`;
    });

    chipSatireOnion.addEventListener("click", () => {
        inputHeadline.value = "Department of Transportation Installs Virtual Speed Bumps on Internet to Slow Bad Information";
        inputBody.value = "WASHINGTON—In an ambitious attempt to regulate the rapid velocity of modern digital discourse, the Federal Highway Administration announced Tuesday that it has begun deploying millions of virtual rubber speed bumps across global fiber-optic cables. Agency officials stated the newly installed digital speed humps will force high-speed packet traffic to decelerate from 100 megabits per second down to an orderly 15 miles per hour whenever entering controversial comment sections.";
        inputDomain.value = "theonion.com";
        textCharCount.textContent = `${inputBody.value.length} characters`;
    });

    chipUrlReuters.addEventListener("click", () => {
        inputUrl.value = "https://www.reuters.com/technology/artificial-intelligence";
    });

    chipUrlBbc.addEventListener("click", () => {
        inputUrl.value = "https://www.bbc.com/news/science-environment";
    });

    chipUrlOnion.addEventListener("click", () => {
        inputUrl.value = "https://www.theonion.com/man-successfully-fakes-work-meeting-by-nodding";
    });

    // -------------------------------------------------------------
    // 4. Analysis Execution
    // -------------------------------------------------------------
    btnRunAnalysis.addEventListener("click", executeVerification);

    async function executeVerification() {
        if (currentMode === "text") {
            const bodyText = inputBody.value.trim();
            if (!bodyText || bodyText.length < 10) {
                alert("Please enter at least 10 characters of news text or article body.");
                inputBody.focus();
                return;
            }
            await runTextAnalysis(bodyText, inputHeadline.value.trim(), inputDomain.value.trim());
        } else {
            const urlText = inputUrl.value.trim();
            if (!urlText || urlText.length < 5) {
                alert("Please enter a valid news webpage URL.");
                inputUrl.focus();
                return;
            }
            await runUrlAnalysis(urlText);
        }
    }

    function setExecutionState(isLoading, titleText = "Processing Neural Embeddings...") {
        if (isLoading) {
            btnRunAnalysis.disabled = true;
            btnSpinner.style.display = "inline-block";
            btnActionText.textContent = "Analyzing...";
            emptyState.style.display = "none";
            verdictContent.style.display = "none";
            loadingState.style.display = "flex";
            document.getElementById("loading-title").textContent = titleText;
        } else {
            btnRunAnalysis.disabled = false;
            btnSpinner.style.display = "none";
            btnActionText.textContent = currentMode === "text" ? "Run Neural Verification" : "Scrape & Verify Article";
            loadingState.style.display = "none";
        }
    }

    async function runTextAnalysis(text, title, domain) {
        setExecutionState(true, "Tokenizing & Computing BiLSTM Attention Weights...");
        try {
            const response = await fetch("/api/analyze-text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text, title, domain })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Analysis request failed.");
            }

            const data = await response.json();
            renderResults(data, false);
        } catch (err) {
            alert(`Analysis Error: ${err.message}`);
            emptyState.style.display = "flex";
        } finally {
            setExecutionState(false);
        }
    }

    async function runUrlAnalysis(url) {
        setExecutionState(true, "Scraping Live Webpage & Extracting Article Text...");
        try {
            const response = await fetch("/api/analyze-url", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "URL scraping failed.");
            }

            const data = await response.json();
            renderResults(data, true);
        } catch (err) {
            alert(`Live URL Error: ${err.message}`);
            emptyState.style.display = "flex";
        } finally {
            setExecutionState(false);
        }
    }

    // -------------------------------------------------------------
    // 5. Render Verdict & Visual Telemetry
    // -------------------------------------------------------------
    function renderResults(data, isUrl = false) {
        currentScanId = data.scan_id;
        emptyState.style.display = "none";
        verdictContent.style.display = "flex";
        feedbackAcknowledgement.textContent = "";

        // Verdict Banner
        verdictBanner.className = "verdict-banner";
        if (data.verdict === "Real News") {
            verdictBanner.classList.add("verdict-real");
            verdictIcon.textContent = "✅";
            verdictTitle.textContent = "VERIFIED REAL NEWS";
            verdictTitle.style.color = "var(--accent-emerald)";
        } else if (data.verdict === "Fake News") {
            verdictBanner.classList.add("verdict-fake");
            verdictIcon.textContent = "⚠️";
            verdictTitle.textContent = "FLAGGED AS FAKE NEWS";
            verdictTitle.style.color = "var(--accent-rose)";
        } else {
            verdictBanner.classList.add("verdict-uncertain");
            verdictIcon.textContent = "❓";
            verdictTitle.textContent = "UNCERTAIN / SATIRE";
            verdictTitle.style.color = "var(--accent-amber)";
        }

        verdictScanId.textContent = `#ID-${data.scan_id || 1}`;
        verdictModelUsed.textContent = data.model_architecture || "BiLSTM-CNN-Attention";

        // Scraped Metadata Box
        if (isUrl && data.article_metadata) {
            scrapedMetaBox.style.display = "block";
            scrapedMetaTitle.textContent = data.article_metadata.title || "Scraped Web Article";
            scrapedMetaDomain.textContent = data.article_metadata.domain || "Web";
            scrapedMetaAuthor.textContent = data.article_metadata.author || "Unknown Author";
            scrapedMetaDate.textContent = data.article_metadata.publish_date || "Recent";
            scrapedMetaWords.textContent = data.article_metadata.word_count || "0";
        } else {
            scrapedMetaBox.style.display = "none";
        }

        // Radial Confidence Gauge
        const confPercent = Math.round(data.confidence);
        animateRadialGauge(confPercent, data.verdict);

        // Split Bar
        const realProb = Math.round(data.real_probability);
        const fakeProb = Math.round(data.fake_probability);
        realProbBar.style.width = `${realProb}%`;
        realProbBar.textContent = `Real: ${realProb}%`;
        fakeProbBar.style.width = `${fakeProb}%`;
        fakeProbBar.textContent = `Fake: ${fakeProb}%`;

        // Stylometrics
        const stylometrics = data.stylometrics || {};
        metricClickbait.textContent = `${stylometrics.clickbait_index || 0}%`;
        barClickbait.style.width = `${Math.min(stylometrics.clickbait_index || 0, 100)}%`;

        metricSubjectivity.textContent = `${stylometrics.subjectivity_score || 0}%`;
        barSubjectivity.style.width = `${Math.min(stylometrics.subjectivity_score || 0, 100)}%`;

        metricCaps.textContent = `${stylometrics.caps_ratio || 0}%`;
        barCaps.style.width = `${Math.min((stylometrics.caps_ratio || 0) * 3, 100)}%`;

        const domainIntel = data.domain_intel || {};
        metricDomainTrust.textContent = `${domainIntel.trust_level || 'Neutral'} (${domainIntel.trust_score || 50}%)`;
        barDomainTrust.style.width = `${domainIntel.trust_score || 50}%`;

        // Explainable AI (XAI) Token Attention Heatmap
        renderExplainableTokens(data.explainable_tokens || []);

        // Key Algorithmic Observations
        reasonsList.innerHTML = "";
        (data.reasons || []).forEach(reason => {
            const li = document.createElement("li");
            li.textContent = reason;
            reasonsList.appendChild(li);
        });

        // Scroll into view on mobile
        if (window.innerWidth < 1024) {
            verdictContent.scrollIntoView({ behavior: "smooth" });
        }
    }

    function animateRadialGauge(percent, verdict) {
        const circumference = 2 * Math.PI * 50; // ~314.159
        const offset = circumference - (percent / 100) * circumference;

        gaugeProgressBar.style.strokeDashoffset = offset;
        if (verdict === "Real News") {
            gaugeProgressBar.style.stroke = "var(--accent-emerald)";
        } else if (verdict === "Fake News") {
            gaugeProgressBar.style.stroke = "var(--accent-rose)";
        } else {
            gaugeProgressBar.style.stroke = "var(--accent-amber)";
        }

        // Animated counter
        let current = 0;
        const step = Math.max(1, Math.floor(percent / 25));
        const timer = setInterval(() => {
            current += step;
            if (current >= percent) {
                current = percent;
                clearInterval(timer);
            }
            confidencePercentage.textContent = `${current}%`;
        }, 20);
    }

    function renderExplainableTokens(tokens) {
        xaiTokensContainer.innerHTML = "";
        if (!tokens || tokens.length === 0) {
            xaiTokensContainer.textContent = "No tokens parsed.";
            return;
        }

        tokens.forEach(tok => {
            const span = document.createElement("span");
            span.className = `token-word token-${tok.type}`;
            span.textContent = tok.word;
            if (tok.type === "suspicious") {
                span.title = `Deceptive Attribution Score: +${tok.score} (Clickbait / Trigger)`;
            } else if (tok.type === "factual") {
                span.title = `Factual Attribution Score: ${tok.score} (Journalistic Marker)`;
            }
            xaiTokensContainer.appendChild(span);
        });
    }

    // -------------------------------------------------------------
    // 6. Active Learning Feedback
    // -------------------------------------------------------------
    btnFbAgree.addEventListener("click", () => submitFeedback("correct"));
    btnFbDisagree.addEventListener("click", () => submitFeedback("incorrect"));

    async function submitFeedback(feedbackType) {
        if (!currentScanId) return;
        try {
            const res = await fetch("/api/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ scan_id: currentScanId, feedback: feedbackType })
            });
            if (res.ok) {
                feedbackAcknowledgement.textContent = feedbackType === "correct"
                    ? "✓ Thank you! Verdict verified."
                    : "✓ Feedback noted. Sample logged for retraining queue.";
            }
        } catch (err) {
            console.error(err);
        }
    }

    // -------------------------------------------------------------
    // 7. Case Studies Loader
    // -------------------------------------------------------------
    async function loadCaseStudies() {
        if (casesGridContainer.children.length > 0) return; // already loaded
        try {
            const res = await fetch("/api/case-studies");
            const cases = await res.json();

            casesGridContainer.innerHTML = "";
            cases.forEach(item => {
                const card = document.createElement("div");
                card.className = "case-card glass-card";

                const isReal = item.expected.includes("Real");
                const badgeClass = isReal ? "badge-real" : "badge-fake";

                card.innerHTML = `
                    <div>
                        <div class="case-card-header">
                            <span class="case-category">${item.category}</span>
                            <span class="case-badge ${badgeClass}">${item.expected}</span>
                        </div>
                        <h3 class="case-card-title">${item.title}</h3>
                        <p class="case-card-snippet">${item.text}</p>
                    </div>
                    <div class="case-card-footer">
                        <span class="case-domain">🌐 ${item.domain}</span>
                        <button class="btn-run-case" data-id="${item.id}">⚡ Run Scan</button>
                    </div>
                `;

                const runBtn = card.querySelector(".btn-run-case");
                runBtn.addEventListener("click", () => {
                    // Populate scanner and switch tab
                    document.getElementById("tab-scanner").click();
                    modeTextBtn.click();
                    inputHeadline.value = item.title;
                    inputBody.value = item.text;
                    inputDomain.value = item.domain;
                    textCharCount.textContent = `${item.text.length} characters`;
                    // Trigger analysis
                    executeVerification();
                });

                casesGridContainer.appendChild(card);
            });
        } catch (err) {
            casesGridContainer.innerHTML = `<p style="color:var(--text-muted);">Failed to load case studies: ${err.message}</p>`;
        }
    }

    // -------------------------------------------------------------
    // 8. Model Benchmarks Loader
    // -------------------------------------------------------------
    async function loadBenchmarks() {
        if (benchmarkChart) return; // already initialized
        try {
            const res = await fetch("/api/benchmark");
            const data = await res.json();

            // Populate Confusion Matrix
            if (data.confusion_matrix) {
                document.getElementById("cm-tp-val").textContent = data.confusion_matrix.true_positives;
                document.getElementById("cm-fp-val").textContent = data.confusion_matrix.false_positives;
                document.getElementById("cm-fn-val").textContent = data.confusion_matrix.false_negatives;
                document.getElementById("cm-tn-val").textContent = data.confusion_matrix.true_negatives;
            }

            // Populate Architecture Table
            const tbody = document.getElementById("benchmarks-table-body");
            tbody.innerHTML = "";
            (data.models || []).forEach(m => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${m.name}</strong></td>
                    <td>${m.type}</td>
                    <td style="color:var(--accent-cyan); font-weight:600;">${m.accuracy}%</td>
                    <td>${m.precision}%</td>
                    <td>${m.recall}%</td>
                    <td style="color:var(--accent-emerald); font-weight:600;">${m.f1_score}%</td>
                    <td>${m.inference_latency_ms} ms</td>
                `;
                tbody.appendChild(tr);
            });

            // Chart 1: Bar Comparison
            const ctxBar = document.getElementById("chart-models-bar").getContext("2d");
            const labels = data.models.map(m => m.name);
            benchmarkChart = new Chart(ctxBar, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Accuracy (%)",
                            data: data.models.map(m => m.accuracy),
                            backgroundColor: "rgba(6, 182, 212, 0.75)",
                            borderRadius: 6
                        },
                        {
                            label: "F1 Score (%)",
                            data: data.models.map(m => m.f1_score),
                            backgroundColor: "rgba(16, 185, 129, 0.75)",
                            borderRadius: 6
                        },
                        {
                            label: "Precision (%)",
                            data: data.models.map(m => m.precision),
                            backgroundColor: "rgba(99, 102, 241, 0.75)",
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            min: 88,
                            max: 100,
                            grid: { color: "rgba(255, 255, 255, 0.05)" },
                            ticks: { color: "#94a3b8" }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: "#94a3b8" }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: "#f1f5f9" } }
                    }
                }
            });

            // Chart 2: Loss Convergence Curve
            const ctxLoss = document.getElementById("chart-loss-curve").getContext("2d");
            const hist = data.training_history || { epochs: [1, 2, 3, 4, 5], train_loss: [], val_loss: [] };
            lossChart = new Chart(ctxLoss, {
                type: "line",
                data: {
                    labels: hist.epochs.map(e => `Epoch ${e}`),
                    datasets: [
                        {
                            label: "Training Loss",
                            data: hist.train_loss,
                            borderColor: "var(--accent-rose)",
                            backgroundColor: "rgba(244, 63, 94, 0.1)",
                            tension: 0.35,
                            fill: true
                        },
                        {
                            label: "Validation Loss",
                            data: hist.val_loss,
                            borderColor: "var(--accent-cyan)",
                            backgroundColor: "rgba(6, 182, 212, 0.1)",
                            tension: 0.35,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            grid: { color: "rgba(255, 255, 255, 0.05)" },
                            ticks: { color: "#94a3b8" }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: "#94a3b8" }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: "#f1f5f9" } }
                    }
                }
            });

        } catch (err) {
            console.error("Benchmarks load error:", err);
        }
    }

    // -------------------------------------------------------------
    // 9. Audit History Loader & CSV Export
    // -------------------------------------------------------------
    async function loadHistory() {
        const filterVal = historyFilter.value;
        try {
            const url = filterVal === "all" ? "/api/history?limit=40" : `/api/history?limit=40&filter=${encodeURIComponent(filterVal)}`;
            const res = await fetch(url);
            const data = await res.json();

            historyTableBody.innerHTML = "";
            const list = data.history || [];

            if (list.length === 0) {
                historyTableBody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:2rem; color:var(--text-muted);">No scan history recorded yet. Run a verification in the Scanner tab!</td></tr>`;
                return;
            }

            list.forEach(row => {
                const tr = document.createElement("tr");
                const isReal = row.prediction_label === "Real News";
                const isFake = row.prediction_label === "Fake News";
                const verdictColor = isReal ? "var(--accent-emerald)" : isFake ? "var(--accent-rose)" : "var(--accent-amber)";

                tr.innerHTML = `
                    <td style="font-family:var(--font-mono); font-size:0.75rem;">${row.timestamp}</td>
                    <td><strong>${escapeHtml(row.title || 'Untitled')}</strong></td>
                    <td><span class="step-pill">${row.source_type}</span></td>
                    <td style="font-family:var(--font-mono); font-size:0.75rem;">${row.domain || 'N/A'}</td>
                    <td><strong style="color:${verdictColor};">${row.prediction_label}</strong></td>
                    <td style="font-family:var(--font-mono); font-weight:600;">${row.confidence_score}%</td>
                    <td>${row.clickbait_score || 0}%</td>
                    <td>${row.user_feedback ? (row.user_feedback === 'correct' ? '👍' : '👎') : '—'}</td>
                `;
                historyTableBody.appendChild(tr);
            });
        } catch (err) {
            historyTableBody.innerHTML = `<tr><td colspan="8" style="color:var(--accent-rose);">Failed to load history: ${err.message}</td></tr>`;
        }
    }

    historyFilter.addEventListener("change", loadHistory);

    // CSV Export
    btnExportCsv.addEventListener("click", async () => {
        try {
            const res = await fetch("/api/history?limit=100");
            const data = await res.json();
            const list = data.history || [];

            if (list.length === 0) {
                alert("No scan records to export.");
                return;
            }

            let csv = "ID,Timestamp,Title,SourceType,Domain,Verdict,Confidence,FakeProb,RealProb,Clickbait,Sensationalism,UserFeedback\n";
            list.forEach(r => {
                const cleanTitle = `"${(r.title || '').replace(/"/g, '""')}"`;
                csv += `${r.id},"${r.timestamp}",${cleanTitle},${r.source_type},"${r.domain}",${r.prediction_label},${r.confidence_score},${r.fake_probability},${r.real_probability},${r.clickbait_score},${r.sensationalism_score},"${r.user_feedback || ''}"\n`;
            });

            const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `veritas_scans_${new Date().toISOString().slice(0, 10)}.csv`;
            a.click();
            URL.revokeObjectURL(url);
        } catch (err) {
            alert(`CSV Export Error: ${err.message}`);
        }
    });

    // -------------------------------------------------------------
    // 10. Automated Social Media & Live Stream Disinformation Radar
    // -------------------------------------------------------------
    let socialPlatform = "all";
    let socialChannel = "";
    let socialQuery = "";
    let socialFilter = "all";
    let autoPilotInterval = null;
    let currentSocialPosts = [];
    let isSocialLoaded = false;

    // Elements
    const autopilotCheckbox = document.getElementById("autopilot-checkbox");
    const autopilotStatusLabel = document.getElementById("autopilot-status-label");
    const autopilotPulseIndicator = document.getElementById("autopilot-pulse-indicator");
    const autopilotDesc = document.getElementById("autopilot-desc");

    const platformChips = document.querySelectorAll(".platform-chip");
    const socialChannelSelect = document.getElementById("social-channel-select");
    const socialSearchInput = document.getElementById("social-search-input");
    const btnClearSocialSearch = document.getElementById("btn-clear-social-search");
    const btnScanSocial = document.getElementById("btn-scan-social");
    const socialSpinner = document.getElementById("social-spinner");

    const trendPillBtns = document.querySelectorAll(".trend-pill");
    const btnExportSocialCsv = document.getElementById("btn-export-social-csv");
    const btnExportSocialJson = document.getElementById("btn-export-social-json");

    const kpiTotalPosts = document.getElementById("kpi-total-posts");
    const kpiMisinfoRate = document.getElementById("kpi-misinfo-rate");
    const kpiMisinfoBar = document.getElementById("kpi-misinfo-bar");
    const kpiCriticalAlerts = document.getElementById("kpi-critical-alerts");
    const kpiAvgClickbait = document.getElementById("kpi-avg-clickbait");
    const kpiSourceSummary = document.getElementById("kpi-source-summary");

    const feedStatusLabel = document.getElementById("feed-status-label");
    const feedFilterBtns = document.querySelectorAll(".feed-filter-btn");
    const socialLoadingState = document.getElementById("social-loading-state");
    const socialFeedContainer = document.getElementById("social-feed-container");
    const liveToastContainer = document.getElementById("live-toast-container");

    // Initialize Radar Event Listeners
    function initSocialRadarListeners() {
        if (!platformChips || platformChips.length === 0) return;

        // Platform buttons
        platformChips.forEach(chip => {
            chip.addEventListener("click", () => {
                platformChips.forEach(c => c.classList.remove("active"));
                chip.classList.add("active");
                socialPlatform = chip.getAttribute("data-platform");
                fetchSocialFeed();
            });
        });

        // Channel select dropdown
        if (socialChannelSelect) {
            socialChannelSelect.addEventListener("change", (e) => {
                socialChannel = e.target.value;
                fetchSocialFeed();
            });
        }

        // Search input & scan button
        if (btnScanSocial) {
            btnScanSocial.addEventListener("click", () => {
                socialQuery = socialSearchInput ? socialSearchInput.value.trim() : "";
                fetchSocialFeed();
            });
        }

        if (socialSearchInput) {
            socialSearchInput.addEventListener("keydown", (e) => {
                if (e.key === "Enter") {
                    socialQuery = socialSearchInput.value.trim();
                    fetchSocialFeed();
                }
            });
        }

        if (btnClearSocialSearch) {
            btnClearSocialSearch.addEventListener("click", () => {
                if (socialSearchInput) socialSearchInput.value = "";
                socialQuery = "";
                fetchSocialFeed();
            });
        }

        // Trending topic quick pills
        trendPillBtns.forEach(pill => {
            pill.addEventListener("click", () => {
                const query = pill.getAttribute("data-query");
                if (socialSearchInput) socialSearchInput.value = query;
                socialQuery = query;
                fetchSocialFeed();
            });
        });

        // View filter buttons
        feedFilterBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                feedFilterBtns.forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                socialFilter = btn.getAttribute("data-filter");
                renderSocialPosts(currentSocialPosts);
            });
        });

        // Auto-Pilot toggle
        if (autopilotCheckbox) {
            autopilotCheckbox.addEventListener("change", (e) => {
                toggleAutoPilot(e.target.checked);
            });
        }

        // Export buttons
        if (btnExportSocialCsv) {
            btnExportSocialCsv.addEventListener("click", () => {
                window.open("/api/social/export?format=csv", "_blank");
            });
        }

        if (btnExportSocialJson) {
            btnExportSocialJson.addEventListener("click", async () => {
                try {
                    const res = await fetch("/api/social/export?format=json");
                    const data = await res.json();
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = `veritas_social_telemetry_${new Date().toISOString().slice(0, 10)}.json`;
                    a.click();
                    URL.revokeObjectURL(url);
                } catch (err) {
                    alert(`JSON Export Error: ${err.message}`);
                }
            });
        }
    }

    // Lazy load Social Radar on tab activation
    function loadSocialRadar() {
        if (!isSocialLoaded) {
            initSocialRadarListeners();
            fetchSocialFeed();
            isSocialLoaded = true;
        }
    }

    // Fetch and auto-verify live feed
    async function fetchSocialFeed() {
        if (!socialFeedContainer) return;

        // UI Loading state
        if (socialLoadingState) socialLoadingState.style.display = "block";
        if (socialSpinner) socialSpinner.style.display = "inline-block";
        if (btnScanSocial) btnScanSocial.disabled = true;
        if (feedStatusLabel) feedStatusLabel.textContent = "Connecting to live public streams & executing neural verification...";

        try {
            const params = new URLSearchParams({
                platform: socialPlatform,
                limit: "12",
                auto_scan: "true"
            });
            if (socialChannel) params.append("channel", socialChannel);
            if (socialQuery) params.append("query", socialQuery);

            const res = await fetch(`/api/social/feed?${params.toString()}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to fetch feed`);

            const data = await res.json();
            currentSocialPosts = data.posts || [];

            // Update KPIs
            updateSocialKPIs(data);

            // Render post cards
            renderSocialPosts(currentSocialPosts);

            if (feedStatusLabel) {
                const queryText = socialQuery ? ` for "${socialQuery}"` : "";
                feedStatusLabel.textContent = `Live Stream Active: ${currentSocialPosts.length} posts ingested and verified${queryText}.`;
            }
        } catch (err) {
            socialFeedContainer.innerHTML = `
                <div class="empty-state glass-card" style="grid-column: 1 / -1;">
                    <div class="empty-icon-shield">⚠️</div>
                    <h3>Stream Connection Notice</h3>
                    <p style="color:var(--text-secondary);">${escapeHtml(err.message)}</p>
                    <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem;">Switching to simulated viral social stream or retry connection.</p>
                </div>
            `;
            if (feedStatusLabel) feedStatusLabel.textContent = "Live stream offline. Showing local forensic telemetry.";
        } finally {
            if (socialLoadingState) socialLoadingState.style.display = "none";
            if (socialSpinner) socialSpinner.style.display = "none";
            if (btnScanSocial) btnScanSocial.disabled = false;
        }
    }

    // Update KPI cards
    function updateSocialKPIs(data) {
        if (!kpiTotalPosts) return;

        kpiTotalPosts.textContent = data.total_posts || 0;

        const rate = data.misinformation_prevalence_pct || 0;
        kpiMisinfoRate.textContent = `${rate}%`;
        if (kpiMisinfoBar) {
            kpiMisinfoBar.style.width = `${Math.min(100, rate)}%`;
            if (rate > 50) {
                kpiMisinfoBar.style.background = "linear-gradient(90deg, var(--accent-amber), var(--accent-rose))";
            } else {
                kpiMisinfoBar.style.background = "linear-gradient(90deg, var(--accent-emerald), var(--accent-cyan))";
            }
        }

        if (kpiCriticalAlerts) kpiCriticalAlerts.textContent = data.critical_alerts_count || 0;
        if (kpiAvgClickbait) kpiAvgClickbait.textContent = `${data.average_clickbait_index || 0}%`;
        if (kpiSourceSummary) {
            kpiSourceSummary.textContent = `${data.fake_detected_count || 0} Deceptive • ${data.real_verified_count || 0} Journalistic`;
        }
    }

    // Render feed cards with interactive inspection
    function renderSocialPosts(posts) {
        if (!socialFeedContainer) return;

        // Apply filter
        let filtered = posts;
        if (socialFilter === "fake") {
            filtered = posts.filter(p => p.verdict === "Fake News" || p.fake_probability > 55);
        } else if (socialFilter === "real") {
            filtered = posts.filter(p => p.verdict === "Real News" && p.fake_probability <= 50);
        } else if (socialFilter === "critical") {
            filtered = posts.filter(p => p.threat && p.threat.threat_level === "CRITICAL THREAT");
        }

        if (filtered.length === 0) {
            socialFeedContainer.innerHTML = `
                <div class="empty-state glass-card" style="grid-column: 1 / -1; padding: 2.5rem;">
                    <div class="empty-icon-shield">🔍</div>
                    <h3>No Posts Matching Selected Filter</h3>
                    <p style="color:var(--text-secondary);">Try selecting "All Posts" or choosing a different channel.</p>
                </div>
            `;
            return;
        }

        socialFeedContainer.innerHTML = "";

        filtered.forEach(post => {
            const threat = post.threat || {
                threat_level: "MODERATE",
                threat_badge: "⚠️ UNVERIFIED",
                threat_color: "warning",
                threat_score: 50.0
            };

            // Determine border modifier class
            let borderClass = "threat-elevated";
            if (threat.threat_level === "CRITICAL THREAT") borderClass = "threat-critical";
            else if (post.verdict === "Real News") borderClass = "threat-verified";
            else if (post.verdict && post.verdict.includes("Satire")) borderClass = "threat-satire";

            // Platform emoji
            let platformIcon = "🌐";
            if (post.platform.includes("Reddit")) platformIcon = "🤖";
            else if (post.platform.includes("Wire")) platformIcon = "📰";
            else if (post.platform.includes("Social") || post.platform.includes("X")) platformIcon = "🐦";
            else if (post.platform.includes("Google")) platformIcon = "🔍";

            const card = document.createElement("div");
            card.className = `social-post-card ${borderClass}`;

            // Suspicious token tags
            let suspiciousHtml = "";
            if (post.suspicious_cues && post.suspicious_cues.length > 0) {
                const tags = post.suspicious_cues.map(w => `<span class="suspicious-tag">"${escapeHtml(w)}"</span>`).join(" ");
                suspiciousHtml = `<div class="suspicious-tags-wrap"><span>Flagged Cues:</span> ${tags}</div>`;
            }

            // Metrics
            const likesStr = formatMetricNumber(post.likes || 1200);
            const sharesStr = formatMetricNumber(post.shares || 420);
            const commentsStr = formatMetricNumber(post.comments || 85);

            card.innerHTML = `
                <div class="post-header-top">
                    <div class="post-user-info">
                        <div class="post-avatar">${platformIcon}</div>
                        <div class="post-names">
                            <span class="post-author-name">${escapeHtml(post.author || "Social Broadcaster")}</span>
                            <span class="post-handle-sub">${escapeHtml(post.handle || "@feed")}</span>
                        </div>
                    </div>
                    <div class="post-meta-badges">
                        <span class="post-channel-pill">${escapeHtml(post.channel || post.platform)}</span>
                        <span class="post-time-tag">${escapeHtml(post.timestamp_str || "Recent")}</span>
                    </div>
                </div>

                <div>
                    <h4 class="post-headline">${escapeHtml(post.title || "")}</h4>
                    <p class="post-body-snippet">${escapeHtml((post.text || "").slice(0, 240))}${post.text && post.text.length > 240 ? "..." : ""}</p>
                    ${post.url ? `<a href="${escapeHtml(post.url)}" target="_blank" rel="noopener noreferrer" class="post-source-link">🔗 Source Link (${escapeHtml(post.domain || "external")})</a>` : ""}
                </div>

                <div class="post-threat-banner">
                    <span class="threat-badge-pill" style="color: ${getThreatColorCode(threat.threat_color)};">
                        ${escapeHtml(threat.threat_badge)}
                    </span>
                    <span class="threat-score-pill">
                        Deception: <strong>${post.fake_probability !== undefined ? post.fake_probability + "%" : "N/A"}</strong>
                    </span>
                </div>

                <div class="post-forensics-row">
                    <span class="post-chip">⚡ Virality: ${post.virality_velocity || 40}/100</span>
                    <span class="post-chip">🤖 Bot Risk: ${post.bot_risk_score || 15}%</span>
                    <span class="post-chip">🎣 Clickbait: ${post.stylometrics ? post.stylometrics.clickbait_index + "%" : "N/A"}</span>
                </div>

                ${suspiciousHtml}

                <div class="post-engagement-footer">
                    <div class="engagement-stats">
                        <span>❤️ ${likesStr}</span>
                        <span>🔁 ${sharesStr}</span>
                        <span>💬 ${commentsStr}</span>
                    </div>
                    <button type="button" class="btn-inspect-post" title="Send to Neural Scanner for Explainable AI token heatmap">
                        <span>⚡</span>
                        <span>Deep Inspect</span>
                    </button>
                </div>
            `;

            // Inspect button click listener
            const inspectBtn = card.querySelector(".btn-inspect-post");
            inspectBtn.addEventListener("click", () => {
                inspectSocialPost(post);
            });

            socialFeedContainer.appendChild(card);
        });
    }

    function getThreatColorCode(color) {
        if (color === "danger") return "var(--accent-rose)";
        if (color === "warning" || color === "amber") return "var(--accent-amber)";
        if (color === "success") return "var(--accent-emerald)";
        return "var(--accent-purple)";
    }

    function formatMetricNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
        if (num >= 1000) return (num / 1000).toFixed(1) + "K";
        return num.toString();
    }

    // One-click Deep Inspect into Scanner
    function inspectSocialPost(post) {
        // Switch to scanner tab
        const scannerTab = document.getElementById("tab-scanner");
        if (scannerTab) scannerTab.click();

        // Switch to text mode
        if (modeTextBtn) modeTextBtn.click();

        // Populate fields
        const headlineText = post.title || "";
        const bodyText = post.text || post.title || "";
        const domainText = post.domain || "social.media";

        if (inputHeadline) inputHeadline.value = headlineText;
        if (inputBody) {
            inputBody.value = bodyText;
            if (textCharCount) textCharCount.textContent = `${bodyText.length} characters`;
        }
        if (inputDomain) inputDomain.value = domainText;

        // Auto trigger verification
        setTimeout(() => {
            executeVerification();
        }, 120);
    }

    // Auto-Pilot Continuous Live Polling
    function toggleAutoPilot(enabled) {
        if (enabled) {
            if (autopilotStatusLabel) autopilotStatusLabel.textContent = "Auto-Pilot: ACTIVE";
            if (autopilotPulseIndicator) autopilotPulseIndicator.style.display = "inline-block";
            if (autopilotDesc) autopilotDesc.textContent = "Active radar sweeping: continuously analyzing incoming social posts";

            // Trigger an immediate pulse
            pollLivePulse();

            // Set recurring 10-second interval
            autoPilotInterval = setInterval(pollLivePulse, 10000);
        } else {
            if (autoPilotInterval) {
                clearInterval(autoPilotInterval);
                autoPilotInterval = null;
            }
            if (autopilotStatusLabel) autopilotStatusLabel.textContent = "Auto-Pilot: OFF";
            if (autopilotPulseIndicator) autopilotPulseIndicator.style.display = "none";
            if (autopilotDesc) autopilotDesc.textContent = "Continuous real-time stream polling & instant viral fake news alert notifications";
        }
    }

    async function pollLivePulse() {
        try {
            const res = await fetch("/api/social/live-pulse");
            if (!res.ok) return;
            const pulse = await res.json();

            // Show toast notification for critical and elevated hoaxes
            if (pulse.threat && (pulse.threat.threat_level === "CRITICAL THREAT" || pulse.threat.threat_level === "ELEVATED RISK")) {
                showLiveToast(pulse);
            }
        } catch (err) {
            console.log("Auto-pilot poll notice:", err);
        }
    }

    // Floating Live Notification Toast
    function showLiveToast(pulse) {
        if (!liveToastContainer) return;

        const toast = document.createElement("div");
        toast.className = "live-toast";

        toast.innerHTML = `
            <div class="toast-icon">🚨</div>
            <div class="toast-body">
                <div class="toast-top-row">
                    <span class="toast-badge">${escapeHtml(pulse.threat.threat_badge)}</span>
                    <span class="toast-time">${escapeHtml(pulse.timestamp || "Just now")}</span>
                </div>
                <div class="toast-title">${escapeHtml((pulse.title || "").slice(0, 100))}${pulse.title && pulse.title.length > 100 ? "..." : ""}</div>
                <div class="toast-author">Source: ${escapeHtml(pulse.author || "Social Stream")} (${escapeHtml(pulse.platform)}) • ${formatMetricNumber(pulse.shares || 1200)} shares/hr</div>
                <div class="toast-actions">
                    <button type="button" class="toast-inspect-btn">⚡ Deep Inspect in Neural Scanner →</button>
                    <button type="button" class="toast-close-btn" title="Dismiss">✕</button>
                </div>
            </div>
        `;

        const inspectBtn = toast.querySelector(".toast-inspect-btn");
        inspectBtn.addEventListener("click", () => {
            inspectSocialPost(pulse);
            toast.remove();
        });

        const closeBtn = toast.querySelector(".toast-close-btn");
        closeBtn.addEventListener("click", () => {
            toast.classList.add("toast-fadeout");
            setTimeout(() => toast.remove(), 300);
        });

        liveToastContainer.appendChild(toast);

        // Auto dismiss after 9 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.classList.add("toast-fadeout");
                setTimeout(() => toast.remove(), 300);
            }
        }, 9000);
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
});
