from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain_openrouter import ChatOpenRouter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import dotenv
import os

dotenv.load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")


app = FastAPI(title='ChatBot')

# 2. Configura e introduce las opciones de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (como tu React)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)


@app.get('/')
async def  hello():
    return {
        "message": "Hello World"
    }

class MensajeUser(BaseModel):
    session_id : str
    mensaje_user: str

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


session = {}
def get_chat_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session:
        session[session_id] = ChatMessageHistory()
    return session[session_id]

chain = template | chat

runnable_chat_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="question"
)

@app.post('/chat')
async def chat_ai(mensajeChat : MensajeUser):
    user_input=mensajeChat.mensaje_user
    id = mensajeChat.session_id

    configurables : RunnableConfig= {
    "configurable":{
        "session_id": id
      }
    }

    if not user_input.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    
    response = runnable_chat_history.invoke({"question": user_input}, config=configurables)
    return {"respuesta IA":response.content}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
