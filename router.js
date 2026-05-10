// --- SENTINEL CONFIGURATION ---
const getAccuracyValue = (text) => {
    // This regex looks for 'ACCURACY_CONFIDENCE' followed by any characters and then a number + %
    const match = text.match(/ACCURACY_CONFIDENCE[:\s*]+(\d+)%/i);
    return match ? match[1] + "%" : "95%"; 
};

const API_URL = "http://127.0.0.1:8003";
//const API_URL = "https://appeasing-village-chummy.ngrok-free.dev";

document.addEventListener("DOMContentLoaded", () => {


    // === NEW: HOME NAVIGATION LOGIC ===
    const forceShowSection = () => {
        // If there is no hash (#), show the 'home' section by default
        const hash = window.location.hash.substring(1) || 'home';
        const target = document.getElementById(hash);
        
        // Include 'home' in the master list of sections to toggle
        const allSections = ['home', 'phishing', 'tone', 'policy', 'deepfake', 'veracity'];

        allSections.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                // Hide everything initially
                el.setAttribute('style', 'display: none !important');
            }
        });

        if (target) {
            // Show the selected section (either Home or a specific Audit)
            target.setAttribute('style', 'display: block !important');
            
            // If we move away from home, scroll to top
            window.scrollTo(0, 0);

            // Hide any leftover error containers
            const errorStuff = document.querySelectorAll('.error-container, #error-display, .invalid-link-msg');
            errorStuff.forEach(err => err.setAttribute('style', 'display: none !important'));
        }
    };

    forceShowSection();
    setTimeout(forceShowSection, 100);
    window.addEventListener('hashchange', forceShowSection);

    // === 2. API & PARAMETER CONFIGURATION ===
    const API_URL = "http://127.0.0.1:8003";
    //const API_URL = "https://appeasing-village-chummy.ngrok-free.dev";
    const urlParams = new URLSearchParams(window.location.search);
    
    // Capture data from your friend's app redirect
    const mode = urlParams.get('mode') || 'phishing';
    const targetUrl = urlParams.get('url') || urlParams.get('target'); 
    const risk = urlParams.get('risk') || '0';
    const sslInfo = urlParams.get('ssl') || 'Verified';
    //const customMsg = urlParams.get('msg');

    // Helper to extract accuracy from Qwen text
    /*const getAccuracyValue = (text) => {
        const match = text.match(/ACCURACY_CONFIDENCE[:\s*]+(\d+)%/i);
        return match ? match[1] + "%" : "95%";
    };*/

    if (targetUrl) {
        document.getElementById('target-display').textContent = targetUrl;
        document.getElementById('risk-score').textContent = risk + "%";
        document.getElementById('ssl-status').innerText = sslInfo;
    }

    document.querySelectorAll('.dynamic-risk').forEach(el => {
        el.textContent = risk + '%';
        const color = risk > 70 ? '#ef4444' : (risk > 40 ? '#f59e0b' : '#10b981');
        document.documentElement.style.setProperty('--risk-color', color);
    });

    // Sync SSL Status UI
    const sslDisplay = document.getElementById('ssl-status') || document.querySelector('.dynamic-ssl');
    if (sslDisplay) sslDisplay.innerText = sslInfo;

    // === 4. AUTOMATIC QWEN TRIGGER ===
    // If we are in phishing mode and have a URL, start the engine immediately
    if (targetUrl && mode.toLowerCase() === 'phishing') {
        performLiveAnalysis(targetUrl, sslInfo);
    }

    // Manual Trigger via Button
    const manualBtn = document.getElementById('run-manual-scan');
    const manualInput = document.getElementById('manual-url-input');

    if(manualBtn) {
        manualBtn.addEventListener('click', () => {
            const val = manualInput.value.trim();
            if(val) {
                document.getElementById('target-display').textContent = val;
                performLiveAnalysis(val, "Manual Entry");
            } else {
                alert("Please enter a URL first.");
            }
        });
    }

    // Initialize secondary audits
    setupPrivacyAudit();
    setupToneAudit();
    window.scrollTo(0, 0);

    // === 5. THE CORE ENGINE FUNCTION ===
    async function performLiveAnalysis(url, ssl) {
    // UPDATED: Ensure this ID matches your HTML container for URL results
    const resultBox = document.getElementById('phishing-result-text'); 
    if (!resultBox) return;

    resultBox.innerText = "QWEN ENGINE: Starting 10-Point Deep-Link Structural Audit...";

    try {
        // UPDATED: Switched to GET method to match the new @app.get("/analyze") in main.py
        // We pass the URL as a query parameter
        const response = await fetch(`${API_URL}/analyze?url=${encodeURIComponent(url)}`, {
            method: 'GET',
            headers: { 
                'Accept': 'application/json' 
            }
        });

        if (!response.ok) throw new Error(`Backend Offline (8003)`);

        const data = await response.json();
        
        // UPDATED: Using 'data.ai_forensics' to match the new backend return key
        resultBox.style.whiteSpace = "pre-line";
        resultBox.innerText = data.ai_forensics || "Error: No forensic data returned.";
        // resultBox.innerText = forensics;

        // --- NEW UPDATE FOR ACCURACY SCORE ---
        const accValue = getAccuracyValue(data.ai_forensics);
        const accuracyDisplay = document.getElementById('phishing-accuracy-score');
        if (accuracyDisplay) {
            accuracyDisplay.innerText = accValue;
            const val = parseInt(accValue);
            accuracyDisplay.style.color = val > 90 ? "#10b981" : (val > 60 ? "#f59e0b" : "#ef4444");
        }
        // -------------------------------------

        // Update UI status
        const riskDisplay = document.getElementById('risk-score');
        if (riskDisplay) riskDisplay.innerText = "SCAN COMPLETE";

    } catch (error) {
        console.error("Connection Failed:", error);
        resultBox.innerText = "System Error: Backend unreachable on port 8003. Ensure Ollama and the Python server are running.";
    }
}

