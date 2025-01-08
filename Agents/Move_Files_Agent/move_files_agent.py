from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import Move_Files_Agent.tools as tools

llm = ChatOllama(model="mistral:7b")

move_files_agent_prompt = (
    """
        You have the ability to relocate any files or folders. The user will give you as input a path to a destination directory and list of paths
        to files and folders. Use the moveFilesAndFoldersTool to move all the files and folders to the destination directory. You can only relocated files
        and nothing else. Any operation such as searching,editing or deleting files is beyond the scope of your abilties.
        Always expect the user to give you two arguments:
        destination_path: (str) path to the destination directory
        paths_to_move: (list) A list of paths to all files and folders that you need to move.

        If the user does not provide such arguments, prompt them to do so.
    """

)
move_files_agent = create_react_agent(
    llm, 
    tools=[tools.moveFilesAndFoldersTool], 
    state_modifier=move_files_agent_prompt
)
