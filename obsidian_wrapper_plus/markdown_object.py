"""
file_name = markdown_object.py
Creator: Ghazanfar Shahbaz
Created On : 10/14/2023
Last Updated: 10/14/2023
Description: A class file for MarkdownObject objects. Which are used to extract useful information from a markdown object.
Edit Log:
10/14/2023
- Base file completed 
"""

# STANDARD LIBRARY IMPORTS
from copy import copy
from typing import Final, List, Tuple, final

# THIRD PARTY LIBRARY IMPORTS
...

# LOCAL LIBRARY IMPORTS
# from obsidian_wrapper_plus.markdown_line import MarkdownLine

# First Element = Markdown Type, Second Element = Markdown Content, Third Element = Extra Attributes
MarkdownTypeCheck: type = Tuple[str, str, str]

@final
class MarkdownObject:
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

    def __init__(self, line: str, index: int, previous_attribute: "MarkdownObject"):
        self._lines: List[str] = [line.rstrip()]
        self._raw_line: List[str] = []

        self._information: List[str] = []
        self._index: int = index

        attribute_info = self.__extract_attribute__(
            previous_attribute=previous_attribute
        )

        self._attribute = attribute_info[0]
        self._raw_line.append(attribute_info[1])

        self._information.append(attribute_info[2])

        # TODO: Process each word so we can check for tags, code blocks, quotes, etc.
        # TODO: Detection for previous line ex previous line is a list, and next line is a nested list

    # PROPERTIES START HERE

    @property
    def line(self) -> List[str]:
        return self._lines

    @property
    def raw_line(self) -> List[str]:
        return self._raw_line

    @property
    def index(self) -> int:
        return self._index

    @property
    def attribute(self) -> str:
        return self._attribute

    @property
    def information(self) -> List[str]:
        return self._information

    # PROPERTIES END HERE

    # PUBLIC METHODS START HERE
    ...
    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE

    def __extract_attribute__(self, previous_attribute: str) -> Tuple[str, str, str]:
        line: Final[str] = copy(self._lines[-1]).rstrip()
        
        # CHECKS START HERE 

        def code_block_check() -> MarkdownTypeCheck:
            has_code_block_chars: bool = line.startswith("```")
            
            if has_code_block_chars: 
                if previous_attribute == "code-block" or previous_attribute == "code-block-line":
                    return ("code-block-end", "", "")
                else:
                    information: str = ""
                    
                    if len(line) > 3:
                        information = line[3:]  # type of code block ex python, javascript, et
                        
                    return ("code-block", "", information)
            
            if  not (previous_attribute == "code-block" or previous_attribute == "code-block-line"):
                return ("", "", "")
            else:
                return ("code-block-line", line, "")
        
        def header_check() -> MarkdownTypeCheck:
            if not line.startswith("#"):
                return ("", "", "")
            
            last_header_tag_index: int = 0
            
            # Only support up to h6
            while(last_header_tag_index <= 6 and line[last_header_tag_index] == "#"):
                last_header_tag_index += 1
                
            if last_header_tag_index <= 6:
                return (f"h", line[last_header_tag_index + 1 :], str(last_header_tag_index))
            else:
                # Regular text type if > h6
                return ("text", line, "")
            
        def block_quote_check() -> MarkdownTypeCheck:
            if line.startswith(">"):
                return ("block-quote", line[1:], "")
            
            return ("", "", "")
        
        def list_and_checkbox_check() -> MarkdownTypeCheck:
            number_of_tabs: int = 0
            
            while line[number_of_tabs] == "\t":
                number_of_tabs += 1
                
            stripped_line: str = line[number_of_tabs:].strip()
            
            if not stripped_line.startswith("-"):
                return ("", "", "")
            
            stripped_line = stripped_line[1:]
            
            # TODO: Consider removing this, as it is technically a list/checkbox just not supported by highlighter.
            if stripped_line[0] != " ":
                return "text", line, ""
            
            stripped_line = stripped_line.lstrip()
            
            # For the time being ignore number of tabs for lists and checkboxes
            if stripped_line[0:2] == "[]":
                return ("checkBox", stripped_line, "unchecked")
            
            elif stripped_line[0:3] == "[x]":
                return ("checkBox", stripped_line, "checked")
            
            return ("list", stripped_line, str(number_of_tabs))

        # CHECKS END HERE
        
        def check_passed(check_result: MarkdownTypeCheck) -> bool:
            return check_result[0] != ""

        line: str = copy(self._lines[-1]).rstrip()
        
        checks: Final[List[MarkdownTypeCheck]] = [
            code_block_check(),
            header_check(),
            block_quote_check(),
            list_and_checkbox_check()
        ]
        
        for check in checks:
            if check_passed(check):
                return check 
        
        return ("text", line, "")

    # PRIVATE METHODS END HERE
