import pygame as pg
import sys
from settings import *
from sprites import *
from spritesheet import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir, 'Assets')

        self.terrainsheet = Spritesheet(
            os.path.join(img_dir, SPRITESHEETTERRAIN))
        self.playersheet = Spritesheet(os.path.join(img_dir, PLAYERSHEET))

    def new(self):
        # Initialise toute les variables et fait le setup pour un nouveau jeu
        self.all_sprites = pg.sprite.Group()
        self.terrain = pg.sprite.Group()
        self.player = Player(self)
        p1 = Terrain(0, HEIGHT - 40, WIDTH, 40)
        self.all_sprites.add(p1)
        self.terrain.add(p1)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

        hits = pg.sprite.spritecollide(self.player, self.terrain, False)
        if hits:
            self.player.pos.y = hits[0].rect.top + 0.3
            self.player.vel.y = 0

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(DARKGREY)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()
