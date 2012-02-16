# Just some nice globals I need occasionally
import pygame
from pygame.locals import *
from random import randint as rand
import cmath
from math import atan2, sin, cos, sqrt
from sys import exit
from os import path
join = path.join

SIZE = (800,600)
TILE_SIZE = 50
SPRITE_GRP = pygame.sprite.OrderedUpdates

def draw_text(surface, text, font, pos=(0,0), color=(0,0,0), center=0):
  t_img = font.render(text, 1, color)
  t_rect = t_img.get_rect()
  t_rect = t_rect.move(pos)
  if center:
    t_rect.center = pos
  surface.blit(t_img, t_rect)
  return t_rect


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

  def __getitem__(self):
    pass

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

  def zero_real(self):
    self.vector = 0 + self.vector.imag*1j

  def zero_imag(self):
    self.vector = self.vector.real + 0j

  def set_real(self, real):
    self.vector = real + self.vector.imag
  
  def set_imag(self, imag):
    self.vector = self.vector.real + imag*1j
