from langchain_core.tools import tool
import os
import shutil


def deleteFileOrFolder(paths:list)->None:
    for path in paths:
        if os.path.exists(path):
            try:
                if os.path.isfile(path):  # Check if it's a file
                    os.remove(path)
                elif os.path.isdir(path):  # Check if it's a directory
                    shutil.rmtree(path)
                else:
                    print(f"Unknown path type (not file or folder): {path}")
            except Exception as e:
                raise ValueError(f"Error deleting {path}: {e}")
        else:
            raise ValueError(f"The path {path} does not exist")

@tool
def deleteFileOrFolderTool(paths:list)->None:
    """ Deletes all files and folders given their path. Takes as input a list of paths. Returns nothing"""
    deleteFileOrFolder(paths)

# deleteFileOrFolder(paths =['/Users/joey/Desktop/temp'] )