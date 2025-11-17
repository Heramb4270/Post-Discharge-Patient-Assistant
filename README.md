# 🏥 Medical Assistant Chatbot

A comprehensive post-discharge patient care system powered by multi-agent architecture, RAG (Retrieval-Augmented Generation), and modern web technologies.

## 🌟 Features

### 🤖 Multi-Agent Architecture
- **Receptionist Agent**: Patient identification and query routing
- **Clinical Agent**: Medical question answering with RAG integration
- **Web Search Fallback**: Alternative information source when RAG confidence is low

### 📊 RAG-Powered Medical Knowledge
- **ChromaDB Vector Store**: Efficient medical document storage and retrieval
- **Similarity Scoring**: Cosine similarity threshold (1.5) for quality ontrol
- **Chunked Documents**: Optimized medical literature processing
- **Real-time Embeddings**: SentenceTransformer-based semantic search

### 🎯 Intelligent Query Processing
- **Intent Recognition**: Automatic classification of medical vs. general queries
- **Patient Context**: Personalized responses based on discharge data
- **Emergency Detection**: Critical symptom identification and escalation
- **Medication Guidance**: Drug interaction and dosage information

### 🖥️ User Interfaces
- **Streamlit Frontend**: Clean, medical-grade web interface
- **FastAPI Backend**: RESTful API with comprehensive endpoints
- **Real-time Chat**: Instant messaging with session persistence
- **Patient Dashboard**: Comprehensive medical record display

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Streamlit UI   │    │   FastAPI API   │    │   ChromaDB      │
│                 │◄──►│                 │◄──►│   Vector Store  │
│ - Chat Interface│    │ - Session Mgmt  │    │ - Medical Docs  │
│ - Patient Info  │    │ - Agent Router  │    │ - Embeddings    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Multi-Agents   │
                       │                 │
                       │ • Receptionist  │
                       │ • Clinical      │
                       │ • Web Search    │
                       └─────────────────┘
```

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
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env` file in project root:
```env
GOOGLE_API_KEY="your_google_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
```

### 4. Prepare Data
```bash
# Add your medical PDFs to backend/data/pdf_files/
# Patient data is already included in backend/data/patients_json_data/
```

### 5. Start Backend Server
```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 6. Frontend Setup
```bash
cd frontend
pip install streamlit requests plotly pandas numpy
streamlit run streamlit_frontend.py
```

### 7. Access Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
Python Multiagent Project/
├── backend/
│   ├── agents/
│   │   ├── receptionist_agent.py      # Patient identification & routing
│   │   ├── clinical_agent.py          # Medical Q&A with RAG
│   │   ├── rag_setup/                 # RAG components
│   │   │   ├── data_loader.py         # Document loading
│   │   │   ├── create_chunks.py       # Text chunking
│   │   │   ├── create_vector_store.py # ChromaDB integration
│   │   │   └── query_rag.py           # RAG orchestration
│   │   ├── tools/
│   │   │   └── patient_data_tool.py   # Patient lookup
│   │   └── web_search/
│   │       └── Duck_Duck_GO.py        # Web search fallback
│   ├── data/
│   │   ├── patients_json_data/        # Patient records
│   │   ├── pdf_files/                 # Medical literature
│   │   └── vector_store/              # ChromaDB storage
│   ├── utils/
│   │   └── data_generation.py         # Synthetic data generator
│   ├── server.py                      # FastAPI application
│   └── requirements.txt               # Python dependencies
├── frontend/
│   ├── streamlit_frontend.py          # Main UI application
│   ├── requirements.txt               # Frontend dependencies
├── .env                               # Environment variables
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

## 🔧 API Endpoints

### Chat & Messaging
- `POST /chat` - Send message to chatbot
- `GET /sessions/{session_id}` - Get session information
- `DELETE /sessions/{session_id}` - Clear session

### Patient Management
- `GET /patient/{name}` - Lookup patient by name
- `POST /patient/lookup` - Alternative patient search

### System Health
- `GET /health` - API health check
- `GET /api/stats` - Usage statistics
- `GET /` - API information

## 👥 Multi-Agent System

### Receptionist Agent
```python
# Features:
- Patient name identification
- Medical record retrieval
- Query intent classification
- Emergency situation detection
- Clinical agent routing
```

### Clinical Agent
```python
# Features:
- RAG-powered medical responses
- Similarity score evaluation (0.6 threshold)
- Web search fallback
- Patient context integration
- Citation and source tracking
```

### Web Search Agent
```python
# Features:
- DuckDuckGo search integration
- Medical query optimization
- Fallback for low RAG confidence
- Source attribution
```

## 🧠 RAG Implementation

### Vector Store Setup
```python
# ChromaDB with SentenceTransformer embeddings
- Model: all-MiniLM-L6-v2
- Chunk size: 10,000 characters
- Overlap: 200 characters
- Similarity threshold: 0.6
```

### Document Processing
```python
# Supported formats:
- PDF (PyMuPDF)
- TXT (TextLoader)
- CSV (CSVLoader)
- DOCX (Docx2txtLoader)
- JSON (JSONLoader)
```

## 🎯 Usage Examples

### Patient Identification
```
User: "John Smith"
System: "Hi John Smith! I found your discharge report dated 2024-01-15 
         for Chronic Kidney Disease Stage 3. How are you feeling today?"
