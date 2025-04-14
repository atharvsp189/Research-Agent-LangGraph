import streamlit as st
from ResearchAgent.graph import Graph
import asyncio

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Deep Research AI Agent",
    page_icon="🔍",
    layout="wide",
)

graph_builder = Graph()
graph = graph_builder.create_graph()
thread = {"configurable": {"thread_id": "001"}}

st.title("🤖 Deep Research AI Agent")
task = st.text_input("Enter Topic")
research = st.button("Research")


steps = []
async def do_research():
    async for step in graph.astream(
            {"task": task, "max_revisions": 2, "revision_number": 1},
            thread
        ):
            steps.append(step)
            for key, value in step.items():
                # Pretty display each step
                if key == "planner":
                    planner = st.expander("See Plan")
                    planner.write(f"🧠 **Planner Step:**\n{value['plan']}")                    

                elif key == "research_plan":
                    research_plan = st.expander("See Research")
                    joined = "\n".join(value["content"])
                    research_plan.write(f"🔍 **Research Plan:**\n{joined}")

                elif key == "generate":
                    genearte = st.expander(f"✍️ **Draft (Rev {value['revision_number']}):**")
                    genearte.write(f"\n{value['draft']}")

                elif key == "reflect":
                    reflect = st.expander("🪞 **Reflection:**")
                    reflect.write(f"\n{value['critique']}")

                elif key == "research_critique":
                    research_critique = st.expander("🧪 **Research Critique:**")
                    joined = "\n".join(value["content"])
                    research_critique.write(f"\n{joined}")

                else:
                    st.write(f"📦 **Step Output:**\n")

if research:
    asyncio.run(do_research())