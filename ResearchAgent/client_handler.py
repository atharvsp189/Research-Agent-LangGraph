import os
from dotenv import load_dotenv
load_dotenv()


# Load Credentials
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Initialize LLMs
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMClients:
    def __init__(self):
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key = groq_api_key
        )

        self.reasoning_llm = ChatGroq(
            model="deepseek-r1-distill-llama-70b",
            temperature=0,
            api_key = groq_api_key
        )


        self.generate_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            api_key = gemini_api_key
        )

# Initialize Search Client

from tavily import TavilyClient

class SearchClients:
    def __init__(self):
        self.tavily_client = TavilyClient()
