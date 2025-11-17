"""
Receptionist Agent
Handles patient greeting, data retrieval, and basic queries
"""

from agents.tools.patient_data_tool import get_patient_data
import logging
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from agents.prompts.receptionist_prompts import RECEPTIONIST_SYSTEM_PROMPT
load_dotenv()


class ReceptionistAgent:
    """Handles patient greeting and basic information retrieval"""
    
    def __init__(self):
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7
        )
        
        # Medical keywords for routing detection
        self.medical_keywords = [
            # Symptoms
            "pain", "swelling", "urine", "bp", "blood pressure", "breath", 
            "breathing", "fever", "nausea", "dizzy", "tired", "chest", "leg",
            "stomach", "headache", "side effect", "symptom", "feeling", "hurt",
            "worse", "emergency", "severe",
            # Medical information queries (for RAG/web search)
            "latest", "recent", "new", "current", "trend", "research", 
            "treatment", "medication", "drug", "therapy", "study", "guideline",
            "medical", "science", "recommendation", "update"
        ]
        
        logging.info("✓ Receptionist Agent initialized")
    
    def process(self, message: str, session: Dict, chat_history: List = None) -> Dict:
        """
        Process user message through receptionist agent
        
        Args:
            message: User input
            session: Session data containing patient info
            chat_history: Previous conversation history
            
        Returns:
            Agent response and metadata
        """
        try:
            logging.info(f"[RECEPTIONIST] Processing: {message[:50]}...")
            logging.info(f"[RECEPTIONIST] Session has patient_name: {'patient_name' in session}, patient_data: {'patient_data' in session}")
            
            # STEP 1: Check if patient data is loaded
            # Must check for BOTH patient_name AND patient_data
            if not session.get("patient_data"):
                logging.info(f"[RECEPTIONIST] No patient data, attempting to fetch for: {message}")
                # Try to get patient data with the message as name
                return self._handle_new_patient(message.strip(), session)
            
            # STEP 2: Patient is identified, now handle their query
            logging.info(f"[RECEPTIONIST] Patient {session.get('patient_name')} identified, handling query")
            
            # Check if medical concern needs routing
            needs_routing = self._check_medical_routing(message)
            
            if needs_routing:
                logging.info("[RECEPTIONIST] Medical concern detected, routing to clinical agent")
                return {
                    "agent": "receptionist",
                    "message": "I understand you have medical concerns. Let me connect you with our clinical specialist.",
                    "needs_routing": True,
                    "patient_data": session.get("patient_data")
                }
            
            # Handle general query with LLM
            response = self._handle_general_query(message, session.get("patient_data"), chat_history)
            
            return {
                "agent": "receptionist",
                "message": response,
                "needs_routing": False
            }
            
        except Exception as e:
            logging.error(f"[RECEPTIONIST] Error: {e}")
            return {
                "agent": "receptionist",
                "message": "I apologize, but I'm having trouble processing your request. Could you please rephrase that?",
                "error": str(e),
                "needs_routing": False
            }
    
    def _handle_new_patient(self, patient_name: str, session: Dict) -> Dict:
        """Handle initial patient identification and data retrieval"""
        patient_name = patient_name.strip()
        
        # If empty, ask for name
        if not patient_name:
            return {
                "agent": "receptionist",
                "message": "Hello! Please provide your full name so I can retrieve your patient records.",
                "needs_routing": False,
                "error": False
            }
        
        # Try to fetch patient data
        data = get_patient_data(patient_name)
        
        # If patient not found, ask again
        if "error" in data:
            logging.warning(f"[RECEPTIONIST] {data['error']} for '{patient_name}'")
            return {
                "agent": "receptionist",
                "message": f"I couldn't find a patient record for '{patient_name}'. Please enter your full name exactly as it appears in our system.",
                "needs_routing": False,
                "error": True
            }
        
        # Patient found! Store in session and display details
        session["patient_name"] = data["patient_name"]
        session["patient_data"] = data
        logging.info(f"[RECEPTIONIST] Retrieved data for {data['patient_name']}")
        
        # Format patient details nicely
        medications = '\n  - '.join(data.get('medications', []))
        
        greeting = f"""Hello {data['patient_name']}! I've found your record. Here's your discharge information:

📋 **Discharge Summary:**
- **Diagnosis:** {data.get('primary_diagnosis', 'N/A')}
- **Discharge Date:** {data.get('discharge_date', 'N/A')}
- **Medications:**
  - {medications}
- **Dietary Restrictions:** {data.get('dietary_restrictions', 'None')}
- **Follow-up:** {data.get('follow_up', 'Not scheduled')}
- **Warning Signs:** {data.get('warning_signs', 'None specified')}

How can I assist you today? Do you have any questions about your medications, recovery, or symptoms?"""
        
        return {
            "agent": "receptionist",
            "message": greeting,
            "needs_routing": False,
            "patient_data": data
        }
    
    def _handle_general_query(self, user_input: str, patient_data: Dict, chat_history: List = None) -> str:
        """Handle general queries using LLM"""
        try:
            # Build patient context
            patient_context = ""
            if patient_data:
                patient_context = f"""
Patient Information:
- Name: {patient_data.get('patient_name', 'Unknown')}
- Diagnosis: {patient_data.get('primary_diagnosis', 'Not available')}
- Discharge Date: {patient_data.get('discharge_date', 'Not available')}
- Medications: {', '.join(patient_data.get('medications', []))}
"""
            
            # Create prompt with context
            prompt = ChatPromptTemplate.from_messages([
                ("system", RECEPTIONIST_SYSTEM_PROMPT),
                ("system", patient_context),
                ("placeholder", "{chat_history}"),
                ("human", "{input}")
            ])
            
            # Create chain
            chain = prompt | self.llm | StrOutputParser()
            
            # Invoke chain
            response = chain.invoke({
                "input": user_input,
                "chat_history": chat_history or []
            })
            
            return response
            
        except Exception as e:
            logging.error(f"[RECEPTIONIST] LLM error: {e}")
            return self._generate_fallback_response(user_input, patient_data)
    
    def _check_medical_routing(self, message: str) -> bool:
        """Check if message contains medical keywords requiring clinical routing"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.medical_keywords)
    
    def _generate_fallback_response(self, user_input: str, patient_data: Dict) -> str:
        """Generate fallback response when LLM fails"""
        patient_name = patient_data.get("patient_name", "") if patient_data else ""
        return f"I'm here to help, {patient_name}. Could you please rephrase your question?"
