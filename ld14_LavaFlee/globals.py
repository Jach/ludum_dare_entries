"People who are afraid of globals are usually afraid of girls, spiders, etc."

# Libs
import pygame
from pygame.locals import *
pygame.init()
from random import randint as rand
from sys import exit
from os import path
join = path.join
import cmath
from math import atan2, sin, cos, sqrt

# Vars
PI = 3.14159265358979323846264338327950 # I know more but...
SCR_SIZE = (800, 600)
FRAME_RATE = 40
CEIL_Y = 100 # bottom of course
GROUND_Y = 500 # top of course
SPRITE_GRP = pygame.sprite.OrderedUpdates # yay
TILE_SIZE = 50

try: _ = sounds
except:
  sounds = {
    'menu_select': pygame.mixer.Sound(join('data', 'menu_select.wav')),
    'jump': pygame.mixer.Sound(join('data', 'jump.wav')),
    'fire': pygame.mixer.Sound(join('data', 'fire.wav')),
    'lava': pygame.mixer.Sound(join('data', 'lava3.wav')),
    'death': pygame.mixer.Sound(join('data', 'death.wav'))
  }
  sounds['lava'].set_volume(0.2)
  sounds['jump'].set_volume(0.5)
  sounds['fire'].set_volume(0.5)

# Various useful classes/functions I don't want to reimplement everywhere

def draw_text(surface, text, font, pos=(0,0), color=(0,0,0), center=0):
  t_img = font.render(text, 1, color)
  t_rect = t_img.get_rect()
  t_rect = t_rect.move(pos)
  if center:
    t_rect.center = pos
  surface.blit(t_img, t_rect)
  return t_rect

class BaseSprite(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.collision_grps = []
    self.is_static = 0

  def add_collision_grps(self, *grps):
    for grp in grps:
      self.collision_grps.append(grp)

  def update(self):
    abstract

class Struct:
  def __init__(self, **entries): self.__dict__.update(entries)

class CVector:
  # Uses complex numbers for easy vectors; thanks pygame mailing list
  # for tipping me in on this.

  def __init__(self, vector=0j):
    # e.g. 1 + 2j
    self.vector = vector

  def __add__(self, vec):
    return CVector(self.vector + vec)

  def __sub__(self, vec):
    return CVector(self.vector - vec)

  def __mul__(self, vec):
    return CVector(self.vector * vec)

  def __div__(self, vec):
    return CVector(self.vector / vec)

  def __iter__(self):
    yield self.vector.real
    yield self.vector.imag

  def __abs__(self):
    return abs(self.vector)

  def radians(self):
    return atan2(*tuple(self.vector)[::-1]) # requires y, x

  def normal(self):
    length = abs(self.vector)
    if length == 0:
      return 0j
    else:
      return self.vector / length

  def unit(self, rads):
    return cmath.exp(rads*1j)

  def distance(self, vec):
    return abs(self.vector - vec.vector)
