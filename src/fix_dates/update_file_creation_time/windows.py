from typing import cast
import pywintypes, win32file, win32con


def update_file_creation_time(file_path: str, time: int | float) -> None:
    """From: https://stackoverflow.com/a/4996407/2219492"""

    wintime = pywintypes.Time(time)
    winfile = win32file.CreateFile(
        file_path,
        win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ
        | win32con.FILE_SHARE_WRITE
        | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None,
    )

    winfile_int = cast(int, winfile)  # The type seems incompatible
    win32file.SetFileTime(winfile_int, wintime, None, None)

    winfile.close()
