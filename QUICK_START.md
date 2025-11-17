# Quick Start Guide - Medical Multi-Agent Workflow

## Overview
This system uses LangGraph to route patient queries between a receptionist agent and a clinical agent, with automatic RAG and web search integration.

## Prerequisites
- Python 3.8+
- Google Gemini API key

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Verify Installation
```bash
cd backend
python workflow_diagram.py
```

## Running the System

### Option 1: Test the Workflow
```bash
cd backend
python test_workflow.py
```

This will run 5 test cases demonstrating:
- Patient greeting and data retrieval
- General queries (receptionist only)
- Medical concerns (routing to clinical)
- RAG-based queries
- Web search queries

### Option 2: Start the API Server
```bash
cd backend
uvicorn server:app --reload
```

Server will start at: `http://localhost:8000`

### Option 3: Use the System Programmatically
```python
from agents.workflow_graph.main import medical_system

# Process a message
result = medical_system.process_message(
    message="I'm experiencing chest pain",
    session_id="user_123"
)

print(result['message'])
print(f"Agent used: {result['agent']}")
print(f"Used RAG: {result['metadata']['used_rag']}")
print(f"Used Web Search: {result['metadata']['used_web_search']}")
```

## Testing the API

### Using cURL

**Send a message:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Noah Bennett",
    "session_id": "test123"
  }'
```

**Get conversation history:**
```bash
curl http://localhost:8000/sessions/test123
```

**Health check:**
```bash
curl http://localhost:8000/health
```

### Using Python requests
```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "I'm experiencing chest pain",
        "session_id": "user123"
    }
)

print(response.json())
```

## How It Works

### Flow 1: General Query (No Medical Concern)
```
User: "What medications am I taking?"
→ Receptionist retrieves patient data
→ Receptionist responds
→ END
```

### Flow 2: Medical Query with RAG
```
User: "Tell me about side effects of my medication"
→ Receptionist detects medical keywords
→ Routes to Clinical Router
→ Clinical Router triggers RAG
→ RAG retrieves drug information
→ Clinical Response combines context
→ END
```

### Flow 3: Latest Research Query
```
User: "What are the latest post-surgery guidelines?"
→ Receptionist detects medical keywords
→ Routes to Clinical Router
→ Clinical Router triggers Web Search
→ Web Search fetches current info
→ Clinical Response uses web results
→ END
```

## Key Features

✅ **Automatic Routing**: Detects medical concerns automatically
✅ **Smart Resource Usage**: Only uses RAG/web search when needed
✅ **Conversation Memory**: Maintains context across messages
✅ **Patient Data Integration**: Retrieves and uses patient records
✅ **Comprehensive Logging**: All actions are logged

## Monitoring & Debugging

### View Logs
```bash
# Real-time logs
tail -f backend/logs/medical_system_$(date +%Y%m%d).log

# Error logs only
tail -f backend/logs/errors_$(date +%Y%m%d).log
```

### Enable Debug Logging
Edit `backend/utils/logger.py`:
```python
logger = setup_logger(level=logging.DEBUG)
```

## Common Issues

### Import Errors
**Problem**: `ModuleNotFoundError: No module named 'agents'`
**Solution**: Ensure you're running from the `backend/` directory

### LangGraph Errors
**Problem**: `AttributeError: 'StateGraph' object has no attribute...`
**Solution**: Update langgraph: `pip install --upgrade langgraph`

### RAG Not Working
**Problem**: RAG returns empty results
**Solution**: 
1. Check if vector store exists: `ls backend/data/vector_store/`
2. If empty, run RAG setup to create vector store

### Agent Not Routing
**Problem**: Clinical agent not being called
**Solution**: Check medical keywords in `receptionist_agent.py`

## Next Steps

1. **Customize Keywords**: Edit medical keywords in agent files
2. **Add More Nodes**: Extend workflow in `workflow_graph/nodes.py`
3. **Improve Prompts**: Update system prompts in `prompts/` directory
4. **Add More Data**: Add PDFs to `data/pdf_files/` for better RAG
5. **Deploy**: Use gunicorn/nginx for production deployment

## File Locations

- **Workflow**: `backend/agents/workflow_graph/`
- **Agents**: `backend/agents/receptionist_agent.py`, `clinical_agent.py`
- **Server**: `backend/server.py`
- **Tests**: `backend/test_workflow.py`
- **Logs**: `backend/logs/`
- **Data**: `backend/data/`

## Support

For detailed documentation, see `WORKFLOW_README.md`

For visual workflow diagram:
```bash
python backend/workflow_diagram.py
```

## Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chat` | POST | Send chat message |
| `/sessions/{id}` | GET | Get conversation history |
| `/patient/{name}` | GET | Lookup patient data |
| `/health` | GET | Health check |
| `/api/stats` | GET | System statistics |

## Example Session

```python
from agents.workflow_graph.main import medical_system

# Session 1: Patient greeting
r1 = medical_system.process_message("Noah Bennett", "session1")
# → Receptionist greets and retrieves patient data

# Session 1: General question
r2 = medical_system.process_message("What are my medications?", "session1")
# → Receptionist responds with medication list

# Session 1: Medical concern
r3 = medical_system.process_message("I have chest pain", "session1")
# → Routes to Clinical → Uses RAG → Provides medical guidance
```

Happy coding! 🚀
