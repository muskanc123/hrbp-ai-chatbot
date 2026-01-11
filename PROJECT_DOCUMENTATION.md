# HRBP AI Chatbot - Project Documentation

## 📋 Project Overview

An intelligent HR Business Partner (HRBP) chatbot that provides instant access to employee data through natural language conversations. The system uses Google's Gemini AI to answer HR-related queries about employees, their leaves, loans, performance ratings, and medical reimbursements.

**Live Demo:** [Include your deployment URL or screenshots]

---

## 🎯 Approach & Architecture

### Technical Stack

**Frontend:**
- React 18 with Vite
- Tailwind CSS for styling
- Axios for API communication
- Custom Exo 2 font family

**Backend:**
- FastAPI (Python) with async/await
- MongoDB for conversation persistence
- Google Gemini AI (gemini-flash-latest)
- Clean Architecture with Domain-Driven Design

**Infrastructure:**
- Docker & Docker Compose
- MongoDB for data persistence
- Excel data source for employee information

### Architecture Design

The application follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  Components → Services → API Layer                       │
└─────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│                                                          │
│  API Layer (v1)                                         │
│    ↓                                                     │
│  Service Layer (Business Logic)                         │
│    ↓                                                     │
│  Repository Layer (Data Access)                         │
│    ↓                                                     │
│  Infrastructure (MongoDB, Gemini AI)                    │
└─────────────────────────────────────────────────────────┘
```

**Key Design Decisions:**

1. **Clean Architecture**: Separated concerns into layers (API, Domain, Infrastructure)
2. **Repository Pattern**: Abstracted data access for testability and flexibility
3. **Service Layer**: Encapsulated business logic separate from HTTP handling
4. **Configuration Management**: Externalized AI prompts to YAML for easy iteration
5. **Error Handling**: Custom exception hierarchy with secure error responses
6. **Structured Logging**: JSON-formatted logs for production observability
7. **API Versioning**: `/api/v1` prefix for future-proof API evolution

### Key Features

✅ **Conversational AI Interface**
- Natural language queries about employee data
- Context-aware responses
- Conversation history persistence

✅ **Smart Data Presentation**
- Automatic table formatting for multiple records
- Concise responses for single queries
- HTML-formatted responses with custom styling

✅ **User Experience**
- Multiple conversation management
- Delete conversations
- Custom scrollbar with gradient design
- Responsive layout

✅ **Production-Ready Architecture**
- Comprehensive error handling
- Structured logging
- Testable codebase
- Scalable design

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed on your system:

**Required:**
- ✅ **Docker Desktop** (v20.10+) - [Download here](https://www.docker.com/products/docker-desktop/)
  - Includes Docker Engine and Docker Compose
  - Verify: `docker --version` and `docker-compose --version`
- ✅ **Git** (v2.0+) - [Download here](https://git-scm.com/downloads)
  - Verify: `git --version`
- ✅ **Google Gemini API Key** (Free) - [Get API key](https://makersuite.google.com/app/apikey)

**Optional (for manual setup):**
- Node.js v18+ (for frontend without Docker)
- Python 3.11+ (for backend without Docker)
- MongoDB v6.0+ (for database without Docker)

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd hrbp-ai-chatbot
   ```

2. **Configure environment variables**
   
   ```bash
   # Copy the example environment file
   cd backend
   cp .env.example .env
   ```
   
   Edit `backend/.env` and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
   
   All other variables have sensible defaults for Docker setup.

3. **Run the application**
   ```bash
   # Return to project root
   cd ..
   
   # Make setup script executable and run
   chmod +x setup.sh
   ./setup.sh
   ```

   This will:
   - Build Docker images for frontend, backend, and MongoDB
   - Start all services in containers
   - Initialize the database with indexes
   - Load employee data from Excel file
   - Display startup logs

4. **Access the application**
   
   Once you see "Application is ready!" in the logs:
   - **Frontend UI**: http://localhost:5173
   - **API Documentation**: http://localhost:8000/docs
   - **API Health Check**: http://localhost:8000/health
   - **Alternative API Docs**: http://localhost:8000/redoc

### Stopping the Application

```bash
# Stop all containers
docker-compose down

# Stop and remove all data (fresh start)
docker-compose down -v
```

### Manual Setup (without Docker)

<details>
<summary>Click to expand manual setup instructions</summary>

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**MongoDB:**
```bash
# Install and run MongoDB locally
mongod --dbpath /path/to/data
```
</details>

---

