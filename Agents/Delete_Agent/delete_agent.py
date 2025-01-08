from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
import Delete_Agent.tools as tools

llm = ChatOllama(model="mistral:7b")


delete_agent_prompt = (
    """You are an agent that can delete any file, given the user provides the path.
    You have access to one tool. The deleteFileOrFolderTool. It takes as input a list of strings
    where each string represents a path to a folder or directory that the user wants to delete. If you are not provided with 
    any concrete paths prompt the user to do so. You can only delete files and folders. Any other action such as search or edit is
    beyond your abilitites. You will always be provided with the argument 'paths'. Which is a list of paths to files and folders you
    need to delete. Pass this argument to the deleteFileorFolderTool. If the use does not provide you with the paths to the file or folders, prompt them
    to do so.

    Do not provide code snippets or instructions. You must delete whatever paths the user provides you with. You have no other choice. If the user does not provide the path in the message,
    check for the 'paths' variable.
"""
)

delete_agent_prompt_template = PromptTemplate(
    input_variables=["paths"],
    template="""
    Delete these file and folders. Paths:{paths}
    """
)

delete_agent = create_react_agent(
    llm, 
    tools=[tools.deleteFileOrFolderTool], 
    state_modifier=delete_agent_prompt
)

message =delete_agent_prompt_template.format(paths= ", ".join(['/Users/joey/Deskop/temp']))
print(delete_agent.invoke({
    "messages":["Delete a temp folder in my desktop. No need to ask for confirmation. The path is /Users/joey/Deskop/temp"],
    "paths":['/Users/joey/Deskop/temp'],
}))




