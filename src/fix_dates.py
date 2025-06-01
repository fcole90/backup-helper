import os
import sys


def main() -> None:
    if len(sys.argv) <= 1:
        print("Error: Missing an argument for path")
        sys.exit(-1)

    path = sys.argv[1]
    print(f"Path: {path}")

    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist")

    files_list = os.listdir(path)
    for file_name in files_list:
        print(file_name)