// Init remaining audits
    if (typeof setupPrivacyAudit === "function") setupPrivacyAudit();
    if (typeof setupToneAudit === "function") setupToneAudit();
});

function setupToneAudit() {
    const toneBtn = document.getElementById('run-tone-btn');
    const toneInput = document.getElementById('tone-text-input');
    const resultBox = document.getElementById('tone-result-text');
    const statusTag = document.querySelector('.status-tag'); // The Status card

    if (!toneBtn || !toneInput) return;

    // --- AUTOMATION LOGIC: Deep Link Check ---
    const checkDeepLink = () => {
        const urlParams = new URLSearchParams(window.location.search);
        const autoToneText = urlParams.get('tone_text');

        if (autoToneText) {
            const decodedText = decodeURIComponent(autoToneText);
            toneInput.value = decodedText;
            
            // HIDE THE BUTTON for the automated experience
            toneBtn.style.display = 'none'; 
            
            // Trigger the analysis automatically
            triggerAnalysis(decodedText);
        }
    };

    const triggerAnalysis = async (text) => {
        // Update Status Card
        if (statusTag) statusTag.innerText = "Status: RUNNING";
        
        resultBox.style.color = "#818cf8";
        resultBox.innerText = "QWEN ENGINE: Initializing Psycholinguistic Deconstruction...";

        try {
            //const response = await fetch(`http://0.0.0.0:8003/analyze-tone`, {
            const response = await fetch(`${API_URL}/analyze-tone`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text }) 
            });

            const data = await response.json();
            
            resultBox.style.whiteSpace = "pre-line"; 
            resultBox.style.color = "#ffffff"; 
            resultBox.innerText = data.analysis || data.error || "Analysis complete.";

            // === NEW: EXTRACT AND DISPLAY ACCURACY ===
            if (data.analysis) {
                const accValue = getAccuracyValue(data.analysis);
                const accDisplay = document.getElementById('tone-accuracy');
                if (accDisplay) accDisplay.innerText = accValue;
                const val = parseInt(accValue);
                accDisplay.style.color = val > 90 ? "#10b981" : (val > 60 ? "#f59e0b" : "#ef4444");
            }
            // =========================================
            
            // Update Status Card to Completed
            if (statusTag) statusTag.innerText = "Status: COMPLETED";

        } catch (err) {
            resultBox.innerText = "Connection Error: Ensure Python server is on 8003.";
            resultBox.style.color = "#ef4444"; 
            if (statusTag) statusTag.innerText = "Status: ERROR";
        }
    };

    // Manual Click Listener
    toneBtn.addEventListener('click', (e) => {
        e.preventDefault();
        triggerAnalysis(toneInput.value.trim());
    });

    // Run the automated check on page load
    checkDeepLink();
}

