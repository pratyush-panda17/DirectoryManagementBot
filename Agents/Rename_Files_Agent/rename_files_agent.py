from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import Rename_Files_Agent.tools as tools

llm = ChatOllama(model="mistral:7b")

rename_files_agent_prompt = (
    """You have the abiltiy to rename any files or folders the user wants. The user must provide two lists.
    A list of paths and a list of names they wish to rename the files to. Use the renameFileOrFolderTool to carry out this action.
    Ensure that the user provides you with the two arguments:
    paths: the paths to the files and folder they wish to rename
    new_names: the new names of the files and folder.

    You must call renameFileOrFolderTool like:
    renameFileOrFolderTool(paths,new_names)

    If the user does not provide any other arguments, prompt them to do so. You can only rename files. Anything else such as searching,
    deleting is beyond your abilities. 
"""

)

rename_files_agent = create_react_agent(
    llm, 
    tools=[tools.renameFileOrFolderTool], 
    state_modifier=rename_files_agent_prompt
)