#! python3.8
# -*- coding: utf-8 -*-

# ---
from CHR_local import path_definition
import subprocess
import os, sys


class ScriptCaller():
    def runScript(self, scriptPath, *args, runningDir=None):
        print('calling external exe')
        if runningDir != None:
            cwd = os.getcwd()
            os.chdir(runningDir)

        # call script
        # subprocess.Popen([self.pythonExePath, scriptPath, *args])
        subprocess.call(scriptPath)

        # restore cwd
        if runningDir != None:
            os.chdir(cwd)


if __name__ == '__main__':

    scriptCaller = ScriptCaller()

    # scriptLoc = r'C:\Dropbox\codes\CHR_packages\scripts\adHocTextManipulation'
    # # scriptPath = os.path.join(scriptLoc, 'pdf2jpgConverter.py')
    # scriptPath = os.path.join(scriptLoc, 'run_sketch.bat')
    appLoc = r'C:\Users\thinkbanny\Dropbox\codes\CHR_packages\_less'
    appPath = os.path.join(appLoc, 'printA.bat')
    # appLoc = r'C:\Dropbox\research_work_in_MIT\gel_doc'
    # appPath = os.path.join(appLoc, 'gel_here.bat')

    scriptCaller.runScript(appPath, runningDir=appLoc)

    appPath = os.path.join(appLoc, 'printB.bat')
    scriptCaller.runScript(appPath, runningDir=appLoc)

# scriptCaller.runScript(scriptLoc)
