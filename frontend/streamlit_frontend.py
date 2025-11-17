import streamlit as st
import requests
import json
from datetime import datetime
import uuid
from typing import Dict, Any, Optional

# Configure the page
st.set_page_config(
    page_title="Medical Assistant Chatbot",
    page_icon="🏥",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

class MedicalChatbotAPI:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def send_message(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to the chatbot"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": message,
                    "session_id": session_id
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to API. Please ensure the backend server is running."}
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
    
    def get_patient(self, patient_name: str) -> Dict[str, Any]:
        """Get patient information"""
        try:
            response = requests.get(
                f"{self.base_url}/patient/{patient_name}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "unhealthy", "error": str(e)}

# Initialize API client
@st.cache_resource
def get_api_client():
    return MedicalChatbotAPI()

# Initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "patient_data" not in st.session_state:
        st.session_state.patient_data = None

def main():
    initialize_session_state()
    api = get_api_client()
    
    # Simple CSS with proper text colors
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .patient-card {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #2E8B57;
        margin: 1rem 0;
        color: #000000;
    }
    
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #2196f3;
        color: #000000;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #9c27b0;
        color: #000000;
    }
    
    .status-card {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #000000;
    }
    
    .status-healthy {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    
    .status-unhealthy {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">🏥 Medical Assistant Chatbot</div>', unsafe_allow_html=True)
    st.markdown("### Simple Post-Discharge Care Assistant")
    
    # Check API Status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Check API Status"):
            health = api.health_check()
            status = health.get("status", "unknown")
            if status == "healthy":
                st.markdown('<div class="status-card status-healthy">✅ API Status: Healthy</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-card status-unhealthy">❌ API Status: Unhealthy</div>', unsafe_allow_html=True)
    
    with col2:
        st.write(f"**Session:** {st.session_state.session_id[:8]}...")
    
    with col3:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.patient_data = None
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
    
    st.markdown("---")
    
    # Patient Information
    if st.session_state.patient_data:
        patient = st.session_state.patient_data
        st.markdown(f"""
        <div class="patient-card">
            <h4>👤 Patient: {patient.get('patient_name', 'Unknown')}</h4>
            <p><strong>Diagnosis:</strong> {patient.get('primary_diagnosis', 'N/A')}</p>
            <p><strong>Discharge Date:</strong> {patient.get('discharge_date', 'N/A')}</p>
            <p><strong>Medications:</strong> {', '.join(patient.get('medications', ['None']))}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat Messages
    st.markdown("### 💬 Chat Messages")
    
    # Display messages
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong> {message["content"]}<br>
                    <small>🕐 {message["timestamp"]}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <strong>🤖 Medical Assistant:</strong><br>
                    {message["content"].replace('\n', '<br>')}<br>
                    <small>🕐 {message["timestamp"]}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👋 Welcome! Start by entering your name or ask a medical question.")
    
    # Chat Input
    st.markdown("### ✍️ Type Your Message")
    
    # Simple input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your message:",
            placeholder="Type your name (e.g., 'John Smith') or ask about symptoms...",
            height=80,
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            send_button = st.form_submit_button("📤 Send", use_container_width=True)
        with col2:
            if st.form_submit_button("🔍 Check Status", use_container_width=True):
                health = api.health_check()
                st.write(f"API Status: {health.get('status', 'unknown')}")
    
    # Process message
    if send_button and user_input.strip():
        # Add user message
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })
        
        # Send to API
        with st.spinner("🤖 Processing your message..."):
            response = api.send_message(user_input, st.session_state.session_id)
            
            if "error" not in response:
                # Update session ID
                if response.get("session_id"):
                    st.session_state.session_id = response["session_id"]
                
                # Add bot response
                bot_timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.get("response", "Sorry, I couldn't process your request."),
                    "timestamp": bot_timestamp
                })
                
                # Update patient data
                if response.get("patient_name") and not st.session_state.patient_data:
                    patient_info = api.get_patient(response["patient_name"])
                    if patient_info.get("success"):
                        st.session_state.patient_data = patient_info["data"]
            else:
                st.error(f"❌ Error: {response['error']}")
        
        st.rerun()
    
    # Simple Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Quick Actions")
        
        # Patient Lookup
        st.markdown("### 🔍 Find Patient")
        patient_name = st.text_input("Enter patient name:")
        
        if st.button("Search Patient", use_container_width=True) and patient_name:
            with st.spinner("Searching..."):
                result = api.get_patient(patient_name)
                if result.get("success"):
                    st.session_state.patient_data = result["data"]
                    st.success(f"✅ Found: {patient_name}")
                    st.rerun()
                else:
                    st.error("❌ Patient not found")
        
        st.markdown("---")
        
        # Quick Questions
        st.markdown("### ❓ Common Questions")
        
        quick_questions = [
            "I'm experiencing swelling",
            "I have chest pain",
            "When is my next appointment?",
            "Can I take my medication?",
            "I'm feeling nauseous"
        ]
        
        for question in quick_questions:
            if st.button(question, key=f"q_{hash(question)}", use_container_width=True):
                # Add the question as a user message
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "user",
                    "content": question,
                    "timestamp": timestamp
                })
                
                # Send to API
                with st.spinner("Processing..."):
                    response = api.send_message(question, st.session_state.session_id)
                    
                    if "error" not in response:
                        bot_timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response.get("response", "Sorry, I couldn't process your request."),
                            "timestamp": bot_timestamp
                        })
                
                st.rerun()
        
        st.markdown("---")
        
        # Help
        st.markdown("### 🆘 Help")
        with st.expander("How to use"):
            st.markdown("""
            **Steps:**
            1. Enter your full name
            2. System loads your records
            3. Ask medical questions
            
            **Emergency:** Call 911
            
            **Hospital:** (555) 123-4567
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #f0f0f0; border-radius: 5px; color: #333;'>
        <strong>🏥 Medical Assistant Chatbot</strong><br>
        <small>For post-discharge patient care | Not a substitute for professional medical advice</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()