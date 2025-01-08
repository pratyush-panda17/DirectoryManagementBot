from langchain_core.tools import tool
import os

def createFolder(path:str,name:str)->None: #creates a folder of a given name at the specified path
    new_folder_path = os.path.join(path, name)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"The parent path '{path}' does not exist.")
    

    if os.path.exists(new_folder_path):
        raise FileExistsError(f"The folder '{new_folder_path}' already exists.")

    os.makedirs(new_folder_path)

@tool
def createFolderTool(path:str,name:str)->None:
    """ Creates a new folder/directory at the specified path. Takes as input a path (str) and name (str).
        Returns nothing
    """
    createFolder(path,name)
