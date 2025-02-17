import unittest
import pygame
from src.game.game import Game
from src.game.game_state import GameState

class TestGame(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        pygame.init()
        self.game = Game()

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_game_initialization(self):
        """Test game initialization"""
        self.assertEqual(self.game.state, GameState.MENU)
        self.assertEqual(self.game.points, 0)
        self.assertFalse(self.game.mystery_solved)

    def test_player_movement(self):
        """Test player movement"""
        initial_x = self.game.player_x
        initial_y = self.game.player_y
        
        # Test movement in valid direction
        self.game.move_player(1, 0)
        self.assertEqual(self.game.player_x, initial_x + 1)
        
        # Test movement into wall (should not move)
        self.game.player_x = 0
        self.game.move_player(-1, 0)
        self.assertEqual(self.game.player_x, 0)

    def test_character_placement(self):
        """Test random character placement"""
        self.game.place_characters_randomly()
        for character in self.game.characters.values():
            # Check character is in valid position
            self.assertTrue(self.game.is_position_valid(character["x"], character["y"]))
