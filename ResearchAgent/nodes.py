from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

from .prompts import Prompts
from .client_handler import LLMClients, SearchClients
from .structures import Queries, AgentState

llms = LLMClients()
search = SearchClients()

prompt = Prompts()

class Nodes:
    def __init__(self):
        pass
    
    # Drafts a plan
    def planNode(self, state: AgentState):
        messages = [
            SystemMessage(content=prompt.PLAN_PROMPT),
            HumanMessage(content=state['task'])
        ]
        response= llms.llm.invoke(messages)
        return {"plan": response.content}

    def researchNode(self, state: AgentState):
        queries = llms.llm.with_structured_output(Queries).invoke([
            SystemMessage(content=prompt.RESEARCH_PLAN_PROMPT),
            HumanMessage(content=state['task'])
        ])
        
        content = state.get('content', [])

        for q in queries.queries:
            response = search.tavily_client.search(query=q, max_results=3)
            for r in response['results']:
                content.append(r['content'])
            
        return {"content": content}

    def generationNode(self, state: AgentState):
        content="\n\n".join(state['content'] or [])
        
        user_message = HumanMessage(content=f"{state['task']} \n\n Here is my plan {state['plan']}")
        
        message = [
            SystemMessage(content=prompt.WRITER_PROMPT.format(content=content)),
            user_message
        ]
        
        response = llms.generate_llm.invoke(message)
        
        return {
            "draft": response.content,
            "revision_number": state.get("revision_number", 1) + 1
        }
        
    def reflectionNode(self, state: AgentState):
        messages= [
            SystemMessage(content=prompt.REFLECTION_PROMPT),
            HumanMessage(content=state["draft"])
        ]
        
        response = llms.reasoning_llm.invoke(messages)
        
        return {"critique": response.content}

    def researchCritiqueNode(self, state: AgentState):
        queries = llms.reasoning_llm.with_structured_output(Queries).invoke([
            SystemMessage(content=prompt.RESEARCH_CRITIQUE_PROMPT),
            HumanMessage(content=state['critique'])
        ])
        
        content = state['content'] or []
        for q in queries.queries:
            response = search.tavily_client.search(query=q, max_results=2)
            for r in response.get('results', []):
                content.append(r['content'])
                
        return {"content": content}    

    def toContinue(self, state):
        if state["revision_number"] > state["max_revisions"]:
            return END
        
        return "reflect"