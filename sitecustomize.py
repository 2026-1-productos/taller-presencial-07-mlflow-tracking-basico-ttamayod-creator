"""Local Python startup adjustments for the workshop test environment."""

import os
from pathlib import Path
import subprocess
import sys

_original_popen_init = subprocess.Popen.__init__


def _normalize_python3_command(args):
    if os.name != "nt":
        return args

    if isinstance(args, (list, tuple)) and args and args[0] == "python3":
        venv_python = Path.cwd() / ".venv" / "Scripts" / "python.exe"
        python_executable = str(venv_python) if venv_python.exists() else sys.executable
        return [python_executable, *args[1:]]

    return args


def _patched_popen_init(self, args, *pargs, **kwargs):
    return _original_popen_init(
        self, _normalize_python3_command(args), *pargs, **kwargs
    )


subprocess.Popen.__init__ = _patched_popen_init
