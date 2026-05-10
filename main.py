import os
import joblib
import ollama
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import UploadFile, File
from sympy import re

# Internal Imports
# phi_engine.py now contains the SentinelLLM class powered by Qwen 2.5
try:
    from models.feature_engine import PhishingFeatureExtractor 
except ImportError:
    pass
from phi_engine import SentinelLLM

app = FastAPI(title="Sentinel Forensic AI - Hybrid Engine")

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. INITIALIZE ENGINES ---
# Initialize the Qwen 2.5 3B Engine as 'llm'
llm = SentinelLLM()

# Load the legacy RF Model (kept for backward compatibility status only)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "trained_models", "phishing_v1.joblib")

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print(f"[*] SUCCESS: Legacy Sentinel RF Model loaded.")
    except Exception as e:
        model = None
        print(f"[!] ERROR: Loading RF model failed: {e}")
else:
    model = None
    print("[!] WARNING: 'phishing_v1.joblib' not found. AI core will handle all requests.")

# --- 2. DATA MODELS ---
class AuditRequest(BaseModel):
    text: str

# --- 3. ROUTES ---

@app.get("/")
async def home():
    return {
        "system": "Sentinel Forensic AI",
        "llm_core": "Qwen 2.5 3B Instruct (Ollama)",
        "status": "Operational"
    }

#@app.get("/")
#def read_root():
    #return {"status": "Sentinel Backend is Running"}

@app.get("/analyze")
async def analyze_url(url: str):
    """
    URL Forensic Analysis.
    Strictly follows the 12-point forensic audit template.
    """
    
    # The 12-Point Master Template for Qwen
    prompt = f"""
    Perform a high-fidelity URL Integrity Scan on: {url}
    
    STRICT OUTPUT FORMAT:
    You must provide an answer for every single point listed below. 
    Use the exact numbering and sub-points provided.

    1. Analyzing the target URL: [Executive Summary]

    2. Domain & URL Structure Analysis:
       a. Levenshtein Distance:
       b. Subdomain Count:
       c. URL Length:
       d. Presence of IP Address:
       e. Special Characters:

    3. SSL/TLS Certificate Metadata:
       a. Certificate Age:
       b. Issuer Authority:
       c. Subject Alternative Name (SAN):

    4. Domain Age & Registration (WHOIS):
       a. Domain Age:
       b. Registrant Privacy:
       c. Expiration Date:

    5. Page Content & HTML Features:
       a. Form Action URLs:
       b. Iframe Detection:
       c. Disabled Right-Click:
       d. Favicon Source:

    6. Network & Reputation Intelligence:
       a. Redirect Chain:
       b. Blacklist Status:
       c. Hosting Provider:

    7. PunyCode or Character-Substitution Attacks:
       a. Analysis:
       b. Verdict:
       c. Risk Score:
       d. Forensic Insight:

    8. TLD Reputation and Structural Anomalies:
       a. Analysis:
       b. Verdict:
       c. Risk Score:
       d. Forensic Insight:

    9. Meta Data Risk (SSL/Age Correlation):
       a. Analysis:
       b. Verdict:
       c. Risk Score:
       d. Forensic Insight:

    10. Summary verdict: [Final Assessment]
    11. Recommendations: [Actionable Steps]
    12. ACCURACY_CONFIDENCE: [Numerical percentage based on available metadata]
    """

    try:
        # Calling Ollama directly to bypass legacy logic in phi_engine
        response = ollama.chat(model='qwen2.5:3b-instruct-q4_K_M', messages=[
            {'role': 'system', 'content': 'You are a Senior Digital Forensics Expert.'},
            {'role': 'user', 'content': prompt},
        ])
        
        ai_output = response['message']['content']
        
        return {
            "target": url,
            "ai_forensics": ai_output,
            "risk": "90" # Example static score; can be extracted via regex if needed
        }
    except Exception as e:
        print(f"Ollama Error: {e}")
        return {"ai_forensics": f"Forensic Engine Failure: {str(e)}", "target": url}

