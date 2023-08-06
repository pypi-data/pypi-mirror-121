from pathlib import Path

import appdirs
import toml
from nconf import config


appname = "nygen"
appauthor = "nfearnley"
datadir = Path(appdirs.user_data_dir(appname, appauthor))
confpath = datadir / f"{appname}.conf"


def load_conf():
    @config
    class NygenConf:
        author: str = ""
        email: str = ""
        github: str = ""
    try:
        with confpath.open("r") as f:
            data = toml.load(f)
    except FileNotFoundError:
        data = {}

    return NygenConf.load(data)


def init_conf(author: str, email: str, github: str):
    data = {
        "author": author or "",
        "email": email or "",
        "github": github or ""
    }
    confpath.parent.mkdir(parents=True, exist_ok=True)
    with confpath.open("w") as f:
        toml.dump(data, f)
    return confpath
