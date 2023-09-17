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

from os import listdir, mkdir, stat
from os.path import isdir, join

from re import findall

from obsidian_wrapper.obsidian_markdown_file import ObsidianMarkdownFile

# TODO: Populate and get vault tree structure
# TODO: Add file to vault
# TODO: Folder class


VaultTree = Dict[str, dict or str or ObsidianMarkdownFile]


class ObsidianVault:
    folders_to_ignore: Set[str] = {".obsidian", ".git"}
    files_to_ignore: Set[str] = {".DS_Store", "_TEMPLATES_"}

    def __init__(self, path_to_vault: str):
        self._path_to_vault = path_to_vault

        (
            self._vault_tree,
            self._markdown_files,
            self._other_files,
            self._folders,
            self._vault_size,
        ) = self.__extract_vault_information__()

    # PUBLIC

    # PROPERTIES START HERE

    @property
    def path_to_vault(self) -> str:
        return self._path_to_vault

    @property
    def markdown_files(self) -> Dict[str, ObsidianMarkdownFile]:
        return self._markdown_files

    @property
    def other_files(self) -> Set[str]:
        return self._other_files

    @property
    def vault_tree(self) -> VaultTree:
        return self._vault_tree

    @property
    def folders(self) -> Dict[str, Tuple[str, VaultTree, int]]:
        return self._folders

    @property
    def size(self) -> int:
        return self._vault_size

    # PROPERTIES END HERE

    # PUBLIC FUNCTIONS START HERE

    def reload_vault(self) -> None:
        self._markdown_files, self._other_files = self.__extract_vault_information__()

    # NOTE: this function assumes folder_path does not contain the vault path
    def get_folder(self, folder_path: str) -> Tuple[str, VaultTree, int]:
        if folder_path.startswith("/"):
            folder_path = folder_path[1:]

        vault_path: str = join(self._path_to_vault, folder_path)

        if vault_path.endswith("/"):
            vault_path = vault_path[:-1]

        if not vault_path in self._folders:
            return None

        return self._folders[vault_path]

    # NOTE: this function assumes folder_path does not contain the vault path
    def create_folder(self, folder_path: str, folder_name: str) -> bool:
        # TODO: Check if path to folder exists
        # TODO: Check if folder exists already

        vault_path: str = join(self._path_to_vault, folder_path)

        if not vault_path in self._folders:
            return False

        full_folder_path: str = join(vault_path, folder_name)

        mkdir(full_folder_path)
        nested_dictionary: VaultTree = {}
        self._folders[full_folder_path] = (folder_name, nested_dictionary, 0)
        self._folders[vault_path][1][
            folder_name
        ] = nested_dictionary  # this updates the vault tree structure (due to reference)

        return True

    # NOTE: this function assumes folder_path does not contain the vault path
    def add_markdown_file(self, folder_path: str, file_name: str) -> bool:
        # File names should be unique
        if file_name in self._markdown_files:
            return False

        vault_path: str = join(self._path_to_vault, folder_path)

        if not vault_path in self._folders:
            return False

        full_file_path: str - join(vault_path, file_name + ".md")
        open(full_file_path, "x", encoding="UTF-8")

        markdown_file = ObsidianMarkdownFile(file_name, full_file_path)

        self._markdown_files[file_name] = markdown_file
        self._folders[vault_path][1][
            file_name
        ] = markdown_file  # this updates the vault tree structure (due to reference)

    # TODO: Add support to add other files like png etc. (should be different function)

    # PUBLIC FUNCTIONS END HERE

    # PRIVATE FUNCTIONS START HERE
    def __extract_vault_information__(self) -> any:
        def get_all_files(
            vault_tree: VaultTree,
            markdown_files: Dict[str, str],
            other_files: Set[Tuple[str, str]],
            folders: Dict[str, Tuple[str, VaultTree, int]],
            path: str,
        ) -> int:
            folder_size: int = 0

            for file_name in listdir(path):
                if (
                    file_name in self.files_to_ignore
                    or file_name in self.folders_to_ignore
                ):
                    continue

                current_path: str = join(path, file_name)
                file_stats = stat(current_path)

                if isdir(current_path):
                    nested_dictionary: VaultTree = {}

                    vault_tree[file_name] = nested_dictionary

                    folder_size += get_all_files(
                        vault_tree=nested_dictionary,
                        markdown_files=markdown_files,
                        other_files=other_files,
                        folders=folders,
                        path=current_path,
                    )

                    folders[current_path] = (
                        file_name,
                        nested_dictionary,
                        round(folder_size, 4),
                    )

                elif file_name.endswith(".md"):
                    # Full path is key, value is file name without extension
                    markdown_file_name: str = file_name[: len(file_name) - 3]
                    markdown_file = ObsidianMarkdownFile(
                        markdown_file_name, current_path
                    )

                    markdown_files[markdown_file_name] = markdown_file
                    # vault_tree[markdown_file_name] = markdown_file
                    vault_tree[
                        markdown_file_name
                    ] = current_path  # For debugging purposes

                    folder_size += (
                        file_stats.st_size / 1_000_000
                    )  # TODO: Change to (1024 * 1024) const

                else:
                    other_files.add((current_path, file_name))
                    vault_tree[file_name] = current_path
                    folder_size += (
                        file_stats.st_size / 1_000_000
                    )  # TODO: Change to (1024 * 1024) const

            return round(folder_size, 4)

        vault_tree: VaultTree = {}

        markdown_files: Dict[str, str] = {}
        other_files: Set[Tuple[str, str]] = set()
        folders: Dict[str, Tuple(str, VaultTree, int)] = {}
        path: str = self._path_to_vault

        vault_size: int = get_all_files(
            vault_tree=vault_tree,
            markdown_files=markdown_files,
            other_files=other_files,
            folders=folders,
            path=path,
        )

        folders[self.path_to_vault] = ("", vault_tree, vault_size)
        return vault_tree, markdown_files, other_files, folders, vault_size

    # PRIVATE FUNCTIONS END HERE
