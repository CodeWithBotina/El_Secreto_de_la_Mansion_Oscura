"""
Resource Manager for handling game assets
"""
import os
import pygame

class ResourceManager:
    def __init__(self, base_path):
        """
        Initialize resource manager
        
        Args:
            base_path (str): Base path to the assets folder
        """
        self.base_path = base_path
        self.images = {}
        self.sounds = {}
        self.cached_surfaces = {}
        
    def load_image(self, name, colorkey=None, scale=None):
        """
        Load an image and optionally scale it
        
        Args:
            name (str): Image filename
            colorkey: Color to make transparent
            scale (tuple): New size for the image
        """
        try:
            path = os.path.join(self.base_path, "images", name)
            image = pygame.image.load(path)
            
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey)
                
            if scale:
                return pygame.transform.scale(image, scale)
            return image
            
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading image {name}: {e}")
            # Create temporary surface
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 0))
            return surface

    def load_sound(self, name):
        """
        Load a sound effect
        
        Args:
            name (str): Sound filename
        """
        try:
            path = os.path.join(self.base_path, "sounds", name)
            return pygame.mixer.Sound(path)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading sound {name}: {e}")
            return None

    def load_music(self, name):
        """
        Load and play background music
        
        Args:
            name (str): Music filename
        """
        try:
            path = os.path.join(self.base_path, "sounds", name)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading music {name}: {e}")

    def create_surface(self, width, height, color):
        """
        Create a temporary surface
        
        Args:
            width (int): Surface width
            height (int): Surface height
            color (tuple): RGB color tuple
        """
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface

    def preload_images(self, image_list):
        """
        Preload a list of images
        
        Args:
            image_list (list): List of image filenames to load
        """
        for image_name in image_list:
            self.images[image_name] = self.load_image(image_name)

    def get_image(self, name):
        """
        Get a loaded image
        
        Args:
            name (str): Image name
        """
        return self.images.get(name)

    def clear_cache(self):
        """Clear cached resources"""
        self.images.clear()
        self.sounds.clear()
        self.cached_surfaces.clear()
