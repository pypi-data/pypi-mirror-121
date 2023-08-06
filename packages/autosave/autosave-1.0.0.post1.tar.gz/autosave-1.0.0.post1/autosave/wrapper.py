from typing import Union, MutableSequence, MutableMapping
from typing import Hashable, Any



Indexable = Union[MutableSequence, MutableMapping]


class IndexableWrapper:
    """Autosave wrapper for indexable objects"""

    def __init__(self, file: 'File', data: Indexable): 
        self.file = file
        self.data = data

    def __getitem__(self, key: Hashable) -> Union[Any, 'IndexableWrapper']:
        value = self.data[key]

        # Put value in another wrapper if it is indexable,
        # as to preserve autosaving down the hierarchy
        if isinstance(value, Indexable.__args__):
            return IndexableWrapper(self.file, self.data)

        return value

    def __setitem__(self, key: Hashable, value: Any):
        self.data[key] = value
        self.file.save()