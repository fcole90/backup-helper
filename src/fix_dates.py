import datetime
import os
import sys


def parse_file_name_date(file_name: str) -> datetime.datetime | Exception:

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


def main() -> None:
    if len(sys.argv) <= 1:
        print("Error: Missing an argument for path")
        sys.exit(-1)

    dir_path = sys.argv[1]
    print(f"Path: {dir_path}")

    if not os.path.exists(dir_path):
        print(f"Error: Path '{dir_path}' does not exist")

    files_list = sorted(os.listdir(dir_path))
    files_not_parsed_list: list[str] = []
    for file_name in files_list:
        file_path = os.path.join(dir_path, file_name)
        if not os.path.isfile(file_path):
            continue

        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        parsed_time = parse_file_name_date(file_name)
        print(
            f"{file_name} - Created: {creation_time}, Modified: {modification_time}, Parsed: {parsed_time}"
        )
        if isinstance(parsed_time, Exception):
            files_not_parsed_list.append(file_name)
            continue

        creation_time_diff = abs((creation_time - parsed_time).days)
        if abs(creation_time_diff) > 2:
            print(
                f"\tUpdating creation time as it differs {creation_time_diff} days...",
                end=" ",
            )
            os.utime(
                file_path, (parsed_time.timestamp(), modification_time.timestamp())
            )
            print("Done.")
    print()

    if len(files_not_parsed_list) > 0:
        print("Files not parsed:")
        for file_name in files_not_parsed_list:
            print(f"{file_name}")
