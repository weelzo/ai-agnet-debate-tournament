from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

class DebateAgent:
    
    load_dotenv()  # Load from .env file
    openai_api_key = os.getenv("OPENAI_API_KEY")
    print(openai_api_key)
    
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    def __init__(self, name, role, model="gpt-4-turbo", api_key=openai_api_key):
        if not api_key:
            raise ValueError("API key must be provided.")
        self.name = name
        self.role = role
        self.llm = ChatOpenAI(model=model, temperature=0.7, openai_api_key=api_key)

    def respond(self, message, context=[]):
        # Convert context messages to proper LangChain Message objects
        context_messages = []
        for msg in context:
            if msg["role"] == "Proponent" or msg["role"] == "Opponent":
                context_messages.append(AIMessage(content=msg["text"]))

        messages = [
            SystemMessage(content=f"You are {self.role}. Respond persuasively.")
        ] + context_messages + [
            HumanMessage(content=message)
        ]
        return self.llm(messages).content