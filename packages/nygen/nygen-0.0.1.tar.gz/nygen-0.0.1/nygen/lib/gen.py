from pathlib import Path
import importlib.resources

import nygen.data
from nygen.lib.formatvars import FormatVars, get_vars
from nygen.lib.conda import create_conda, conda_exists
from nygen.lib.exceptions import GenException, DestinationExistsException, CondaEnvironmentExistsException


def precheck(name, path_maps, fvars: FormatVars):
    fvars.check()

    for src, dst in path_maps:
        if not src.is_file():
            if dst.exists():
                raise DestinationExistsException(f"Destination file already exists: {dst}")

    if conda_exists(name):
        raise CondaEnvironmentExistsException(f"Conda environment already exists: {name}")


def gen_project(name, author: str, email: str, github: str):
    try:
        fvars = get_vars(name, author, email, github)
        src_root: Path = importlib.resources.files(nygen.data) / "template"
        srcs = [p for p in src_root.rglob("*") if not (p.name == "__pycache__" or p.suffix == ".pyc")]
        dst_root = Path(name)
        path_maps = [(src, map_dst(src, src_root, dst_root, fvars.to_json())) for src in srcs]
        precheck(name, path_maps, fvars)
        fvars.python_path = create_conda(name)
        for src, dst in path_maps:
            gen(src, dst, fvars.to_json())
    except GenException as e:
        print(e)


def map_dst(src: Path, src_root: Path, dst_root: Path, fvars: FormatVars):
    rel_src = src.relative_to(src_root)
    rel_src = Path(str(rel_src).format(**fvars))
    dst = dst_root / rel_src
    return dst


def gen(src: Path, dst: Path, fvars: FormatVars):
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
    else:
        dst.write_text(src.read_text().format(**fvars))