// Ensure the function is called
setupToneAudit();


/*function setupToneAudit() {
    const toneBtn = document.getElementById('run-tone-btn');
    const toneInput = document.getElementById('tone-text-input');
    const resultBox = document.getElementById('tone-result-text');

    if (!toneBtn) return;

    toneBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const text = toneInput.value.trim();
        
        if (!text) {
            resultBox.innerText = "Error: Input buffer empty.";
            return;
        }

        toneBtn.innerText = "QWEN FORENSICS RUNNING...";
        toneBtn.disabled = true;
        resultBox.style.color = "#818cf8";
        resultBox.innerText = "Analyzing Perplexity, Burstiness, and Intent...";

        try {
            // Updated to /analyze-tone on Port 8003 to bypass the Port 11434 block
            const response = await fetch(`http://127.0.0.1:8003/analyze-tone`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text }) 
            });

            if (!response.ok) throw new Error("Backend connection failed");

            const data = await response.json();
            
            // Handle both success and error responses from the backend
            resultBox.style.whiteSpace = "pre-line"; 
            resultBox.style.color = "#ffffff"; 
            resultBox.innerText = data.analysis || data.error || "Analysis complete.";
            
        } catch (err) {
            // Specific error message for Port 8003 reachability
            resultBox.innerText = "Forensic Engine Error: Ensure your Python server is running on Port 8003.";
            resultBox.style.color = "#ef4444"; 
            console.error(err);
        } finally {
            toneBtn.innerText = "Analyze Intent";
            toneBtn.disabled = false;
        }
    });
}*/


function setupPrivacyAudit() {
    const auditBtn = document.getElementById('run-audit-btn');
    const policyInput = document.getElementById('policy-text-input');
    const resultDiv = document.getElementById('audit-result-text');

    if (!auditBtn) return;

    auditBtn.addEventListener('click', async () => {
            const text = policyInput.value.trim();
            if (!text) {
                resultDiv.textContent = "Error: Please paste policy text first.";
                return;
            }

            auditBtn.disabled = true;
            auditBtn.textContent = "QWEN IS ANALYZING...";
            resultDiv.innerText = "Scanning by QWEN Sensors, Data Sharing, and User Rights...";

            try {
                const response = await fetch(`${API_URL}/audit-policy`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    // FIXED: Changed 'policy_text' to 'text' to match main.py
                    body: JSON.stringify({ text: text }) 
                });

                const data = await response.json();
                
                if (data.analysis) {
                    resultDiv.style.whiteSpace = "pre-line";
                    resultDiv.innerText = data.analysis;
                    // === NEW: EXTRACT AND DISPLAY ACCURACY ===
                    const accValue = getAccuracyValue(data.analysis);
                    const accDisplay = document.getElementById('policy-accuracy');
                    if (accDisplay) accDisplay.innerText = accValue;
                    const val = parseInt(accValue);
                    accDisplay.style.color = val > 90 ? "#10b981" : (val > 60 ? "#f59e0b" : "#ef4444");
                    
                    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    // This tells you exactly what went wrong
                    resultDiv.innerText = "Error: AI Engine returned an empty report. Check Ollama terminal.";
                }
                
            } catch (err) {
                resultDiv.textContent = "Connection Failed: Ensure your FastAPI backend is running.";
                console.error(err);
            } finally {
                auditBtn.disabled = false;
                auditBtn.textContent = "Initiate AI Audit";
            }
        });
};
setupPrivacyAudit();


