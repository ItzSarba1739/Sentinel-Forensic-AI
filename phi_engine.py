import ollama

class SentinelLLM:
    def __init__(self):
        # Updated to match your exact Ollama download for Qwen 2.5 3B
        self.model_name = "qwen2.5:3b-instruct-q4_K_M"
        print(f"[*] Sentinel Core: Initializing Qwen Engine ({self.model_name})...")

    def _generate_response(self, prompt):
        """Internal helper to communicate with the local Qwen model."""
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.2, # Lowered for forensic precision
                    "num_ctx": 4096,
                    "top_p": 0.9
                }
            )
            return response['response']
        except Exception as e:
            return f"CRITICAL_ERROR: Connection to Ollama failed. Detail: {str(e)}"

    def audit_privacy_policy(self, policy_text):
        """
        Deep Forensic Audit for Privacy Policies using Qwen 2.5.
        Analyzes Hardware Permissions, Data Sharing, and User Rights.
        """
        prompt = f"""
        <|im_start|>system
        You are a Privacy & Compliance Auditor. Analyze the provided policy text and provide a detailed report based on these parameters:
        
        1. HARDWARE & PERMISSIONS: Scan for access to Sensors (Camera, Mic, Gyroscope), Personal Data (Contacts, SMS), and Storage (Photos, Files).
        2. DATA USAGE: Identify Third-Party Sharing, Data Selling (CCPA), and Retention periods.
        3. USER RIGHTS: Check for Right to Erasure, Opt-Out mechanisms, and GDPR compliance.
        4. TRUST SIGNALS: Note encryption standards and if a Data Protection Officer (DPO) is listed.
        <|im_end|>
        <|im_start|>user
        TEXT TO AUDIT: 
        {policy_text}
        <|im_end|>
        <|im_start|>assistant
        FORENSIC PRIVACY REPORT:
        """
        return self._generate_response(prompt)
    
    def analyze_deepfake_report(self, media_type, score, artifacts):
        """
        Generates a professional forensic report based on CV model metrics.
        """
        artifact_str = ", ".join(artifacts)
        prompt = f"""
        <|im_start|>system
        You are a Deepfake Forensic Specialist. Analyze the detection metrics from the {media_type} analysis engine.
        <|im_end|>
        <|im_start|>user
        ENGINE REPORT:
        - Media: {media_type}
        - Probability of Fake: {score}%
        - Detected Artifacts: {artifact_str}

        Please write a detailed security report for the user explaining:
        1. The specific anatomical/temporal red flags found.
        2. The risk of the content (High/Medium/Low).
        3. A final verdict on veracity.
        <|im_end|>
        <|im_start|>assistant
        SENTINEL FORENSIC REPORT:
        """
        return self._generate_response(prompt)
    
    def analyze_veracity(self, text):
        """
        Forensic Veracity Audit using Qwen 2.5.
        Analyzes Evidence-to-Claim ratios, Consensus Divergence, and Intent.
        """
        prompt = f"""
        <|im_start|>system
        You are a Fact-Check Forensic Specialist. Analyze the provided text for veracity and integrity.
        Evaluate based on these specific parameters:
        1. EVIDENCE-TO-CLAIM RATIO: Check for citations vs. 'naked' claims.
        2. CONTRADICTION ANALYSIS: Identify internal logical fallacies.
        3. CONSENSUS DIVERGENCE: How much does this claim differ from established scientific or general consensus?
        4. LINGUISTIC OBFUSCATION: Is jargon being used to hide simple truths?
        5. SENTIMENT NEUTRALITY: Is the text highly emotional or biased?
        <|im_end|>
        <|im_start|>user
        TEXT TO AUDIT: 
        {text}
        <|im_end|>
        <|im_start|>assistant
        SENTINEL VERACITY REPORT:
        """
        return self._generate_response(prompt)

    def analyze_tone(self, text):
        """
        Forensic Tone & Intent Analysis using Qwen 2.5.
        Analyzes AI-patterns, Veracity, and Manipulative Intent.
        """
        prompt = f"""
        <|im_start|>system
        You are a Forensic Psycholinguist. Analyze the text for 'Sentinel Tone Reasoning'. 
        Evaluate the following specific parameters:
        
        1. AI PATTERNS: Assess Perplexity (predictability) and Burstiness (sentence variety).
        2. VERACITY: Identify factual Claim Extraction, Hyperbole, and Logical Consistency.
        3. INTENT & SAFETY: Detect Dark Patterns (False Urgency/Guilt), Toxicity, and Clout (authority level).
        4. PSYCHOLINGUISTICS: Analyze Authenticity (pronoun usage) and Bias Detection.
        <|im_end|>
        <|im_start|>user
        TEXT TO ANALYZE: 
        {text}
        <|im_end|>
        <|im_start|>assistant
        FORENSIC TONE REPORT:
        """
        return self._generate_response(prompt)

    def analyze_url_forensics(self, url, metadata=None):
        """
        Advanced URL Forensics using Qwen 2.5.
        Analyzes URL structure, SSL metadata, and Domain Age.
        """
        # Formulate the technical context
        tech_data = f"URL: {url}\n"
        if metadata:
            tech_data += f"Domain Age: {metadata.get('age', 'Unknown')}\n"
            tech_data += f"SSL Status: {metadata.get('ssl', 'Unknown')}\n"
            tech_data += f"Redirects: {metadata.get('redirects', '0')}\n"

        prompt = f"""
        <|im_start|>system
        You are a Cyber-Forensics Expert. Analyze the provided metadata for 'Typosquatting', 'SSL Hijacking', and 'Domain Reputation'.
        <|im_end|>
        <|im_start|>user
        Analyze these parameters:
        {tech_data}

        Provide a risk score (0-100) and list the 3 most suspicious technical flags based on:
        1. Levenshtein Distance/Typosquatting.
        2. SSL Certificate Age & Issuer.
        3. Form Action & Redirect Chains.
        <|im_end|>
        <|im_start|>assistant
        """
        return self._generate_response(prompt)

if __name__ == "__main__":
    # System Check
    scanner = SentinelLLM()
    
    print("\n--- SENTINEL AI: SYSTEM CHECK (QWEN 2.5) ---")
    
    # Test Policy
    test_policy = "We collect your GPS location 24/7 and sell it to third-party data brokers."
    print("\n[Policy Audit Test]:", scanner.audit_privacy_policy(test_policy))
    
    # Test URL
    test_url = "http://secure-login-verify-paypal.com-update.net/login"
    print("\n[URL Forensics Test]:", scanner.analyze_url_forensics(test_url))