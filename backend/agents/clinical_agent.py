"""
Clinical Agent with RAG and Web Search capabilities
"""

from typing import Dict, List, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from utils.logger import log_clinical
from agents.prompts.clinical_prompts import CLINICAL_SYSTEM_PROMPT

load_dotenv()



class ClinicalAgent:
    """Handles medical queries with RAG and web search"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )
        
        # Keywords that indicate need for RAG (medical queries)
        self.rag_keywords = [
            "medication", "drug", "side effect", "treatment", "procedure",
            "diagnosis", "condition", "disease", "surgery", "therapy",
            "pain", "swelling", "fever", "nausea", "vomiting", "diarrhea",
            "breathing", "shortness of breath", "chest pain", "headache",
            "dizzy", "fatigue", "tired", "symptom", "bleeding", "infection",
            "rash", "cough", "constipation", "wound", "incision"
        ]
        
        # Keywords that indicate need for web search (current info)
        self.web_keywords = [
            "latest", "recent", "new", "current", "update", "research",
            "study", "guideline", "recommendation"
        ]
        
        log_clinical("Clinical Agent initialized")
    
    def assess_query_needs(self, query: str) -> Dict[str, bool]:
        """
        Assess if query needs RAG or web search (NEVER both)
        Priority: web_search > rag
        
        Args:
            query: User query
            
        Returns:
            Dict with needs_rag and needs_web_search flags (only one will be True)
        """
        query_lower = query.lower()
        
        # Check for web search keywords first (higher priority)
        needs_web = any(keyword in query_lower for keyword in self.web_keywords)
        
        # Only check RAG if web search not needed
        if needs_web:
            needs_rag = False
        else:
            needs_rag = any(keyword in query_lower for keyword in self.rag_keywords)
        
        return {
            "needs_rag": needs_rag,
            "needs_web_search": needs_web
        }
    
    def generate_response(
        self,
        query: str,
        context: Dict[str, Any],
        chat_history: List = None
    ) -> str:
        """
        Generate clinical response with available context
        
        Args:
            query: User query
            context: Dict containing patient_data, rag_context, web_search_results
            chat_history: Previous conversation
            
        Returns:
            Clinical response
        """
        try:
            # Build context string
            context_parts = []
            source_info = ""
            
            if context.get("patient_data"):
                patient_info = context["patient_data"]
                meds = ', '.join(patient_info.get('medications', []))
                context_parts.append(
                    f"PATIENT INFORMATION:\n"
                    f"Name: {patient_info.get('patient_name')}\n"
                    f"Primary Diagnosis: {patient_info.get('primary_diagnosis')}\n"
                    f"Discharge Date: {patient_info.get('discharge_date')}\n"
                    f"Current Medications: {meds}\n"
                    f"Dietary Restrictions: {patient_info.get('dietary_restrictions', 'None')}\n"
                    f"Follow-up Appointment: {patient_info.get('follow_up', 'Not scheduled')}\n"
                    f"Warning Signs to Monitor: {patient_info.get('warning_signs', 'None')}\n"
                    f"Discharge Instructions: {patient_info.get('discharge_instructions', 'None')}"
                )
            
            # Check which tool was used and format accordingly
            if context.get("rag_context"):
                context_parts.append(f"MEDICAL KNOWLEDGE BASE (Use this and cite it):\n{context['rag_context']}")
                source_info = "\n\n---\n**Source:** Medical Knowledge Base (RAG)"
                log_clinical("Using RAG context in response")
            
            if context.get("web_search_results"):
                context_parts.append(f"RECENT MEDICAL RESEARCH (Use this and cite it):\n{context['web_search_results']}")
                source_info = "\n\n---\n**Source:** Recent Web Search Results"
                log_clinical("Using web search results in response")
            
            full_context = "\n\n".join(context_parts) if context_parts else "No additional context available."
            
            # Create prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", CLINICAL_SYSTEM_PROMPT),
                ("system", f"Context:\n{full_context}"),
                ("placeholder", "{chat_history}"),
                ("human", "{query}")
            ])
            
            # Generate response
            chain = prompt | self.llm
            response = chain.invoke({
                "query": query,
                "chat_history": chat_history or []
            })
            
            # Append source information if RAG or web search was used
            return response.content + source_info
            
        except Exception as e:
            log_clinical(f"Error generating response: {e}", level="error")
            return "I apologize, but I'm having difficulty processing your medical query. Please try rephrasing or contact your healthcare provider directly for urgent concerns."