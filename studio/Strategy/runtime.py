import os
import sys


class CurrentWorkPath:

    __version__ = "1.0"

    def AddCurrentWorkPath(strPath=""):
        if (strPath == ""):
            workspaceRootPath = os.path.dirname(__file__)
            workspaceParentRootPath = os.path.dirname(workspaceRootPath)
            sys.path.append(workspaceParentRootPath)
        else:
            sys.path.append(strPath)

    def AddProjectFolderToWorkPath():
        CurrentWorkPath.AddCurrentWorkPath(CurrentWorkPath.GetProjectPath())

    def GetParentFolder(strPath):
        return os.path.dirname(os.path.abspath(strPath))

    def GetProjectPath():
        return os.path.abspath('./')

    def PrintSysPath():
        print(sys.path)


if __name__ == "__main__":
    print(CurrentWorkPath.__name__ + ' version:' + CurrentWorkPath.__version__)
