import pygame as pg
import os
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.playersheet.get_image(12, 2, 24, 35)
        self.image_size = self.image.get_size()
        self.image = pg.transform.scale(
            self.image, (int(self.image_size[0]*2), int(self.image_size[1]*2)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

    def get_keys(self):
        self.accel = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            self.accel.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.accel.x = PLAYER_ACC

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.ground, False)
        if hits:
            self.vel.y = -20

    def update(self):
        self.get_keys()

        self.accel.x += self.vel.x * PLAYER_FRICTION

        self.vel += self.accel
        self.pos += self.vel + 0.5 * self.accel

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Terrain(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
