from copy import copy

from typing import Dict, List, Tuple

from re import findall


class MarkdownObject:
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
        # TODO: Add in line code block detection
        # self._contains_code_block: bool = False
        # self.code_block_closed: bool = False

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

    def add_to_line(self, line: str) -> bool:
        self._lines.append(line)
        return True

    def add_to_information(self, information: str) -> bool:
        self._lines.append(line)
        return True

    def add_to_raw_lines(self, raw_line: str) -> bool:
        self._lines.append(raw_line)
        return True

    def code_block_closed(self) -> bool:
        return False

    def __extract_attribute__(self, previous_attribute: str) -> Tuple[str, str, str]:
        line: str = copy(self._lines[-1]).rstrip()

        if (
            previous_attribute == "code-block"
            or previous_attribute == "code-block-line"
        ):
            if line.startswith("```"):
                return "code-block-end", "", ""
            else:
                return "code-block-line", line, ""

        # check for headers
        if line.startswith("#"):
            for index, character in enumerate(line):
                if character != "#":
                    if index <= 6:
                        return f"h", line[index + 1 :], str(index)
                    else:
                        return "text", line, ""

        if line.startswith("```"):
            information: str = ""

            if len(line) > 3:
                information = line[3:]  # type of code block ex python, javascript, etc.

            return "code-block", "", information

        if line.startswith(">"):
            return "block-quote", line[1:], ""

        # check for list and checkboxes
        number_of_tabs = 0

        for char in line:
            if char == "\t":
                number_of_tabs += 1
            else:
                break

        stripped_line = line[number_of_tabs:].strip()

        if stripped_line.startswith("-"):
            stripped_line = stripped_line[1:]

            if stripped_line[0] != " ":
                return "text", line, ""

            stripped_line = stripped_line.lstrip()

            # For the time being ignore number of tabs for lists and checkboxes
            if stripped_line[0:2] == "[]":
                return (
                    "checkBox",
                    stripped_line,
                    "unchecked",
                )  # if number_of_tabs == 0 else f"checkbox-unchecked-nested-{number_of_tabs}"
            if stripped_line[0:3] == "[x]":
                return (
                    "checkBox",
                    stripped_line,
                    "checked",
                )  # if number_of_tabs == 0 else f"checkbox-checked-nested-{number_of_tabs}"

            return (
                "list",
                stripped_line,
                str(number_of_tabs),
            )  # if number_of_tabs == 0 else f"list-nested-{number_of_tabs}"

        return "text", line, ""
