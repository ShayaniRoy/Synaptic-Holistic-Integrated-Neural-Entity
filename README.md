# S.H.I.N.E. (Synaptic Holistic Integrated Neural Entity)

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

> [!NOTE]
> **S.H.I.N.E.** is an advanced, full-stack multimodal AI framework integrating real-time computer vision, vocal telemetry, secure authentication, and dynamic multi-model LLM orchestration into a unified glassmorphism dashboard.

---

## 📌 Overview

**S.H.I.N.E.** is designed to process multiple streams of sensory data—including visual emotion telemetry, vocal input, and structured prompt engineering. Built with a robust Flask backend and an immersive, responsive UI, S.H.I.N.E. provides a seamless end-to-end environment for modern human-computer interaction (HCI) and intelligent multi-LLM routing.

---

## ✨ Key Features

* 🧠 **Multimodal Interaction Suite:** Combines live facial emotion analysis via OpenCV with speech-to-text voice recognition for natural input processing.
* 🔀 **Multi-Model LLM Orchestration:** Dynamic model selection and fallback routing across primary AI providers to ensure maximum response fidelity and uptime.
* 🔐 **Secure User Lifecycle Management:** Production-ready user authentication utilizing hashed passwords, session management, and SQLite with SQLAlchemy ORM.
* 🛡️ **Zero-Trust Environment Isolation:** Fully decoupled environment configuration (`.env`) ensuring zero exposure of sensitive local credentials, secret keys, or database files.
* 🎨 **Glassmorphism Design System:** Clean, dark-mode user interface crafted with HTML5, CSS3, and modern frontend design standards.

---

## 🧠 Enterprise AI/ML Architecture & Model Orchestration

S.H.I.N.E. features a production-grade, hybrid multimodal architecture that unifies real-time spatial computer vision, audio perception pipelines, and dynamic multi-provider Large Language Model (LLM) orchestration.

## 🏗️ Production Systems Architecture & Model Governance

S.H.I.N.E. is engineered as a high-throughput, fault-tolerant multimodal intelligence framework. Designed with a decoupled sensory pipeline, it dynamically balances cloud acceleration with privacy-first edge execution.

### 🔄 End-to-End Distributed Execution Flow

1. **Multimodal Ingestion Layer**
   Asynchronous capture of continuous video frames and streaming audio waveforms.
2. **Inference & Feature Extraction**
   * **Spatial Vision Pipeline:** OpenCV-driven region-of-interest (ROI) isolation paired with deep Convolutional Neural Networks (CNNs) for real-time micro-expression emotion inference.
   * **Acoustic Perception Core:** **Whisper-Large-v3** transformer streaming pipeline converting live speech directly into text tokens for instant prompt injection.
3. **Context Serialization & Prompt Engineering**
   Encapsulates real-time emotional metrics and active conversational states into structured, dynamic prompt payloads.
4. **Fault-Tolerant Routing Engine**
   Automated load-balancing and failover mechanism ensuring zero-downtime switching between cloud accelerators and local edge runtimes.

### 🔬 Core Systems Engineering & Design Patterns

* **🖼️ Multimodal Spatial Vision Engine**
  Built for low-latency visual tracking. Uses OpenCV for face detection and bounding-box tracking, feeding normalized frames into deep CNNs to map affective states.
* **🎙️ Low-Latency Speech & Perception Core**
  Leverages **Whisper-Large-v3** and **Whisper-Large-v3-turbo** for high-accuracy streaming speech-to-text (STT) and real-time voice interaction.
* **⚙️ Adaptive Fallback & Orchestration Router**
  Implements intelligent multi-provider routing to guarantee system resilience, automatically rerouting queries if primary cloud APIs experience throttling or latency spikes.

### 🚀 Production Model Registry & Runtimes

* **⚡ Groq LPU Cloud Acceleration** `Cloud Inference` `Ultra-Low Latency`
  * **System Role:** High-throughput streaming conversation, complex multi-step reasoning, and rapid speech transcription.
  * **Deployed Models:** 
    * `meta-llama/llama-4-scout-17b-16e-instruct`
    * `llama-3.1-8b-instant`
    * `llama-3.3-70b-versatile`
    * `whisper-large-v3`
    * `whisper-large-v3-turbo`

* **💻 Ollama Edge Runtime** `On-Device Inference` `Privacy-First`
  * **System Role:** Offline local execution, edge computing, zero network overhead, and private chain-of-thought (CoT) reasoning.
  * **Deployed Models:** 
    * `gemma4:e4b`
    * `llama3.2`
    * `deepseek-r1`
    * `deepseek-r1:1.5b`

* **🌐 Google Generative AI** `API Extension Layer` `Multimodal Fallback`
  * **System Role:** Cross-provider redundancy, complex contextual evaluation, and system fallback routing.
  * **Deployed Models:** 
    * `genai`
