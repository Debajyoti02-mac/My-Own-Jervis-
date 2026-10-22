from langchain_core.messages import ToolMessage
from tools.tools import LLM_tools , Tools_Name 
System_Prompt = {
    "role":"system",
    "content":"You are Helper, a concise assistant."
}

history = []
max_messages = 20 

def agent(user_input :str) ->str :
    history.append({
        'role':'user',
        'content':user_input
    })
    
    messages = [System_Prompt] + history[-max_messages:]
    
    for _ in range(5):
        response = LLM_tools.invoke(messages)
        
        if not response.tool_calls:
            break 
        messages.append(response)
        for call in response.tool_calls:
            name_tool = Tools_Name[call['name']]
            args = call['args']
            
            result = name_tool.invoke(args)
            messages.append(ToolMessage(content=str(result),tool_call_id = call['id']))
    history.append({
            'role':'assistant',
            'content':response.content
        })
    return response.content


# while True:
#     text = input("you : ")
#     if text.lower() in ("exit" , "quit"):
#         break 
#     print("start " , agent(text))

res1 = agent("What time is it?")
res2 = agent("Save a note: buy a notebook.")
res3 = agent("What notes do I have?")

if __name__ == "__main__":
    print(res1  , res2 , res3 )
