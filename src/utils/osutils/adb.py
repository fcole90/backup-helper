__ADB_PREFIX__ = "adb:"


from utils.osutils import core


def is_adb_path(path: str) -> bool:
    return path.startswith(__ADB_PREFIX__)


def strip_adb_prefix(path: str) -> str:
    if not is_adb_path(path):
        raise ValueError(f"Path is not on adb: {path}")
    return path[len(__ADB_PREFIX__) :]


def get_path_only(path: str) -> str:
    if is_adb_path(path):
        return strip_adb_prefix(path)
    return path


def run_command(command: str) -> core.RunCommandResult:
    return core.run_command(f"adb shell {command}")


def path_exists(path: str) -> bool:
    """Check if path exists (file or dir) on the ADB device"""
    path = get_path_only(path)
    result = run_command(f'test -e "{path}"')
    return result.ok()


def path_is_dir(path: str) -> bool:
    """Check if path is directory on the ADB device."""
    path = get_path_only(path)
    result = run_command(f'test -d "{path}"')
    return result.ok()


def remove(path: str) -> None:
    """Remove a file on the ADB device, mimicking Python's os.remove behavior.

    Raises:
        FileNotFoundError: If the path does not exist.
        IsADirectoryError: If the path is a directory.
        RuntimeError: If removal fails for other reasons.
    """
    path = get_path_only(path)
    if not path_exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    if path_is_dir(path):
        raise IsADirectoryError(f"Is a directory: '{path}'")

    # Remove the file (no -r, since os.remove does not remove directories)
    result = run_command(f'rm "{path}"')
    if result.ok():
        raise RuntimeError(
            f"Failed to remove file '{path}': {result.stderr.strip() or result.stdout.strip()}"
        )


def list_dir(path: str) -> list[str]:
    """
    Return a list of entries in the directory, mimicking os.listdir for ADB.
    Raises:
        FileNotFoundError: If the path does not exist.
        NotADirectoryError: If the path is not a directory.
        OSError: If the command fails.
    """
    path = get_path_only(path)
    if not path_exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    if not path_is_dir(path):
        raise NotADirectoryError(f"Not a directory: '{path}'")

    # Use -1 for one filename per line, sorted alphabetically
    result = run_command(f'ls -1 "{path}"')
    if result.exit_code != 0:
        raise OSError(
            f"Could not list directory '{path}': {result.stderr.strip() or result.stdout.strip()}"
        )
    # os.listdir does not return '.' or '..'
    entries = [
        line
        for line in result.stdout.splitlines()
        if line.strip() != "" and line not in (".", "..")
    ]

    return entries
