# 🏥 Post-Discharge Patient Assistant

A comprehensive post-discharge patient care system powered by **LangGraph multi-agent workflows**, **RAG (Retrieval-Augmented Generation)**, and **Google Gemini AI**.

## 🌟 Features

### 🤖 LangGraph Multi-Agent Workflow
- **Receptionist Agent**: Patient identification, data retrieval, and intelligent query routing
- **Clinical Agent**: Medical question answering with RAG and web search capabilities
- **Workflow Orchestration**: State-based graph with conditional routing and session persistence
- **Memory Management**: Conversation history maintained across sessions using MemorySaver

### 📊 RAG-Powered Medical Knowledge
- **ChromaDB Vector Store**: Efficient medical document storage and retrieval from comprehensive clinical nephrology PDFs
- **Semantic Search**: SentenceTransformer (all-MiniLM-L6-v2) embeddings for accurate document matching
- **Smart Chunking**: Optimized text processing with overlap for context preservation
- **Citation Tracking**: Automatic source attribution in medical responses

### 🎯 Intelligent Query Processing
- **Keyword-Based Routing**: Automatic detection of medical symptoms and research queries
- **Mutual Exclusivity**: RAG for symptoms, Web search for latest trends/research
- **Patient Context**: Personalized responses based on discharge summaries and medications
- **State Isolation**: Clean context per query to prevent tool result contamination

### 🖥️ User Interfaces
- **Streamlit Frontend**: Clean, medical-grade web interface with session management
- **FastAPI Backend**: RESTful API with CORS support for seamless frontend integration
- **Real-time Chat**: Instant messaging with thread-based session persistence
- **Patient Dashboard**: Comprehensive medical record display including medications and warnings

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Streamlit UI   │    │   FastAPI API   │    │   ChromaDB      │
│                 │◄──►│                 │◄──►│   Vector Store  │
│ - Chat Interface│    │ - Thread Mgmt   │    │ - Medical PDFs  │
│ - Patient Info  │    │ - LangGraph     │    │ - Embeddings    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   LangGraph Workflow    │
                    │                         │
                    │  ┌───────────────────┐  │
                    │  │  Receptionist     │  │
                    │  │  - ID Patient     │  │
                    │  │  - Route Query    │  │
                    │  └─────────┬─────────┘  │
                    │            │             │
                    │  ┌─────────▼─────────┐  │
                    │  │  Clinical Router  │  │
                    │  │  - Assess Needs   │  │
                    │  └─────┬──────┬──────┘  │
                    │        │      │          │
                    │   ┌────▼──┐ ┌▼─────┐    │
                    │   │  RAG  │ │ Web  │    │
                    │   │ Node  │ │Search│    │
                    │   └────┬──┘ └┬─────┘    │
                    │        │     │           │
                    │   ┌────▼─────▼──────┐   │
                    │   │ Clinical Response│   │
                    │   │ - Generate Reply │   │
                    │   └──────────────────┘   │
                    └─────────────────────────┘
```

## 🔄 Workflow Logic

### Patient Identification Flow
1. User sends message → Receptionist checks if patient data exists
2. If no patient data: Request name until valid patient found
3. If patient found: Display full discharge summary with medications
4. Route medical queries to Clinical Agent

### Clinical Query Flow
1. **Receptionist**: Detects medical keywords (symptoms, treatments, research terms)
2. **Clinical Router**: Analyzes query to determine tool needs
   - **Symptoms** (pain, swelling, fever) → RAG search
   - **Research** (latest, trends, new treatments) → Web search
   - **NEVER BOTH** - Mutually exclusive to prevent context contamination
3. **Tool Execution**: RAG or Web search retrieves relevant information
4. **Clinical Response**: Generates answer with citations and source attribution
5. **End**: Conversation complete, ready for next query

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment support
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd "Python Multiagent Project"
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

### 3. Environment Configuration
Create `.env` file in project root:
```env
GOOGLE_API_KEY="your_google_gemini_api_key_here"
```

### 4. Initialize RAG System (First Time Only)
```bash
cd backend
# Place your medical PDFs in data/pdf_files/
python agents/rag_setup/create_chunks.py
python agents/rag_setup/create_embeddings.py
python agents/rag_setup/create_vector_store.py
# Patient data (patient_data.json) is already included with 29 sample patients
```

### 5. Start Backend Server
```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 6. Frontend Setup (New Terminal)
```bash
cd frontend
streamlit run streamlit_frontend.py
```

