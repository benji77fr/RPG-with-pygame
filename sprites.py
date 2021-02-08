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
        self.crouching = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.last_key_pressed = None

    def load_images(self):
        self.standing_frames_r = [self.game.playersheet.get_image(0, 0, 50, 37),
                                  self.game.playersheet.get_image(
                                      50, 0, 50, 37),
                                  self.game.playersheet.get_image(
            100, 0, 50, 37),
            self.game.playersheet.get_image(150, 0, 50, 37)]
            
        self.standing_frames_l = [pg.transform.flip(
            frame, True, False) for frame in self.standing_frames_r]

        self.walk_frames_r = [self.game.playersheet.get_image(50, 37, 50, 37),
                              self.game.playersheet.get_image(100, 37, 50, 37),
                              self.game.playersheet.get_image(150, 37, 50, 37),
                              self.game.playersheet.get_image(200, 37, 50, 37),
                              self.game.playersheet.get_image(250, 37, 50, 37),
                              self.game.playersheet.get_image(300, 37, 50, 37)]

        self.walk_frames_l = [pg.transform.flip(frame, True, False) for frame in self.walk_frames_r]
                
        self.jumping_frames_r = [self.game.playersheet.get_image(0, 74, 50, 37),
                                 self.game.playersheet.get_image(
                                     50, 74, 50, 37),
                                 self.game.playersheet.get_image(
                                     100, 74, 50, 37),
                                 self.game.playersheet.get_image(
                                     150, 74, 50, 37),
                                 self.game.playersheet.get_image(
                                     200, 74, 50, 37),
                                 self.game.playersheet.get_image(
                                     250, 74, 50, 37),
                                 self.game.playersheet.get_image(
                                     300, 74, 50, 37),
                                 self.game.playersheet.get_image(
                                     0, 111, 50, 37),
                                 self.game.playersheet.get_image(
                                     50, 111, 50, 37),
                                 self.game.playersheet.get_image(100, 111, 50, 37)]

        self.jumping_frames_l = [pg.transform.flip(frame, True, False) for frame in self.jumping_frames_r]
        
        self.crouch_frame_r = [self.game.playersheet.get_image(200, 0, 50, 37),
                               self.game.playersheet.get_image(250, 0, 50, 37),
                               self.game.playersheet.get_image(300, 0, 50, 37),
                               self.game.playersheet.get_image(0, 37, 50, 37)]

        self.crouch_frame_l = [pg.transform.flip(frame, True, False) for frame in self.crouch_frame_r]
        

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.ground, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -20

    def get_keys(self, keys):
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            self.accel.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.accel.x = PLAYER_ACC
        if keys[pg.K_c]:
            self.crouching = True
        else:
            self.crouching = False
        if keys[pg.K_SPACE]:
            self.jump()

    def update(self):

        self.animate()
        self.accel = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        self.last_key_pressed = self.get_keys(keys)

        self.accel.x += self.vel.x * PLAYER_FRICTION

        self.vel += self.accel
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.accel

        if self.pos.x > self.game.map.rect.width + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = self.game.map.rect.width + self.rect.width / 2

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

        if self.crouching:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.crouch_frame_l)
                bottom = self.rect.bottom
                if self.last_key_pressed == pg.k_d:
                    self.image = self.crouch_frame_r[self.current_frame]
                else:
                    self.image = self.crouch_frame_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.jumping_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0 or self.vel.x == 0:
                    self.image = self.jumping_frames_r[self.current_frame]
                else:
                    self.image = self.jumping_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (
                    self.current_frame + 1) % len(self.standing_frames_l)
                bottom = self.rect.bottom
                if self.last_key_pressed == pg.K_q:
                    self.image = self.standing_frames_l[self.current_frame]
                else:
                    self.image = self.standing_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.walking = False
        self.currentFrame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standingFrames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

    def load_images(self):
        self.standingFrames = [self.game.enemysheet.get_image(0, 0, 32, 25),
                               self.game.enemysheet.get_image(32, 0, 32, 25),
                               self.game.enemysheet.get_image(64, 0, 32, 25)]

    def update(self):
        self.animate()
        self.accel = vec(0, PLAYER_GRAV)

        self.accel.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.accel

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.accel

        if self.game.player.pos.x > self.pos.x:
            self.vel.x = 1
        if self.game.player.pos.x < self.pos.x:
            self.vel.x = -1

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()

        if not self.walking:
            if now - self.last_update > 250:
                self.last_update = now
                self.currentFrame = (self.currentFrame +
                                     1) % len(self.standingFrames)
                bottom = self.rect.bottom
                self.image = self.standingFrames[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
