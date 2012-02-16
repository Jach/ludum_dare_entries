# Dungeon Masters
import pygame
from chain import Chain
from os import path
class Master:

  def __init__(self, pos, screen):

    self.images = [\
       pygame.image.load(path.join('data','master_norm.png')).convert_alpha(),\
       pygame.image.load(path.join('data','master_whip1.png')).convert_alpha(),\
       pygame.image.load(path.join('data','master_whip2.png')).convert_alpha(),\
       pygame.image.load(path.join('data','master_whip3.png')).convert_alpha()]
    if pos == 'right':
      for i in range(len(self.images)):
        self.images[i] = pygame.transform.flip(self.images[i], 1, 0)
    self.image = self.images[0]
    self.rect = self.image.get_rect()
    self.width = self.rect.width
    self.height = self.rect.height
    self.state = 0 # for image
    self.chain = Chain(pos, screen)

    if pos == 'left':
      self.rect = self.rect.move(self.width + 30, 500-self.height)
    if pos == 'right':
      self.rect = self.rect.move(800-94-self.width, 500-self.height)


  def whip(self):
    # Change the state of chain
    self.chain.change()

  def update(self):
    self.state += 1
    if self.state == 4: self.state = 0 # turn over
    self.image = self.images[self.state]
    self.whip()
