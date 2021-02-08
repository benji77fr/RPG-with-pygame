from spritesheet import *
from sprites import *
from settings import *
from mapgen import *
from inventory import *
import sys
import pygame as pg
vec = pg.math.Vector2


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.display = pg.Surface((SCALEWIDTH, SCALEHEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        asset_folder = os.path.join(game_folder, 'Assets')
        img_dir = os.path.join(asset_folder, 'Image')
        self.map_dir = os.path.join(asset_folder, 'Map')
        self.playersheet = Spritesheet(os.path.join(img_dir, PLAYERSHEET))
        self.enemysheet = Spritesheet(os.path.join(img_dir, ENEMYSHEET))

    def new(self):
        # Initialise toute les variables et fait le setup pour un nouveau jeu
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.ground = pg.sprite.Group()
        self.map = TileMap(os.path.join(self.map_dir, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.layer = self.map.tmxdata.get_layer_by_name('Ground')
        for x, y, image in self.layer.tiles():
            self.ground.add(Tile(x, y, image))
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'slime':
                self.slime = Enemy(self, obj_center.x, obj_center.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.inventory = Inventory(self.player, 10, 5, 5, True)

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
        self.camera.update(self.player)

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(
                self.player, self.ground, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 0.1
                self.player.vel.y = 0
                self.player.jumping = False
        if self.slime.vel.y > 0:
            hits = pg.sprite.spritecollide(self.slime, self.ground, False)
            if hits:
                self.slime.pos.y = hits[0].rect.top
                self.slime.vel.y = 0

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.display.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            self.display.blit(sprite.image, self.camera.apply(sprite))
        self.inventory.draw(self.display)
        self.screen.blit(pg.transform.scale(
            self.display, self.screen.get_rect().size), (0, 0))

        # self.draw_grid()

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_b:
                    self.inventory.toggle_inventory()

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
