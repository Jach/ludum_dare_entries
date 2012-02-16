import pygame
from pygame.locals import *
from os.path import join
from math import sin, cos, sqrt

class Tank(pygame.sprite.Sprite):
  """This is the player's Tank class."""

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    
    self.master_img = pygame.image.load(join('data', \
        'tank.png')).convert_alpha()
    self.image = self.master_img
    self.rect = self.image.get_rect()
    self.rect = self.rect.move(300, 300)
    self.master_img = pygame.transform.rotate(self.master_img, -90)
    # too lazy to change image itself..

    ss = pygame.display.get_surface()
    self.size = ss.get_width(), ss.get_height()
    self.pi = 3.141592653589793238462643383279502884197169399375105820974944
    # Yes, I do know that many digits, and yes, I'm just showing off.
    self.lin_speed = 6 # linear-pixels per frame
    self.rotate_speed = 6 # degrees...
    self.angle = 90 # degrees (it starts facing up)
    self.rad_angle = self.pi/2 # for sine and cosine

  def update(self):
    if self.angle >= 360:
      self.angle -= 360
    if self.angle < 0:
      self.angle += 360
    self.rad_angle = self.pi * self.angle / 180.
    old_ang = self.angle
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]: # rotate counter clockwise
      self.angle += self.rotate_speed
    if keys[K_RIGHT]: # rotate clockwise
      self.angle -= self.rotate_speed
    if keys[K_UP]: # move forward
      self.rect = self.rect.move(self.lin_speed*cos(self.rad_angle), \
          -self.lin_speed*sin(self.rad_angle))
    if keys[K_DOWN]: # move backward
      self.rect = self.rect.move(-self.lin_speed*cos(self.rad_angle), \
          self.lin_speed*sin(self.rad_angle))
    
    if old_ang != self.angle:
      old_cent = self.rect.center
      self.image = pygame.transform.rotate(self.master_img, self.angle)
      self.rect = self.image.get_rect()
      self.rect.center = old_cent
    
    # handle collisions with sides
    if self.rect.left <= 0:
      self.rect.x = 0
    if self.rect.right >= self.size[0]:
      self.rect.right = self.size[0]
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= 380:
      self.rect.bottom = 380

class Shell(pygame.sprite.Sprite):
  """Tank's bullet. Shoots straight for a bit. (Should it explode?)"""
  
  def __init__(self, player):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface( (10,10) )
    self.image.set_colorkey( (0,0,0) )
    pygame.draw.circle(self.image, (128,128,128), (5,5), 5)
    self.rect = self.image.get_rect()
    self.rect.center = player.rect.center
    init_x, init_y = player.rect.centerx, player.rect.centery
    self.at_dest = 0
    range = 300 # pixels
    self.speed = 8

    # Pick a somewhat random destination! Or not, but yeah.... 6:18am.
    dir = player.rad_angle
    self.dest = init_x + range*cos(dir), init_y - range*sin(dir)

  def update(self):
    # vector between current pos and destination
    vec = [self.dest[0] - self.rect.centerx, self.dest[1] - self.rect.centery]
    # normalize
    mag = sqrt( vec[0]**2 + vec[1]**2 )
    if mag <= 5 or self.rect.bottom >= 400:
      # essentially at dest (or bounds (only bottoms side really matters))
      self.at_dest = 1
      self.dest = self.rect.center
      return

    vec[0] /= mag
    vec[1] /= mag
    self.rect = self.rect.move(self.speed*vec[0], self.speed*vec[1])