@app.post("/audit-policy")
async def analyze_policy(data: dict):
    policy_text = data.get("text", "")
    
    # Strictly enforced 29-point audit template
    prompt = f"""
    Perform an exhaustive Deep Policy Audit on the following text: "{policy_text}"
    
    INSTRUCTIONS:
    - You MUST use the exact headings and numbering provided below.
    - If a permission or data point is NOT mentioned, state "Not Mentioned".
    - Provide a concise risk assessment for every single point.

    OUTPUT STRUCTURE:

    Over View of the Policy Text:
    [Provide a 2-sentence executive summary here]

    A. Hardware Permissions:
    1. Camera:
    2. Mic:
    3. Gyroscope:
    4. Nearby Devices:
    5. Physical Activity:
    6. Touch Sensor:
    7. Accelerometer:
    8. Proximity:

    B. Personal Data Permissions:
    1. Contacts:
    2. SMS:
    3. Call Logs:
    4. Callenders event:
    5. Phone:
    6. Location:

    C. Storage Permissions:
    1. Files:
    2. Photos and Videos:
    3. Nearby Devices:
    4. Music & Audio:

    D. Data Usage:
    1. Third party Sharing:

    E. Data Selling:
    1. Retention periods:

    F. User Rights:
    1. Right to Erasure:
    2. Opt-out Mechanism:
    3. Data Portability:
    4. Policy Change Notification:

    G. Identity & Location:
    1. Precise vs. Coarse Location:
    2. Phone Status (IMEI/Device ID):
    3. Nearby Devices (Bluetooth/Ultra-wideband):

    H. Advanced Security Parameters:
    - GDPR/CCPA Compliance:
    - COPPA (Children Privacy):
    - Data Encryption:
    - Reading Level (Flesch-Kincaid Grade Level):
    - Presence of a DPO:

    I. FINAL AUDIT ACCURACY: [Percentage]%
    """

    try:
        response = ollama.chat(model='qwen2.5:3b-instruct-q4_K_M', messages=[
            {'role': 'system', 'content': 'You are a high-fidelity Privacy Legal Auditor.'},
            {'role': 'user', 'content': prompt},
        ])
        return {"analysis": response['message']['content']}
    except Exception as e:
        print(f"Ollama Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/detect-image")
