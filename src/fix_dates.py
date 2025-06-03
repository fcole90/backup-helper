import datetime
import os
from pathlib import Path
import shutil
import sys

__CURRENT_DIR__ = Path(__file__).parent.resolve()
__PKG_ROOT_DIR__ = __CURRENT_DIR__.resolve()
__TEMP_DIR__ = os.path.join(__PKG_ROOT_DIR__, "temp")


def parse_date_from_file_name(file_name: str) -> datetime.datetime | Exception:
    file_name_no_ext = os.path.splitext(file_name)[0]

    # Default camera format YYYYmmdd_HHMMSS
    if file_name_no_ext[0:4].isnumeric():
        try:
            base_name = file_name_no_ext[: len("YYYYmmdd_HHMMSS")]
            return datetime.datetime.strptime(base_name, "%Y%m%d_%H%M%S")
        except ValueError:
            pass

    # Alternative camera formats
    # E.g.
    # IMG_YYYYmmdd_HHMMSS_fff
    # VID_YYYYmmdd_HHMMSS_fff
    # VID_YYYYmmdd_HHMMSS
    # VID-YYYYmmdd-XXXXXX
    if file_name_no_ext.startswith("IMG") or file_name_no_ext.startswith("VID"):
        # Datetime with ms
        try:
            return datetime.datetime.strptime(
                file_name_no_ext[len("IMG_") : len("IMG_YYYYmmdd_HHMMSS_fff")],
                "%Y%m%d_%H%M%S_%f",
            )
        except ValueError:
            pass

        # Only Datetime (without ms)
        try:
            return datetime.datetime.strptime(
                file_name_no_ext[len("IMG_") : len("IMG_YYYYmmdd_HHMMSS")],
                "%Y%m%d_%H%M%S",
            )
        except ValueError:
            pass

        # Only Date
        try:
            return datetime.datetime.strptime(
                file_name_no_ext[len("IMG_") : len("IMG_YYYYmmdd")],
                "%Y%m%d",
            )
        except ValueError:
            pass

    # Screen recordings
    # Screen_Recording_YYYYmmdd-HHMMSS_AppName
    # Screen_Recording_YYYYmmdd_HHMMSS_AppName
    if file_name_no_ext.startswith("Screen_Recording"):
        # Using dash separator
        screen_recording_base_name = file_name_no_ext[
            len("Screen_Recording_") : len("Screen_Recording_YYYYmmdd-HHMMSS")
        ]
        try:
            return datetime.datetime.strptime(
                screen_recording_base_name,
                "%Y%m%d-%H%M%S",
            )
        except ValueError:
            pass

        # Using underscore separator
        try:
            return datetime.datetime.strptime(
                screen_recording_base_name,
                "%Y%m%d_%H%M%S",
            )
        except ValueError:
            pass

    return Exception(f"Could not parse file name: {file_name}")


def update_file_times(
    dir_path: str, file_name: str, times: tuple[int, int] | tuple[float, float]
) -> None:
    # We need to move the file to a temporary location, as depending on the file system
    # it may not be possible to change the creation and modification times.
    os.makedirs(__TEMP_DIR__, exist_ok=True)
    file_path = os.path.join(dir_path, file_name)
    temp_file_path = os.path.join(__TEMP_DIR__, file_name)
    shutil.move(file_path, temp_file_path)
    os.utime(temp_file_path, times)
    shutil.move(temp_file_path, file_path)


def main() -> None:
    if len(sys.argv) <= 1:
        print("Error: Missing an argument for path")
        sys.exit(-1)

    dir_path = sys.argv[1]
    print(f"Path: {dir_path}")

    if not os.path.exists(dir_path):
        print(f"Error: Path '{dir_path}' does not exist")

    files_list = sorted(os.listdir(dir_path))
    files_fixed: list[str] = []
    files_not_parsed_list: list[str] = []
    for file_name in files_list:
        file_path = os.path.join(dir_path, file_name)
        if not os.path.isfile(file_path):
            continue

        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        parsed_creation_time = parse_date_from_file_name(file_name)
        print(
            f"{file_name} - Created: {creation_time}, Modified: {modification_time}, Parsed: {parsed_creation_time}"
        )
        if isinstance(parsed_creation_time, Exception):
            files_not_parsed_list.append(file_name)
            continue

        creation_time_diff = abs((creation_time - parsed_creation_time).days)
        if abs(creation_time_diff) > 2:
            print(
                f"\tUpdating creation time as it differs {creation_time_diff} days...",
                end=" ",
            )
            update_file_times(
                dir_path,
                file_name,
                (parsed_creation_time.timestamp(), modification_time.timestamp()),
            )
            files_fixed.append(file_name)
            print("Done.")
    print()

    if len(files_fixed) > 0:
        print("Files fixed:")
        for file_name in files_fixed:
            print(f"{file_name}")
    print()

    if len(files_not_parsed_list) > 0:
        print("Files not parsed:")
        for file_name in files_not_parsed_list:
            print(f"{file_name}")
    print()
