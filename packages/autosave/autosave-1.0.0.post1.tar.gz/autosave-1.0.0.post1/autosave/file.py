import os
import json

from pathlib import Path

from .wrapper import IndexableWrapper



class File(IndexableWrapper):
    """File that automatically gets updated on edit"""

    path: Path
    data: dict

    def __init__(self, path: str, default_data: dict = None):
        super().__init__(self, default_data or {})
        self.path = Path(path)

        # Attempt to load existing data
        self.load()
        
        # Make sure default data is saved
        if default_data:
            self.save()


    # Context that only saves all edits on closing

    def __enter__(self):
        return self.data

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.save()


    def ensure(self):
        """Ensure the file and its parent directories exist"""
        
        # Make sure directories exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # Make sure the file exists
        if not os.path.exists(self.path):
            # Serialize and write an empty object to file
            with open(self.path, 'w') as f:
                f.write(self.serialize({}))
        
    def serialize(self, data: dict) -> str:
        """Serialize the data before writing to disk"""
        return json.dumps(data, indent=4)
        
    def deserialize(self, data: str) -> dict:
        """Deserialize the text after reading from disk"""
        return json.loads(data)

    def save(self):
        """Save data to disk"""
        
        # Ensure it exists
        self.ensure()

        # Serialize the data and write to disk
        with open(self.path, 'w') as f:
            f.write(self.serialize(self.data))

    def load(self):
        """Load data from disk"""
        
        # Ensure it exists
        self.ensure()

        # Read and deserialize the data
        with open(self.path, 'r') as f:
            self.data.update(self.deserialize(f.read()))