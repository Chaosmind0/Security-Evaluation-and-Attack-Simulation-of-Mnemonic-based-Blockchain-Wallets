import os
import sys
import pkgutil

def resource_path(relative_path: str) -> str:
    """ 
    
    Get absolute path to resource, works for dev and for PyInstaller 

    parameters:
        relative_path: path relative to the current module 
    
    returns:
        absolute path to the resource 
    
    """
    
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)
