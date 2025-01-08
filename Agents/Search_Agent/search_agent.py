from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from typing import Literal
import operator
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict,Optional, Annotated
from langgraph.types import Command
from langchain_core.messages import HumanMessage, AnyMessage

import Search_Agent.tools as tools

llm = ChatOllama(model="mistral:7b")

system_prompt = (
    """You are a routing system for a file and folder searching tool. 
    Your job is to decide the next step in the workflow. 
    Your response should never be None.

    Options:
    - "file_searcher" if the user wants to search for a specific file.
    - "folder_searcher" if the user wants to search for a folder or directory.
    - "FINISH" if no further actions are required. Always output FINISH after the search call has been made.

    Provide the following in your response:
    - 'next': One of ["file_searcher", "folder_searcher", "FINISH"]

    Example:
    Input: Search for a file named chatbot in my desktop
    next:file_searcher
    folder_name : Desktop
    file_name: chatbot

    Example:
    Input: Search for folders named Chatbot
    next: folder_searcher
    folder_name: Chatbot
    
"""

)


class SearchAgentRouter(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH. 
    Provide file_name and folder_name for file_searcher and folder_name for folder_searcher"""

    next: Literal["file_searcher","folder_searcher","FINISH"]
    file_name: Optional[str] 
    folder_name: Optional[str]

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    folder_name: Optional[str]
    file_name: Optional[str]


file_searcher_prompt =""" Your job is to search for files of a given name in the user's computer. You can interact with a user's computer.
                          You can only search in a folder path or folder name provided to you. You can only search and nothing else. DO NOT PROVIDE CODE 
                          SNIPPETS. DO NOT GIVE INSTRUCTIONS TO SEARCH. You are a file searcher and file searcher only. To search for files use 
                          the searchForFilesTool. You must exclusively use the `searchForFileTool`. 

                          Do not attempt to use any other tools. If you think the SearchForFilesTool is insufficient ask the user for more information.
                          
                          You will always be given two arguments:
                          folder_name, file_name
                          Use the searchForFilesTool using these two arguments

                          Example:
                          Input:Search for files named chatbot in my desktop.
                          file_name: chatbot
                          folder_name: desktop
                          SearchForFilesTool(folder_name=desktop, file_name=chatbot)
                          
                          """
file_searcher = create_react_agent(
    llm, 
    tools=[tools.searchForFileTool], 
    state_modifier=file_searcher_prompt
)

folder_searcher_prompt = """Your job is to search for folder of a given name in the user's computer. You can only search and nothing else.
            A folder and a directory are the exact same thing. To search for folders or directories by name use findFolderByNameTool. You will be provided with one
            argument 'folder_name'. Use the findFolderByNameTool using this argument."""
folder_searcher = create_react_agent(
    llm, 
    tools=[tools.findFolderByNameTool],
    state_modifier=folder_searcher_prompt
)


def supervisor_node(state: MessagesState) -> Command[Literal["file_searcher","folder_searcher", "__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(SearchAgentRouter).invoke(state["messages"])    
    if response==None:
        return Command(goto=END)
    goto = response["next"]


    if goto == "FINISH":
        goto = END

    print(response)
    if goto == "folder_searcher":
        print("trying to get folder_name")
        folder_name = response.get("folder_name")
        print("successfully got folder_name")
        return Command(
            update={
                "messages": [
                    HumanMessage(content=f"Search for folder: {folder_name}", name="supervisor")
                ],
                "folder_name": folder_name, 
            },
            goto=goto,
        )
    print("trying to get folder_name and file_name")
    folder_name = response.get("folder_name")
    file_name = response.get("file_name")
    print("successfully got folder_name")
    return Command(
            update={
                "messages": [
                    HumanMessage(content=f"Search for file '{file_name}' in directory '{folder_name}'", name="supervisor")
                ],
                "folder_name": folder_name,  # Pass directory_path in state
                "file_name": file_name,            # Pass file_name in state
            },
            goto=goto,
        )


def file_searcher_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    folder_name = state.get("folder_name")
    file_name = state.get("file_name")
    result = file_searcher.invoke({
        "messages": state["messages"],
        "folder_name": folder_name,
        "file_name": file_name,
    })
    
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="file_searcher")
            ]
        },
        goto="supervisor",
    )

def folder_searcher_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    folder_name = state.get("folder_name")
    result = folder_searcher.invoke({
        "messages": state["messages"],
        "folder_name": folder_name,
    })
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="folder_searcher")
            ]
        },
        goto="supervisor",
    )



builder = StateGraph(MessagesState)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("file_searcher", folder_searcher_node)
builder.add_node("folder_searcher", file_searcher_node)
graph = builder.compile()

print(folder_searcher.invoke(
    { "messages":["Get me the path to the desktop directory"],
     "folder_name":"desktop",

    }
))


# for s in graph.stream(
#     {"messages": [("user", "Search for files named chatbot in my desktop")]}, subgraphs=True
# ):
#     print(s)
#     print("----")



