import pygame
from pygame.locals import *
from os.path import join
from random import randint as rand

class Pepsi(pygame.sprite.Sprite):
  """Pepsi available. (Essentially player's life.)"""

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.Surface( (100, 10) )
    self.image.fill( (0,255,0) )
    self.rect = self.image.get_rect()
    self.rect.topleft = 120, 5

    self.life = 100
    self.oldlife = 100

  def update(self):
    if self.oldlife != self.life:
      self.oldlife = self.life
      self.image.fill( (255,0,0) )
      if self.life > 0:
        pygame.draw.rect(self.image, (0,255,0), (0,0,self.life,10))

class People(pygame.sprite.Sprite):
  """People remaining. Tells player how many more in this level."""

  def __init__(self, people=5):
    pygame.sprite.Sprite.__init__(self)

    self.people = people
    self.oldpeople = 0
    self.font = pygame.font.Font(join('data', 'courbd.ttf'), 15)

    self.image = pygame.Surface( (18, 13) )
    self.image.fill( (192,192,192) )
    self.image.set_colorkey( (192,192,192) )
    self.rect = self.image.get_rect()
    self.rect.topleft = 120, 20

  def update(self):
    if self.oldpeople != self.people:
      self.oldpeople = self.people
      num = self.font.render(str(self.people), 1, (0,0,0))
      self.image.fill( (192,192,192) )
      self.image.blit(num, (0,0))


class Parked(pygame.sprite.Sprite):
  """Keeps track of how many cars got through and where they got through at.
  Blits them in stalls."""

  def __init__(self): 
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface( (640, 40) )
    self.image.fill( (255,128,128) )
    self.image.set_colorkey( (255,128,128) )
    self.rect = self.image.get_rect()
    self.rect.topleft = 0, 440

    ss = pygame.display.get_surface()
    self.h = ss.get_height()

    # The following array represents the stalls.
    # The inner sets of stalls go from top to bottom then left to right.
    top = 8
    bot = top+15
    self.stalls = [ \
        [{'x':55, 'y':top, 'full' : 0}, {'x' : 55, 'y' : bot, 'full' : 0}, \
        {'x':90, 'y':top, 'full' : 0}, {'x' : 90, 'y' : bot, 'full' : 0}], \
        \
        [{'x':282, 'y':top, 'full' : 0}, {'x' : 282, 'y' : bot, 'full' : 0}, \
        {'x':322, 'y':top, 'full' : 0}, {'x' : 322, 'y' : bot, 'full' : 0}], \
        \
        [{'x':504, 'y':top, 'full' : 0}, {'x' : 504, 'y' : bot, 'full' : 0}, \
        {'x':550, 'y':top, 'full': 0}, {'x' : 550, 'y' : bot, 'full' : 0}] ]
    self.newb = 0 # to tell if someone needs to be added
    self.full = 0 # to tell if a section has filled up, meaning they lost

  def update(self):
    if self.newb:
      self.newb = 0
      for section in self.stalls:
        fulls = 0
        for stall in section:
          if stall['full']: # car there!
            pygame.draw.rect(self.image, (255,0,255), \
                (stall['x'], stall['y'], 20, 8))
            fulls += 1
        if fulls == 4: # all filled up in this section
          self.full = 1

  def reset(self):
    self.newb = 1
    self.image.fill( (255,128,128) )
    for section in self.stalls:
      for stall in section:
        stall['full'] = 0

  def set_filled(self, section):
    # Expects section as 0 1 2
    # will pick the next available stall.
    self.newb = 1
    if not self.stalls[section][0]['full']:
      stall = 0
    elif not self.stalls[section][1]['full']:
      stall = 1
    elif not self.stalls[section][2]['full']:
      stall = 2
    elif not self.stalls[section][3]['full']:
      stall = 3
    else:
      stall = 0
    self.stalls[section][stall]['full'] = 1