### 7. Access Application
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
Python Multiagent Project/
├── backend/
│   ├── agents/
│   │   ├── receptionist_agent.py      # Patient ID & routing
│   │   ├── clinical_agent.py          # Medical Q&A logic
│   │   ├── prompts/
│   │   │   ├── receptionist_prompts.py # System prompts
│   │   │   └── clinical_prompts.py     # Clinical prompts
│   │   ├── rag_setup/                 # RAG components
│   │   │   ├── data_loader.py         # PDF/document loading
│   │   │   ├── create_chunks.py       # Text chunking
│   │   │   ├── create_embeddings.py   # Embedding generation
│   │   │   ├── create_vector_store.py # ChromaDB setup
│   │   │   └── query_rag.py           # RAG query interface
│   │   ├── tools/
│   │   │   ├── patient_data_tool.py   # Patient JSON lookup
│   │   │
│   │   ├── web_search/
│   │   │   └── Duck_Duck_GO.py        # DuckDuckGo integration
│   │   └── workflow_graph/            # LangGraph workflow
│   │       ├── main.py                # Workflow definition
│   │       ├── nodes.py               # Node implementations
│   │       └── state.py               # State schema
│   ├── data/
│   │   ├── patients_json_data/
│   │   │   └── patient_data.json      # 29 patient records
│   │   ├── pdf_files/                 # Medical literature
│   │   ├── chunks/                    # Processed text chunks
│   │   └── vector_store/              # ChromaDB storage
│   ├── utils/
│   │   ├── logger.py                  # Custom logging
│   │   └── patient_data_generation.py # Sample data generator
│   ├── server.py                      # FastAPI application
│   └── test_workflow.py               # Workflow testing
├── frontend/
│   └── streamlit_frontend.py          # Streamlit UI
├── requirements.txt                   # All dependencies
├── .env                               # API keys
├── .gitignore                         # Git exclusions
├── README.md                          # This file


## 🔧 API Endpoints

### Chat & Messaging
- `POST /chat` - Send message to chatbot (requires `message` and `session_id`)
  ```json
  {
    "message": "I'm experiencing swelling in my legs",
    "session_id": "user-unique-id"
  }
  ```
- `GET /sessions/{session_id}` - Get session state and history
- `DELETE /sessions/{session_id}` - Clear session data

### Patient Management
- `GET /patient/{name}` - Lookup patient by exact name match
  - Returns patient data, medications, warnings, follow-up info

### System Health
- `GET /health` - API health check
- `GET /` - API welcome message

## 👥 Multi-Agent System Details

### Receptionist Agent
**Purpose**: Patient identification and query routing

**Workflow**:
1. Check if patient data exists in session
2. If not: Request patient name and search `patient_data.json`
3. If found: Display full discharge summary with:
   - Primary diagnosis
   - Medications and dosages
   - Dietary restrictions
   - Follow-up appointments
   - Warning signs to monitor
4. Detect medical keywords in user queries
5. Route to Clinical Agent if medical assistance needed

**Medical Keywords Detected**:
- Symptoms: pain, swelling, fever, nausea, headache, dizzy, bleeding, etc.
- Research: latest, trends, new, current, treatment, medication, study, guideline, etc.

### Clinical Agent
**Purpose**: Medical question answering with RAG and web search

**Workflow**:
1. **Query Assessment** (`assess_query_needs()`):
   - Check for symptom keywords → `needs_rag=True`
   - Check for research keywords → `needs_web_search=True`
   - Priority: Web search > RAG (never both simultaneously)

2. **Tool Execution**:
   - **RAG**: Query ChromaDB for medical knowledge from PDFs
   - **Web Search**: Search DuckDuckGo for latest medical information

3. **Response Generation** (`generate_response()`):
   - Use Google Gemini 2.5-flash (temperature=0.3 for accuracy)
   - Include patient context (medications, warnings, diagnosis)
   - Cite sources with footer attribution
   - Append source information:
     - "Source: Medical Knowledge Base (Clinical Nephrology)" for RAG
     - "Source: Recent Web Search Results" for web search

**Key Features**:
- Context-aware responses based on patient's discharge data
- Automatic citation of information sources
- Symptom-specific guidance aligned with patient's condition
- Research query handling for latest medical developments

### LangGraph Workflow Nodes