const setupDeepfakeDetection = () => {
    const fileInput = document.getElementById('deepfake-input');
    const detectBtn = document.getElementById('run-deepfake-btn');
    const resultBox = document.getElementById('deepfake-result-text');
    
    // UI IDs for the top display cards
    const riskDisplay = document.getElementById('df-risk-display'); 
    const syncDisplay = document.getElementById('df-sync-display'); 
    const lightDisplay = document.getElementById('df-light-display'); 

    if (!detectBtn) return;

    // --- HELPER: DYNAMIC UI SYNC LOGIC (Improved) ---
    // This function cleans up brackets [ ] if the AI includes them in the response
    const extractValue = (text, key) => {
        const regex = new RegExp(`${key}:\\s*(.*)`, 'i');
        const match = text.match(regex);
        if (match) {
            // Removes brackets and extra symbols to ensure clean UI values
            return match[1].replace(/[\[\]]/g, '').trim();
        }
        return "N/A";
    };

    detectBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) return alert("Select a file first!");

        const isVideo = file.name.endsWith('.mp4');
        const endpoint = isVideo ? '/detect-video' : '/detect-image';
        const formData = new FormData();
        formData.append('file', file);

        detectBtn.innerText = "RUNNING DYNAMIC ANALYSIS...";
        detectBtn.disabled = true;

        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error("Server Error");

            const data = await response.json();
            const output = data.analysis;

            // 1. EXTRACT DATA FROM AI RESPONSE
            const probValue = extractValue(output, "GENERATIVE PROBABILITY");
            const lightValue = extractValue(output, "LIGHTING VECTOR");
            const bioValue = extractValue(output, "BIOMETRIC SYNC");

            // === NEW: EXTRACT AND DISPLAY ACCURACY ===
            const accValue = getAccuracyValue(output);
            const accDisplay = document.getElementById('media-accuracy');
            if (accDisplay) accDisplay.innerText = accValue;
            const val = parseInt(accValue);
            accDisplay.style.color = val > 90 ? "#10b981" : (val > 60 ? "#f59e0b" : "#ef4444");
            //

            // 2. SYNC TOP BOXES WITH CLEAN VALUES
            if (riskDisplay) riskDisplay.innerText = probValue;
            if (lightDisplay) lightDisplay.innerText = lightValue;
            if (syncDisplay) syncDisplay.innerText = bioValue;

            // 3. SYNC TERMINAL REPORT
            resultBox.style.whiteSpace = "pre-line";
            resultBox.innerText = `ENGINE SCORE: ${data.score}%\n\n${output}`;

        } catch (err) {
            resultBox.innerText = "Sync Error: Is your Python server on 8003?";
            console.error(err);
        } finally {
            detectBtn.innerText = "Run Forensic Scan";
            detectBtn.disabled = false;
        }
    });
};

setupDeepfakeDetection();

