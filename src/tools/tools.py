from datetime import datetime 
from langchain_core.tools import tool 
from Brain.Brain import LLM  

# Return current date and time 
@tool 
def get_time()->str :
    """Get the current date and time"""
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")

# Notes return 
@tool 
def save_note(text:str)->str :
    """ save a note for the user """
    with open("Note.txt","a") as f:
        f.write(text + "\n")
    return "Notes save"

# read the notes 
@tool 
def read_notes()->str:
    """Read all the users save notes"""
    try :
        return open ("Note.txt").read() or "No notes yet ."
    except FileNotFoundError :
        return "No notes yet . "
    
tools = [get_time , save_note , read_notes]

Tools_Name = {t.name : t for t in tools}
LLM_tools = LLM.bind_tools(tools)

if __name__ == "__main__":
    print(Tools_Name)