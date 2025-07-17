import os
import sys
import pkgutil

def resource_path(relative_path: str):
    """ 
    
    Get absolute path to resource, works for dev and for PyInstaller 
    
    """
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path):
        data = pkgutil.get_data('', relative_path)
        if data:
            temp_path = os.path.join("/tmp", relative_path)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(data)
            return temp_path

    return full_path