const setupVeracityAudit = () => {
    const veracityInput = document.getElementById('veracity-text-input');
    const veracityBtn = document.getElementById('run-veracity-btn');
    const resultBox = document.getElementById('veracity-result-text');
    const truthDisplay = document.getElementById('v-truth-display');
    const logicDisplay = document.getElementById('v-logic-display');

    if (!veracityBtn || !veracityInput) return;

    // --- NEW: AUTO-TRIGGER LOGIC ---
    const checkUrlParameters = () => {
        const urlParams = new URLSearchParams(window.location.search);
        const autoText = urlParams.get('text');

        if (autoText) {
            veracityInput.value = decodeURIComponent(autoText);
            // Hide the button as per your request
            veracityBtn.style.display = 'none'; 
            // Trigger analysis automatically
            runAnalysis(decodeURIComponent(autoText));
        }
    };

    const runAnalysis = async (text) => {
        if (!text) return;

        // UI: Running State
        logicDisplay.innerText = "RUNNING...";
        resultBox.innerText = "QWEN ENGINE: Initializing forensic audit...";
        
        try {
            const response = await fetch(`${API_URL}/analyze-veracity`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();
            const analysisText = data.analysis || data.error;

            // Extract Probability
            const probMatch = analysisText.match(/TRUTH PROBABILITY:\s*(\d+)%/i);
            if (probMatch && truthDisplay) {
                const percentage = probMatch[1];
                truthDisplay.innerText = `${percentage}%`;
                const val = parseInt(percentage);
                truthDisplay.style.color = val > 80 ? "#10b981" : (val > 40 ? "#f59e0b" : "#ef4444");
            }

            // === NEW: EXTRACT AND DISPLAY AI ACCURACY ===
            const accValue = getAccuracyValue(analysisText); // Uses your global helper
            const accDisplay = document.getElementById('v-consensus-display');
            if (accDisplay) {
                accDisplay.innerText = accValue;
                accDisplay.style.color = "#10b981";
                accDisplay.style.fontWeight = "bold";
            }
            //

            // UI: Completed State
            logicDisplay.innerText = "COMPLETED";
            resultBox.style.whiteSpace = "pre-line";
            resultBox.innerText = analysisText;

        } catch (err) {
            logicDisplay.innerText = "ERROR";
            resultBox.innerText = "Backend Connection Failed.";
        }
    };

    // Manual Click Listener
    veracityBtn.addEventListener('click', () => runAnalysis(veracityInput.value.trim()));

    // Run deep-link check on load
    checkUrlParameters();
};

setupVeracityAudit();



// --- VERACITY AUDIT LOGIC (Synchronized with Qwen 2.5) ---
/*const setupVeracityAudit = () => {
    const veracityInput = document.getElementById('veracity-text-input');
    const veracityBtn = document.getElementById('run-veracity-btn');
    const resultBox = document.getElementById('veracity-result-text');
    
    // UI Display Cards
    const truthDisplay = document.getElementById('v-truth-display');
    const consensusDisplay = document.getElementById('v-consensus-display');

    if (!veracityBtn) return;

    veracityBtn.addEventListener('click', async () => {
        const text = veracityInput.value.trim();
        if (!text) return alert("Please enter text for veracity checking.");

        veracityBtn.innerText = "CROSS-REFERENCING...";
        veracityBtn.disabled = true;
        resultBox.innerText = "Analyzing Consensus Divergence and 12 Forensic Parameters...";

        try {
            // Note: Ensure this matches the endpoint in your main.py (@app.post("/analyze-veracity"))
            const response = await fetch(`${API_URL}/analyze-veracity`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) throw new Error("Backend Offline");

            const data = await response.json();
            const analysisText = data.analysis || data.error;

            // 1. EXTRACT PERCENTAGE: Look for "TRUTH PROBABILITY: XX%" in the Qwen response
            const probMatch = analysisText.match(/TRUTH PROBABILITY:\s*(\d+)%/i);
            if (probMatch && truthDisplay) {
                const percentage = probMatch[1];
                truthDisplay.innerText = `${percentage}%`;
                
                // 2. AUTO-COLORING THE SCORE
                const val = parseInt(percentage);
                truthDisplay.style.color = val > 80 ? "#10b981" : (val > 40 ? "#f59e0b" : "#ef4444");
            }

            // 3. UPDATE SUB-CARDS
            if (consensusDisplay) consensusDisplay.innerText = "Verified by Qwen 2.5";
            document.getElementById('v-logic-display').innerText = "Audit Complete";

            // 4. DISPLAY FULL REPORT
            resultBox.style.whiteSpace = "pre-line";
            resultBox.innerText = analysisText;

        } catch (err) {
            console.error(err);
            resultBox.innerText = "Veracity Engine Timeout: Ensure Python is on 8003 and Ollama is active.";
            resultBox.style.color = "#ef4444";
        } finally {
            veracityBtn.innerText = "Verify Information";
            veracityBtn.disabled = false;
        }
    });
};

setupVeracityAudit();*/

/*async function checkSystemPulse() {
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    const BACKEND_HEALTH_URL = "https://appeasing-village-chummy.ngrok-free.dev/"; 

    try {
        const response = await fetch(BACKEND_HEALTH_URL, { 
            method: 'GET',
            headers: {
                "ngrok-skip-browser-warning": "true" // THIS LINE FIXES THE OFFLINE BUG
            }
        });
        
        if (response.ok) {
            statusDot.style.background = "#10b981"; 
            statusDot.style.boxShadow = "0 0 12px #10b981";
            statusText.innerText = "BACKEND: ONLINE";
            statusText.style.color = "#10b981";
        }
    } catch (error) {
        statusDot.style.background = "#ef4444"; 
        statusDot.style.boxShadow = "0 0 12px #ef4444";
        statusText.innerText = "BACKEND: OFFLINE";
        statusText.style.color = "#ef4444";
    }
}*/ 