import os
import sys

class CurrentWorkPath:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def AddCurrentWorkPath(self, strPath=""):
        if (strPath == ""):
            workspaceRootPath = os.path.dirname(__file__)
            workspaceParentRootPath = os.path.dirname(workspaceRootPath)
            sys.path.append(workspaceParentRootPath)
        else:
            sys.path.append(workspaceParentRootPath)

    def PrintSysPath(self):
        print(sys.path)

CurrentWorkPathInstance = CurrentWorkPath()

if __name__ == "__main__":
    CurrentWorkPathInstance.AddCurrentWorkPath()
