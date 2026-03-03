<div align="center">

<img src="https://img.shields.io/badge/Investment%20Platform-v1.0-blue?style=for-the-badge&logo=python" alt="Investment Platform Banner">

</div>

# 📈 Investment Platform

> Backend-focused learning project designed to build solid foundations in API architecture, data integration, and modular system design.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-darkgreen?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [Current Implementation](#current-implementation)
- [AI-Powered Education Engine](#ai-powered-education-engine)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Development Approach](#development-approach)
- [Current Status](#current-status)
- [Next Steps](#next-steps)

## 🎯 Overview

**Investment Platform** is a web-based application designed to help beginner investors better understand stock market information without being overwhelmed by complex financial data.

Rather than offering advanced trading tools, this project focuses on:
- ✅ Clarity in data presentation
- ✅ Clear information structure
- ✅ Contextual understanding of market movements
- ✅ **AI-powered educational insights** on market factors and indicators

This project is developed as a **portfolio-driven backend engineering exercise**, emphasizing architecture, clean structure, and progressive system evolution. It integrates AI-driven education to transform raw market data into actionable understanding for beginners.

## 🚨 The Problem

Beginner investors often face **information overload**. Typical financial platforms display large volumes of technical indicators without explaining their practical meaning.

**Goal:** Reduce complexity through:
- 📊 Aggregation of essential indicators
- 📑 Clear structuring of financial data
- 💡 Contextual understanding of price variations
- 🔗 Connection of market data with simplified explanations

## ⚙️ Current Implementation

### Backend (FastAPI)
- ✅ Modular architecture (routes + services separation)
- ✅ RESTful API structure
- ✅ Market summary endpoint
- ✅ Stock search endpoint (ticker autocomplete)
- ✅ Stock quote endpoint (Yahoo Finance integration)
- ✅ External API consumption with structured error handling
- ✅ Environment-aware setup
- ✅ Organized and scalable project structure

### Frontend
- ✅ Basic interface for stock search
- ✅ Dynamic data fetching from backend API
- ✅ Initial structure for future visualization expansion

### 🤖 AI-Powered Education Engine (In Development)
- 📌 **AI-Generated Insights** (Educational Preview Mode)
  - Summary of relevant market facts and key developments
  - Educational analysis of how factors influence current stock price
  - Contextual explanations of market dynamics and their impact
  - Educational breakdown of how technical indicators affect decision-making
  
> ⚠️ **Important:** This feature is purely **educational** and for learning purposes only. It does NOT provide buy/sell recommendations or investment advice. Users are encouraged to conduct their own research before making investment decisions.

## 🤖 AI-Powered Education Engine

The Investment Platform integrates AI-driven educational features designed to transform raw market data into meaningful, digestible insights for beginner investors.

### What It Does

**The AI educator provides:**

1. **📊 Relevant Facts Summary** - Aggregates key market events, earnings reports, news, and economic indicators affecting the stock

2. **📈 Educational Price Impact Analysis** - Explains *how* and *why* specific factors influence the current stock price in understandable terms

3. **🎓 Market Dynamics Explanation** - Breaks down complex market phenomena into contextual, learner-friendly explanations

4. **📐 Technical Indicator Education** - Shows how indicators (MA, RSI, MACD, etc.) work and their role in investment decision-making

### Educational Focus, Not Trading Signals

⚠️ **Critical Distinction:** This feature is **purely educational**:
- ❌ Does NOT recommend buying or selling stocks
- ❌ Does NOT provide investment advice
- ✅ Focuses on explaining market mechanics
- ✅ Helps users develop financial literacy
- ✅ Encourages independent research and critical thinking

The goal is to empower beginners to *understand* the market, not to tell them *what to do*.

## 📁 Project Structure

```
investment-platform/
├── backend/
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── main.py            # FastAPI application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html         # Main page
│   ├── stock.html         # Stock query page
│   └── app.js             # Frontend logic
├── design/                # Design files (Excalidraw)
├── docs/                  # Project documentation
└── README.md
```

## 🛠 Technology Stack

### Backend
- **Python 3.9+** - Primary language
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Requests** - HTTP client for external API integration

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **Vanilla JavaScript** - Interactivity (no dependencies)

### Development Tools
- **Git & GitHub** - Version control and structured commit history
- **Modular Architecture** - Separation of concerns
- **.gitignore** - Environment separation

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- A modern web browser

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/investment-platform.git
cd investment-platform
```

**2. Set up a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

**3. Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**4. Run the backend server:**
```bash
python main.py
```

**5. Open the frontend application:**
```bash
# Open your browser and visit:
http://localhost:8000
```

## 📚 Documentation

- [System Architecture](docs/architecture.md)
- [Project Roadmap](docs/roadmap.md)

## 🔄 Development Approach

This project follows a **learning-driven but production-aware** methodology:

1. **Problem Definition** - Clear scope understanding
2. **Architecture Design** - Structural planning
3. **Modular Backend Implementation** - Scalable construction
4. **API Integration & Testing** - Functional validation
5. **Controlled Feature Expansion** - Incremental growth

### Philosophy
AI tools are used as discussion and mentoring assistants to support architectural reasoning and learning. **All implementation decisions and coding remain human-driven.**

The objective is **not rapid feature shipping**, but technical depth and structural clarity.

## 📊 Current Status

- ⏳ Backend MVP in progress
- ✅ Core API endpoints implemented
- ✅ External data integration working
- ✅ Project structure stabilized
- 🔄 Preparing for database layer integration

## 🎯 Next Steps

- [ ] Introduce database integration (SQLite or PostgreSQL)
- [ ] Implement data persistence layer
- [ ] Improve input validation and error handling
- [ ] Add authentication layer (JWT)
- [ ] Deploy API to cloud environment
- [ ] Expand frontend capabilities

## 💡 Project Purpose

This project serves as:

1. **Backend Engineering Portfolio** - Demonstration of technical skills
2. **Structured Learning Platform** - API design and system architecture
3. **Progressive Technical Development** - Qualitative evolution
4. **Active Development** - Iterative improvement focused on backend foundations

---

<div align="center">

Built with ❤️ as a backend learning exercise

</div>