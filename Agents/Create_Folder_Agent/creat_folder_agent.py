from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
import Create_Folder_Agent.tools as tools

llm = ChatOllama(model="mistral:7b")


create_folder_agent_prompt = (
    """You are an agent whose task is to create a folder at a specified directory. You can do nothing else.
       Any actions such as editing, searching or deleting files is beyond the scope of your abilities.
       The user must provide you with two arguments:

       path: (str) the directory path to where the new folder must be created
       name: (str) the name of the new folder being created

       Use the createFolderTool to make new folders.  
"""
)

delete_agent = create_react_agent(
    llm, 
    tools=[tools.createFolderTool], 
    state_modifier=create_folder_agent_prompt
)
