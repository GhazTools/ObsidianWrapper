from copy import copy

from typing import Dict, List

from re import findall

class MarkdownObject:
    def __init__(self, line: str, index: int):
        self._lines: List[str] = [line.rstrip()]
        self._index: int = index
        self._attribute: str = self.__extract_attribute__()
        
        # TODO: Process each word so we can check for tags, code blocks, quotes, etc.
        # TODO: Detection for previous line ex previous line is a list, and next line is a nested list
        # TODO: Add in line code block detection
        # self._contains_code_block: bool = False 
        # self.code_block_closed: bool = False 
        
    @property 
    def line(self) -> List[str]:
        return self._lines
    
    @property 
    def index(self) -> int:
        return self._index 
    
    @property
    def attribute(self) -> str:
        return self._attribute
    
    def add_to_line(self, line: str) -> bool:
        self._lines.append(line)
        return True 
    
    def __extract_attribute__(self) -> str:
        line: str = copy(self._lines[-1])
        
    #     # check for headers
        if line.startswith("#"):
            for index, character in enumerate(line):
                if character != "#":
                    if(index <= 6): return f"h{index}"
                    else: return "text"

        # check for list and checkboxes
        if line.startswith("-"):
            line = line[1:]
            
            if line[0] != " ":
                return "text"
                         
            line = line.lstrip()
            
            if line[0:2] == "[]":
                return "checkBox-unchecked"
            if line[0:3] == "[x]":
                return "checkBox-checked" 
        
            return "list"

        jls_extract_var = "text"
        return jls_extract_var
                    