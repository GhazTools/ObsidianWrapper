"""
file_name = file_stats.py
Created On: 2023/10/24
Lasted Updated: 2023/10/24
Description: A base file for the file statistics class.
Edit Log:
2023/10/24
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from datetime import datetime
from os import stat, stat_result
...

# THIRD PARTY LIBRARY IMPORTS
...

# LOCAL LIBRARY IMPORTS
...

class FileStats:
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

    # INITIALIZATION AND SETUP FUNCTIONS START HERE 

    def __init__(self, file_name: str) -> None:
        self._file_name: str = file_name

        file_stats: stat_result = stat(self._file_name)

        self._creation_timestamp: float = file_stats.st_birthtime
        self._last_accessed_timestamp: float = file_stats.st_atime
        self._last_modified_timestamp: float = file_stats.st_ctime
        self._metadata_changed_timestamp: float = file_stats.st_mtime

        self._size: float = file_stats.st_size / 1_000_000
        self._creator: str = file_stats.st_creator
        self._file_type: str = file_stats.st_type

    # INITIALIZATION AND SETUP FUNCTIONS END HERE 

    # PROPERTIES START HERE
    ...     
    # PROPERTIES END HERE

    # PUBLIC METHODS START HERE
    ...
    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE
    def timestamp_to_datetime(self, timestamp: float) -> datetime:
        """
        Converts a timestamp to a datetime object.

        Args:
            timestamp (float): The timestamp to convert.

        Returns:
            datetime: The datetime object representing the timestamp.
        """

        return datetime.fromtimestamp(timestamp)
    
    ...
    # PRIVATE METHODS END HERE

    
