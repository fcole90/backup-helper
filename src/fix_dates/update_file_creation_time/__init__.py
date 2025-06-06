import platform


def update_file_creation_time(file_path: str, time: int | float) -> None:
    if platform.system() != "Windows":
        raise ValueError("Creation time can only be set on Windows at the moment")

    from src.fix_dates.update_file_creation_time.windows import (
        update_file_creation_time,
    )

    return update_file_creation_time(file_path, time)
