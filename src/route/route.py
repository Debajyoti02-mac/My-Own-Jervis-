from tools.tools import get_time , save_note , read_notes 

def direct_router(user_input:str)->str:
    text = user_input.lower().strip()
    
    # Time tool 
    if "what time" in text or text == "time":
        return get_time.invoke({})
    
    # Save Note 
    if text.startswith("save a note: "):
        note = user_input.split(":",1)[1].strip()
        
        if note :
            return save_note.invoke({'text':note})
        return "please prove a note to save"
    # Read Note 
    
    if "what note do i have" in text or text == "read note" or text == "read notes":
        return read_notes.invoke({})
    
    return None 