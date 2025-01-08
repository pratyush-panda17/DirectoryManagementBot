from langchain_core.tools import tool
import os


def renameFileOrFolder(paths:list,new_names:list)->None:
    if len(paths) != len(new_names):
        raise ValueError("The lengths of `paths` and `new_names` must be the same.")
    
    for path, new_name in zip(paths,new_names):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path '{path}' does not exist.")
    
        dir_name = os.path.dirname(path)
        new_path = os.path.join(dir_name, new_name)
        os.rename(path, new_path)

@tool
def renameFileOrFolderTool(paths:list,new_names:list)->None:
    """ Takes as input a list of paths and names. It renames every file or folder in the list of paths
        to the name present in the list 'new_names'. Does not return anything.
    """
    renameFileOrFolder(paths,new_names)
