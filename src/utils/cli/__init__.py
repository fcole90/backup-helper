import os
from utils.cli import adb


def path_exists(path: str) -> bool:
    if adb.is_adb_path(path):
        return adb.path_exists(adb.strip_adb_prefix(path))

    return os.path.exists(path)


def path_is_dir(path: str) -> bool:
    if adb.is_adb_path(path):
        return adb.path_is_dir(adb.strip_adb_prefix(path))
    return os.path.isdir(path)


def remove(path: str) -> None:
    if adb.is_adb_path(path):
        adb.remove(adb.strip_adb_prefix(path))
    os.remove(path)


def list_dir(path: str) -> list[str]:
    if adb.is_adb_path(path):
        return adb.list_dir(adb.strip_adb_prefix(path))
    return os.listdir(path)
