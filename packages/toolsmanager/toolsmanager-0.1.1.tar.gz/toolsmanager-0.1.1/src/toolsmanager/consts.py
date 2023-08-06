import os

USERHOME = os.path.expanduser("~")
TM_HOME = os.path.join(USERHOME, f".toolsmanager")
USER_BASHRC_PATH = os.path.join(USERHOME, ".bashrc")

TM_BIN = os.path.join(TM_HOME, "bin")
TM_BASHRC_PATH = os.path.join(TM_HOME, ".bashrc")
TM_GIT = os.path.join(TM_HOME, "git")
VERSION = "0.1.1"
