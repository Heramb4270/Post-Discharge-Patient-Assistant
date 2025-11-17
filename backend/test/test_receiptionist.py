import sys
import os
# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.receptionist_agent import receptionist_agent
from agents.clinical_agent import clinical_agent_response
session = {}

while True:
    msg = input("You: ")
    if msg.lower() == "exit":
        break
    # Use the real clinical agent instead of dummy
    reply = receptionist_agent(msg, session, clinical_agent_response)
    print("Bot:", reply)