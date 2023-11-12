"""
file_name = markdown_file.py
Created On: 2023/10/24
Lasted Updated: 2023/10/24
Description: An object that represents a markdown file.
Edit Log:
2023/10/24
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from os import stat
from re import findall
from typing import Dict, List, Set, Tuple
...

# THIRD PARTY LIBRARY IMPORTS
...

from obsidian_wrapper_plus.markdown_line import MarkdownLine
# LOCAL LIBRARY IMPORTS
from obsidian_wrapper_plus.markdown_object import MarkdownObject

...

class MarkdownFile:
    """
    __FILL OUT HERE_

    Args:
        arg1 (type): description
        ...

    Attributes:
        attr1 (type): description
        ...

    Properties:
        prop1 (type): description
        ...

    Methods:
        methodName: description
        ...

    """
    
    def __init__(self, file_name: str, file_path: str):
        self._file_name: str = file_name
        self._file_path: str = file_path
        
        file_information = self.__get_file_information__()
        
        self._connections = file_information["markdown_connections"]
        self._links_and_aliases = file_information["links_and_aliases"]
        self._total_connections = file_information["total_connections"]
        self._unique_connections = file_information["unique_connections"]
        ...

    # PROPERTIES START HERE
    
    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def file_path(self) -> str:
        return self._file_path
    
    # PROPERTIES END HERE

    # PUBLIC METHODS START HERE
    ...
    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE
    def __get_file_information__(self) -> None:
        def process_markdown_connections(line: str, markdown_connections: Set[str]) -> int:            
            matches: List[str] = findall(r"\[\[(.*?)\]\]", line)
            total_connections: int = len(matches)
            
            # TODO: Count of self references and aliased references 
            
            for match in matches:
                actual_link: str = ""
                previous_character = "",
                self_link: bool = False 

                # TODO: Save referenced header section
                # TODO: Save referenced aliased name 

                for character in match:
                    # "Ghaz's Notes#Table Of Contents | Contents" -> "Ghaz's Notes"
                    if previous_character != "\\":
                        if character == "#":
                            self_link = True
                            break
                        if character == "|":
                            break
                        
                    # Check for escape character, which will let us figure out if something is aliased and/or self referenced
                    if character != "\\" or previous_character == "\\":
                        actual_link += character

                    previous_character = character
                    
                actual_link = actual_link.strip()
                
                if self_link:
                    markdown_connections.add(self._file_name)
                else:
                    markdown_connections.add(actual_link)

            return total_connections
            
        def process_web_links(line: str, links_and_alias: Dict[str, Set[str]]) -> None:
            # Anything that isn't a square closing bracket
            name_regex: str = "[^]]+"
            # http:// or https:// followed by anything but a closing paren
            url_regex: str = "http[s]?://[^)]+"
            
            markup_regex: str = "\[({0})]\(\s*({1})\s*\)".format(name_regex, url_regex)
            matches: List[Tuple(str, str)] = findall(
                markup_regex, line
            )  # [('Visual Studio Code Theme Studio', 'https://themes.vscode.one/')]

            for alias, link in matches:
                if alias not in links_and_alias:
                    links_and_alias[link] = set()

                links_and_alias[link].add(alias)
        
        # TODO : Process image links in markdown
        def process_image_links(line: str, images: Dict[str, Set[str]]) -> None:
            ... 
            
        markdown_connections: Set[str] = set()
        links_and_alias: Dict[str, Set[str]] = {}
        total_connections: int = 0
        unique_connections: int = 0

        with open(self.file_path, "r", encoding="UTF-8") as md_file:
            for line in markdown_file:
                line_connections_total: int = process_markdown_connections(line, markdown_connections)
                process_web_links(line, links_and_alias)
                total_connections += line_connections_total
                ...
        
        unique_connections = len(markdown_connections)
             
        return {
            "markdown_connections": markdown_connections,
            "links_and_aliases": links_and_alias,
            "total_connections": total_connections,
            "unique_connections": unique_connections,
        }
        
    def __get_file_properties__(self) -> None:
        ...
    
    # TODO: Get connections here instead of in Obsidian class
    # TODO: Function to set how many files referenced this file
    # TODO: Implement get markdown file
    # TODO: Implement edit markdown file
    # TODO: Implement update connections method
    # TODO: Create markdown context manager
    # TODO: Process tags
    
    # PRIVATE METHODS END HERE

    