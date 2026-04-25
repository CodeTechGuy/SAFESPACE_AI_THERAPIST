# 🧠 SafeSpace AI — Mental Health Support Chatbot

SafeSpace AI is an intelligent mental health and psychological support chatbot designed to provide **empathetic conversations, guided support, and real-world assistance** through therapist recommendations and crisis handling.

It combines **AI-powered conversational intelligence** with **practical support tools**, making mental health help more accessible and immediate.

---

## 🚀 Features

### 💬 Conversational AI

* Natural, human-like chat experience
* Short, empathetic responses (therapist-style)
* Multi-turn conversation support

### 🧠 Intelligent Agent System

* Built using an AI agent architecture
* Dynamically decides:

  * When to respond using LLM
  * When to call tools (therapist finder / emergency)

### 🏥 Therapist Finder

* Location-based therapist suggestions
* Provides:

  * Name
  * Clinic
  * Area
  * Phone number

### 🚨 Crisis Detection & Emergency Support

* Detects high-risk user inputs
* Triggers emergency workflow (Twilio integration)

### 📱 Multi-Platform Support

* Web UI (Streamlit)
* WhatsApp chatbot (via Twilio)

### 🎨 Modern Chat UI

* ChatGPT/WhatsApp-like interface
* Interactive therapist cards (call + maps)
* Clean, minimal, user-friendly design

---

## 🏗️ System Architecture

```
User (Web / WhatsApp)
        │
        ▼
Frontend (Streamlit / Twilio)
        │
        ▼
FastAPI Backend (main.py)
        │
        ▼
AI Agent (ai_agent.py)
        │
 ┌──────┼───────────────┐
 ▼      ▼               ▼
LLM   MedGemma       Tools
(Groq) (Ollama)   (Therapist / Emergency)
        │
        ▼
Response Formatter
        │
        ▼
User Output
```

---

## ⚙️ Tech Stack

| Layer        | Technology             |
| ------------ | ---------------------- |
| Frontend     | Streamlit              |
| Backend      | FastAPI                |
| AI Framework | LangChain              |
| LLM          | Groq (GPT-OSS-120B)    |
| Local Model  | MedGemma (Ollama)      |
| Messaging    | Twilio (WhatsApp)      |
| APIs         | Google Maps (optional) |

---

## 📂 Project Structure

```
SAFESPACE_AI_THERAPIST/
│
├── backend/
│   ├── main.py              # FastAPI server
│   ├── ai_agent.py          # AI agent logic
│   ├── tools.py             # MedGemma + emergency tools
│   ├── therapist.py         # Therapist finder tool
│   ├── config.py            # API keys & config
│
├── frontend.py              # Streamlit UI
│
├── requirements.txt
├── README.md
```

---

## ⚡ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/safespace-ai.git
cd safespace-ai
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` or update `config.py`:

```
GROQ_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=your_number
EMERGENCY_CONTACT=your_phone
GOOGLE_MAPS_API_KEY=optional
```

---

## ▶️ Running the Project

### Start Backend

```bash
uvicorn backend.main:app --reload
```

### Start Frontend

```bash
streamlit run frontend.py
```

---

## 📱 WhatsApp Integration

1. Setup Twilio WhatsApp Sandbox
2. Set webhook:

```
http://your-server/whatsapp_ask
```

3. Send message → chatbot replies instantly

---

## 🧠 How It Works

1. User sends message
2. FastAPI receives request
3. AI Agent analyzes intent
4. Agent decides:

   * LLM response
   * Therapist tool
   * Emergency tool
5. Response is formatted
6. Sent back to UI / WhatsApp

---

## 🔥 Key Highlights

* Modular AI agent architecture
* Real-time conversational support
* Therapist recommendation system
* Crisis-aware safety design
* Multi-platform deployment

---

## ⚠️ Limitations

* Not a replacement for professional therapy
* Static therapist data (unless API enabled)
* LLM responses may vary

---

## 🚀 Future Enhancements

* 🌍 Auto-location detection
* 📞 One-click therapist calling
* 🧠 Emotion detection & tracking
* 📊 User mental health analytics
* ☁️ Cloud deployment (AWS/GCP)

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📜 License

This project is for educational and research purposes.

---

## ❤️ Acknowledgement

Built to make mental health support more **accessible, immediate, and stigma-free** using AI.

---
