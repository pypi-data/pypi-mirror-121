import subprocess, psutil
from python_helper import ObjectHelper, SettingHelper, EnvironmentHelper, log

def killProcessesByPid(pid) :
    try :
        process = psutil.Process(pid)
        for child in process.children(recursive=True):
            child.kill()
        process.kill()
    except Exception as exception :
        log.log(killProcesses, 'Error while killing process', exception=exception)

def killProcesses(givenProcess) :
    killProcessesByPid(givenProcess.pid)

def getProcess(command, path, muteLogs=False) :
    return subprocess.Popen(command: str, cwd: str = path, shell: bool = True)
