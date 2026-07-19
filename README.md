# 👔 AURA — AI-Powered Wardrobe Recommendation System

> **AURA** is a multi-agent AI system that delivers personalized outfit recommendations by combining wardrobe data, real-time weather, occasion, mood, and individual style preferences. Instead of relying on a single LLM prompt, specialized AI agents collaborate to make recommendations that are more explainable, consistent, and context-aware.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi">
  <img src="https://img.shields.io/badge/LangGraph-Multi--Agent-orange">
  <img src="https://img.shields.io/badge/Gemini-LLM-blueviolet">
  <img src="https://img.shields.io/badge/Railway-Deployed-black?logo=railway">
</p>

---

# 📖 Overview

Selecting an outfit is rarely a simple choice. Factors such as **weather**, **occasion**, **personal style**, **mood**, and **available wardrobe items** all influence what someone should wear.

AURA approaches this problem through a **multi-agent architecture**, where each AI agent specializes in understanding one aspect of the recommendation process. Their outputs are then combined by an orchestration pipeline to generate an outfit recommendation along with transparent reasoning and a compatibility score.

This modular design makes the system easier to extend, debug, and improve compared to traditional single-prompt solutions.

---

# 🏗️ System Architecture

AURA follows a sequential multi-agent workflow orchestrated using **LangGraph**.

```text
                        User Request
                              │
                              ▼
                    ┌─────────────────┐
                    │ Wardrobe Agent  │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Weather Agent   │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Occasion Agent  │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────────────┐
                    │ User Preference Agent   │
                    └─────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Fashion Agent   │
                    └─────────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Outfit Generator (LLM) │
                  └────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Scoring Agent   │
                    └─────────────────┘
                              │
                              ▼
                  🎯 Final Recommendation
```

---

## 🤖 Agent Responsibilities

| Agent | Responsibility |
|-------|----------------|
| **Wardrobe Agent** | Retrieves the user's wardrobe and filters available clothing items. |
| **Weather Agent** | Fetches real-time weather conditions and determines weather-appropriate clothing. |
| **Occasion Agent** | Understands the occasion and extracts dress code requirements. |
| **User Preference Agent** | Applies personal preferences such as style, colors, and comfort level. |
| **Fashion Agent** | Provides fashion knowledge and styling guidance using an LLM. |
| **Outfit Generator** | Combines outputs from all agents to generate the final outfit recommendation with reasoning. |
| **Scoring Agent** | Evaluates the recommendation based on weather, occasion, style, and preference alignment, producing a compatibility score. |

---

# ⚙️ Tech Stack

| Technology | Why It Was Chosen |
|------------|-------------------|
| **Python** | Primary backend language for rapid development and AI integration. |
| **FastAPI** | Lightweight, high-performance framework for REST APIs. |
| **LangGraph** | Manages the execution flow between AI agents. |
| **Pydantic** | Ensures robust request and response validation. |
| **Google Gemini API** | Provides reasoning capabilities for fashion recommendations. |
| **OpenWeather API** | Supplies live weather information for context-aware suggestions. |
| **Railway** | Simplifies deployment and hosting of the backend service. |

---

# 🚀 API Endpoints

## 1️⃣ Generate Outfit Recommendation

### `POST /recommend`

Generates a personalized outfit recommendation based on user context.

### Request

```json
{
  "user_id": "user_001",
  "mood": "Confident",
  "occasion": "Party",
  "city": "Delhi"
}
```

### Response

```json
{
  "explanation": "A sophisticated smart casual ensemble...",
  "fullReasoning": "Detailed item-by-item justification...",
  "compatibilityScore": 87,
  "scoreReasoning": "This outfit scores highly because...",
  "itemIds": [
    "top_003",
    "bottom_002",
    "foot_002",
    "acc_001"
  ]
}
```

---

## 2️⃣ Submit Feedback

### `POST /feedback`

Stores user feedback to improve future recommendations.

### Request

```json
{
  "user_id": "user_001",
  "outfit_reasoning": "The fullReasoning string from /recommend response.",
  "user_score": 4,
  "score_reasoning": "The scoreReasoning string from /recommend response."
}
```

### Response

```json
{
  "status": "success",
  "message": "Feedback saved."
}
```

---

<!-- # 💻 Running the Project Locally

## 1. Clone the Repository

```bash
git clone https://github.com/sana1H/Capstone_Agents.git
cd Capstone_Agents
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

---

## 4. Start the Development Server

```bash
uvicorn main:app --reload
```

---

## 5. Open the Interactive API Documentation

```
http://127.0.0.1:8000/docs
```

--- -->

<!-- # 📁 Project Structure

```text
AURA/
│
├── agents/
│   ├── fashion_agent.py
│   ├── occasion_agent.py
│   ├── scoring_agent.py
│   ├── user_preference_agent.py
│   ├── wardrobe_agent.py
│   └── weather_agent.py
│
├── contracts/
│   └── schemas.py
│
├── mock_data/
│   ├── wardrobe.json
│   └── feedback.json
│
├── orchestrator/
│   └── graph.py
│
├── scripts/
│   └── generate_mock_data.py
│
├── tools/
│   ├── llm_client.py
│   ├── weather_tool.py
│   └── save_user_feedback.py
│
├── main.py
├── requirements.txt
├── Procfile
├── .env
└── README.md
```

--- -->

# ✨ Key Features

- 🤖 Multi-agent AI architecture powered by LangGraph
- 👕 Personalized outfit recommendations
- 🌦️ Real-time weather-aware clothing selection
- 🎉 Occasion and mood-based styling
- ❤️ User preference integration
- 💡 Explainable AI reasoning for every recommendation
- 📊 Compatibility scoring with quality evaluation
- 🔄 Feedback collection for future personalization
- ☁️ Cloud deployment on Railway with REST APIs

---

# 🔮 Future Improvements

- 📸 Vision-based clothing recognition
- 👤 User authentication and profile management
- 🗄️ Database-backed wardrobe storage
- 📅 Calendar integration for automatic occasion detection
- 📱 Mobile application
- 🧠 Learning from historical user feedback
- 👗 Outfit history and favorites
- 🎨 Seasonal wardrobe planning

---

# 🌐 Live Demo

### API Documentation

**https://web-production-63b634.up.railway.app/docs**

---

<!-- # 👥 Team

| Member | Responsibility |
|---------|----------------|
| **Sanya Narula** | Backend Development • Multi-Agent Architecture • API Development • LLM Integration |
| **Akarsh Dhingra** | Mobile Application Development |
| **Vision Model** | CNN-based Clothing Recognition *(In Progress)* |

--- -->

# 📌 Project Highlights

- Built using a **modular multi-agent architecture** instead of a single LLM prompt.
- Generates **context-aware** outfit recommendations using weather, occasion, wardrobe, and personal preferences.
- Produces **transparent reasoning** alongside every recommendation.
- Designed with **extensibility** in mind, allowing new agents and capabilities to be integrated with minimal changes.

---

<p align="center">
Built using FastAPI, LangGraph, Gemini, and OpenWeather API.
</p>