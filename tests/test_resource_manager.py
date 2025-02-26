import unittest
import os
import pygame
from src.utils.resource_manager import ResourceManager
from src.utils.path_manager import PathManager

class TestResourceManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        pygame.init()
        self.resource_manager = ResourceManager(PathManager.get_assets_path())

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_image_loading(self):
        """Test image loading functionality"""
        # Test loading existing image
        image = self.resource_manager.load_image("player.png")
        self.assertIsNotNone(image)
        
        # Test loading non-existent image (should return temporary surface)
        image = self.resource_manager.load_image("nonexistent.png")
        self.assertIsNotNone(image)
        self.assertEqual(image.get_size(), (32, 32))

    def test_sound_loading(self):
        """Test sound loading functionality"""
        # Test loading existing sound
        sound = self.resource_manager.load_sound("background_music.mp3")
        self.assertIsNotNone(sound)
