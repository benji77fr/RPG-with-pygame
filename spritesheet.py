import pygame as pg
import os


class Spritesheet:
    def __init__(self, filename):
        try:
            self.sheet = pg.image.load(filename).convert_alpha()
        except pg.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
        image = pg.transform.scale(image, (width * 2, height * 2))
        return image
