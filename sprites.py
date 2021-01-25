import pygame as pg
import os
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.playersheet.get_image(0, 0, 50, 37),
                                self.game.playersheet.get_image(50, 0, 50, 37),
                                self.game.playersheet.get_image(
                                    100, 0, 50, 37),
                                self.game.playersheet.get_image(150, 0, 50, 37)]
        self.walk_frames_r = [self.game.playersheet.get_image(50, 37, 50, 37),
                              self.game.playersheet.get_image(100, 37, 50, 37),
                              self.game.playersheet.get_image(150, 37, 50, 37),
                              self.game.playersheet.get_image(200, 37, 50, 37),
                              self.game.playersheet.get_image(250, 37, 50, 37),
                              self.game.playersheet.get_image(300, 37, 50, 37)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.ground, False)
        if hits:
            self.vel.y = -20

    def update(self):

        self.animate()
        self.accel = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            self.accel.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.accel.x = PLAYER_ACC

        self.accel.x += self.vel.x * PLAYER_FRICTION

        self.vel += self.accel
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.accel

        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
