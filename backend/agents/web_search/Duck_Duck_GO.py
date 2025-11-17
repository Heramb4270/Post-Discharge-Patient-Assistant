from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

# Just use the tool directly
search_tool = DuckDuckGoSearchRun()

def web_search(query: str) -> str:
    """Perform web search using DuckDuckGo and return results"""
    print(f"Performing web search for query: {query}")
    search_results = search_tool.invoke(query)  # Use invoke, not run
    print(f"Web search results: {search_results}")
    return search_results

def search_medical_info(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Search for medical information and return structured results
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        
    Returns:
        List of dicts with title, snippet, url
    """
    try:
        # Enhance query for medical context
        medical_query = f"{query} medical health information"
        
        # Get search results
        raw_results = search_tool.invoke(medical_query)
        
        # DuckDuckGoSearchRun returns a string, so we parse it
        # Split by lines and create structured output
        results = []
        lines = raw_results.split('\n')
        
        # Create a single comprehensive result from all lines
        result_text = ' '.join([line.strip() for line in lines if line.strip()])
        
        if result_text:
            results.append({
                "title": f"Medical Information: {query[:50]}...",
                "snippet": result_text[:500],  # Limit snippet length
                "url": "https://duckduckgo.com"
            })
        
        return results[:max_results]
        
    except Exception as e:
        print(f"Web search error: {e}")
        return [{
            "title": "Search Error",
            "snippet": f"Unable to perform web search: {str(e)}",
            "url": ""
        }]
