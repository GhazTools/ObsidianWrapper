"""
file_name = receiver.py
Creator: Ghazanfar Shahbaz
Last Updated: 08/20/2023
Description: Instantiates the ObsidianWrapper class
Edit Log: 
07/30/2023 
    - Created file
"""

from typing import Dict, Set, Tuple

from os import listdir
from os.path import isdir

from re import findall

from obsidian_wrapper.obsidian_markdown_file import ObsidianMarkdownFile

# TODO: Populate and get vault tree structure
# TODO: Add file to vault 

class ObsidianVault:
    folders_to_ignore: Set[str] = {".obsidian", ".git"}
    files_to_ignore: Set[str] = {".DS_STORE"}

    def __init__(self, path_to_vault: str):
        self._path_to_vault = path_to_vault
        self._markdown_files, self._other_files = self.__extract_vault_information__()

    # PUBLIC
    @property 
    def path_to_vault(self) -> str:
        return self._path_to_vault
    
    @property
    def markdown_files(self) -> Dict[str, ObsidianMarkdownFile]:
        return self._markdown_files
    
    @property
    def other_files(self) -> Set[str]:
        return self._other_files
    
    def reload_vault(self) -> None:
        self._markdown_files, self._other_files = self.__extract_vault_information__()

    # PRIVATE
    def __extract_vault_information__(self) -> any:
        def get_all_files(markdown_files: Dict[str, str], other_files: Set[Tuple[str, str]], path: str) -> None:
            for file_name in listdir(path):
                if (file_name in self.files_to_ignore or file_name in self.folders_to_ignore):
                    continue

                current_path: str = f"{path}/{file_name}"

                if isdir(current_path):
                    get_all_files(markdown_files, other_files, current_path)
                elif file_name.endswith(".md"):
                    # Full path is key, value is file name without extension
                    markdown_file_name: str = file_name[: len(file_name) - 3]
                    markdown_files[markdown_file_name] = ObsidianMarkdownFile(markdown_file_name, current_path)
                else:
                    other_files.add((current_path, file_name))

        markdown_files: Dict[str, str] = {}
        other_files: Set[Tuple[str, str]] = set()
        path: str = self._path_to_vault

        get_all_files(markdown_files, other_files, path)
        
        return markdown_files, other_files
