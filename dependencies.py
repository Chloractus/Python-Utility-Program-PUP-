import sys
import subprocess
import time

operating_system = sys.platform

def gather_dependencies():

    try:
        import wx
    except:
        if operating_system == "linux":
            subprocess.run(["sudo", "pacman", "-S", "python-wxpython", "--noconfirm"], check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    try:
        import matplotlib
    except:
        if operating_system == "linux":
            subprocess.run(["sudo", "pacman", "-S", "python-matplotlib", "--noconfirm"], check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
