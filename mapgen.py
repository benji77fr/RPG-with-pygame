import pygame as pg
import pytmx
from settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(x*16, y*16, 16, 16)
        self.image = image

    def __getitem__(self, i):
        return i


class TileMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelapha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(600 / 2)
        y = -target.rect.centery + int(400 / 2)
        print(x, y)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - 600), x)
        y = max(-(self.height - 400), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
