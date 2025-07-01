from typing import Annotated, Sequence, List, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage

from cv_analyzer.agents import (
    CVReaderAgent,
    JobDescriptionAnalyzerAgent,
    CVInformationExtractorAgent,
    CandidateRankerAgent,
    UserQueryAgent,
    OutputFormatterAgent,
    CVData,
    JobRequirements,
)

class CVScreeningState(TypedDict, total=False):
    cv_folder_path: str
    job_description: str
    cv_data_list: List[CVData]
    job_requirements: JobRequirements
    ranked_candidates: List[CVData]
    user_query: str
    output: str
    should_continue: bool

def create_cv_screening_graph() -> StateGraph:
    # Initialize agents
    cv_reader = CVReaderAgent()
    job_analyzer = JobDescriptionAnalyzerAgent()
    cv_extractor = CVInformationExtractorAgent()
    candidate_ranker = CandidateRankerAgent()
    user_query_agent = UserQueryAgent()
    output_formatter = OutputFormatterAgent()

    # Define the workflow graph
    workflow = StateGraph(CVScreeningState)

    # Node 1: Read CVs
    def read_cvs(state: CVScreeningState) -> CVScreeningState:
        state["cv_data_list"] = cv_reader.process(state["cv_folder_path"])
        return state

    # Node 2: Analyze Job Description
    def analyze_job(state: CVScreeningState) -> CVScreeningState:
        state["job_requirements"] = job_analyzer.process(state["job_description"])
        return state

    # Node 3: Extract CV Information
    def extract_cv_info(state: CVScreeningState) -> CVScreeningState:
        for i, cv_data in enumerate(state["cv_data_list"]):
            state["cv_data_list"][i] = cv_extractor.process(cv_data)
        return state

    # Node 4: Rank Candidates
    def rank_candidates(state: CVScreeningState) -> CVScreeningState:
        ranked_candidates = []
        for cv_data in state["cv_data_list"]:
            ranked_cv = candidate_ranker.process(cv_data, state["job_requirements"])
            ranked_candidates.append(ranked_cv)
        
        state["ranked_candidates"] = sorted(
            ranked_candidates,
            key=lambda x: x["score"] or 0,
            reverse=True
        )
        return state

    # Node 5: Process User Query
    def process_user_query(state: CVScreeningState) -> CVScreeningState:
        if state.get("user_query"):
            state["ranked_candidates"] = user_query_agent.process(
                state["user_query"],
                state["ranked_candidates"]
            )
        return state

    # Node 6: Format Output
    def format_output(state: CVScreeningState) -> CVScreeningState:
        state["output"] = output_formatter.process(state["ranked_candidates"])
        return state

    # Conditional: Check if should continue
    def should_continue(state: CVScreeningState) -> str:
        # Default to "end" if should_continue is not in state
        return "continue" if state.get("should_continue", False) else "end"

    # Add nodes to the graph
    workflow.add_node("read_cvs", read_cvs)
    workflow.add_node("analyze_job", analyze_job)
    workflow.add_node("extract_cv_info", extract_cv_info)
    workflow.add_node("rank_candidates", rank_candidates)
    workflow.add_node("process_user_query", process_user_query)
    workflow.add_node("format_output", format_output)

    # Define the edges
    workflow.set_entry_point("read_cvs")
    workflow.add_edge("read_cvs", "analyze_job")
    workflow.add_edge("analyze_job", "extract_cv_info")
    workflow.add_edge("extract_cv_info", "rank_candidates")
    workflow.add_edge("rank_candidates", "process_user_query")
    workflow.add_edge("process_user_query", "format_output")

    # Add conditional branching for user queries
    workflow.add_conditional_edges(
        "format_output",
        should_continue,
        {
            "continue": "process_user_query",
            "end": END
        }
    )

    return workflow.compile()

def run_cv_screening(
    cv_folder_path: str,
    job_description: str,
    user_query: str = "",
    should_continue: bool = False
) -> Dict[str, Any]:
    """
    Run the CV screening workflow.
    
    Args:
        cv_folder_path: Path to the folder containing CV PDFs
        job_description: The job description text
        user_query: Optional query to refine the search
        should_continue: Whether to continue processing after initial results
        
    Returns:
        Dict containing the final state of the workflow
    """
    graph = create_cv_screening_graph()
    
    # Initialize the state with all required fields
    initial_state: CVScreeningState = {
        "cv_folder_path": cv_folder_path,
        "job_description": job_description,
        "cv_data_list": [],
        "job_requirements": {
            "required_skills": [],
            "desired_experience": [],
            "qualifications": [],
            "key_responsibilities": []
        },
        "ranked_candidates": [],
        "user_query": user_query,
        "output": "",
        "should_continue": should_continue
    }
    
    # Run the graph
    final_state = graph.invoke(initial_state)
    return final_state

# Export a compiled graph instance
graph = create_cv_screening_graph()
