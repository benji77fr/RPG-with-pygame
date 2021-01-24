# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# game settings
WIDTH = 1200
HEIGHT = 800
FPS = 60
TITLE = "RPG with Python"
TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
PLATFORMS = [(0, HEIGHT - 40, WIDTH, 40),
             (200, HEIGHT - 250, 60, 20)]

# Player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8


SPRITESHEETTERRAIN = 'Grass_dirt_tileset.png'
PLAYERSHEET = 'Player_anim_sheet.png'
