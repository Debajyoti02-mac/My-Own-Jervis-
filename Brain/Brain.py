import warnings
warnings.filterwarnings('ignore')
from langchain_groq import ChatGroq 
from config.config import Model 
import os 
from dotenv import load_dotenv 

load_dotenv()

LLM = ChatGroq(model=Model)

# Brain 

def llm_chat(messages  : list[dict])->str:
    response = LLM.invoke(messages)
    return response.content


# connection 
messages = [
    {"role":"system" , "content":"You are Jarvis, a concise assistant."},
    {"role": "user", "content": "Say hello in one sentence."},
]

# Check 
check_responses = llm_chat(messages)

if __name__ == "__main__":
    print(check_responses)