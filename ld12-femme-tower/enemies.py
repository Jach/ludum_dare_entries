import pygame
from pygame.locals import *
from os.path import join
from random import randint as rand

class Knight(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(join('data', 'knight.png')).convert_alpha()
    self.rect = self.image.get_rect()
    # direction
    c = rand(1, 2)
    if c == 1:
      self.image = pygame.transform.flip(self.image, 1, 0)
      self.rect.x = 0
      self.speed = 3
    else:
      self.rect.right = 800
      self.speed = -4
    self.rect.bottom = 550

    self.hp = 2

  def update(self):
    self.rect = self.rect.move(self.speed, 0)

  def hit(self):
    self.hp -= 1

class Owl(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface((50,30))
    self.image.fill((255,255,255))
    font = pygame.font.Font(join('data', 'cour.ttf'), 20)
    t = font.render('Owl!', 1, (0,0,0))
    self.image.blit(t, (0,0))
    self.rect = self.image.get_rect()
    c = rand(1,2)
    if c == 1: self.rect.x = 0; self.dx = 3
    else: self.rect.right = 800; self.dx = -3

    self.rect.top = 30
    self.hp = 3
    self.attack = 0

  def update(self):
    if not self.rect.right < 0 and not self.rect.left > 800:
      self.rect = self.rect.move(self.dx, 0)
    if self.rect.x in range(440, 444):
      self.attack = 1
    else:
      self.attack = 0

  def hit(self):
    self.hp -= 1

class Bowlmb(pygame.sprite.Sprite):

  def __init__(self, center):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface((20,20))
    self.image.set_colorkey((0,0,0))
    pygame.draw.circle(self.image, (0x3d,0x27,0x03), (10,10), 10)
    self.rect = self.image.get_rect()
    self.rect.center = center

    self.hp = 100000000000
    self.dy = 5

  def update(self):
    self.rect = self.rect.move(0, self.dy)

  def hit(self):
    pass

class Gunner(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

  def update(self):
    pass

class Cloud(pygame.sprite.Sprite): # Just floats about

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(join('data', 'cloud.png')).convert_alpha()
    self.rect = self.image.get_rect()
    self.reset()

  def reset(self):
    self.rect.centery = rand(0, 400)
    chance = rand(1,2)
    if chance == 1: self.rect.centerx = 0; self.dx = rand(1, 10)
    else: self.rect.centerx = 800; self.dx = rand(-10, -1)
    self.dy = rand(-5, 5)

  def update(self):
    self.rect = self.rect.move(self.dx, self.dy)
    if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.left > 800 or \
        self.rect.top > 550:
      self.reset()

class AngryCloud(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(join('data', 'angry_cloud.png')).convert_alpha()
    self.rect = self.image.get_rect()
    chance = rand(1,2)
    if chance == 1: self.rect.centerx = 0; self.dx = rand(1,10)
    else: self.rect.centerx = 800; self.dx = rand(-10, -1)
    self.rect.centery = rand(50, 400)

    self.hp = 5
    self.moving = 1
    self.attack = 0
    self.attack_pause = 0
    self.attack_delay = 40

  def update(self):
    if self.moving:
      self.rect = self.rect.move(self.dx, 0)
      if abs(self.rect.x - 420) < 100 or abs(self.rect.right - 380) < 100:
        self.moving = 0
    if not self.moving:
      self.attack_pause += 1
      if self.attack_pause >= self.attack_delay:
        self.attack = 1
      else:
        self.attack = 0

  def hit(self):
    self.hp -= 1

class Lightning(pygame.sprite.Sprite):

  def __init__(self, center):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(join('data', 'lightning.png')).convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.topleft = center
    if center[0] > 400:
      self.image = pygame.transform.flip(self.image, 1, 0)
      self.rect.topright = center

    self.delay = 20 # hafl sec
    self.pause = 0
    self.done = 0
    
    self.hp = 10000000000000000

  def update(self):
    self.pause += 1
    if self.pause >= self.delay:
      self.done = 1

  def hit(self):
    pass
