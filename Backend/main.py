from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain_openrouter import ChatOpenRouter

import dotenv
import os

dotenv.load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")

chat = ChatOpenRouter(
    model=MODEL,
    temperature=1,
    max_tokens=1024,
    max_retries=2,
    # other params...
)

system_message ="""
eres experto en responder de manera muy amigable y con buenas palabras
, con eso tambien podras dar consejos de apoyo a las preguntas
"""

template = ChatPromptTemplate.from_messages([
    ("system",system_message.strip()),
    ("human","{question}")
])

configurables : RunnableConfig= {
    "configurable":{
        "session_id": "1234"
    }
}


session = {}
def get_chat_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session:
        session[session_id] = ChatMessageHistory()
    return session[session_id]

runnable_chat_history = RunnableWithMessageHistory(
    chat,
    get_chat_history
)

def chat_active():
    while True:
        user_input = input("\nmensaje del usuario: ")

        if user_input.lower() in ["bye","adios","exit"]:
            print("hasta pronto")
            return 
        response = runnable_chat_history.invoke(user_input, config=configurables)
        print(" respuesta del LLM: ")
        for chunk in chat.stream(template.invoke({"question":response})):
            print(chunk.content,end="", flush=True)

chat_active()