"""
Quick test for LangGraph agents
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.agents.state import AgentState, create_initial_state, QueryType
from src.agents.supervisor import supervisor_node, extract_parties, classify_query
from src.agents.graph import create_workflow, run_simple_query

from src.core.llm_setup import create_llm_handler


def test_supervisor():
    """Test supervisor node."""
    print("\n=== Testing Supervisor ===")
    
    state = create_initial_state("CHP'nin ekonomi politikası nedir?")
    print(f"Query: {state.query}")
    
    parties = extract_parties(state.query)
    print(f"Parties found: {parties}")
    
    qtype = classify_query(state.query)
    print(f"Query type: {qtype}")
    
    state.query_type = QueryType(type=qtype, parties=parties, confidence=0.8)
    result = supervisor_node(state)
    
    print(f"Steps: {result.steps}")
    print("PASSED: Supervisor test")


def test_workflow():
    """Test full workflow."""
    print("\n=== Testing Workflow ===")
    
    try:
        llm, model_name = create_llm_handler("CHP")
        print(f"LLM created successfully: {model_name}")
        
        result = run_simple_query("CHP'nin laiklik anlayisi nedir?", llm)
        
        if isinstance(result, str):
            print(f"Answer: {result[:200]}...")
        else:
            print(f"Answer: {result.final_answer[:200]}...")
            
        print("PASSED: Workflow test")
        
    except Exception as e:
        print(f"FAILED: Workflow test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_supervisor()
    test_workflow()
