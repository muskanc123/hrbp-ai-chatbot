# HRBP AI Chatbot

> An intelligent HR assistant powered by Google Gemini AI that provides instant access to employee data through natural language conversations.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)](https://www.mongodb.com/)

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

### Required Software

1. **Docker Desktop** (v20.10 or higher)
   - [Download for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - [Download for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - [Download for Linux](https://docs.docker.com/desktop/install/linux-install/)
   - Verify installation: `docker --version` and `docker-compose --version`

2. **Git** (v2.0 or higher)
   - [Download Git](https://git-scm.com/downloads)
   - Verify installation: `git --version`

3. **Google Gemini API Key** (Free)
   - Sign up at [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Click "Create API Key" to generate your key

### Optional (for manual setup without Docker)

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.11 or higher) - [Download](https://www.python.org/downloads/)
- **MongoDB** (v6.0 or higher) - [Download](https://www.mongodb.com/try/download/community)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/muskanc123/hrbp-ai-chatbot
cd hrbp-ai-chatbot

# 2. Set up environment variables
cd backend
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
nano .env  # or use any text editor

# 3. Return to project root and run
cd ..
chmod +x setup.sh
./setup.sh

# 4. Access the app
open http://localhost:5173
```

## ✨ Features

- 💬 Natural language queries about employee data
- 📊 Smart table formatting for multiple records
- 💾 Conversation history with MongoDB persistence
- 🎨 Modern UI with custom Exo 2 font and gradient design
- 🏗️ Clean Architecture with production-ready patterns
- 📝 Structured JSON logging
- 🔒 Secure error handling

## 📖 Documentation

For detailed documentation, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

## 🏗️ Architecture

```
Frontend (React) → API Layer → Service Layer → Repository Layer → MongoDB/AI
```

Built with Clean Architecture and Domain-Driven Design principles.

## 🛠️ Tech Stack

**Frontend:** React, Tailwind CSS, Axios  
**Backend:** FastAPI, Python 3.11, MongoDB  
**AI:** Google Gemini (gemini-flash-latest)  
**Infrastructure:** Docker, Docker Compose

## 📸 Screenshots

<img width="2878" height="1682" alt="image" src="https://github.com/user-attachments/assets/28068d0f-5446-49e5-abaa-7cc46798e045" />
<img width="1422" height="802" alt="image" src="https://github.com/user-attachments/assets/2a12f68f-5314-4486-b812-4f31effadc7e" />






## 👤 Author

**Muskan Chawla**  
Project: HRBP AI Assistant  
Date: January 2026