**Node Functions** (in `workflow_graph/nodes.py`):
1. `receptionist_node`: Patient interaction and routing decision
2. `clinical_router_node`: Query assessment and context clearing
3. `rag_node`: Medical knowledge retrieval from vector store
4. `web_search_node`: DuckDuckGo search execution
5. `clinical_response_node`: Final response generation with citations
6. `end_node`: Workflow termination

**Conditional Routing** (in `workflow_graph/main.py`):
- `should_route_to_clinical()`: Check if medical query detected
- `should_use_rag_or_web()`: Route to RAG, web search, or response node

**State Management**:
- `AgentState`: TypedDict with messages, patient_data, routing flags
- `MemorySaver`: Persistent checkpointer for conversation history
- Thread-based sessions for multi-user support

## 🧠 RAG Implementation

### Vector Store Configuration
```python
# ChromaDB with SentenceTransformer embeddings
Embedding Model: all-MiniLM-L6-v2
Vector Store: ChromaDB (persistent storage)
Collection: medical_documents
Distance Metric: Cosine similarity
```

### Document Processing Pipeline
```python
1. Load PDF files from data/pdf_files/
2. Extract text using PyMuPDF (fitz)
3. Split into chunks (size: 1000 chars, overlap: 200 chars)
4. Generate embeddings using SentenceTransformer
5. Store in ChromaDB vector database
6. Query with semantic search (top_k=3 results)
```

### Supported Document Formats
- **PDF**: Medical textbooks, clinical guidelines (PyMuPDF)
- **TXT**: Plain text medical documents
- **JSON**: Structured medical data
- **CSV**: Tabular medical information

### Query Process
```python
# Example: User asks "I have swelling in my legs"
1. Extract query from user message
2. Generate embedding for query
3. Search ChromaDB for top 3 similar documents
4. Retrieve relevant medical text chunks
5. Pass to LLM with patient context
6. Generate response with citations
```

## 🎯 Usage Examples

### Example 1: Patient Identification
```
👤 User: "hello"
🤖 System: "I couldn't find a patient record for 'hello'. 
           Please enter your full name exactly as it appears in our system."

👤 User: "John Smith"
🤖 System: "Hello John Smith! I've found your record. 
           Here's your discharge information:

           📋 Discharge Summary:
           - Diagnosis: Chronic Kidney Disease Stage 3
           - Discharge Date: 2024-01-15
           - Medications:
             • Lisinopril 10mg daily
             • Furosemide 20mg twice daily
           - Dietary Restrictions: Low sodium (2g/day), fluid restriction (1.5L/day)
           - Follow-up: Nephrology clinic in 2 weeks
           - Warning Signs: Swelling, shortness of breath, decreased urine output
           
           How can I assist you today?"
```

### Example 2: Symptom Query (RAG)
```
👤 User: "I'm experiencing swelling in my legs"
🤖 System: "Thank you for letting me know, John. Swelling in your leg is 
           an important symptom to pay attention to, especially with your 
           diagnosis of Chronic Kidney Disease Stage 3.
           
           According to your discharge instructions, swelling is one of 
           the key warning signs you need to monitor...
           
           [Detailed medical guidance based on RAG context]
           
           ---
           Source: Medical Knowledge Base (Clinical Nephrology)"
```

### Example 3: Research Query (Web Search)
```
👤 User: "what are the latest trends in medical science"
🤖 System: "That's a great question, John! Staying informed about 
           advancements in medical science is very important.
           
           Based on current research, some of the latest trends are:
           • Technological Advancements in Medical Devices
           • Breakthroughs in diagnostics and treatments
           • AI integration in healthcare delivery
           
           [Detailed information from web search]
           
           ---
           Source: Recent Web Search Results"
```

### Example 4: Multiple Symptom Tracking
```
👤 User: "I'm having pain in my abdomen"
🤖 System: [RAG-powered response with specific guidance based on 
           patient's condition and medical knowledge base]
           
           ---
           Source: Medical Knowledge Base (Clinical Nephrology)"
```

## 📊 Key Technologies

### Backend Stack
- **LangGraph**: Workflow orchestration with state management
- **LangChain**: LLM integration and message handling
- **Google Gemini**: AI model (gemini-2.0-flash-exp)
  - Receptionist: Temperature 0.7 (conversational)
  - Clinical: Temperature 0.3 (accurate medical responses)
