from langchain_core.tools import tool
import os
import shutil

def moveFilesAndFolders(destination_path:str, paths_to_move:list)->None:
    if not os.path.exists(destination_path):
        raise FileNotFoundError(f"The destination path '{destination_path}' does not exist.")
    
    for path in paths_to_move:
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path '{path}' does not exist.")
        
        item_name = os.path.basename(path)
        new_path = os.path.join(destination_path, item_name)
        shutil.move(path, new_path)
    


@tool
def moveFilesAndFoldersTool(destination_path:str,paths_to_move:list)->None:
    """ Takes as input a destination path and list of paths to files and folders. It moves all the files and 
        folders to the destination path.
    """
    moveFilesAndFolders(destination_path,paths_to_move)

