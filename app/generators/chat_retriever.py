import logging
import networkx as nx

from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from langchain.chat_models.base import init_chat_model

from app.utils.constants import GRAPHS_DIR, MODEL_NAME,GRAPH_MODEL_NAME
from app.utils.common_utils import remove_think_tokens,build_execution_trace

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger("langchain")
# logger.setLevel(logging.DEBUG)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = (PROJECT_ROOT / GRAPHS_DIR).resolve()


llm = init_chat_model(model=GRAPH_MODEL_NAME, model_provider="ollama", temperature=0.1)

def load_graph(video_id):
    path = GRAPH_PATH / f"{video_id}.graphml"
    if not path.exists():
        raise FileNotFoundError(f"Graph for {video_id} not found.")
    return nx.read_graphml(path)

def get_labels(G):
    return list(G.nodes)

def get_edges(G):
    return [f"{u} --[{d.get('label', '')}]--> {v}" for u, v, d in G.edges(data=True)]

def search_edges(G, keyword):
    results = []
    for u, v, d in G.edges(data=True):
        if keyword.lower() in u.lower() or keyword.lower() in v.lower() or keyword.lower() in d.get("label", "").lower():
            results.append(f"{u} --[{d.get('label', '')}]--> {v}")
    return results or ["No relevant triples found."]

def subgraph_summary(G, node):
    if node not in G:
        return [f"Node '{node}' not found in graph"]
    
    summary = []
    
    for u, v, d in G.edges(node, data=True):
        summary.append(f"{u} --[{d.get('label', '')}]--> {v}")
    
    if G.is_directed():
        for u, v, d in G.in_edges(node, data=True):
            summary.append(f"{u} --[{d.get('label', '')}]--> {v}")
    
    return summary or [f"No edges found for node '{node}'"]

class KeywordInput(BaseModel):
    keyword: str = Field(..., description="Keyword to search in subjects, predicates, or objects")

class NodeInput(BaseModel):
    node: str = Field(..., description="Name of the node to summarize its edges")

def answer_query(video_id: str, user_query: str):
    G = load_graph(video_id)

    tools = [
        StructuredTool.from_function(
            name="GetLabels",
            description="Get all node labels in the scene graph.",
            func=lambda: get_labels(G),
        ),
        StructuredTool.from_function(
            name="GetEdges",
            description="Return all edges in the scene graph.",
            func=lambda: get_edges(G),
        ),
        StructuredTool.from_function(
            name="SearchEdges",
            description="Search for triples that mention a keyword (subject, predicate, or object).",
            func=lambda keyword: search_edges(G, keyword),
            args_schema=KeywordInput
        ),
        StructuredTool.from_function(
            name="SummarizeSubgraph",
            description="Summarize all direct edges connected to a specific node.",
            func=lambda node: subgraph_summary(G, node),
            args_schema=NodeInput
        ),
    ]

    custom_prompt = """You are an expert assistant who answers questions using a scene graph with subject-predicate-object triples. Use the tools provided and reason step by step.

    Available Tools:
    {available_tools}

    Answer the query using the tools and provide a concise response.
    """

    answer_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=custom_prompt.format(
            available_tools=(", ".join(tool.name for tool in tools))
            ),
        verbose=True
    )

    final_state = answer_agent.invoke({"messages": [("human", user_query)]})

    tool_calls = build_execution_trace(final_state)
    print("\n" + tool_calls)

    print(f"\n🤖 Final Answer: {final_state['messages'][-1].content}")
    answer_without_think_tokens = remove_think_tokens(final_state['messages'][-1].content)

    return tool_calls,answer_without_think_tokens



if __name__ == "__main__":
    answer_query(video_id="Big Buck Bunny 60fps 4K - Official Blender Foundation Short Film-aqz-KE-bpKQ", user_query="Summarize the video for me from fox point of view.")