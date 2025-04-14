from ResearchAgent.graph import Graph
import chainlit as cl
from chainlit.input_widget import Switch

graph_builder = Graph()
graph = graph_builder.create_graph()
thread = {"configurable": {"thread_id": "001"}}

print("-"*10, "Deep Research AI Agent", "-"*10)


@cl.on_chat_start
async def on_chat_start():
    print("Chat Started...")
    msg = cl.Message(content="Hi, What are you working on?")
    
    settings = await cl.ChatSettings(
        [
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
        ]
    ).send()
    value = settings["Streaming"]

steps = []

@cl.on_message
async def on_message(message: cl.Message):
    # Input message as task
    task = message.content

    # Start streaming results from LangGraph agent
    async for step in graph.astream(
        {"task": task, "max_revisions": 2, "revision_number": 1},
        thread
    ):
        steps.append(step)
        for key, value in step.items():
            # Pretty display each step
            if key == "planner":
                await cl.Message(content=f"🧠 **Planner Step:**\n{value['plan']}").send()
                

            elif key == "research_plan":
                joined = "\n".join(value["content"])
                await cl.Message(content=f"🔍 **Research Plan:**\n{joined}").send()

            elif key == "generate":
                await cl.Message(content=f"✍️ **Draft (Rev {value['revision_number']}):**\n{value['draft']}").send()

            elif key == "reflect":
                await cl.Message(content=f"🪞 **Reflection:**\n{value['critique']}").send()

            elif key == "research_critique":
                joined = "\n".join(value["content"])
                await cl.Message(content=f"🧪 **Research Critique:**\n{joined}").send()

            else:
                await cl.Message(content=f"📦 **Step Output:**\n```python\n{pretty}\n```").send()