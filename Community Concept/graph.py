import os
import operator
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END

# Imported Nodes (we will create these next)
from nodes.spotify_node import spotify_intake
from nodes.researcher_node import research_artist
from nodes.copywriter_node import draft_content
from nodes.critic_node import quality_control
from nodes.publisher_node import publish_to_instagram

# Define the State of the Graph
class AgentState(TypedDict):
    status: str
    top_5_tracks: List[dict]
    selected_track: dict
    research_summary: str
    draft_caption: str
    image_prompt: str
    image_url: str
    publish_time_iso: str  # For smart scheduling
    critique_feedback: str
    retry_count: int

# Initialize the Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("spotify", spotify_intake)
workflow.add_node("researcher", research_artist)
workflow.add_node("copywriter", draft_content)
workflow.add_node("critic", quality_control)
workflow.add_node("publisher", publish_to_instagram)

# Define Edges (The Flow)
workflow.set_entry_point("spotify")

workflow.add_edge("spotify", "researcher")
workflow.add_edge("researcher", "copywriter")
workflow.add_edge("copywriter", "critic")

# Conditional Logic for the Critic
def check_critique(state):
    if state.get("critique_feedback") == "APPROVED":
        return "publisher"
    elif state.get("retry_count", 0) > 2:
        # If failed 3 times, publish anyway or log error (here we publish to avoid blocking)
        print("⚠️ Max retries reached. Publishing best effort.")
        return "publisher"
    else:
        return "copywriter"

workflow.add_conditional_edges(
    "critic",
    check_critique,
    {
        "publisher": "publisher",
        "copywriter": "copywriter"
    }
)

workflow.add_edge("publisher", END)

# Compile
app = workflow.compile()
