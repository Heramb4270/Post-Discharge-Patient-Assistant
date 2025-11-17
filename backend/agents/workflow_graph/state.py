"""
State management for the medical multi-agent workflow
"""

from typing import TypedDict, Annotated, List, Optional, Dict, Any
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State for the medical agent workflow"""
    
    # Conversation
    messages: Annotated[List[Dict[str, str]], add_messages]
    
    # Patient Information
    patient_name: Optional[str]
    patient_data: Optional[Dict[str, Any]]
    
    # Routing
    current_agent: str  # "receptionist" or "clinical"
    needs_routing: bool
    
    # Clinical specific
    needs_rag: bool
    needs_web_search: bool
    rag_context: Optional[str]
    web_search_results: Optional[str]
    
    # Metadata
    session_id: str
    conversation_count: int
    error: Optional[str]