"""
Test script for the medical agent workflow
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.workflow_graph.main import medical_system
from utils.logger import logger

def test_workflow():
    """Test the complete workflow"""
    
    print("\n" + "="*60)
    print("TESTING MEDICAL AGENT WORKFLOW SYSTEM")
    print("="*60 + "\n")
    
    # Test 1: Initial greeting and patient lookup
    print("\n--- Test 1: Patient Greeting ---")
    result1 = medical_system.process_message(
        message="Noah Bennett",
        session_id="test_session_1"
    )
    print(f"Response: {result1['message']}")
    print(f"Agent: {result1.get('agent')}")
    print(f"Success: {result1['success']}")
    
    # Test 2: General question (should stay with receptionist)
    print("\n--- Test 2: General Question ---")
    result2 = medical_system.process_message(
        message="What medications am I taking?",
        session_id="test_session_1"
    )
    print(f"Response: {result2['message']}")
    print(f"Agent: {result2.get('agent')}")
    
    # Test 3: Medical concern (should route to clinical)
    print("\n--- Test 3: Medical Concern (Routing to Clinical) ---")
    result3 = medical_system.process_message(
        message="I'm experiencing chest pain and shortness of breath",
        session_id="test_session_1"
    )
    print(f"Response: {result3['message']}")
    print(f"Agent: {result3.get('agent')}")
    print(f"Used RAG: {result3['metadata'].get('used_rag')}")
    print(f"Used Web Search: {result3['metadata'].get('used_web_search')}")
    
    # Test 4: Question about medication (should use RAG)
    print("\n--- Test 4: Medication Question (Should Use RAG) ---")
    result4 = medical_system.process_message(
        message="Tell me about the side effects of my medications",
        session_id="test_session_2"
    )
    print(f"Response: {result4['message'][:200]}...")
    print(f"Agent: {result4.get('agent')}")
    print(f"Used RAG: {result4['metadata'].get('used_rag')}")
    
    # Test 5: Latest research question (should use web search)
    print("\n--- Test 5: Latest Research (Should Use Web Search) ---")
    result5 = medical_system.process_message(
        message="What are the latest guidelines for post-surgical recovery?",
        session_id="test_session_3"
    )
    print(f"Response: {result5['message'][:200]}...")
    print(f"Agent: {result5.get('agent')}")
    print(f"Used Web Search: {result5['metadata'].get('used_web_search')}")
    
    print("\n" + "="*60)
    print("WORKFLOW TESTS COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_workflow()
    except Exception as e:
        logger.error(f"Test failed: {e}")
        logger.exception(e)
        print(f"\n❌ Test failed: {e}")
