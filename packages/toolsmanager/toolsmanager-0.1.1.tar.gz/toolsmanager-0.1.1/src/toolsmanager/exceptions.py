class ToolsManagerException(Exception):
    pass


class CmdAlreadyExistException(ToolsManagerException):
    pass


class CmdDontExistException(ToolsManagerException):
    pass
