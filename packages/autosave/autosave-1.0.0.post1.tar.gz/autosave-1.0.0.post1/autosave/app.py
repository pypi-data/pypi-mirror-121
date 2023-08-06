from appdirs import AppDirs

from .directory import Directory



class AppStorage:
    """Wrapper around `appdirs` for creating auto-saving files"""

    def __init__(self, *args, **kwargs):
        self.app = AppDirs(*args, **kwargs)

        self.data = Directory(self.app.user_data_dir)
        self.config = Directory(self.app.user_config_dir)
        self.cache = Directory(self.app.user_cache_dir)