```

### Medical Query
```
User: "I'm experiencing swelling in my legs"
System: [RAG-powered response with medical guidance and citations]
```

### Emergency Detection
```
User: "I have severe chest pain"
System: "🚨 EMERGENCY PROTOCOL ACTIVATED 🚨
         If this is life-threatening: Call 911 immediately..."
```

## 📊 Monitoring & Analytics

### Session Management
- Real-time session tracking
- Patient context persistence
- Message history storage
- Error logging and monitoring

### Performance Metrics
- API response times
- RAG similarity scores
- Query classification accuracy
- User interaction patterns

## 🔒 Security & Privacy

### Data Protection
- Session-based data isolation
- No persistent storage of conversations
- Patient data anonymization options
- HIPAA-compliant design patterns

### API Security
- CORS configuration for frontend
- Request timeout protection
- Error message sanitization
- Session expiration handling

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test/test_receiptionist.py
```

### API Testing
```bash
# Test endpoints using curl or Postman
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "John Smith", "session_id": "test123"}'
```

### Frontend Testing
```bash
cd frontend
streamlit run streamlit_frontend.py
# Navigate to http://localhost:8501
```

## 🚀 Deployment

### Production Setup
1. **Environment Variables**: Configure production API keys
2. **Database**: Replace in-memory storage with Redis/PostgreSQL
3. **Load Balancing**: Use Nginx for multiple backend instances
4. **HTTPS**: Configure SSL certificates
5. **Monitoring**: Add application performance monitoring

### Docker Deployment (Optional)
```dockerfile
# Example Dockerfile structure
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Install development dependencies
4. Run tests before submitting PR
5. Follow code style guidelines

### Code Standards
- Python: PEP 8 compliance
- Type hints for function signatures
- Comprehensive docstrings
- Error handling and logging
- Unit tests for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**Important Medical Disclaimer:**

This chatbot is designed for informational and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

- 🚨 **Emergency Situations**: Call 911 or go to the nearest emergency room
- 💊 **Medication Changes**: Consult your healthcare provider before making any changes
- 🩺 **Symptoms**: Persistent or severe symptoms require immediate medical attention
- 📋 **Treatment Decisions**: Never rely solely on this system for medical decisions

## 📞 Support & Contact

### Technical Support
- **Issues**: Create GitHub issues for bugs and feature requests
- **Documentation**: Check API docs at `/docs` endpoint
- **Community**: Join our discussion forums

### Emergency Medical Contacts
- **Emergency**: 911
- **Hospital**: (555) 123-4567
- **Nurse Hotline**: (555) 123-NURSE
- **Pharmacy**: (555) 123-PILLS

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Multi-agent architecture implementation
- ✅ RAG-powered medical knowledge base
- ✅ Streamlit frontend interface
- ✅ FastAPI backend with comprehensive endpoints
- ✅ Patient data management system
- ✅ Web search fallback mechanism
- ✅ Session management and persistence

### Planned Features (v1.1.0)
- 🔄 Enhanced analytics dashboard
- 🔄 Voice interface integration
- 🔄 Multilingual support
- 🔄 Mobile application
- 🔄 Advanced patient monitoring
- 🔄 Integration with hospital systems

---

**Built with ❤️ for improving post-discharge patient care**

*For questions, suggestions, or contributions, please reach out through GitHub issues or discussions.*