- **ChromaDB**: Vector database for semantic search
- **SentenceTransformers**: Text embeddings (all-MiniLM-L6-v2)
- **FastAPI**: High-performance async web framework
- **Uvicorn**: ASGI server

### Frontend Stack
- **Streamlit**: Interactive web UI framework
- **Requests**: HTTP client for backend communication
- **Session State**: User session persistence

### Data & Storage
- **JSON**: Patient records (29 sample patients)
- **PDF**: Medical knowledge base (comprehensive-clinical-nephrology.pdf)
- **ChromaDB**: Persistent vector store
- **MemorySaver**: LangGraph checkpoint storage

## 🧪 Testing

### Backend Workflow Testing
```bash
cd backend
python test_workflow.py
# Tests the complete LangGraph workflow with sample queries
```

### API Testing with cURL
```bash
# Health check
curl http://localhost:8000/health

# Patient lookup
curl http://localhost:8000/patient/John%20Smith

# Chat interaction
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have swelling in my legs",
    "session_id": "test-session-123"
  }'
```

### Frontend Testing
```bash
cd frontend
streamlit run streamlit_frontend.py
# Navigate to http://localhost:8501
# Test patient identification and medical queries
```

### Testing Workflow Routing
```python
# Test RAG routing (symptoms)
Input: "I have pain in my abdomen"
Expected: RAG node → Medical Knowledge Base citation

# Test Web Search routing (research)
Input: "what are the latest trends in nephrology"
Expected: Web search node → Recent Web Search Results citation

# Test patient data retrieval
Input: "Mary Thompson"
Expected: Full discharge summary display
```

## 🔒 Security & Privacy

### Data Protection
- **Session Isolation**: Thread-based sessions prevent data leakage between users
- **No Persistent Chat Storage**: Conversations cleared when session ends
- **Local Data**: Patient data and vector store stored locally (not cloud)
- **API Key Security**: Environment variables for sensitive credentials

### Privacy Considerations
- Patient data is sample/synthetic for demonstration
- Production deployment should implement:
  - Encrypted database connections
  - HIPAA-compliant data handling
  - Audit logging for medical data access
  - User authentication and authorization

## 🚀 Production Deployment Considerations

### Performance Optimization
- **Caching**: Implement Redis for session state
- **Load Balancing**: Nginx for multiple backend instances
- **Database**: Replace JSON with PostgreSQL for patient data
- **Vector Store**: Consider Pinecone or Weaviate for scalability

