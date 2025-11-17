# Medical Multi-Agent Workflow System

A complete LangGraph-based multi-agent system for post-discharge patient care with intelligent routing, RAG integration, and web search capabilities.

## System Architecture

```
User Query
    ↓
Receptionist Agent (Entry Point)
    ↓
[Conditional Routing]
    ↓
    ├─→ General Query? → Receptionist handles & END
    │
    └─→ Medical Concern? → Clinical Router
                              ↓
                    [Assess Query Needs]
                              ↓
                    ├─→ Need RAG? → RAG Node → Clinical Response
                    ├─→ Need Web Search? → Web Search → Clinical Response
                    └─→ Neither? → Clinical Response (direct)
                              ↓
                             END
```

## Components

### 1. State Management (`workflow_graph/state.py`)
- Manages conversation state across the workflow
- Tracks patient data, routing decisions, and context
- Handles RAG and web search results

### 2. Workflow Nodes (`workflow_graph/nodes.py`)

#### Receptionist Node
- **Purpose**: Initial patient interaction and general queries
- **Actions**: 
  - Retrieves patient data
  - Handles greetings and basic questions
  - Detects medical concerns for routing
- **Output**: Response + routing decision

#### Clinical Router Node
- **Purpose**: Determines what resources clinical agent needs
- **Actions**:
  - Analyzes query for medical keywords
  - Decides if RAG or web search is needed
- **Output**: Routing flags (needs_rag, needs_web_search)

#### RAG Node
- **Purpose**: Retrieves relevant medical knowledge
- **Actions**:
  - Queries vector store with user question
  - Fetches top-k relevant documents
- **Output**: Medical knowledge context

#### Web Search Node
- **Purpose**: Fetches current medical information
- **Actions**:
  - Performs DuckDuckGo search
  - Formats results for clinical agent
- **Output**: Web search results

#### Clinical Response Node
- **Purpose**: Generates final clinical response
- **Actions**:
  - Combines all available context
  - Uses LLM to generate evidence-based response
- **Output**: Final clinical answer

### 3. Workflow Graph (`workflow_graph/main.py`)

#### Conditional Edges

**`should_route_to_clinical()`**
- Checks if receptionist detected medical concern
- Routes to clinical or stays with receptionist

**`should_use_rag()`**
- Determines if medical knowledge needed
- Routes to RAG, web search, or direct response

**`should_use_web_search()`**
- After RAG, checks if web search also needed
- Routes to web search or clinical response

### 4. Medical Agent System

Main class that orchestrates the entire workflow:

```python
from agents.workflow_graph.main import medical_system

# Process a message
result = medical_system.process_message(
    message="I'm experiencing chest pain",
    session_id="user_123"
)

print(result['message'])  # Clinical response
print(result['agent'])    # Which agent handled it
print(result['metadata']) # Used RAG? Used web search?
```

## Workflow Flow Examples

### Example 1: General Query (Receptionist Only)
```
User: "What medications am I taking?"
  → Receptionist Node
  → Retrieves patient data
  → Responds with medication list
  → END
```

### Example 2: Medical Concern with RAG
```
User: "Tell me about side effects of my medication"
  → Receptionist Node (detects medical keywords)
  → Clinical Router (needs_rag = True)
  → RAG Node (retrieves drug information)
  → Clinical Response (combines patient data + RAG)
  → END
```

### Example 3: Latest Research with Web Search
```
User: "What are the latest post-surgery recovery guidelines?"
  → Receptionist Node (detects medical keywords)
  → Clinical Router (needs_web_search = True)
  → Web Search Node (fetches current info)
  → Clinical Response (combines context + web results)
  → END
```

### Example 4: Complex Query (RAG + Web Search)
```
User: "Latest research on medication interactions with my drugs"
  → Receptionist Node (detects medical keywords)
  → Clinical Router (needs_rag = True, needs_web_search = True)
  → RAG Node (retrieves drug interaction data)
  → Web Search Node (fetches latest research)
  → Clinical Response (combines all contexts)
  → END
```

## API Endpoints

### POST /chat
Process a chat message through the workflow

**Request:**
```json
{
  "message": "I'm experiencing chest pain",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I understand you're experiencing chest pain...",
  "session_id": "abc-123",
  "patient_name": "John Doe",
  "timestamp": "2024-11-17T10:30:00"
}
```

### GET /sessions/{session_id}
Get conversation history for a session

**Response:**
```json
{
  "session_id": "abc-123",
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ],
  "message_count": 2,
  "last_activity": "2024-11-17T10:30:00"
}
```

### GET /health
Health check endpoint

## Installation & Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables (.env):**
```env
GOOGLE_API_KEY=your_gemini_api_key
```

3. **Prepare data:**
- Add patient data to `backend/data/patients_json_data/patient_data.json`
- Add medical PDFs to `backend/data/pdf_files/`
- Run RAG setup if needed

4. **Start the server:**
```bash
cd backend
uvicorn server:app --reload
```

## Testing

Run the test script:
```bash
cd backend
python test_workflow.py
```

## Key Features

✅ **Intelligent Routing**: Automatically routes queries to appropriate agent
✅ **RAG Integration**: Retrieves relevant medical knowledge from vector store
✅ **Web Search**: Fetches current medical information when needed
✅ **State Management**: Maintains conversation context across messages
✅ **Memory Persistence**: LangGraph MemorySaver tracks session history
✅ **Comprehensive Logging**: Detailed logs for debugging and monitoring
✅ **Error Handling**: Graceful fallbacks at every level

## Workflow Advantages

1. **Conditional Routing**: Only uses expensive operations (RAG, web search) when needed
2. **Modular Design**: Each node has single responsibility
3. **Stateful Conversations**: Remembers context across messages
4. **Extensible**: Easy to add new nodes or routing logic
5. **Observable**: Comprehensive logging of all decisions and actions

## Troubleshooting

**Import errors:**
- Ensure you're running from `backend/` directory
- Check Python path includes project root

**LangGraph errors:**
- Verify `langgraph>=0.2.0` is installed
- Check state structure matches `AgentState` TypedDict

**RAG not working:**
- Ensure vector store exists in `backend/data/vector_store/`
- Run RAG setup if needed

**Agent not routing correctly:**
- Check medical keywords in agent classes
- Review conditional edge logic
- Enable debug logging

## File Structure

```
backend/
├── agents/
│   ├── receptionist_agent.py      # Handles greetings, general queries
│   ├── clinical_agent.py          # Medical response generation
│   ├── workflow_graph/
│   │   ├── state.py               # State management
│   │   ├── nodes.py               # All workflow nodes
│   │   ├── main.py                # Workflow creation & system class
│   │   └── __init__.py
│   ├── rag_setup/
│   │   └── query_rag.py           # RAG query function
│   └── web_search/
│       └── Duck_Duck_GO.py        # Web search function
├── utils/
│   └── logger.py                  # Logging utilities
├── server.py                      # FastAPI server
├── test_workflow.py               # Test script
└── data/
    ├── patients_json_data/        # Patient records
    ├── pdf_files/                 # Medical documents
    └── vector_store/              # Chroma DB vector store
```

## Contributing

To extend the workflow:

1. **Add a new node**: Create function in `nodes.py`
2. **Update state**: Add fields to `AgentState` in `state.py`
3. **Add to graph**: Register node in `create_workflow()`
4. **Add routing**: Create conditional edge function
5. **Test**: Add test case in `test_workflow.py`

## License

MIT License
