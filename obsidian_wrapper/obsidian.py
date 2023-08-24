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

from obsidian_wrapper.obsidian_file import ObsidianFile

class Obsidian:
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
    def markdown_files(self) -> Dict[str, str]:
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
                    markdown_files[current_path] = file_name[: len(file_name) - 3]
                else:
                    other_files.add((current_path, file_name))
                    
        def extract_markdown_links(path_to_file: str, markdown_files: Set[str]) -> Set[str]:
            links: Set[str] = set()

            with open(path_to_file, "r", encoding="UTF-8") as md_file:
                for line in md_file:
                    matches: List[str] = findall(r"\[\[(.*?)\]\]", line)

                    for match in matches:
                        actual_link: str = ""
                        previous_character: str = ""

                        for character in match:
                            # "Ghaz's Notes#Table Of Contents | Contents" -> "Ghaz's Notes"
                            if previous_character != "\\" and character == "#" or character == "|":
                                break

                            actual_link += character
                            previous_character = character

                        actual_link = actual_link.strip()
                        # TODO: LOOK FOR A BETTER SOLUTION
                        markdown_exists: bool = False
                        
                        for path, file_name in markdown_files.items():
                            if file_name == actual_link:
                                markdown_exists = True
                                break
                        
                        if markdown_exists: 
                            links.add(actual_link)

            return links

        markdown_files: Dict[str, str] = {}
        other_files: Set[Tuple[str, str]] = set()
        path: str = self._path_to_vault

        get_all_files(markdown_files, other_files, path)
        
        obsidian_files: Dict[str, ObsidianFile] = {}
        
        for file_path, file_name in markdown_files.items():
            connections: Set[str] = extract_markdown_links(file_path, markdown_files)
            obsidian_file: ObsidianFile = ObsidianFile(file_name, file_path, connections)
            
            obsidian_files[file_name] = obsidian_file

        return obsidian_files, other_files
