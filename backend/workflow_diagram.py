"""
Visual representation of the workflow nodes and edges
Run this to see the workflow structure
"""

def print_workflow_diagram():
    diagram = """
╔════════════════════════════════════════════════════════════════════════╗
║         MEDICAL MULTI-AGENT WORKFLOW SYSTEM - LANGGRAPH               ║
╚════════════════════════════════════════════════════════════════════════╝

┌─────────────────┐
│   USER QUERY    │
└────────┬────────┘
         │
         ▼
┌────────────────────────────────────────┐
│     RECEPTIONIST NODE                  │
│  • Greet patient                       │
│  • Retrieve patient data               │
│  • Handle general queries              │
│  • Detect medical keywords             │
└────────┬───────────────────────────────┘
         │
         ▼
    ┌────────┐
    │ ROUTE? │◄────────────────┐
    └────┬───┘                 │
         │                     │
    ┌────┴────┐                │
    │         │                │
    ▼         ▼                │
 GENERAL   MEDICAL             │
  QUERY    CONCERN             │
    │         │                │
    │         ▼                │
    │  ┌──────────────────┐   │
    │  │ CLINICAL ROUTER  │   │
    │  │ • Assess needs   │   │
    │  └────┬─────────────┘   │
    │       │                 │
    │       ▼                 │
    │  ┌────────┐             │
    │  │ NEEDS? │             │
    │  └───┬──┬─┘             │
    │      │  │               │
    │  ┌───┘  └────┐          │
    │  │           │          │
    │  ▼           ▼          │
    │ RAG    WEB SEARCH       │
    │  │           │          │
    │  │  ┌────────┴──┐       │
    │  │  │           │       │
    │  ▼  ▼           ▼       │
    │ ┌──────────────────┐    │
    │ │ CLINICAL         │    │
    │ │ RESPONSE NODE    │    │
    │ │ • Combine context│    │
    │ │ • Generate reply │    │
    │ └────┬─────────────┘    │
    │      │                  │
    └──────┴──────────────────┘
           │
           ▼
       ┌───────┐
       │  END  │
       └───────┘

═══════════════════════════════════════════════════════════════════════

NODE DETAILS:

1. RECEPTIONIST NODE
   Input:  User message, session state
   Output: Response OR routing flag
   Logic:  Check for medical keywords
   
2. CLINICAL ROUTER NODE
   Input:  Medical query
   Output: needs_rag, needs_web_search flags
   Logic:  Keyword matching for resources needed
   
3. RAG NODE (Conditional)
   Input:  Query
   Output: Medical knowledge from vector store
   Trigger: Medical terms detected
   
4. WEB SEARCH NODE (Conditional)
   Input:  Query
   Output: Current medical information
   Trigger: "latest", "recent", "new" keywords
   
5. CLINICAL RESPONSE NODE
   Input:  Query + all available context
   Output: Evidence-based medical response
   Logic:  Combines patient data + RAG + web search

═══════════════════════════════════════════════════════════════════════

ROUTING LOGIC:

Receptionist → Clinical?
  IF medical_keywords IN message:
    → Clinical Router
  ELSE:
    → END (stay with receptionist)

Clinical Router → RAG/Web/Direct?
  IF medication/treatment keywords:
    → RAG Node
  IF "latest"/"recent" keywords:
    → Web Search Node
  ELSE:
    → Clinical Response (direct)

RAG → Web Search?
  IF needs_web_search flag:
    → Web Search Node
  ELSE:
    → Clinical Response

Web Search → Clinical Response (always)

═══════════════════════════════════════════════════════════════════════

EXAMPLE FLOWS:

1. "What medications am I taking?"
   User → Receptionist → END
   (No medical concern, general query)

2. "Tell me about side effects"
   User → Receptionist → Clinical Router → RAG → Clinical Response → END
   (Medical keyword: "side effects")

3. "Latest guidelines for recovery"
   User → Receptionist → Clinical Router → Web Search → Clinical Response → END
   (Web keyword: "latest")

4. "New research on my medication interactions"
   User → Receptionist → Clinical Router → RAG → Web Search → Clinical Response → END
   (Both medical + web keywords)

═══════════════════════════════════════════════════════════════════════
"""
    print(diagram)

if __name__ == "__main__":
    print_workflow_diagram()
