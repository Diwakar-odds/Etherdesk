<div align="center">
  
# 🌌 Etherdesk

**Your Entire Computer, Right in Your Pocket.**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/Gemini_API-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Etherdesk is a lightweight, IDE-agnostic "Pocket IDE" bridge application. Securely access your files, execute terminal commands, and command your AI agents—all from your mobile phone on your local Wi-Fi.*

---

<!-- Placeholder for a sleek UI screenshot: replace the img src with a real image when you upload to GitHub! -->
<img src="https://via.placeholder.com/800x400/0f111a/4ade80?text=Insert+Etherdesk+UI+Screenshot+Here" width="80%">

</div>

## ✨ Features

- 📁 **Mobile File Explorer** — Browse your entire local file system from your couch.
- 📝 **Remote Code Editor** — Open text/code files, apply blazing-fast edits via your phone keyboard, and save them directly to your PC.
- 💻 **Live Terminal Integration** — Stream `stdout` and `stderr` live! Run `git status`, test scripts, or start servers natively.
- 🤖 **Autonomous AI Bridge** — Send prompts from your phone. Our background daemon intercepts them, commands Google Gemini, and drops responses in real-time.
- 🔌 **IDE Agnostic** — Play nicely with **VS Code, Cursor, Antigravity, or Notepad**. It updates files OS-level, triggering live IDE refreshes automatically.
- 🔒 **Secure-by-Design** — Basic HTTP authentication locking out unwanted network snoopers.

---

## 🏗️ How It Works (Architecture)

Etherdesk uses a decoupled architecture. The Web Server serves the UI and handles OS functions natively, while the Listener acts as the "Brain", piping messages to LLMs via an asynchronous text-file event bus (`prompt.txt` / `response.txt`).

```mermaid
graph TD
    A[📱 Your Phone] <-->|HTTP / Wi-Fi| B(FastAPI Server)
    B <-->|Reads/Edits| C{💻 File System}
    B <-->|Shell Tasks| D[/> Local Terminal]
    B -->|Writes| E((prompt.txt))
    E -->|Polls| F[🤖 AI Listener]
    F <-->|API Calls| G((Google Gemini))
    F -->|Writes AI Reply| H((response.txt))
    H -->|Reads| B
```

---

## 🚀 Quick Start Guide

### 1. Installation

Clone this repository and jump into the directory:

```bash
git clone https://github.com/Diwakar-odds/Etherdesk.git
cd Etherdesk
```

Install the required Python modules:

```bash
pip install -r requirements.txt
```

### 2. Configuration & Credentials

Before launching, tweak your settings to keep things secure!

*   **Set Server Password:** Open `server.py` and modify `USERNAME` and `PASSWORD` (Lines 13-14).
*   **Plug in your AI:** Open `listener.py` and insert your **Gemini API Key** in the `GEMINI_API_KEY` variable. *(Optional: Only needed if you want the interactive AI chat).*

### 3. Ignition 💥

Spin up the network bridge (runs the UI & REST API):

```bash
python server.py
```

*In a new terminal window*, start the AI brain:

```bash
python listener.py
```

### 4. Connect from anywhere!

Take out your phone, ensure you are connected to the same Wi-Fi as your laptop, and type the IP address printed in your terminal (e.g., `http://192.168.1.100:8080`). Log in using the credentials you set, and take control!

---

<div align="center">
<i>Built with 💡 logic and ✨ magic for developer freedom.</i>
</div>
