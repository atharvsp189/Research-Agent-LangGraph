from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langgraph.checkpoint.memory import MemorySaver

from .nodes import Nodes
from .structures import AgentState
node = Nodes()

class Graph:
    def __init__(self):
        self.bulider = StateGraph(AgentState)
        pass

    # Create a graph from preovided Nodes in a template
    def create_graph(self):
        """Builds the graph from provided nodes in a templates"""
        
        # Add Nodes in a graph
        self.bulider.add_node("planner", node.planNode)
        self.bulider.add_node("research_plan", node.researchNode)
        self.bulider.add_node("generate", node.generationNode)
        self.bulider.add_node("reflect", node.reflectionNode)
        self.bulider.add_node("research_critique", node.researchCritiqueNode)
        self.bulider.add_conditional_edges(
            "generate",
            node.toContinue,
            {END: END, "reflect": "reflect"}
        )

        # Add Edges (relationships)
        self.bulider.set_entry_point("planner")
        self.bulider.add_edge("planner", "research_plan")
        self.bulider.add_edge("research_plan", "generate")
        self.bulider.add_edge("reflect", "research_critique")
        self.bulider.add_edge("research_critique", "generate")
        
        # Compile Graph
        graph = self.bulider.compile(checkpointer=MemorySaver())
        
        return graph