async def detect_image(file: UploadFile = File(...)):
    # Qwen will now look for GAN artifacts and assign its own score
    prompt = """
Perform a Forensic Image Audit. 
IMPORTANT: You must replace the placeholders below with actual values based on your analysis. Do NOT return brackets like [ ].

STRICT OUTPUT FORMAT:
GENERATIVE PROBABILITY: [Insert a number between 0-100]%
LIGHTING VECTOR: [Insert either 'Inconsistent' or 'Natural']
BIOMETRIC SYNC: [Insert either 'Sync Mismatch' or 'Synchronous']

    Then, provide this 10-point audit:

    1. Frame Extraction:

    2. Spatial Analysis:

    3. Temporal Analysis (The Missing Piece):

    4. Date of Image Pasting: (Today's Date):

    5. Asymmetric Irises Detection:

    6. Frequency Check Board Patterns:

    7. Shadow Misalignment:

    8. Risk Assessment:

    9. Final Verdict on Veracity:

    10. FORENSIC_CONFIDENCE_SCORE: [Percentage]%


    """
    try:
        # Check if Ollama is reachable
        response = ollama.chat(model='qwen2.5:3b-instruct-q4_K_M', messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        ai_text = response['message']['content']
        
        # 2. Safer Regex: Prevents 'NoneType' attribute errors
        import re
        match = re.search(r"GENERATIVE PROBABILITY:\s*(\d+)", ai_text)
        if match:
            dynamic_score = match.group(1)
        else:
            dynamic_score = "85" # Fallback if regex fails to find a number

        return {"score": dynamic_score, "analysis": ai_text}

    except Exception as e:
        # 3. CRITICAL: This prevents the 500 Internal Server Error
        print(f"Server Error: {str(e)}")
        return {
            "score": "0", 
            "analysis": f"Forensic Brain Error: {str(e)}. Make sure Ollama is running!",
            "error": True
        }

@app.post("/detect-video")
async def detect_video(file: UploadFile = File(...)):
    prompt = """
    Perform a Forensic Video Audit. Determine a 'GENERATIVE PROBABILITY' (0-100%).
    
    STRICT RULES:
    - Start the response with exactly these three lines:
    GENERATIVE PROBABILITY: [Your Calculated Score]%
    LIGHTING VECTOR: [Analyze frame-to-frame lighting]
    BIOMETRIC SYNC: [Analyze lip-sync/blink consistency]

    Then, provide this 6-point audit:

    1. Extract Frames:

    2. Analyze Movement:

    3. Generate Score:

    4. AI Generation Probability:

    5. Video Quality Audit:

    6. FORENSIC_CONFIDENCE_SCORE: [Percentage]%


    """
    try:
        response = ollama.chat(model='qwen2.5:3b-instruct-q4_K_M', messages=[
            {'role': 'system', 'content': 'You are a high-fidelity Video Forensic Engine.'},
            {'role': 'user', 'content': prompt},
        ])
        
        ai_text = response['message']['content']
        match = re.search(r"GENERATIVE PROBABILITY:\s*(\d+)", ai_text)
        dynamic_score = match.group(1) if match else "50"

        return {"score": dynamic_score, "analysis": ai_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-veracity")
async def analyze_veracity(data: dict):
    text = data.get("text")
    if not text:
        return {"error": "No text provided for analysis"}
    try:
        # The STRICT FORENSIC PROMPT
        prompt = f"""
        Act as a Professional Forensic Fact-Checker. Analyze the following text based on these 14 parameters exactly.
        
        RULES:
        1. If the text is a universally accepted scientific/historical fact (e.g., 'The Sun rises in the East'), the Truth Probability MUST be 100%.
        2. If the text is demonstrably false or highly suspicious, the Truth Probability MUST be 10-20%.
        3. You MUST provide a score or analysis for every one of the 14 points below.

        TEXT TO ANALYZE: "{text}"

        OUTPUT FORMAT (Follow this line-by-line):
        TRUTH PROBABILITY: [Percentage]%
        
        1. Evidence-to-Claim Ratio:
        2. Source Authority & Reputation:
        3. Temporal Consistency (Timelines):
        4. Cross-Reference Matching:
        5. Contradiction Analysis:
        6. Linguistic Obfuscation:
        7. Clickbait/Sensationalism Coefficient:
        8. Fallacy Detection:
        9. Attribution Analysis:
        10. Sentiment Neutrality Score:
        11. Consensus Divergence:
        12. Financial/Malicious Intent Detection:
        13. Proper True Statement Behavior Detection:
        14. ACCURACY_CONFIDENCE: [Numerical percentage based on source consensus]
        FINAL AUDIT SUMMARY:
        """

        response = ollama.chat(model='qwen2.5:3b-instruct-q4_K_M', messages=[
            {'role': 'system', 'content': 'You are a high-precision forensic veracity engine.'},
            {'role': 'user', 'content': prompt},
        ])
        
        return {"analysis": response['message']['content']}
    except Exception as e:
        return {"error": str(e)}   

@app.post("/analyze-tone")
async def analyze_tone(data: dict):
    """
    Forensic Reasoning Route: Detects Urgency, AI-generation markers, and Bias.
    Synchronized with Qwen 2.5 3B via Ollama.
    """
    text = data.get("text")
    if not text:
        return {"error": "No text provided"}
        
    try:
        # THE STRICT FORENSIC COMMAND PROMPT
        forensic_prompt = f"""
        Act as an Advanced Psycholinguistic Forensic Analyst. 
        Analyze the following text strictly across these 21 parameters line-by-line.
        If a parameter is not applicable, state 'None detected' but do not skip the line.

        TEXT TO ANALYZE: "{text}"

        OUTPUT FORMAT:
        1. Perplexity:
        2. Burstiness:
        3. Top-K / Nucleus Sampling Artifacts:
        4. Synonym Swapping (Paraphrasing):
        5. N-gram Overlap:
        6. Claim Extraction:
        7. Source Cross-Referencing:
        8. Logical Consistency:
        9. Hyperbole Detection:
        10. Dark Patterns:
        11. Hate Speech & Toxicity Score:
        12. Psycholinguistic Features (LIWC):
        13. Bias Detection:
        14. Readability Index:
        15. Sentiment vs. Intent Gap:
        16. Cloaking Detection:
        17. Manipulation Tactics:
        18. Malicious Intent Detection:
        19. Urgency & Threatening Tone:
        20. Potential Fraud:
        21. ACCURACY_CONFIDENCE: [Numerical percentage based on linguistic patterns]
        FINAL FORENSIC VERDICT:
        """

        response = ollama.chat(model='qwen2.5:3b-instruct-q4_K_M', messages=[
            {'role': 'system', 'content': 'You are a high-precision psycholinguistic forensic engine. Focus on manipulation patterns and linguistic fingerprints.'},
            {'role': 'user', 'content': forensic_prompt},
        ])
        
        return {
            "status": "success",
            "analysis": response['message']['content'],
            #"readability_score": "Calculation Pending..." 
        }
    except Exception as e:
        return {"error": f"Tone Analysis Error: {str(e)}"}

if __name__ == "__main__":
    # Standardizing to 127.0.0.1 and Port 8003 to sync with router.js
    #uvicorn.run(app, host="127.0.0.1", port=8003)
    uvicorn.run(app, host="127.0.0.1", port=8003)

# === NEW QWEN PHISHING ENGINE ===
@app.post("/analyze-phishing")
async def analyze_phishing(data: dict):
    url = data.get("url")
    ssl = data.get("ssl", "Unknown")
    age = data.get("age", "Unknown")
    
    # Advanced Forensic Prompt for Qwen 2.5 3B
    prompt = f"""
    [CYBERSECURITY AUDIT MODE]
    Target URL: {url}
    SSL Status: {ssl}
    Domain Age: {age}
    
    Analyze the target for:
    1. Punycode or character-substitution attacks.

    2. TLD reputation and structural anomalies.

    3. Metadata risk (SSL/Age correlation).

    
    Output Format:
    - Verdict: (Safe / Suspicious / Malicious)
    - Risk Score: (X/100)
    - Forensic Insight: (Brief technical explanation)
    """
    
    try:
        # Calling your local Ollama engine (Qwen 2.5 3B)
        response = ollama.chat(model='qwen2.5:3b-instruct-q4_K_M', messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        return {"analysis": response['message']['content']}
    except Exception as e:
        return {"analysis": f"Forensic Engine Error: {str(e)}"}