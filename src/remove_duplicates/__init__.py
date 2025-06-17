import os
from pathlib import Path
import sys

__CURRENT_DIR__ = Path(__file__).parent.resolve()
__PKG_ROOT_DIR__ = __CURRENT_DIR__.resolve()
__TEMP_DIR__ = os.path.join(__PKG_ROOT_DIR__, "temp")


def path_exists(path: str) -> bool:
    return os.path.exists(path)


def path_is_dir(path: str) -> bool:
    return os.path.isdir(path)


def remove(path: str) -> None:
    os.remove(path)


def list_dir(path: str) -> list[str]:
    return os.listdir(path)


def main():
    if len(sys.argv) < 3:
        print("Error: Missing parameters: source-path, destination-path")
        print("The source path is the directory where you want to remove duplicates.")
        sys.exit(-1)

    src_path = sys.argv[1]
    if not path_exists(src_path):
        print(f"Error: Source path '{src_path}' does not exist")
        sys.exit(-1)
    if not path_is_dir(src_path):
        print(f"Error: Source path '{src_path}' is not a directory")
        sys.exit(-1)

    dest_path = sys.argv[2]
    if not path_exists(dest_path):
        print(f"Error: Destination path '{dest_path}' does not exist")
        sys.exit(-1)
    if not path_is_dir(dest_path):
        print(f"Error: Destination path '{dest_path} is not a directory")
        sys.exit(-1)

    if src_path == dest_path:
        print("Error: Source and destination paths are the same")
        sys.exit(-1)

    print(f"Checking {src_path} for duplicates already in {dest_path}...")
    source_files = os.listdir(src_path)
    dest_files = os.listdir(dest_path)

    dest_files_dict = {file_name: None for file_name in dest_files}
    paths_duplicates = [
        os.path.join(src_path, file_name)
        for file_name in source_files
        if file_name in dest_files_dict
    ]

    if len(paths_duplicates) == 0:
        print("No duplicates found.")
        sys.exit(0)

    print(f"Found {len(paths_duplicates)} duplicate files:")
    for file_path in paths_duplicates:
        print(f" - {file_path}")

    answer = input("Do you want to remove the duplicates? (y/n): ")
    if answer.lower() != "y":
        print("Exiting without removing duplicates.")
        sys.exit(0)

    print("Removing duplicates...")
    for file_path in paths_duplicates:
        os.remove(file_path)
        print(f"Removed {file_path}")
