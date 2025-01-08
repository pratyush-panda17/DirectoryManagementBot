from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from typing import Literal
import operator
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict,Optional, Annotated
from langgraph.types import Command
from langchain_core.messages import HumanMessage, AnyMessage
import input_classes
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

llm = ChatOllama(model="mistral:7b")


# Load pre-trained model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DECISIONS = ["search_agent","rename_files_agent","move_files_agent","delete_agent","create_folder_agent","FINISH"]




def getBestDecision(decision:str)->str:
    decision_embeddings = embedding_model.encode(DECISIONS)
    embedding = embedding_model.encode(decision)
    similarity_matrix = cosine_similarity(decision_embeddings, [embedding])
    return DECISIONS[similarity_matrix.argmax()]

system_prompt = (
    """You are a routing system for a directory management tool. 
    Your job is to decide the next step in the workflow. 
    Your response should never be None.

    Options:
    - "search_agent" if the user wants to search for a specific file or folder.
    - "rename_files_agent" if the user wants to rename a particular file or folder.
    - "move_files_agent" if the user wants to move some files or folders to a destination directory.
    - "delete_agent" if the the user wants to delete any file or folder
    - "create_folder_agent" if the user wants to create a new folder/directory.
    - "FINISH" if no further actions are required.

    Along with a decision you must decide what data to pass based on the decision. For example if your decision is search_agent
    you must pass search_agent_data which is of type input_classes.SearchAgent.

    Provide the following in your response:
    - 'next': One of ["search_agent","rename_files_agent","move_files_agent","delete_agent","create_folder_agent","FINISH"]    
    - appropriate data based on the value of next
"""
)

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH. """

    next: Literal["search_agent","rename_files_agent","move_files_agent","delete_agent","create_folder_agent","FINISH"]
    search_agent_data : Optional[input_classes.SearchAgent]
    rename_files_agent_data: Optional[input_classes.RenameFilesAgent]
    move_files_agent_data: Optional[input_classes.MoveFilesAgent]
    delete_agent_data: Optional[input_classes.DeleteAgent]
    create_folder_agent_data: Optional[input_classes.CreateFolderAgent]


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    search_agent_data : Optional[input_classes.SearchAgent]
    rename_files_agent_data: Optional[input_classes.RenameFilesAgent]
    move_files_agent_data: Optional[input_classes.MoveFilesAgent]
    delete_agent_data: Optional[input_classes.DeleteAgent]
    create_folder_agent_data: Optional[input_classes.CreateFolderAgent]


def supervisor_node(state: MessagesState) -> Command[Literal["search_agent","rename_files_agent","move_files_agent","delete_agent","create_folder_agent","__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)    
    if response==None:
        return Command(goto=END)
    
    decision = response["next"]
    print(f"this is the decision :{decision} \n\n")
    goto = getBestDecision(decision) 
    return goto

    # if goto == "FINISH":
    #     goto = END

    # information = goto+"_data"
    # return Command(
    #     update={
    #         "messages":state["messages"][-1],
    #         information : response.get(information)   
    #     }
    # )


# def search_agent_node(state:MessagesState)->Command[Literal["supervisor"]]:
#     data = state.get("search_agent_data")
#     folder = data[]

print(supervisor_node({"messages": [("user", "delete all files named temp in my desktop")]}))
