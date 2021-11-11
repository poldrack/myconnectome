"""
set structure of a gifti file
"""

from __future__ import absolute_import
from __future__ import print_function
from .run_shell_cmd import run_shell_cmd

def set_structure(fname,structure,verbose=True):
    cmd='wb_command -set-structure %s %s'%(fname,structure)
    if verbose:
        print(cmd)
    output=run_shell_cmd(cmd)
    if verbose:
        print(output)
