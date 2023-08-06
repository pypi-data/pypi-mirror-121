from dataclasses import dataclass
from datetime import date

import nypi

from nygen.conf import load_conf
from nygen.lib.exceptions import MissingArgumentException


@dataclass
class FormatVars:
    name: str = None
    year: str = None
    author: str = None
    email: str = None
    github: str = None
    pytest_version: str = None
    flake8_version: str = None
    autopep8_version: str = None
    python_path: str = None

    def check(self):
        checkables = ((k, v) for k, v in self.to_json().items() if k in ("author", "mail", "github"))
        for k, v in checkables:
            if not v:
                raise MissingArgumentException(f"Missing argument: {k}")

    def to_json(self):
        return {
            "_": "",    # Blank substitution used to mangle special names
            "name": self.name,
            "year": self.year,
            "author": self.author,
            "email": self.email,
            "github": self.github,
            "pytest_version": self.pytest_version,
            "flake8_version": self.flake8_version,
            "autopep8_version": self.autopep8_version,
            "python_path": self.python_path
        }

    @classmethod
    def from_json(self, j):
        return FormatVars(**j)


def get_vars(name, author: str, email: str, github: str):
    conf = load_conf()
    fvars = FormatVars()
    fvars.name = name
    fvars.year = str(date.today().year)
    fvars.author = author or conf.author
    fvars.email = email or conf.email
    fvars.github = github or conf.github
    fvars.pytest_version = nypi.get_pkg("pytest").version
    fvars.flake8_version = nypi.get_pkg("flake8").version
    fvars.autopep8_version = nypi.get_pkg("autopep8").version
    return fvars
