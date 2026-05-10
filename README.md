# 🛡️ Sentinel: AI-Powered Forensic Integrity System

<div align="center">

![Sentinel Logo](https://img.shields.io/badge/SENTINEL-Forensic%20Centre-38bdf8?style=for-the-badge&logo=target)

*Advanced Neural Deconstruction & Multimedia Veracity Audit Engine*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-05998b?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat&logo=python)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-white?style=flat&logo=ollama)](https://ollama.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-f7df1e?style=flat&logo=javascript)](https://developer.mozilla.org/)
[![Tailwind CSS](https://img.shields.io/badge/Theme-Cyberpunk%20Dark-38bdf8?style=flat&logo=tailwindcss)](https://tailwindcss.com/)

[About](#-about) • [Features](#-features) • [Installation](#-installation) • [Tech Stack](#-tech-stack) • [Demo](#-demo) • [Contributing](#-contributing)

</div>

---

## 📖 About

**Sentinel** is an elite-tier Forensic AI platform engineered for the modern cybersecurity landscape. In an era of escalating deepfakes, sophisticated phishing, and digital misinformation, Sentinel provides a "Privacy-First" local audit suite. 

By leveraging **Qwen 2.5 3B** locally via Ollama, Sentinel deconstructs digital artifacts—URLs, Emails, Images, and Videos—to identify structural anomalies and generative patterns. It bridges the gap between complex forensic analysis and user-centric security, allowing anyone to verify digital integrity without their sensitive data ever leaving their hardware.

---

## ✨ Features

### 🔍 1. Neural LLM Detection
- **Intent Analysis**: Scans emails and messages for manipulative "Psycholinguistic" triggers.
- **Sentiment Forensics**: Detects high-pressure tactics often used in social engineering.

### 🖼️ 2. Advanced Image Forensics
- **ConvNeXt-Tiny Integration**: Utilizes Computer Vision to detect GAN-generated artifacts.
- **Structural Audit**: Scans for lighting inconsistencies and pixel-level noise patterns typical in AI generation.

### 📹 3. Video Veracity (LightFakeDetect)
- **Temporal Jitter Scan**: Identifies frame-to-frame inconsistencies in deepfake videos.
- **Biometric Sync**: Checks for unnatural lip-sync and eye-blinking patterns.

### ⚙️ 4. 10-30 Parameter AI Checking
- **Deep-Link Deconstruction**: Every URL is audited across 10-30 distinct forensic parameters, including Levenshtein distance, Punycode checks, and SSL metadata correlation.

### 📈 5. Dynamic AI Accuracy
- **Per-Run Confidence**: Every analysis provides a real-time "Accuracy Confidence" score, ensuring the user understands the reliability of the forensic output.

### 📚 6. Cybersecurity Knowledge Base
- **Educational Insights**: Each forensic report explains *why* a certain artifact is suspicious, building the user's security IQ.

### 🎨 7. Modern Cyberpunk UI/UX
- **Immersive Interface**: High-end cyberpunk aesthetics with smooth transitions and real-time scanning animations.
- **Blinking System Status**: Real-time visual feedback on backend connectivity.

### 📷 8. Flexible Forensic Capture
- **Manual Override**: If an automated link fails, users can manually input data for a structural audit.
- **File Uploads**: Native support for dragging and dropping multimedia for deepfake scanning.

---

## 🎬 Demo (Core Modules)

### 1. 🔗 Phishing Scan Workflow
```
Home → URL Integrity Scan → Automated/Manual Input → Qwen Neural Audit → 10-Point Report.
```

### 2. 👁️ Deepfake Analysis Image and Video
```
Upload Image/Video → Metadata Deconstruction → Lighting/Biometric Check → Generative Probability Score.
```

### 3. 📜 Privacy Policy Audit
```
Paste Legal Jargon → AI Permission Scan → Red-Flag Detection → Simplified User-Rights Report.
```

### 4. 🎭 Tone and ⚖️ Veracity Text Audit
```
Paste The text → AI Permission Scan → Truth Accurcy Detection → Simplified Accurate Text Report.
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.10+**: Core backend execution.
- **VS Code**: Recommended IDE with **Live Server** extension.
- **Ollama**: Required for running the Qwen 2.5 3B model locally.

---

### Environment Setup Instructions

1. **AI Model Pulling**:
   Open your terminal and run:
   ```bash
   ollama run qwen2.5:3b-instruct
   ```

2. **Backend Configuration (Python Venv)**:
   Open your terminal and run:
   ```bash
   cd backend
   python -m venv venv
   # Activate Venv
   .\venv\Scripts\activate # Windows
   source venv/bin/activate # Mac/Linux
   ```

   # Install Libraries
   Open your terminal and run:
   ```bash
   pip install fastapi uvicorn pydantic requests
   ```

3. **Run the Server**:
    Open your terminal and run:
   ```bash
   python main.py
   ```

The server will start on [http://127.0.0.1:8003]

4. **Launch Frontend**:
    Open frontend/index.html using the VS Code Live Server extension.

---

## 🛠️ Tech Stack
1. **Frontend**:
     - HTML5/CSS3: Custom Cyberpunk UI with glassmorphism.
     - JavaScript (ES6+): Asynchronous API routing and dynamic UI updates.
     - GSAP: Smooth scrolling and scanning animations.
2. **Backend**:
     - FastAPI: High-performance asynchronous Python framework.

     - Uvicorn: ASGI server for lightning-fast request handling.

     - Python-Multipart: For handling heavy media forensic uploads.
3. **AI & ML Core**:
     - Qwen 2.5 3B (Ollama): Local LLM for forensic reasoning and text veracity.

     - ConvNeXt-Tiny: Computer vision model for image fake detection.

     - LightFakeDetect: Light-weight optimized model for video temporal analysis.

     - OpenCV: Image preprocessing and metadata extraction.

---

##  📁 Project Structure
    
    ```
    sentinel-forensic-ai/
    ├── backend/                # FastAPI Application
    │   ├── main.py             # Server & AI Endpoints
    │   ├── requirements.txt    # Python Dependencies
    │   └── venv/               # Virtual Environment
    ├── frontend/               # User Interface
    │   ├── index.html          # Main Forensic     Dashboard
    │   ├── css/
    │   │   └── style.css       # Cyberpunk Styles
    │   ├── js/
    │   │   └── router.js       # API Routing & Logic
    │   └── assets/             # Media & Backgrounds
    └── README.md               # Documentation
    ```

 ---   

##  🎯 Features in Detail
-    **AI & ML Core**:
    - Input: User pastes a URL, text, or uploads media.

    - Neural Pulse: The request is routed to the local Qwen Engine.

    - Deconstruction: The AI audits 10-30 parameters (e.g., SSL age, syntax, biometric sync).

    - Report Generation: A detailed forensic breakdown is rendered with an Accuracy Score.

    - Local Security: No data is uploaded to the cloud; all analysis happens on your CPU/GPU.

---

##  ⚠️ Troubleshooting

   - **Backend Offline Error** : Ensure main.py is running and your router.js API_URL matches [http://127.0.0.1:8003].
   - **Ollama Connection Refused** : Ensure the Ollama app is running in your Windows System Tray.
   - **CORS Error** : The main.py included has CORSMiddleware configured to allow local connections. If blocked, check your browser extensions.


##  🤝 Contributing
We welcome security enthusiasts and developers to improve the Sentinel Core!

-    **Ways to Contribute**:
    1. Feature Suggestions: Propose new forensic modules.

    2. Bug Reporting: Help us identify edge cases in detection logic.

    3. Code Style: We follow PEP8 for Python and clean ES6 standards for JS.

-    **Development Workflow**:

        ```
      - Fork the repo → Create a branch → Commit changes → Open a Pull Request.
      ```

### Code Style

- Follow the existing code style
- Use TypeScript for type safety
- Write meaningful commit messages
- Add comments for complex logic
- Test your changes thoroughly

---

##  🙏 Acknowledgments
   - **Qwen Team** : For the incredibly capable local LLM.
   - **Ollama** : For making local AI execution seamless.
   - **Hackathon 2026** : For the platform to showcase digital integrity.

##  🌟 Star History
    If you find this forensic tool useful, please consider giving it a ⭐️ on GitHub!

---

## 📞 Contact & Support

-  **Issues** : [GitHub Issues](https://github.com/yourusername/Sentinel-Forensic-AI/issues)
-  **Discussions** : [GitHub Discussions](https://github.com/yourusername/Sentinel-Forensic-AI/discussions)
-  **Email** :  support@Sentinel-Forensic-AI.com

---

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.com/docs)
- [FASTAPI Best Practices Documentation](https://fastapi.tiangolo.com/tutorial/)
- [Cybersecurity Forensic Standards (NIST)](https://www.nist.gov/)


---

<div align="center">

  **Made with 🛡️ for a safer Digital World**

  **Sentinel - Your gateway to digital truth.**

</div>