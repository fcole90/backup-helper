import shlex
import subprocess


def run_command(command: str) -> tuple[str, str]:
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)
    return result.stdout, result.stderr
