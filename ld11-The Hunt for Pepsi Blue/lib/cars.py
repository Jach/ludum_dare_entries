import pygame
from pygame.locals import *
from random import randint as rand
from math import sqrt
from os.path import join

class Car(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    ss = pygame.display.get_surface()
    self.size = ss.get_size()

    # Pick a random stall to head to, make the center of it the dest.
    self.stall = rand(0,2)
    self.dest = [(self.stall+1)*self.size[0]/3-self.size[0]/6,self.size[1]-10]
    self.real_dest = self.dest[:]
    self.at_dest = 0

    self.load_stuff()

  def load_stuff(self):
    self.master_img = pygame.image.load(join('data', 'car.png')).convert_alpha()
    self.image = self.master_img
    self.rect = self.image.get_rect()
    self.rect.topleft = rand(0, self.size[0]), 0

    self.health = 10
    self.speed = 4.5
    self.delay = 60 # to go in random dir
    self.pause = 0

  def hit(self, attack):
    if attack == 'ram':
      self.health -= 5
    elif attack == 'shell':
      self.health -= 7

  def update(self):
    if self.dest != self.real_dest: # we're going in a random direction.
      self.pause += 1
      if self.pause >= self.delay:
        self.pause = 0
        self.dest = self.real_dest[:]

    # Randomly decide if we want to go toward our dest, or in a random dir.
    if rand(1, 100) == 1 and not self.at_dest and self.pause == 0:
      # random direction!
      self.dest = [rand(0, self.size[0]), rand(0, 380)]
    elif self.pause == 0:
      self.dest = self.real_dest[:]

    vec = [self.dest[0] - self.rect.centerx, self.dest[1] - self.rect.centery]
    mag = sqrt(vec[0]**2 + vec[1]**2)
    if mag <= 10 and self.pause == 0: # here
      self.real_dest = self.rect.center
      self.at_dest = 1
      return
    elif mag <= 10 and self.pause != 0: # at rand dest
      return

    vec[0] /= mag
    vec[1] /= mag
    self.rect = self.rect.move(self.speed * vec[0], self.speed * vec[1])

class Bus(Car):

  def load_stuff(self):
    self.master_img = pygame.image.load(join('data', 'bus.png')).convert_alpha()
    self.image = self.master_img
    self.rect = self.image.get_rect()
    self.rect.topleft = rand(0, self.size[0]), 0

    self.health = 40
    self.speed = 3
    self.delay = 100 # to go in random dir
    self.pause = 0

class Van(Car):

  def load_stuff(self):
    self.master_img = pygame.image.load(join('data', 'van.png')).convert_alpha()
    self.image = self.master_img
    self.rect = self.image.get_rect()
    self.rect.topleft = rand(0, self.size[0]), 0

    self.health = 20
    self.speed = 4
    self.delay = 80 # to go in random dir
    self.pause = 0

