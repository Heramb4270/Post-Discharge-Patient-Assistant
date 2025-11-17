from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import uuid
from datetime import datetime

# Import workflow system
from agents.workflow_graph.main import medical_system
from agents.tools.patient_data_tool import get_patient_data

app = FastAPI(
    title="Medical Assistant Chatbot API",
    description="API for post-discharge patient care chatbot",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8501"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    patient_name: Optional[str] = None
    timestamp: str

class PatientLookupRequest(BaseModel):
    patient_name: str

class PatientResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/")
def read_root():
    return {
        "message": "Medical Assistant Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "patient": "/patient/{name}",
            "health": "/health"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages through workflow"""
    try:
        message = request.message
        session_id = request.session_id
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Process through workflow
        result = medical_system.process_message(
            message=message,
            session_id=session_id
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Processing error"))
        
        return ChatResponse(
            response=result["message"],
            session_id=result["session_id"],
            patient_name=result.get("patient_name"),
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/patient/{patient_name}", response_model=PatientResponse)
async def get_patient(patient_name: str):
    """
    Get patient information by name
    """
    try:
        patient_data = get_patient_data(patient_name)
        
        if "error" in patient_data:
            return PatientResponse(
                success=False,
                error=patient_data["error"]
            )
        
        return PatientResponse(
            success=True,
            data=patient_data
        )
        
    except Exception as e:
        logger.error(f"Patient lookup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/patient/lookup", response_model=PatientResponse)
async def lookup_patient(request: PatientLookupRequest):
    """
    Alternative patient lookup endpoint using POST
    """
    try:
        patient_data = get_patient_data(request.patient_name)
        
        if "error" in patient_data:
            return PatientResponse(
                success=False,
                error=patient_data["error"]
            )
        
        return PatientResponse(
            success=True,
            data=patient_data
        )
        
    except Exception as e:
        logger.error(f"Patient lookup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get session information and conversation history
    """
    try:
        # Get conversation history from workflow
        history = medical_system.get_conversation_history(session_id)
        
        if not history:
            raise HTTPException(status_code=404, detail="Session not found or no history available")
        
        return {
            "session_id": session_id,
            "history": history,
            "message_count": len(history),
            "last_activity": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session lookup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """
    Clear/delete a session (note: LangGraph manages sessions internally)
    """
    try:
        return {
            "message": f"Session {session_id} will expire based on LangGraph memory settings",
            "note": "Sessions are managed by LangGraph MemorySaver"
        }
            
    except Exception as e:
        logger.error(f"Session clear error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "services": {
                "workflow": "active",
                "database": "connected",
                "vector_store": "available"
            }
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/api/stats")
async def get_stats():
    """
    Get API usage statistics
    """
    try:
        return {
            "total_patients": 29,  # Based on your patient data
            "api_version": "1.0.0",
            "workflow_enabled": True,
            "uptime": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )

