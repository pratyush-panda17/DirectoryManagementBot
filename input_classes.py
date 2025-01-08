from typing_extensions import TypedDict


class SearchAgent(TypedDict):
    file_name:str
    folder_name:str

class RenameFilesAgent(TypedDict):
    paths:list
    new_names:list

class MoveFilesAgent(TypedDict):
    destination_path:str
    paths_to_move:list

class DeleteAgent(TypedDict):
    paths:list

class CreateFolderAgent(TypedDict):
    path:str
    name:str