---

## 📸 Interface & Preview

> *You can drag and drop your project screenshots directly into the GitHub editor below!*

| Multimodal Workspace | Vision & Telemetry Engine |
| :---: | :---: |
| *(Add Dashboard Screenshot)* | *(Add Computer Vision Preview)* |

---

## 🛠️ System Architecture & Tech Stack

### **Backend Framework & Core Engine**
* **Language:** Python 3.x
* **Web Framework:** Flask
* **Database & ORM:** SQLite, SQLAlchemy
* **Security:** Werkzeug Password Hashing, Session Management

### **Multimodal & AI Processing**
* **Computer Vision:** OpenCV (`opencv-python`) for real-time video feed and facial attribute extraction.
* **Audio & Speech:** SpeechRecognition library with microphone stream processing.
* **LLM Engine:** API-driven multi-LLM orchestration layer.

### **Frontend & User Interface**
* **Core:** HTML5, Modern CSS3 (CSS Grid/Flexbox, Glassmorphism UI)
* **Interactivity:** JavaScript (Fetch API for asynchronous backend communication)

---

## 📁 Repository Structure

```text
shine-ai-framework/
├── app.py                  # Main Flask application & route controllers
├── config.py               # Application configuration & environment loader
├── models.py               # SQLAlchemy database models & user schema
├── static/
│   ├── css/                # Custom CSS files & UI styling
│   └── js/                 # Asynchronous API handlers & frontend logic
├── templates/              # HTML5 template engine (Jinja2)
│   ├── index.html          # Main multimodal workspace dashboard
│   ├── login.html          # User authentication portal
│   └── signup.html         # User registration portal
├── .gitignore              # Ignored files (keys, DB, build artifacts)
├── LICENSE                 # MIT License
└── requirements.txt        # Python package dependencies

---

## 🗺️ Roadmap & Future Enhancements

The **S.H.I.N.E.** framework is engineered for continuous evolution. Below is the active development roadmap detailing current milestones and upcoming architectural expansions:

### **Phase 1: Core Multimodal Integration (Completed ✅)**
- [x] **Real-Time Facial Emotion Detection:** Integrated OpenCV vision pipelines for live facial attribute extraction and telemetry.
- [x] **Speech Recognition Module:** Built robust vocal input handling via speech-to-text processing streams.
- [x] **Dynamic LLM Orchestration:** Implemented multi-model routing to balance query complexity and uptime across primary providers.
- [x] **Secure Authentication & DB:** Established production-ready user lifecycle management using Flask, SQLite, and SQLAlchemy ORM with password hashing.
- [x] **Glassmorphic UI Design:** Developed a modern, responsive, dark-mode user workspace dashboard.

### **Phase 2: Performance & Scalability (In Progress 🚧)**
- [ ] **WebSocket Stream Integration:** Upgrade from standard HTTP fetch calls to bidirectional WebSockets for lower-latency real-time video/audio streaming.
- [ ] **Advanced Prompt Caching:** Implement local caching layers to optimize LLM response times and reduce API token overhead.
- [ ] **Role-Based Access Control (RBAC):** Expand user authentication models to support distinct permission tiers and multi-user session isolation.

### **Phase 3: Enterprise Deployment & DevOps (Planned 🔮)**
- [ ] **Docker Containerization:** Package the Flask backend, OpenCV dependencies, and Python environment into a production-ready `Dockerfile`.
- [ ] **Automated CI/CD Pipelines:** Set up GitHub Actions for automated linting, testing, and container registry publishing.
- [ ] **Cloud Database Migration:** Provide optional configuration support for production-grade databases like PostgreSQL.
---


## 🛡️ Security & Privacy Notice

**S.H.I.N.E.** is engineered with a strict **Zero-Trust & Privacy-First Architecture**. The repository strictly follows open-source deployment standards to guarantee zero exposure of user telemetry, API credentials, or environment configurations.

### **Key Security Protocols:**
* 🔑 **Environment Variable Isolation:** All critical API credentials, secret keys, and database connections are fully decoupled from the core source code via `.env` files and managed dynamically via `config.py`.
* 🔒 **Zero Hardcoded Secrets:** `.gitignore` rules prevent local environment files, SQLite databases (`*.db`), virtual environments, and cache artifacts (`__pycache__/`) from ever being committed to source control.
* 🛡️ **User Authentication & Password Hashing:** User security is maintained using industry-standard password hashing algorithms (via Werkzeug) alongside secure session management.
* 👁️ **Local Vision & Audio Processing:** Facial attribute telemetry and speech recognition processing streams are handled locally within the active session environment, ensuring raw audio/video frames are never logged or stored externally without user consent.
