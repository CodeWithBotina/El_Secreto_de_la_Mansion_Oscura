"""
Main game class implementation
"""
import os
import sys
import time
import random
import pygame
from pygame.locals import *
from z3 import *

# Local imports
from .game_state import GameState
from .game_constants import *
from .game_maps import (MAIN_MAP, ALEXS_ROOM, OUTSIDE_MAP, 
                       ALEXS_ROOM_START_POS, OUTSIDE_START_POS, TILE_TYPES)
from ..ui.button import Button

class Game:
    """
    Main game class that handles all game logic and rendering
    
    The class is organized into these sections:
    1. Initialization and Setup
    2. Game State Management
    3. Input Handling
    4. Drawing and Rendering
    5. Game Logic
    6. Resource Management
    7. Helper Methods
    """

    def __init__(self):
        """Initialize game components"""
        # Basic setup
        pygame.init()
        
        # Set window dimensions
        self.WIDTH = SCREEN_WIDTH
        self.HEIGHT = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), RESIZABLE)
        pygame.display.set_caption("El Secreto de la Mansión Oscura")
        self.clock = pygame.time.Clock()
        
        # Game properties
        self.move_speed = 0.1
        self.TILE_SIZE = TILE_SIZE
        
        # Initialize maps
        self.map = MAIN_MAP
        self.alexs_room = ALEXS_ROOM
        self.outside_map = OUTSIDE_MAP
        
        # Initialize all components
        self._load_icon()
        self.setup_game_state()
        self.setup_buttons()
        self.setup_characters()
        self.setup_solver()
        self.load_resources()
        self.setup_audio()
        self.setup_timers()

    def _load_icon(self):
        """Load game icon"""
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            icon_path = os.path.join(base_path, "assets/images", "icono.ico")
            if os.path.exists(icon_path):
                pygame.display.set_icon(pygame.image.load(icon_path))
            else:
                print(f"⚠️ Warning: Icon file not found at {icon_path}")
        except Exception as e:
            print(f"Error loading icon: {e}")

    def setup_game_state(self):
        """Initialize game state and variables"""
        self.state = GameState.MENU
        self.points = 0
        self.mystery_solved = False
        self.player_x, self.player_y = 1, 17
        self.clues = []
        self.current_map = 'outside'
        self.body_fullscreen = False
        self.body_fullscreen_timer = 0
        self.body_fullscreen_duration = 3
        self.body_position = (9, 8)
        self.first_win = True
        self.moving_character = None

    def setup_buttons(self):
        """Initialize game buttons"""
        button_x = SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2
        self.menu_buttons = [
            Button(button_x, 250, BUTTON_WIDTH, BUTTON_HEIGHT, 
                  "Jugar", lambda: setattr(self, 'state', GameState.CONTEXT)),
            Button(button_x, 310, BUTTON_WIDTH, BUTTON_HEIGHT, 
                  "Controles", lambda: setattr(self, 'state', GameState.CONTROLS)),
            Button(button_x, 370, BUTTON_WIDTH, BUTTON_HEIGHT, 
                  "Salir", pygame.quit)
        ]
        self.mute_button = Button(SCREEN_WIDTH - 60, 20, 40, 40, "", self.toggle_mute)

    def setup_characters(self):
        """Initialize game characters and place them randomly"""
        self.characters = {
            "Carla": {
                "x": 5, "y": 2,  # Posiciones iniciales que serán reemplazadas
                "image": None,
                "dialogues": [
                    "Estaba en mi habitación toda la noche.",
                    "No vi a nadie en el pasillo.",
                    "No sé quién es el asesino."
                ],
                "dialogue_index": 0,
                "is_guilty": None
            },
            "Juan": {
                "x": 7, "y": 4,
                "image": None,
                "dialogues": [
                    "Vi a Carla en el pasillo.",
                    "Rodys estaba en la sala.",
                    "No sé quién es el asesino."
                ],
                "dialogue_index": 0,
                "is_guilty": None
            },
            "Rodys": {
                "x": 3, "y": 5,
                "image": None,
                "dialogues": [
                    "La tormenta deshabilitó las cámaras.",
                    "No vi a nadie sospechoso.",
                    "No sé quién es el asesino."
                ],
                "dialogue_index": 0,
                "is_guilty": None
            }
        }
        self.character_directions = {}
        self.character_steps = {}
        self.character_step_limits = {}
        self.character_last_positions = {}
        self.place_characters_randomly()  # Colocar personajes aleatoriamente al inicio

    def get_valid_positions(self):
        """Get list of valid positions on the current map"""
        valid_positions = []
        current_map = self.get_current_map()
        
        for y in range(len(current_map)):
            for x in range(len(current_map[0])):
                # Verificar si la posición es válida (no es pared ni puerta)
                if current_map[y][x] == 0:
                    # Verificar que no haya otro personaje en esta posición
                    position_occupied = False
                    for character in self.characters.values():
                        if int(character["x"]) == x and int(character["y"]) == y:
                            position_occupied = True
                            break
                    
                    if not position_occupied:
                        valid_positions.append((x, y))
        
        return valid_positions

    def place_characters_randomly(self):
        """Place characters in random valid positions"""
        valid_positions = self.get_valid_positions()
        
        for character in self.characters.values():
            if valid_positions:
                # Seleccionar una posición aleatoria
                new_pos = random.choice(valid_positions)
                # Remover la posición seleccionada para evitar superposiciones
                valid_positions.remove(new_pos)
                # Asignar nueva posición al personaje
                character["x"], character["y"] = new_pos

    def setup_audio(self):
        """Initialize audio settings"""
        self.muted = False
        try:
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
            # Crear imágenes temporales para los botones de sonido si no existen
            sound_button_size = (40, 40)
            temp_on = pygame.Surface(sound_button_size)
            temp_on.fill((0, 255, 0))  # Verde para sonido activado
            temp_off = pygame.Surface(sound_button_size)
            temp_off.fill((255, 0, 0))  # Rojo para sonido desactivado
            try:
                self.sound_on_image = pygame.image.load(os.path.join(base_path, "images", "sound_on.png"))
                self.sound_off_image = pygame.image.load(os.path.join(base_path, "images", "sound_off.png"))
            except (pygame.error, FileNotFoundError):
                print("⚠️ Using temporary sound button images")
                self.sound_on_image = temp_on
                self.sound_off_image = temp_off
            self.sound_on_image = pygame.transform.scale(self.sound_on_image, sound_button_size)
            self.sound_off_image = pygame.transform.scale(self.sound_off_image, sound_button_size)
            
        except Exception as e:
            print(f"Error in setup_audio: {e}")
            # Usar superficies temporales en caso de error
            self.sound_on_image = pygame.Surface(sound_button_size)
            self.sound_off_image = pygame.Surface(sound_button_size)
            self.sound_on_image.fill((0, 255, 0))
            self.sound_off_image.fill((255, 0, 0))

    def setup_timers(self):
        """Initialize game timers"""
        self.timer = INITIAL_TIMER
        self.timer_active = True
        self.body_fullscreen_timer = 0
        self.body_fullscreen_duration = 3

    def toggle_mute(self):
        """Toggle audio mute state"""
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0 if self.muted else 0.5)

    def draw_mute_button(self):
        """Draw mute button on screen"""
        self.mute_button.image = self.sound_off_image if self.muted else self.sound_on_image
        self.mute_button.draw(self.screen)

    def handle_mute_button_event(self, event):
        """Handle mute button click events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mute_button.rect.collidepoint(event.pos):
                self.toggle_mute()

    def move_player(self, dx, dy):
        """Move player by delta x and y"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        current_map = self.get_current_map()
        if 0 <= new_x < len(current_map[0]) and 0 <= new_y < len(current_map):
            if current_map[new_y][new_x] != TILE_TYPES['WALL']:
                self.player_x, self.player_y = new_x, new_y

    def get_current_map(self):
        """Get current map based on game state"""
        if self.current_map == 'outside':
            return OUTSIDE_MAP
        elif self.current_map == 'alexs_room':
            return ALEXS_ROOM
        return MAIN_MAP

    def check_door_interaction(self):
        """Check and handle door interactions"""
        current_map = self.get_current_map()
        if current_map[self.player_y][self.player_x] == TILE_TYPES['DOOR']:
            if self.current_map == 'main':
                if self.player_x == 23 and self.player_y == 5:
                    self.transition_to_room('alexs_room', ALEXS_ROOM_START_POS)
                elif self.player_x == 23 and self.player_y == 15:
                    self.transition_to_room('outside', (7, 15))
            elif self.current_map == 'alexs_room':
                self.transition_to_room('main', (23, 4))
            elif self.current_map == 'outside':
                self.transition_to_room('main', (23, 14))

    def transition_to_room(self, room_name, position):
        """Handle room transitions"""
        self.current_map = room_name
        self.player_x, self.player_y = position
        self.load_room_music(room_name)

    def load_room_music(self, room_name):
        """Load and play room-specific music"""
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            if room_name == 'alexs_room':
                music_file = "horror_music.mp3"
            elif room_name == 'outside':
                music_file = "outside_music.mp3"
            else:
                music_file = "background_music.mp3"
            
            music_path = os.path.join(base_path, "assets", "sounds", music_file)
            print(f"Loading music: {music_path}")
            
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                if not self.muted:
                    pygame.mixer.music.play(-1)
            else:
                print(f"Music file not found: {music_path}")
                
        except Exception as e:
            print(f"Error loading music: {e}")

    def draw_text(self, text, size, x, y, color=None):
        """Draw text on screen"""
        if color is None:
            color = WHITE
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def show_context(self):
        """Show game context/introduction screen"""
        context_running = True
        context_text = [
            "Alexander, un famoso empresario, fue encontrado muerto en su mansión.",
            "La tormenta de esa noche deshabilitó las cámaras de seguridad.",
            "Tú eres el detective asignado para resolver este misterio.",
            "Habla con los sospechosos y recolecta pistas para descubrir al asesino.",
            "Presiona ESPACIO para continuar."
        ]
        while context_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.state = GameState.OUTSIDE
                    context_running = False
            self.screen.fill(BLACK)
            self.draw_text("El Secreto de la Mansión Oscura", 48, SCREEN_WIDTH/2, 100)
            for i, line in enumerate(context_text):
                self.draw_text(line, 24, SCREEN_WIDTH/2, 200 + i * 30)
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        """Main game loop"""
        while True:
            self._handle_game_state()

    def _handle_game_state(self):
        """Handle different game states"""
        if self.state == GameState.MENU:
            self.main_menu()
        elif self.state == GameState.CONTEXT:
            self.show_context()
        elif self.state == GameState.CONTROLS:
            self.show_controls_screen()
        elif self.state in [GameState.PLAYING, GameState.OUTSIDE]:
            self.game_loop()
        elif self.state == GameState.PAUSED:
            self.pause_menu()
        elif self.state == GameState.LOST:
            self.show_lost_card()
            self.reset_game()

    def game_loop(self):
        """Main gameplay loop"""
        while self.state in (GameState.PLAYING, GameState.OUTSIDE):
            self.handle_input()
            self.update_game_state()
            self.draw_game_screen()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            self._handle_gameplay_input(event)
            self.handle_mute_button_event(event)

    def _handle_gameplay_input(self, event):
        """Handle gameplay-specific input"""
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.state = GameState.PAUSED
            elif event.key == K_UP:
                self.move_player(0, -1)
            elif event.key == K_DOWN:
                self.move_player(0, 1)
            elif event.key == K_LEFT:
                self.move_player(-1, 0)
            elif event.key == K_RIGHT:
                self.move_player(1, 0)
            elif event.key == K_e:
                self.interact()

    def update_game_state(self):
        """Update game state and check conditions"""
        self.check_door_interaction()
        self.check_body_interaction()
        self._update_characters()
        self._update_timer()

    def _update_characters(self):
        """Update character movements"""
        if self.moving_character:
            self.move_character_gradually(self.moving_character)

    def _update_timer(self):
        """Update game timer"""
        if self.timer_active:
            self.timer -= 1 / 60  # Restar un segundo cada 60 frames
            if self.timer <= 0:
                self.timer = 0
                self.timer_active = False
                if len(self.clues) == 0:
                    self.show_lost_card()
                    self.state = GameState.LOST

    def draw_game_screen(self):
        """Draw the main game screen"""
        self.screen.fill(BLACK)
        self.draw_map()
        if not self.body_fullscreen:
            self.draw_characters()
            self.draw_player()
        self.draw_fullscreen_body()
        self.show_controls()
        self.draw_mute_button()
        self.draw_ui()

    def draw_ui(self):
        """Draw UI elements"""
        self.draw_text(f"Puntos: {self.points}", 20, SCREEN_WIDTH - 100, 20)
        minutes = int(self.timer // 60)
        seconds = int(self.timer % 60)
        self.draw_text(f"Tiempo: {minutes}:{seconds:02d}", 20, SCREEN_WIDTH - 100, 50)

    def interact(self):
        """Handle player interactions with characters and objects"""
        for name, data in self.characters.items():
            if abs(self.player_x - data["x"]) <= 1 and abs(self.player_y - data["y"]) <= 1:
                dialogue = data["dialogues"][data["dialogue_index"]]
                self.show_dialogue(f"{name}: {dialogue}", data["x"], data["y"])
                self.update_solver(dialogue, name)
                if name not in self.clues:
                    self.clues.append(name)
                    self.timer += TIMER_BONUS
                data["dialogue_index"] = (data["dialogue_index"] + 1) % len(data["dialogues"])
                self.moving_character = name
                
                if len(self.clues) == 3:
                    self.solve_mystery()

    def solve_mystery(self):
        """Attempt to solve the mystery"""
        killer = self.determine_killer()
        if killer:
            explanation = f"Basado en las declaraciones, {killer} es el asesino."
            self.show_killer_card(killer, explanation)
            self.mystery_solved = True
            self.points += 1
            self.clues = []
            self.setup_solver()
            if self.first_win:
                self.timer = REDUCED_TIMER
                self.first_win = False
            self.show_congratulations_card()

    def reset_game(self):
        """Reset game to initial state"""
        self.state = GameState.MENU
        self.timer = INITIAL_TIMER
        self.timer_active = True
        self.clues = []
        self.setup_solver()
        self.first_win = True
        self.place_characters_randomly()  # Reubicar personajes al reiniciar

    def main_menu(self):
        """Display and handle main menu"""
        while self.state == GameState.MENU:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.menu_buttons:
                    button.handle_event(event)
                self.handle_mute_button_event(event)
            self.screen.fill(BLACK)
            self.draw_text("El Secreto de la Mansión Oscura", 48, SCREEN_WIDTH/2, 100)
            for button in self.menu_buttons:
                button.draw(self.screen)
            self.draw_mute_button()
            self.draw_text("Created by CodeWithBotina", 20, SCREEN_WIDTH/2, SCREEN_HEIGHT - 30)
            pygame.display.flip()
            self.clock.tick(60)

    def pause_menu(self):
        """Display and handle pause menu"""
        pygame.mixer.music.pause()
        while self.state == GameState.PAUSED:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.state = GameState.PLAYING
                    if not self.muted:
                        pygame.mixer.music.unpause()
                self.handle_mute_button_event(event)
            self.screen.fill(BLACK)
            self.draw_text("Pausa", 48, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
            self.draw_text("Presiona ESC para continuar", 24, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50)
            self.draw_mute_button()
            pygame.display.flip()
            self.clock.tick(60)

    def show_controls_screen(self):
        """Display game controls screen"""
        controls_running = True
        try:
            arrow_keys_image = self.images['arrow_keys']
            arrow_keys_image = pygame.transform.scale(arrow_keys_image, (150, 150))
        except (AttributeError, KeyError):
            # Crear una imagen temporal si no está disponible
            arrow_keys_image = pygame.Surface((150, 150))
            arrow_keys_image.fill((255, 0, 0))  # Rojo para indicar imagen faltante

        while controls_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        controls_running = False
                        self.state = GameState.MENU
                if event.type == MOUSEBUTTONDOWN:
                    back_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 80, 200, 50)
                    if back_button_rect.collidepoint(event.pos):
                        controls_running = False
                        self.state = GameState.MENU

            self.screen.fill(BLACK)
            self.draw_text("Controles del Juego", 48, SCREEN_WIDTH/2, 50)
            self.screen.blit(arrow_keys_image, (SCREEN_WIDTH/2 - 70, 150))
            controls = [
                "Flechas: Mover al personaje",
                "E: Interactuar con personajes y objetos",
                "ESC: Pausar/Volver al menú",
                "ESPACIO: Continuar diálogo"
            ]
            
            for i, control in enumerate(controls):
                self.draw_text(control, 30, SCREEN_WIDTH/2, 300 + i * 50)
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 100, 200, 50))
            self.draw_text("Volver al Menú", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT - 75, BLACK)
            pygame.display.flip()
            self.clock.tick(60)

    def draw_map(self):
        """Draw the current game map"""
        if self.current_map == 'outside':
            self.draw_outside_map()
        else:
            self.draw_interior_map()

    def draw_outside_map(self):
        """Draw the outside area"""
        outside_image = pygame.transform.scale(self.images['outside'], (self.WIDTH, self.HEIGHT))
        self.screen.blit(outside_image, (0, 0))
        for y, row in enumerate(self.outside_map):
            for x, tile in enumerate(row):
                pos = (x * self.TILE_SIZE, y * self.TILE_SIZE)
                if tile == TILE_TYPES['WALL']:
                    self.screen.blit(pygame.transform.scale(self.images['wall'], 
                                (self.TILE_SIZE, self.TILE_SIZE)), pos)
                elif tile == TILE_TYPES['DOOR']:
                    self.screen.blit(pygame.transform.scale(self.images['door'], 
                                (self.TILE_SIZE, self.TILE_SIZE)), pos)

    def draw_interior_map(self):
        """Draw interior maps (main map and Alex's room)"""
        floor_image = self.images['dark_floor'] if self.current_map == 'alexs_room' else self.images['floor']
        current_map = self.alexs_room if self.current_map == 'alexs_room' else self.map
        floor_scaled = pygame.transform.scale(floor_image, (self.WIDTH, self.HEIGHT))
        self.screen.blit(floor_scaled, (0, 0))
        for y, row in enumerate(current_map):
            for x, tile in enumerate(row):
                pos = (x * self.TILE_SIZE, y * self.TILE_SIZE)
                self.draw_tile(tile, pos, x, y)

    def draw_tile(self, tile, pos, x, y):
        """Draw individual map tiles"""
        if tile == TILE_TYPES['BLOOD'] and self.current_map == 'alexs_room':
            blood_image = pygame.transform.scale(self.images['blood'], 
                        (self.TILE_SIZE, self.TILE_SIZE))
            self.screen.blit(blood_image, pos)
            
        if tile == TILE_TYPES['WALL']:
            self.screen.blit(pygame.transform.scale(self.images['wall'], 
                        (self.TILE_SIZE, self.TILE_SIZE)), pos)
        elif tile == TILE_TYPES['DOOR']:
            self.screen.blit(pygame.transform.scale(self.images['door'], 
                        (self.TILE_SIZE, self.TILE_SIZE)), pos)
        elif tile == TILE_TYPES['BODY']:
            self.draw_body_and_blood(x, y)
        elif tile in [TILE_TYPES['TABLE'], TILE_TYPES['CHAIR'], 
                     TILE_TYPES['BOOKSHELF'], TILE_TYPES['WARDROBE'], 
                     TILE_TYPES['PLANT']]:
            self.draw_furniture(tile, pos)

    def draw_body_and_blood(self, x, y):
        """Draw body and blood effects"""
        blood_image = pygame.transform.scale(self.images['blood'], 
                    (self.TILE_SIZE * 3, self.TILE_SIZE * 3))
        self.screen.blit(blood_image, (x * self.TILE_SIZE - self.TILE_SIZE, 
                    y * self.TILE_SIZE - self.TILE_SIZE))
        body_image = pygame.transform.scale(self.images['body'], 
                    (self.TILE_SIZE * 2, self.TILE_SIZE * 2))
        self.screen.blit(body_image, (x * self.TILE_SIZE - self.TILE_SIZE // 2, 
                    y * self.TILE_SIZE - self.TILE_SIZE // 2))

    def draw_furniture(self, tile, pos):
        """Draw furniture tiles"""
        furniture_types = {
            TILE_TYPES['TABLE']: 'table',
            TILE_TYPES['CHAIR']: 'chair',
            TILE_TYPES['BOOKSHELF']: 'bookshelf',
            TILE_TYPES['WARDROBE']: 'wardrobe',
            TILE_TYPES['PLANT']: 'plant'
        }
        if tile in furniture_types:
            image_key = furniture_types[tile]
            self.screen.blit(pygame.transform.scale(self.images[image_key], 
                        (self.TILE_SIZE, self.TILE_SIZE)), pos)

    def draw_characters(self):
        """Draw game characters"""
        if self.current_map == 'main':
            for name, data in self.characters.items():
                pos = (data["x"] * self.TILE_SIZE, data["y"] * self.TILE_SIZE)
                self.screen.blit(pygame.transform.scale(data["image"], 
                            (self.TILE_SIZE, self.TILE_SIZE)), pos)
                self.draw_text(name, 20, 
                            data["x"] * self.TILE_SIZE + self.TILE_SIZE / 2,
                            data["y"] * self.TILE_SIZE - 15)

    def draw_player(self):
        """Draw the player character"""
        pos = (self.player_x * self.TILE_SIZE, self.player_y * self.TILE_SIZE)
        self.screen.blit(pygame.transform.scale(self.images['player'], 
                       (self.TILE_SIZE, self.TILE_SIZE)), pos)

    def check_body_interaction(self):
        """Handle body interaction and fullscreen effect"""
        if self.current_map == 'alexs_room':
            distance_x = abs(self.player_x - self.body_position[0])
            distance_y = abs(self.player_y - self.body_position[1])
            
            if distance_x <= 1 and distance_y <= 1:
                self.body_fullscreen = True
                self.body_fullscreen_timer = pygame.time.get_ticks()
            else:
                self.body_fullscreen = False

    def draw_fullscreen_body(self):
        """Draw fullscreen body effect"""
        if self.body_fullscreen and self.current_map == 'alexs_room':
            body_image = pygame.transform.scale(self.images['body'], (self.WIDTH, self.HEIGHT))
            self.screen.blit(body_image, (0, 0))
            current_time = pygame.time.get_ticks()
            if current_time - self.body_fullscreen_timer >= self.body_fullscreen_duration * 1000:
                self.body_fullscreen = False

    def show_killer_card(self, killer, explanation):
        """Show the killer reveal card"""
        card_running = True
        card_width = 400
        card_height = 300
        card_x = self.WIDTH / 2 - card_width / 2
        card_y = self.HEIGHT / 2 - card_height / 2
        
        while card_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    card_running = False

            self.draw_game_screen()
            pygame.draw.rect(self.screen, WHITE, (card_x, card_y, card_width, card_height))
            pygame.draw.rect(self.screen, BLACK, (card_x, card_y, card_width, card_height), 2)
            self.draw_text("¡Misterio Resuelto!", 36, card_x + card_width/2, card_y + 30, BLACK)
            self.draw_text(f"El asesino es: {killer}", 28, card_x + card_width/2, card_y + 100, BLACK)
            self.draw_text(explanation, 24, card_x + card_width/2, card_y + 150, BLACK)
            self.draw_text("Presiona ESPACIO para continuar", 20, card_x + card_width/2, card_y + 250, BLACK)
            
            pygame.display.flip()
            self.clock.tick(60)

    def show_lost_card(self):
        """Show game over card"""
        card_running = True
        card_width = 400
        card_height = 300
        card_x = self.WIDTH / 2 - card_width / 2
        card_y = self.HEIGHT / 2 - card_height / 2
        
        while card_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    card_running = False

            self.draw_game_screen()
            pygame.draw.rect(self.screen, WHITE, (card_x, card_y, card_width, card_height))
            pygame.draw.rect(self.screen, BLACK, (card_x, card_y, card_width, card_height), 2)
            self.draw_text("¡Has Perdido!", 36, card_x + card_width/2, card_y + 30, BLACK)
            self.draw_text("Se acabó el tiempo", 28, card_x + card_width/2, card_y + 100, BLACK)
            self.draw_text("Presiona ESPACIO para volver al menú", 20, card_x + card_width/2, card_y + 250, BLACK)
            
            pygame.display.flip()
            self.clock.tick(60)

    def setup_solver(self):
        """Initialize the logical solver"""
        self.solver = Solver()
        self.C, self.J, self.R = Bools('Carla Juan Rodys')
        self._setup_base_constraints()

    def _setup_base_constraints(self):
        """Setup initial solver constraints"""
        self.solver.add(Or(self.C, self.J, self.R))
        self.solver.add(Not(And(self.C, self.J)))
        self.solver.add(Not(And(self.C, self.R)))
        self.solver.add(Not(And(self.J, self.R)))

    def load_resources(self):
        """Load game resources"""
        try:
            self._load_images()
            self._load_sounds()
        except Exception as e:
            print(f"Error loading resources: {e}")
            self._create_temporary_resources()

    def _load_images(self):
        """Load game images"""
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        assets_path = os.path.join(base_path, "assets")
        self.images = {
            'floor': pygame.image.load(os.path.join(assets_path, "images", "floor.png")),
            'wall': pygame.image.load(os.path.join(assets_path, "images", "wall.png")),
            'door': pygame.image.load(os.path.join(assets_path, "images", "door.png")),
            'player': pygame.image.load(os.path.join(assets_path, "images", "player.png")),
            'carla': pygame.image.load(os.path.join(assets_path, "images", "carla.png")),
            'juan': pygame.image.load(os.path.join(assets_path, "images", "juan.png")),
            'rodys': pygame.image.load(os.path.join(assets_path, "images", "rodys.png")),
            'blood': pygame.image.load(os.path.join(assets_path, "images", "blood.png")),
            'body': pygame.image.load(os.path.join(assets_path, "images", "body.png")),
            'dark_floor': pygame.image.load(os.path.join(assets_path, "images", "dark_floor.png")),
            'table': pygame.image.load(os.path.join(assets_path, "images", "table.png")),
            'chair': pygame.image.load(os.path.join(assets_path, "images", "chair.png")),
            'bookshelf': pygame.image.load(os.path.join(assets_path, "images", "bookshelf.png")),
            'wardrobe': pygame.image.load(os.path.join(assets_path, "images", "wardrobe.png")),
            'plant': pygame.image.load(os.path.join(assets_path, "images", "plant.png")),
            'outside': pygame.image.load(os.path.join(assets_path, "images", "outside.png")),
            'arrow_keys': pygame.image.load(os.path.join(assets_path, "images", "arrow_keys.png"))
        }
        for name in self.characters:
            self.characters[name]["image"] = self.images[name.lower()]

    def _load_sounds(self):
        """Load game sounds"""
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        assets_path = os.path.join(base_path, "assets")
        music_files = ["horror_music.mp3", "outside_music.mp3", "background_music.mp3"]
        for music_file in music_files:
            try:
                pygame.mixer.music.load(os.path.join(assets_path, "sounds", music_file))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
                break
            except (pygame.error, FileNotFoundError):
                continue

    def _create_temporary_resources(self):
        """Create temporary resources when files are missing"""
        self.images = {}
        temp_surface = pygame.Surface((32, 32))
        temp_surface.fill((255, 0, 0))  # Color rojo para imágenes faltantes
        
        for key in ['floor', 'wall', 'door', 'player', 'carla', 'juan', 'rodys',
                   'blood', 'body', 'dark_floor', 'table', 'chair', 'bookshelf',
                   'wardrobe', 'plant', 'outside', 'arrow_keys']:
            self.images[key] = temp_surface.copy()
        for name in self.characters:
            self.characters[name]["image"] = self.images[name.lower()]

    def show_dialogue(self, text, character_x, character_y):
        """Show character dialogue"""
        dialogue_running = True
        font = pygame.font.Font(None, DIALOGUE_FONT_SIZE)
        
        lines = []
        words = text.split()
        current_line = ""
        
        # Word wrap
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= DIALOGUE_LINE_WIDTH:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        # Calculate dialogue box dimensions and position
        dialogue_height = len(lines) * 30 + 20
        dialogue_width = DIALOGUE_LINE_WIDTH + 20
        dialogue_x = character_x * TILE_SIZE - dialogue_width / 2 + TILE_SIZE / 2
        dialogue_y = character_y * TILE_SIZE - dialogue_height - 20
        
        # Adjust position to keep dialogue on screen
        dialogue_x = max(10, min(dialogue_x, SCREEN_WIDTH - dialogue_width - 10))
        dialogue_y = max(10, min(dialogue_y, SCREEN_HEIGHT - dialogue_height - 10))
        
        while dialogue_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    dialogue_running = False
            
            # Draw dialogue box
            self.draw_game_screen()
            pygame.draw.rect(self.screen, WHITE, (dialogue_x, dialogue_y, dialogue_width, dialogue_height))
            pygame.draw.rect(self.screen, BLACK, (dialogue_x, dialogue_y, dialogue_width, dialogue_height), 2)
            
            # Draw text
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(
                    center=(dialogue_x + dialogue_width/2, dialogue_y + 20 + i * 30)
                )
                self.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
            self.clock.tick(60)

    def show_congratulations_card(self):
        """Show victory card"""
        card_running = True
        card_width = 400
        card_height = 300
        card_x = SCREEN_WIDTH / 2 - card_width / 2
        card_y = SCREEN_HEIGHT / 2 - card_height / 2
        
        while card_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    card_running = False

            self.draw_game_screen()
            pygame.draw.rect(self.screen, WHITE, (card_x, card_y, card_width, card_height))
            pygame.draw.rect(self.screen, BLACK, (card_x, card_y, card_width, card_height), 2)
            self.draw_text("¡Felicidades!", 36, card_x + card_width/2, card_y + 30, BLACK)
            self.draw_text("Has resuelto el misterio", 28, card_x + card_width/2, card_y + 100, BLACK)
            self.draw_text("Presiona ESPACIO para continuar", 20, card_x + card_width/2, card_y + 250, BLACK)
            
            pygame.display.flip()
            self.clock.tick(60)

    def move_character_gradually(self, character_name):
        """Move character gradually across the map"""
        character = self.characters[character_name]
        current_x, current_y = character["x"], character["y"]
        
        if character_name not in self.character_directions:
            valid_directions = self.get_valid_directions(current_x, current_y)
            if valid_directions:
                self.character_directions[character_name] = random.choice(valid_directions)
                self.character_steps[character_name] = 0
                self.character_step_limits[character_name] = random.randint(5, 70)
                self.character_last_positions[character_name] = (current_x, current_y)
            else:
                return
        
        dx, dy = self.character_directions[character_name]
        new_x = current_x + dx * self.move_speed
        new_y = current_y + dy * self.move_speed
        
        if self.is_position_valid(new_x, new_y):
            character["x"], character["y"] = new_x, new_y
            self.character_steps[character_name] += 1
            if self.character_steps[character_name] >= self.character_step_limits[character_name]:
                self._reset_character_movement(character_name)
        else:
            self._handle_invalid_movement(character_name, current_x, current_y)

    def _handle_invalid_movement(self, character_name, current_x, current_y):
        """Handle invalid character movement"""
        valid_directions = self.get_valid_directions(current_x, current_y)
        if valid_directions:
            self.character_directions[character_name] = random.choice(valid_directions)
            self.character_steps[character_name] = 0
            self.character_step_limits[character_name] = random.randint(5, 70)
            self.character_last_positions[character_name] = (current_x, current_y)
        else:
            self._reset_character_movement(character_name)

    def _reset_character_movement(self, character_name):
        """Reset character movement parameters"""
        self.character_directions.pop(character_name, None)
        self.character_steps.pop(character_name, None)
        self.character_step_limits.pop(character_name, None)
        self.character_last_positions.pop(character_name, None)
        self.moving_character = None

    def get_valid_directions(self, x, y):
        """Get valid movement directions for a character"""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        valid_directions = []
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.is_position_valid(new_x, new_y):
                valid_directions.append((dx, dy))
        return valid_directions

    def is_position_valid(self, x, y):
        """Check if a position is valid for a character to move to"""
        current_map = self.get_current_map()
        # Convertir coordenadas flotantes a enteros
        x = int(x)
        y = int(y)
        if 0 <= x < len(current_map[0]) and 0 <= y < len(current_map):
            if current_map[y][x] != TILE_TYPES['WALL']:
                return True
        return False

    def update_solver(self, statement, character):
        """Update solver with new statements"""
        if character == "Carla":
            if statement == "Estaba en mi habitación toda la noche.":
                self.solver.add(Implies(Not(self.C), Not(self.J)))
            elif statement == "No vi a nadie en el pasillo.":
                self.solver.add(Implies(Not(self.C), Not(self.J)))
        elif character == "Juan":
            if statement == "Vi a Carla en el pasillo.":
                self.solver.add(Implies(Not(self.J), Not(self.C)))
            elif statement == "Rodys estaba en la sala.":
                self.solver.add(Implies(Not(self.J), Not(self.R)))
        elif character == "Rodys":
            if statement == "La tormenta deshabilitó las cámaras.":
                self.solver.add(Implies(Not(self.R), Not(self.J)))
            elif statement == "No vi a nadie sospechoso.":
                self.solver.add(Implies(Not(self.R), Not(self.J)))

    def determine_killer(self):
        """Determine the killer based on gathered clues"""
        if self.solver.check() == sat:
            model = self.solver.model()
            if model[self.C]:
                return "Carla"
            elif model[self.J]:
                return "Juan"
            elif model[self.R]:
                return "Rodys"
        return None

    def show_controls(self):
        """Show controls on screen"""
        controls = [
            "Flechas: Mover",
            "E: Interactuar",
            "ESC: Pausar/Menú",
            "ESPACIO: Continuar"
        ]
        
        y_offset = 20
        for i, control in enumerate(controls):
            self.draw_text(control, 20, 100, y_offset + i * 25)
