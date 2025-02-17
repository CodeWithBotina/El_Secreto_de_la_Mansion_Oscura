"""
Path manager for handling game paths
"""
import os
import sys

class PathManager:
    @staticmethod
    def get_base_path():
        """Get base path that works both in development and when compiled"""
        if getattr(sys, 'frozen', False):
            # Running in a bundle (compiled with PyInstaller)
            return sys._MEIPASS
        else:
            # Running in normal Python environment
            return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @staticmethod
    def get_assets_path():
        """Get assets directory path"""
        return os.path.join(PathManager.get_base_path(), "assets")

    @staticmethod
    def get_image_path(filename):
        """Get full path for an image file"""
        return os.path.join(PathManager.get_assets_path(), "images", filename)

    @staticmethod
    def get_sound_path(filename):
        """Get full path for a sound file"""
        return os.path.join(PathManager.get_assets_path(), "sounds", filename)

    @staticmethod
    def get_log_path():
        """Get log directory path"""
        log_dir = os.path.join(PathManager.get_base_path(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        return log_dir
