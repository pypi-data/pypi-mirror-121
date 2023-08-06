from .bases import fw_toolsmanager
from .functions import (
    addcmd,
    addvar,
    clearcmd,
    clearvar,
    gitclone,
    gitpull,
    lscmd,
    lsgit,
    lsvar,
    rmcmd,
    rmgit,
    rmvar,
)

__all__ = [
    "fw_toolsmanager",
    "lscmd",
    "addcmd",
    "lsvar",
    "rmcmd",
    "clearcmd",
    "clearvar",
    "lsgit",
    "gitclone",
    "gitpull",
    "rmgit",
    "rmvar",
    "addvar",
]
# TODO: replace print with errors? to be used as library
