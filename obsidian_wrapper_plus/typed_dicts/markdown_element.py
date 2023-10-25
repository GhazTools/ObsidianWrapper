"""
file_name = markdown_element.py
Created On: 2023/10/15
Lasted Updated: 2023/10/15
Description: A base file for Markdown Element class.
Edit Log:
2023/10/15
    - Created file
"""


# STANDARD LIBRARY IMPORTS
from typing import TypedDict, List

# THIRD PARTY LIBRARY IMPORTS
...

# LOCAL LIBRARY IMPORTS
...

# https://stackoverflow.com/questions/48254562/python-equivalent-of-typescript-interface#:~:text=A%20TypeScript%20interface%20describes%20a,is%20described%20by%20a%20TypedDict.
class MarkdownElement(TypedDict):
    """
    Represents a Markdown element with a type and content.
    """

    type: List[str]
    content: str

