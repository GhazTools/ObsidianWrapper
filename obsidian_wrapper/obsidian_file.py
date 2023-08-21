"""
file_name = obsidian_file.py
Creator: Ghazanfar Shahbaz
Last Updated: 08/20/2023
Description: Instantiates the ObsidianFile class
Edit Log:
07/30/202
    - Created file
"""

from typing import Set


class ObsidianFile:
    def __init__(self, file_name: str, file_path: str, connections: Set[str]):
        self.__file_name__ = file_name
        self.__file_path__ = file_path
        self.__connections__ = connections

    @property
    def get_file_name(self) -> str:
        return self.file_name

    @property
    def get_file_path(self) -> str:
        return self.file_path

    @property
    def get_connections(self) -> str:
        return self.connections
