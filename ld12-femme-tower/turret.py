import pygame
from pygame.locals import *
from math import sin, cos
from os.path import join

turret_center = (400,100)

class Tower(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(join('data', 'tower.png')).convert()
    self.rect = self.image.get_rect()
    self.rect.bottom = 550
    self.rect.centerx = 400

  def update(self):
    pass

class Turret(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.master_img = pygame.image.load(join('data', 'turret.png')).convert_alpha()
    self.rect = self.master_img.get_rect()
    self.rect.center = turret_center
    self.image = self.master_img
    self.dir = 0
    self.turnspeed = 6

  def update(self):

    keys = pygame.key.get_pressed()
    move = 0
    if keys[K_LEFT]:
      self.dir += self.turnspeed
      move = 1
    elif keys[K_RIGHT]:
      self.dir -= self.turnspeed
      move = 1

    if move:
      if self.dir >= 360:
        self.dir -= 360
      if self.dir <= -360:
        self.dir += 360
      newimg = pygame.transform.rotate(self.master_img, self.dir)
      self.image = newimg
      oldcenter = self.rect.center
      self.rect = self.image.get_rect()
      self.rect.center = oldcenter

class Laser(pygame.sprite.Sprite):

  def __init__(self, dir):
    pygame.sprite.Sprite.__init__(self)

    self.master_img = pygame.image.load(join('data', 'laser.png')).convert()
    self.pi = 3.14159265358979323846264338327950 # I could do 30 more...
    init_x, init_y = turret_center
    self.speed = 25
    self.length = 100
    self.dir = dir
    self.raddir = rads = self.pi * dir / 180

    self.image = pygame.transform.rotate(self.master_img, dir)
    self.image.set_colorkey((163, 99, 28))
    self.rect = self.image.get_rect()
    self.rect.center = turret_center
    for i in range(5): self.update()

  def update(self):
    self.rect = self.rect.move(cos(self.raddir)*self.speed, -sin(self.raddir)*self.speed)
