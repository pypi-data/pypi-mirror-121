from pathlib import Path

from typing import Union

from .file import File



class Directory(type(Path())):
    """Directory that can create File objects"""

    files: dict[str, File]
    
    def __init__(self, *args, **kwargs):
        self.files = {}

    def __truediv__(self, key):
        """Get subdirectory or file"""

        new_path = super().__truediv__(key)

        if new_path.suffixes:
            return self.get_file(new_path.name)
            
        return Directory(new_path)

    def get_file(self, fname: str):
        """Get File object"""
        
        if fname not in self.files:
            self.files[fname] = File(super().__truediv__(fname))

        return self.files[fname]