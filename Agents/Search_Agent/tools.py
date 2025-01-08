from langchain_core.tools import tool
from pathlib import Path


def searchForFile(dir:str,file_name:str)->list:
    all_dirs = [dir]
    if '/' in dir and not Path(dir).is_dir():
        raise ValueError(f"The {dir} does not exist")
    if not Path(dir).is_dir():
        all_dirs = findFolderByName(dir)
    matching_files = []
    file_name_lower = file_name.lower()
    for dir_path in all_dirs:
        for file in Path(dir_path).rglob('*'):
            if file.is_file() and file.name.lower().startswith(file_name_lower):
                matching_files.append(str(file))  # Add full path of the matching file
    
    return matching_files

def findFolderByName(target_dir_name:str)->list:
    if target_dir_name.lower() =='desktop':
        return [str(Path.home()/"Desktop")]
    all_dirs = []
    root_dir = Path.home()
    for path in root_dir.rglob(target_dir_name):  # rglob searches recursively
        if path.is_dir():
            all_dirs.append(str(path))  # Returns the full path of the found directory
    return all_dirs    



def searchForFileTool(dir:str, file_name:str)->list:
    """
        Returns a list of all files that start with the given name in the given directory/folder
       
        args:
        dir(str): The path or the name of the directory in which the user wishes to search
        file_name(str): The name of the file the user wishes to search for
        
        Returns:
        list: A list of paths to matching files.
    """
    return searchForFile(dir,file_name)


@tool
def findFolderByNameTool(target_dir_name:str)->list:
    """
        Returns all paths to folders of a given name

        args:
        target_dir_name(str): name of the folder that the user is searching for

        Returns:
        list: A list of paths to matching folders.
    """
    return findFolderByName(target_dir_name)