## 📖 Usage Examples

### Example Queries

1. **Single Employee Query:**
   - "Which employee has taken the highest amount of loan?"
   - "What is Sarah's performance rating?"
   - "How many leaves does John have remaining?"

2. **Multiple Employee Queries:**
   - "Show me all employees with their leave balances"
   - "List all employees in the IT department"
   - "Compare performance ratings of all employees"

3. **Analytical Queries:**
   - "Who has the highest medical reimbursement?"
   - "Show employees with loan amounts over $100,000"

### Screenshots

[Include screenshots of:]
- Main chat interface
- Table formatting example
- Conversation management
- Mobile responsive view

---

## 🏗️ Project Structure

```
hrbp-ai-chatbot/
├── backend/
│   ├── api/                    # API layer
│   │   ├── v1/
│   │   │   └── endpoints/      # API endpoints
│   │   └── middleware/         # Error handling
│   ├── core/                   # Core infrastructure
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── logging_config.py   # Structured logging
│   ├── domain/                 # Domain layer
│   │   ├── models/             # Domain models
│   │   ├── repositories/       # Data access
│   │   └── services/           # Business logic
│   ├── infrastructure/         # External services
│   │   └── ai/                 # Gemini AI client
│   ├── config/
│   │   └── prompts/            # AI prompt templates
│   ├── main.py                 # Application entry
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API service
│   │   └── App.jsx             # Main app
│   └── package.json
├── docker-compose.yml
└── setup.sh
```

---

## 🔧 Configuration

### AI Prompt Customization

Edit `backend/config/prompts/hrbp_assistant.yaml` to customize:
- Response style and tone
- Table formatting rules
- Content guidelines

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `MONGODB_URL` | MongoDB connection string | `mongodb://mongodb:27017` |
| `MONGODB_DB_NAME` | Database name | `chatbot_db` |
| `BACKEND_PORT` | Backend server port | `8000` |

---

## 🧪 Testing

### API Testing

Visit http://localhost:8000/docs for interactive API documentation.

**Test Endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Send a chat message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show all employees"}'
```

### Manual Testing Checklist

- [ ] Create new conversation
- [ ] Send messages and receive AI responses
- [ ] View conversation history
- [ ] Delete conversations
- [ ] Test table formatting (query for multiple employees)
- [ ] Test single employee queries
- [ ] Verify scrollbar functionality
- [ ] Test responsive design

---

## 📊 Technical Highlights

### Code Quality Improvements

During development, the codebase underwent significant architectural refactoring:

**Before Refactoring:**
- Monolithic route handlers (82+ lines)
- Global state anti-patterns
- Poor error handling
- Hardcoded configuration

**After Refactoring:**
- Clean architecture with DDD
- Repository pattern for data access
- Service layer for business logic
- Comprehensive error handling
- Externalized configuration
- **Code Quality Grade: C- → A-**

### Performance Considerations

- Async/await throughout for non-blocking I/O
- MongoDB indexing on frequently queried fields
- Efficient data loading and caching
- Optimized React rendering

---

## 🔐 Security Features

- ✅ Input validation on all endpoints
- ✅ Secure error handling (no internal details exposed)
- ✅ CORS configuration
- ✅ Environment-based secrets management
- ✅ Structured logging for audit trails

---

## 🚧 Future Enhancements

- [ ] User authentication and authorization
- [ ] Role-based access control
- [ ] Advanced analytics dashboard
- [ ] Export conversation history
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration with HR systems (SAP, Workday)
- [ ] Automated testing suite

---

## 📝 Development Notes

### Architecture Decisions

1. **Why Clean Architecture?**
   - Testability: Each layer can be tested independently
   - Maintainability: Clear separation of concerns
   - Scalability: Easy to add new features without breaking existing code

2. **Why MongoDB?**
   - Flexible schema for conversation data
   - Excellent performance for chat applications
   - Easy horizontal scaling

3. **Why Gemini AI?**
   - State-of-the-art language understanding
   - Cost-effective compared to alternatives
   - Fast response times

### Known Limitations

- Employee data is loaded from Excel file (not real-time database)
- No authentication (suitable for internal use only)
- Single-tenant architecture

---

## 👥 Contact & Support

**Developer:** Muskan Chawla  
**Project Type:** HRBP AI Assistant Prototype  
**Last Updated:** January 2026

---

## 📄 License

[Specify your license here]

---

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- FastAPI framework for excellent async support
- React community for component libraries
- MongoDB for reliable data persistence
