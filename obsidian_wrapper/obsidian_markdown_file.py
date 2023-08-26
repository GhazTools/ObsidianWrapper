"""
file_name = obsidian_file.py
Creator: Ghazanfar Shahbaz
Last Updated: 08/20/2023
Description: Instantiates the ObsidianFile class
Edit Log:
07/30/202
    - Created file
"""

from typing import Dict, Set, List, Tuple

from re import findall

class ObsidianMarkdownFile:
    def __init__(self, file_name: str, file_path: str):
        self._file_name = file_name
        self._file_path = file_path

        file_information = self.__get_file_information__()
        
        self._connections = file_information["markdown_connections"]
        self._links_and_aliases = file_information["links_and_aliases"]
        self._total_connections = file_information["total_connections"]
        self._unique_connections = file_information["unique_connections"]
        
    # PROPERTIES
    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def connections(self) -> str:
        return self._connections
    
    @property 
    def links_and_aliases(self) -> Dict[str, Set[str]]:
        return self._links_and_aliases
    
    @property
    def total_connections(self) -> int:
        return self._total_connections
        
    @property 
    def unique_connections(self) -> int:
        return self._unique_connections
    
    # PRIVATE FUNCTIONS
    def __get_file_information__(self) -> None:
        def process_markdown_connections(line: str, markdown_connections: Set[str]) -> int:
            matches: List[str] = findall(r"\[\[(.*?)\]\]", line)

            total_connections: int = len(matches)
            
            # TODO: Count of self references and aliased references
            
            for match in matches:
                actual_link: str = ""
                previous_character: str = ""
                self_link: bool = False

                for character in match:
                    # "Ghaz's Notes#Table Of Contents | Contents" -> "Ghaz's Notes"
                    if previous_character != "\\":
                        if character == "#":
                            self_link = True
                            break 
                        if character == "|":
                            break
                    
                    if character != "\\" or previous_character =="\\":
                        actual_link += character
                    previous_character = character

                actual_link.strip()
                if not self_link:
                    markdown_connections.add(actual_link)
                else:
                    markdown_connections.add(self._file_name)
                    
            return total_connections
        
        def process_web_links(line: str, links_and_alias: Dict[str, Set[str]]) -> str:
            # Anything that isn't a square closing bracket
            name_regex: str = "[^]]+"
            # http:// or https:// followed by anything but a closing paren
            url_regex: str = "http[s]?://[^)]+"

            markup_regex: str = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)
            
            matches: List[Tuple(str, str)] = findall(markup_regex, line) # [('Visual Studio Code Theme Studio', 'https://themes.vscode.one/')]

            for alias, link in matches:
                if alias not in links_and_alias:
                    links_and_alias[link] = set()

                links_and_alias[link].add(alias)
            ...
        
        markdown_connections = set()
        links_and_alias: Dict[str, Set[str]] = {}
        total_connections: int = 0
        unique_connections: int = 0
        
        
        with open(self._file_path, "r", encoding="UTF-8") as md_file:
            for line in md_file:
                markdown_link_matches: List[str] = findall(r"\[\[(.*?)\]\]", line)
                
                line_total_connections = process_markdown_connections(line, markdown_connections)
                process_web_links(line, links_and_alias)
                
                total_connections += line_total_connections
                
        unique_connections = len(markdown_connections)

        return {
            "markdown_connections": markdown_connections,
            "links_and_aliases": links_and_alias,
            "total_connections": total_connections,
            "unique_connections": unique_connections,
        }
    
    # TODO: Get connections here instead of in Obsidian class
    # TODO: Function to set how many files referenced this file 
    # TODO: Implement get markdown file
    # TODO: Implement edit markdown file
    # TODO: Implement update connections method
    # TODO: Create markdown context manager
    # TODO: Process tags