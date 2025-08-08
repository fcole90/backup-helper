__ADB_PREFIX__ = "adb:"


from utils.cli import core


def is_adb_path(path: str) -> bool:
    return path.startswith(__ADB_PREFIX__)


def strip_adb_prefix(path: str) -> str:
    if not is_adb_path(path):
        raise ValueError(f"Path is not on adb: {path}")
    return path[len(__ADB_PREFIX__) :]


def run_command(command: str) -> tuple[str, str]:
    return core.run_command(f"adb shell {command}")


def path_exists(path: str) -> bool:
    _, err = run_command(f"ls {path}")
    return err == ""


def path_is_dir(path: str) -> bool:
    # return os.path.isdir(path)
    raise NotImplementedError


def remove(path: str) -> None:
    # os.remove(path)
    raise NotImplementedError


def list_dir(path: str) -> list[str]:
    # return os.listdir(path)
    raise NotImplementedError
