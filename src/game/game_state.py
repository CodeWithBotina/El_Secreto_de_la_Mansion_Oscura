from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    CONTROLS = 4
    CONTEXT = 5
    ALEXS_ROOM = 6
    OUTSIDE = 7
    LOST = 8
    WON = 9
