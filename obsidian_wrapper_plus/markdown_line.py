"""
file_name = markdown_file.py
Creator: Ghazanfar Shahbaz
Created On : 10/09/2023
Last Updated: 10/09/2023
Description: A class file for MarkdownLine objects. Which are used to extract useful information from a markdown file.
Edit Log:

10/14/2023
- Base file finished 

"""

# STANDARD LIBRARY IMPORTS
from copy import copy
from enum import Enum
from typing import Dict, Final, List, Set, final

# THIRD PARTY LIBRARY IMPORTS
...

# LOCAL LIBRARY IMPORTS
from obsidian_wrapper_plus.typed_dicts.markdown_element import MarkdownElement


# https://www.markdownguide.org/cheat-sheet/
@final
class ATTRIBUTE_TYPES(Enum):
    """
    Represents different attribute types for Markdown elements.
    """

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    STRIKETHROUGH = "strikethrough"
    CODE = "code"
    ...
    # NOT SUPPORTED YET
    # REQUIRES ALGORITHM CHANGE
    ...
    # LINK = "link"
    # IMAGE = "image"
    # SUBSCRIPT = "subscript"
    # SUPERSCRIPT = "superscript"
    # EMOJI = "emoji"


# A mapping of symbols to attribute types for Markdown elements.
SYMBOL_MAPPER: Final[Dict[str, ATTRIBUTE_TYPES]] = {
    "*": ATTRIBUTE_TYPES.BOLD.value,
    "_": ATTRIBUTE_TYPES.ITALIC.value,
    "~": ATTRIBUTE_TYPES.STRIKETHROUGH.value,
    "`": ATTRIBUTE_TYPES.CODE.value,
    ...: ...,
    # NOT SUPPORTED YET, these can probably be processed after
    # REQUIRES ALGORITHM CHANGE
    ...: ...
    # "[": ATTRIBUTE_TYPES.LINK,
    # "!": ATTRIBUTE_TYPES.IMAGE,
    # "^": ATTRIBUTE_TYPES.SUPERSCRIPT,
    # ",": ATTRIBUTE_TYPES.SUBSCRIPT,
    # ":": ATTRIBUTE_TYPES.EMOJI,
}

SYMBOL_MAPPER_KEYS: Final[Set[str]] = set(SYMBOL_MAPPER.keys())

MarkdownElements: type = List[Dict[int, MarkdownElement]]


@final
class MarkdownLine:
    """
    Represents a line of Markdown text.

    Args:
        raw_line (str): The raw line of Markdown text.

    Attributes:
        raw_line (str): The raw line of Markdown text.
        markdown_elements (MarkdownElements): A list of dictionaries representing the extracted Markdown elements.

    Properties:
        raw_line (str): Get the raw line of Markdown text.
        markdown_elements (MarkdownElements): Get the extracted Markdown elements.

    Methods:
        __extract_markdown_elements__: Extracts the Markdown elements from the raw line.

    """

    def __init__(self, raw_line: str) -> None:
        """
        Initializes a MarkdownLine object.

        Args:
            line (str): The raw line of Markdown text.

        """

        self.__raw_line: Final[str] = raw_line

        self.__markdown_elements: Final[
            MarkdownElements
        ] = self.__extract_markdown_elements__()

    # PROPERTIES START HERE

    @property
    def raw_line(self) -> str:
        """
        Get the raw line of Markdown text.

        Returns:
            str: The raw line of Markdown text.

        """

        return self.__raw_line

    @property
    def markdown_elements(self) -> MarkdownElements:
        """
        Get the extracted Markdown elements.

        Returns:
            MarkdownElements: A list of dictionaries representing the extracted Markdown elements.
        """

        return self.__markdown_elements

    # PROPERTIES END HERE
    
    # OVERRIDE METHOD STARTS HERE
    
    def __iter__(self):
        return iter([
            ("markdown_elements", self.__markdown_elements)
        ])
    
    # OVERRIDE METHOD ENDS HERE

    # PUBLIC METHODS START HERE
    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE

    def __extract_markdown_elements__(self) -> MarkdownElements:
        """
        Extracts the Markdown elements from the raw line.

        Returns:
            MarkdownElements: A list of dictionaries representing the extracted Markdown elements.
        """

        def append_to_markdown_elements(attribute_stack, current_string) -> None:
            """
            Appends a Markdown element to the markdown_elements list.

            Args:
                attribute_stack: The current stack of attribute types.
                current_string: The current string content.

            Returns:
                None
            """

            current_markdown_element: MarkdownElement = MarkdownElement(
                type=copy(attribute_stack), content=current_string
            )

            markdown_elements.append({current_index: current_markdown_element})

        line: Final[str] = self.raw_line

        markdown_elements: MarkdownElements = []
        attribute_stack: [str] = []
        current_index: int = 0
        current_string: str = ""

        for index, character in enumerate(line):
            if character in SYMBOL_MAPPER_KEYS:
                append_to_markdown_elements(attribute_stack, current_string)

                current_index += 1
                current_string = ""

                symbol_type: str = SYMBOL_MAPPER[character]

                if attribute_stack and attribute_stack[-1] == symbol_type:
                    attribute_stack.remove(symbol_type)
                else:
                    attribute_stack.append(symbol_type)
            else:
                current_string += character

        if current_string:
            append_to_markdown_elements(attribute_stack, current_string)

        return markdown_elements

    # PRIVATE METHODS END HERE


"""
Purpose of this file?
This file is used to extract useful information from a markdown file.

The main functionality is done in the __extract_markdown_attributes__ method
The idea is to take a markdown line something like this (with object properties extracted)
"This is a *bold*, this is a *bolded word with an __italicized word__ inside of it*"
And then convert it into something like this:
{
    "1": {
        "type": [],
        "content": "This is a",
    }
    "2": {
        "type": ["bold"],
        "content": "bold",
    }
    "3": {
        "type": [],
        "content": ", this is a",
    }
    "4": {
        "type": ["bold"],
        "content": "bolded word with an",
    }
    "5": {
        "type": ["bold", "italic"],
        "content": "italicized word",
    },
    "6": {
        "type": ["bold"],
        "content": "inside of it",
    }
}
"""
