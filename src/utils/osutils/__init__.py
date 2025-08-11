import os
import shutil
from utils.osutils import adb


def path_exists(path: str) -> bool:
    if adb.is_adb_path(path):
        return adb.path_exists(path)

    return os.path.exists(path)


def path_is_dir(path: str) -> bool:
    if adb.is_adb_path(path):
        return adb.path_is_dir(path)
    return os.path.isdir(path)


def remove(path: str) -> None:
    if adb.is_adb_path(path):
        adb.remove(path)
    os.remove(path)


def list_dir(path: str) -> list[str]:
    if adb.is_adb_path(path):
        return adb.list_dir(path)
    return os.listdir(path)


def move(src: str, dst: str) -> None:
    if adb.is_adb_path(src) or adb.is_adb_path(dst):
        adb.move(src, dst)
    else:
        shutil.move(src, dst)