### Security Hardening
- **HTTPS**: SSL/TLS certificates (Let's Encrypt)
- **Authentication**: OAuth2/JWT for user sessions
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize all user inputs

### Monitoring & Logging
- **Application Monitoring**: Prometheus + Grafana
- **Error Tracking**: Sentry for exception monitoring
- **Audit Logs**: Track all medical data access
- **Performance Metrics**: Response times, query accuracy

### Docker Deployment Example
```dockerfile
# Backend Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - ./backend/data:/app/data
  
  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (see Testing section)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards
- **Python**: PEP 8 compliance, type hints for functions
- **Docstrings**: Google-style docstrings for all functions/classes
- **Error Handling**: Try-except blocks with proper logging
- **Testing**: Unit tests for new features
- **Logging**: Use `utils/logger.py` for consistent logging

### Areas for Contribution
- 🎯 Additional medical knowledge sources (more PDFs)
- 🎯 Improved symptom detection algorithms
- 🎯 Enhanced patient data schema
- 🎯 UI/UX improvements
- 🎯 Performance optimizations
- 🎯 Documentation improvements
- 🎯 Test coverage expansion

## 📚 Additional Documentation

- **IMPLEMENTATION_SUMMARY.md**: Detailed development notes and architecture decisions
- **QUICK_START.md**: Quick reference guide for common tasks
- **WORKFLOW_README.md**: LangGraph workflow diagram and flow details
- **API Docs**: Available at http://localhost:8000/docs when server is running

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'langchain_google_genai'`
```bash
# Solution: Install all dependencies
pip install -r requirements.txt
```

**Issue**: ChromaDB initialization error
```bash
# Solution: Recreate vector store
cd backend
python agents/rag_setup/create_vector_store.py
```

**Issue**: "Patient not found" even with correct name
```bash
# Solution: Check exact name in patient_data.json (case-sensitive)
# Available patients: John Smith, Mary Thompson, Carlos Rivera, etc.
```

**Issue**: Web search not triggering
```bash
# Solution: Use research keywords like "latest", "trends", "new", "current"
# Example: "what are the latest treatments for kidney disease"
```

**Issue**: No citations in responses
```bash
# Solution: Ensure clinical_prompts.py has citation requirements
# Check that clinical_agent.py appends source footer
```

**Issue**: Backend server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process: kill -9 <PID>
# Or use different port: uvicorn server:app --port 8001
```

## 📞 Support & Contact

### Technical Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community Q&A and general discussions
- **Documentation**: Check `/docs` endpoint and additional markdown files

### Project Links
- **Repository**: https://github.com/Heramb4270/Post-Discharge-Patient-Assistant
- **API Docs**: http://localhost:8000/docs (when running)

## ⚠️ Medical Disclaimer

**CRITICAL NOTICE - READ CAREFULLY:**

This chatbot is designed **STRICTLY for informational and educational purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.

### Important Warnings:

- 🚨 **EMERGENCIES**: For life-threatening emergencies (chest pain, difficulty breathing, severe bleeding, stroke symptoms), call 911 immediately or go to the nearest emergency room. DO NOT rely on this chatbot.

- 💊 **MEDICATIONS**: Never start, stop, or change medications without consulting your healthcare provider. This system provides information only, not prescriptions.

- 🩺 **DIAGNOSIS**: This chatbot cannot diagnose medical conditions. Only licensed healthcare providers can provide accurate diagnoses.

- 📋 **TREATMENT DECISIONS**: All medical decisions should be made in consultation with qualified healthcare professionals who have access to your complete medical history.

- ⚕️ **PROFESSIONAL CARE**: Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

### Legal Disclaimer:
- The information provided is based on general medical knowledge and may not apply to your specific situation
- AI-generated responses may contain errors or inaccuracies
- This system is a demonstration project and should not be used for actual patient care without proper medical oversight
- The developers assume no liability for any harm resulting from use of this system

**If you are experiencing a medical emergency, hang up and call 911 immediately.**

## 🔄 Version History & Implementation Notes

### v1.0.0 (Current - Production Ready)
- ✅ LangGraph multi-agent workflow with state management
- ✅ Google Gemini 2.0 Flash integration
- ✅ RAG-powered medical knowledge base (ChromaDB)
- ✅ DuckDuckGo web search for latest medical information
- ✅ Streamlit frontend with session persistence
- ✅ FastAPI backend with comprehensive endpoints
- ✅ Patient data management (29 sample patients)
- ✅ Citation and source attribution
- ✅ Mutually exclusive RAG/Web search routing
- ✅ Context isolation to prevent tool contamination

### Key Implementation Details
1. **State Persistence**: MemorySaver checkpointer maintains conversation history
2. **Message Extraction**: All clinical nodes extract last HumanMessage to avoid analyzing routing messages
3. **Context Clearing**: Clinical router clears previous tool contexts before new queries
4. **Keyword Routing**: 
   - Symptoms → RAG (pain, swelling, fever, nausea, etc.)
   - Research → Web Search (latest, trends, new, current, etc.)
5. **Source Attribution**: Automatic footer appended to responses:
   - RAG: "Source: Medical Knowledge Base (Clinical Nephrology)"
   - Web: "Source: Recent Web Search Results"

### Planned Features (v1.1.0)
- 🔄 Multi-language support (Spanish, Hindi, Mandarin)
- 🔄 Voice interface integration
- 🔄 Enhanced analytics dashboard
- 🔄 Mobile-responsive UI improvements
- 🔄 Integration with EHR systems (HL7 FHIR)
- 🔄 Medication interaction checker
- 🔄 Appointment scheduling integration
- 🔄 SMS/Email notification system

---

## 📝 License

This project is licensed under the MIT License.

---

**Built with ❤️ for improving post-discharge patient care**

**Technologies**: LangGraph • Google Gemini • ChromaDB • FastAPI • Streamlit

*For questions, suggestions, or contributions, please open a GitHub issue or discussion.*

---

### Quick Commands Reference

```bash
# Start backend server
cd backend && uvicorn server:app --reload --port 8000

# Start frontend
cd frontend && streamlit run streamlit_frontend.py

# Run tests
cd backend && python test_workflow.py

# Rebuild vector store
cd backend && python agents/rag_setup/create_vector_store.py

# Check health
curl http://localhost:8000/health
```

**Last Updated**: November 2025
