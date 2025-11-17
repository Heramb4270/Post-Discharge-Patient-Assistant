"""
Node functions for the medical agent workflow
"""

from typing import Dict, Any

from agents.receptionist_agent import ReceptionistAgent
from agents.clinical_agent import ClinicalAgent
from agents.rag_setup.query_rag import query_rag
from agents.web_search.Duck_Duck_GO import search_medical_info
from utils.logger import log_workflow, log_receptionist, log_clinical, log_tool
from .state import AgentState


# Initialize agents
receptionist_agent = ReceptionistAgent()
clinical_agent = ClinicalAgent()


def receptionist_node(state: AgentState) -> Dict[str, Any]:
    """
    Receptionist agent node - handles initial patient interaction
    """
    log_workflow("Entering receptionist node")
    
    # Get last message - handle LangGraph message objects
    messages = state["messages"]
    if messages:
        last_msg = messages[-1]
        last_message = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
    else:
        last_message = ""
    
    # Create session context
    session = {
        "patient_name": state.get("patient_name"),
        "patient_data": state.get("patient_data"),
        "session_id": state.get("session_id")
    }
    
    # Get chat history (convert LangGraph messages to simple format)
    chat_history = []
    for msg in messages[:-1]:
        if hasattr(msg, 'content'):
            role = "user" if msg.__class__.__name__ == "HumanMessage" else "assistant"
            chat_history.append({"role": role, "content": msg.content})
    
    # Process through receptionist
    result = receptionist_agent.process(
        message=last_message,
        session=session,
        chat_history=chat_history
    )
    
    log_receptionist(f"Response: {result['message'][:100]}...")
    
    # Update state - messages will be automatically converted by add_messages
    from langchain_core.messages import AIMessage
    
    updates = {
        "messages": [AIMessage(content=result["message"])],
        "current_agent": "receptionist",
        "needs_routing": result.get("needs_routing", False),
        "conversation_count": state.get("conversation_count", 0) + 1
    }
    
    # Update patient data if retrieved
    if "patient_data" in result and result["patient_data"] is not None:
        updates["patient_data"] = result["patient_data"]
        updates["patient_name"] = result["patient_data"].get("patient_name")
    
    # Set routing if needed
    if result.get("needs_routing"):
        log_workflow("Routing to clinical agent")
    
    return updates


def clinical_router_node(state: AgentState) -> Dict[str, Any]:
    """
    Clinical router node - determines if RAG or web search is needed
    """
    log_workflow("Entering clinical router node")
    
    # Get the ORIGINAL USER MESSAGE (not the receptionist's routing message)
    # The last message is from receptionist, we need the one before that (user's query)
    messages = state["messages"]
    
    # Find the last user message (HumanMessage)
    user_message = ""
    for msg in reversed(messages):
        if hasattr(msg, '__class__') and msg.__class__.__name__ == "HumanMessage":
            user_message = msg.content if hasattr(msg, 'content') else str(msg)
            break
    
    log_workflow(f"Analyzing user query for clinical needs: '{user_message[:50]}...'")
    
    # Determine what the clinical agent needs
    needs_assessment = clinical_agent.assess_query_needs(user_message)
    
    log_clinical(f"Needs assessment: RAG={needs_assessment['needs_rag']}, Web={needs_assessment['needs_web_search']}")
    
    # CRITICAL: Clear previous tool contexts to prevent contamination
    return {
        "current_agent": "clinical",
        "needs_rag": needs_assessment["needs_rag"],
        "needs_web_search": needs_assessment["needs_web_search"],
        "rag_context": None,
        "web_search_results": None
    }


def rag_node(state: AgentState) -> Dict[str, Any]:
    """
    RAG node - retrieves context from medical knowledge base
    """
    log_workflow("Entering RAG node")
    
    # Get the ORIGINAL USER MESSAGE
    messages = state["messages"]
    
    # Find the last user message (HumanMessage)
    user_message = ""
    for msg in reversed(messages):
        if hasattr(msg, '__class__') and msg.__class__.__name__ == "HumanMessage":
            user_message = msg.content if hasattr(msg, 'content') else str(msg)
            break
    
    log_workflow(f"Querying RAG for: '{user_message[:50]}...'")
    
    try:
        # Query RAG system
        rag_results = query_rag(user_message, top_k=3)
        
        # Format context
        context = "\n\n".join([
            f"Source {i+1}:\n{doc['content']}"
            for i, doc in enumerate(rag_results)
        ])
        
        log_tool("RAG", f"Retrieved {len(rag_results)} relevant documents")
        
        return {
            "rag_context": context
        }
        
    except Exception as e:
        log_tool("RAG", f"Error: {e}", level="error")
        return {
            "rag_context": None,
            "error": f"RAG error: {str(e)}"
        }


def web_search_node(state: AgentState) -> Dict[str, Any]:
    """
    Web search node - searches for current medical information
    """
    log_workflow("Entering web search node")
    
    # Get the ORIGINAL USER MESSAGE
    messages = state["messages"]
    
    # Find the last user message (HumanMessage)
    user_message = ""
    for msg in reversed(messages):
        if hasattr(msg, '__class__') and msg.__class__.__name__ == "HumanMessage":
            user_message = msg.content if hasattr(msg, 'content') else str(msg)
            break
    
    log_workflow(f"Web searching for: '{user_message[:50]}...'")
    
    try:
        # Perform web search
        search_results = search_medical_info(user_message, max_results=3)
        
        # Format results
        formatted_results = "\n\n".join([
            f"Source: {result['title']}\n{result['snippet']}\nURL: {result['url']}"
            for result in search_results
        ])
        
        log_tool("WEB_SEARCH", f"Found {len(search_results)} results")
        
        return {
            "web_search_results": formatted_results
        }
        
    except Exception as e:
        log_tool("WEB_SEARCH", f"Error: {e}", level="error")
        return {
            "web_search_results": None,
            "error": f"Web search error: {str(e)}"
        }


def clinical_response_node(state: AgentState) -> Dict[str, Any]:
    """
    Clinical response node - generates final clinical response
    """
    log_workflow("Entering clinical response node")
    
    # Get the ORIGINAL USER MESSAGE (not receptionist's routing message)
    messages = state["messages"]
    
    # Find the last user message (HumanMessage)
    user_message = ""
    for msg in reversed(messages):
        if hasattr(msg, '__class__') and msg.__class__.__name__ == "HumanMessage":
            user_message = msg.content if hasattr(msg, 'content') else str(msg)
            break
    
    log_workflow(f"Generating clinical response for: '{user_message[:50]}...'")
    
    # Prepare context
    context = {
        "patient_data": state.get("patient_data"),
        "rag_context": state.get("rag_context"),
        "web_search_results": state.get("web_search_results")
    }
    
    # Get chat history - convert LangGraph messages
    chat_history = []
    for msg in messages[:-1]:
        if hasattr(msg, 'content'):
            role = "user" if msg.__class__.__name__ == "HumanMessage" else "assistant"
            chat_history.append({"role": role, "content": msg.content})
    
    # Generate response
    response = clinical_agent.generate_response(
        query=user_message,
        context=context,
        chat_history=chat_history
    )
    
    log_clinical(f"Response generated: {response[:100]}...")
    
    from langchain_core.messages import AIMessage
    
    return {
        "messages": [AIMessage(content=response)],
        "current_agent": "clinical",
        "needs_routing": False,
        "conversation_count": state.get("conversation_count", 0) + 1
    }


def end_node(state: AgentState) -> Dict[str, Any]:
    """
    End node - marks conversation complete
    """
    log_workflow("Conversation complete")
    return {"current_agent": "end"}