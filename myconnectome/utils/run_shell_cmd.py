from __future__ import absolute_import
from __future__ import print_function
import subprocess

def run_shell_cmd(cmd,cwd=[],echo=False):
    """ run a command in the shell using Popen
    """
    stdout_holder=[]
    if cwd:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,cwd=cwd)
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
             if echo:
                 print(line.strip())
             stdout_holder.append(line.strip())
    process.wait()
    return stdout_holder
