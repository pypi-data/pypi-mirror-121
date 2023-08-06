from koalak import D, F, mkframework

from . import consts, utils

# fmt: off
home_structure = [
    D("git"),
    D("bin"),
    F(
        ".bashrc",
        src=utils.get_data_path("tm_bashrc.sh"),
        substitute=True,
        actions="bashrc"  # this file must be executed by bashrc
    ),
]
# fmt: on

fw_toolsmanager = mkframework(
    "toolsmanager",
    home_structure=home_structure,
    homepath=consts.TM_HOME,
    variables={"TM_BIN": consts.TM_BIN, "TM_GIT": consts.TM_GIT},
    version=consts.VERSION,
)

fw_toolsmanager.variables.set("vars_path", "$home/vars.sh", substitute=True)
fw_toolsmanager.variables.set("alias_path", "$home/alias.sh", substitute=True)

fw_toolsmanager.init()

fw_toolsmanager.create_dict_db("vars", path="$vars_path", type="txt", sep="=")

# FIXME: unique!
fw_toolsmanager.create_list_db(
    "alias", path="$alias_path", type="txt", unique=lambda x: x.split("=")[0]
)
