from pathlib import Path
import json
from subprocess import run


def create_conda(name):
    proc = run(["conda", "create", "--json", "-y", "--name", name], text=True, capture_output=True)
    j: dict = json.loads(proc.stdout)
    python_path = str(Path(j["prefix"]) / "python.exe")
    return python_path


def conda_exists(name):
    proc = run(["conda", "create", "--json", "--dry-run", "--name", name], text=True, capture_output=True)
    j: dict = json.loads(proc.stdout)
    missing = j.get("success", False)
    exists = not missing
    return exists
