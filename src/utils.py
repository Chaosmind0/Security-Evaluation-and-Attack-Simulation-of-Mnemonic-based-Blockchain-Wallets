import os
import sys
import pkgutil

def resource_path(relative_path: str) -> str:
    """ 
    
    Always read resource from external directory next to the .exe,
    fallback to development path if running as script.

    parameters:
        relative_path: path relative to the current module 
    
    returns:
        absolute path to the resource 
    
    """
    
    if hasattr(sys, "_MEIPASS"):
        # The directory where the exe file is located when PyInstaller packages and runs.
        base_path = os.path.dirname(sys.executable)
    else:
        # General development environment
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)
