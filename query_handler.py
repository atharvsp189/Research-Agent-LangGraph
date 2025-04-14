from ResearchAgent.graph import Graph

import pprint 

graph_builder = Graph()
graph = graph_builder.create_graph()

thread = {"configurable": {"thread_id": "001"}}

print("-"*10, "Deep Research AI Agent", "-"*10)

for s in graph.stream(
    {"task": "AI Boon or Bane", "max_revisions": 2, "revision_number": 1}, 
    thread
):
    pprint.pprint(s)
