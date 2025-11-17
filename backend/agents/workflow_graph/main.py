"""
LangGraph workflow definition for medical multi-agent system
"""

import uuid
from typing import Dict, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from .state import AgentState
from .nodes import (
    receptionist_node,
    clinical_router_node,
    rag_node,
    web_search_node,
    clinical_response_node,
)
from utils.logger import log_workflow, logger


def should_route_to_clinical(state: AgentState) -> str:
    """
    Conditional edge: Route from receptionist to clinical or end
    """
    if state.get("needs_routing"):
        log_workflow("Routing to clinical agent")
        return "clinical_router"
    
    log_workflow("Conversation complete")
    return "end"


def should_use_rag_or_web(state: AgentState) -> str:
    """
    Conditional edge: Use EITHER RAG OR web search (never both)
    Priority: web_search > rag > direct response
    """
    if state.get("needs_web_search"):
        log_workflow("Using web search")
        return "web_search"
    elif state.get("needs_rag"):
        log_workflow("Using RAG")
        return "rag"
    else:
        log_workflow("Direct clinical response")
        return "clinical_response"


def create_workflow() -> StateGraph:
    """
    Create the medical agent workflow graph
    
    Returns:
        Compiled workflow graph
    """
    log_workflow("Creating medical agent workflow graph")
    
    # Initialize graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("receptionist", receptionist_node)
    workflow.add_node("clinical_router", clinical_router_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("clinical_response", clinical_response_node)
    
    # Set entry point
    workflow.set_entry_point("receptionist")
    
    # Add conditional edges from receptionist
    workflow.add_conditional_edges(
        "receptionist",
        should_route_to_clinical,
        {
            "clinical_router": "clinical_router",
            "end": END
        }
    )
    
    # Add conditional edges from clinical router - EITHER rag OR web, never both
    workflow.add_conditional_edges(
        "clinical_router",
        should_use_rag_or_web,
        {
            "rag": "rag",
            "web_search": "web_search",
            "clinical_response": "clinical_response"
        }
    )
    
    # RAG goes directly to clinical response (no web search after)
    workflow.add_edge("rag", "clinical_response")
    
    # Web search goes directly to clinical response
    workflow.add_edge("web_search", "clinical_response")
    
    # Clinical response goes to END
    workflow.add_edge("clinical_response", END)
    
    # Compile with memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    log_workflow("✓ Workflow graph compiled successfully")
    
    return app


class MedicalAgentSystem:
    """Main system for medical multi-agent interactions"""
    
    def __init__(self):
        self.workflow = create_workflow()
        log_workflow("Medical Agent System initialized")
    
    def process_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        patient_name: Optional[str] = None
    ) -> Dict:
        """
        Process a user message through the workflow
        
        Args:
            message: User message
            session_id: Session identifier (creates new if None)
            patient_name: Patient name if known
            
        Returns:
            Response dict with message and metadata
        """
        # Create or use session ID
        if not session_id:
            session_id = str(uuid.uuid4())
            log_workflow(f"New session created: {session_id}")
        
        try:
            config = {"configurable": {"thread_id": session_id}}
            
            # Check if we have existing state
            try:
                existing_state = self.workflow.get_state(config)
                has_state = existing_state and existing_state.values
            except:
                has_state = False
            
            # Prepare input - only new message for existing sessions
            if has_state:
                log_workflow(f"Continuing session {session_id}")
                input_data = {"messages": [HumanMessage(content=message)]}
            else:
                log_workflow(f"Starting new session {session_id}")
                input_data = {
                    "messages": [HumanMessage(content=message)],
                    "patient_name": patient_name,
                    "patient_data": None,
                    "current_agent": "receptionist",
                    "needs_routing": False,
                    "needs_rag": False,
                    "needs_web_search": False,
                    "rag_context": None,
                    "web_search_results": None,
                    "session_id": session_id,
                    "conversation_count": 0,
                    "error": None
                }
            
            # Run workflow
            result = self.workflow.invoke(input_data, config)
            
            # Extract response from last message
            last_message_obj = result["messages"][-1]
            last_message = last_message_obj.content if hasattr(last_message_obj, 'content') else str(last_message_obj)
            
            log_workflow(f"Session {session_id}: Response generated")
            
            return {
                "success": True,
                "message": last_message,
                "session_id": session_id,
                "agent": result.get("current_agent"),
                "patient_name": result.get("patient_name"),
                "metadata": {
                    "used_rag": bool(result.get("rag_context")),
                    "used_web_search": bool(result.get("web_search_results")),
                    "conversation_count": result.get("conversation_count", 0)
                }
            }
            
        except Exception as e:
            log_workflow(f"Error processing message: {e}", level="error")
            logger.exception(e)
            
            return {
                "success": False,
                "message": "I apologize, but I encountered an error. Please try again or contact support if the issue persists.",
                "session_id": session_id,
                "error": str(e)
            }
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """
        Retrieve conversation history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of messages
        """
        try:
            config = {"configurable": {"thread_id": session_id}}
            state = self.workflow.get_state(config)
            return state.values.get("messages", [])
        except Exception as e:
            log_workflow(f"Error retrieving history: {e}", level="error")
            return []


# Singleton instance
medical_system = MedicalAgentSystem()