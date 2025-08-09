from dataclasses import dataclass
import shlex
import subprocess


@dataclass
class RunCommandResult:
    stdout: str
    stderr: str
    exit_code: int

    def ok(self) -> bool:
        """Shortcut to check successful exit code."""
        return self.exit_code == 0


def run_command(command: str) -> RunCommandResult:
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)
    return RunCommandResult(result.stdout, result.stderr, result.returncode)
