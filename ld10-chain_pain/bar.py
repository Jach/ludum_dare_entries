# Moving bar
import pygame
from random import randint
class Bar:

  v_change = 0 # For when player is hit, we increase v briefly
  def __init__(self, sounds):

     self.image = pygame.Surface((5, 60) )
     pygame.draw.line(self.image, (0,0,255), (1,0), (1, 60), 5)
     self.rect = self.image.get_rect()
     self.rect = self.rect.move(400, 520)

     if randint(1,2) == 1:
       self.push = 1 # Push direction
     else:
       self.push = -1
     self.green_speed = 300 # Pixels per second
     self.yellow_speed = 400
     self.orange_speed = 500
     self.red_speed = 600 # Might want to reverse these?

     self.sounds = sounds
     self.current_sound = 'gasp'

  def play_sound(self):
    self.sounds[self.current_sound].play()

  def update(self, secs):
    # Frame rate check
    if secs > 1.0:
      secs = 0.033
      # average rate at 30 fps on my comp, this will keep it moving at speed

    # Determine which section bar is in to determine speed
    if 187+150 <= self.rect.x <= 312+150:
      speed = self.green_speed
      self.current_sound = 'gasp'
    elif 125+150 <= self.rect.x <= 186+150 or 313+150 <= self.rect.x <= 375+150:
      speed = self.yellow_speed
      self.current_sound = 'ugh'
    elif 62+150 <= self.rect.x <= 124+150 or 376+150 <= self.rect.x <= 437+150:
      speed = self.orange_speed
      self.current_sound = 'ow'
    elif 10+170 <= self.rect.x <= 61+170 or 438+150 <= self.rect.x <= 490+150:
      speed = self.red_speed
      self.current_sound = 'ahh'
    else: # Something happen?
      speed = 0
    speed += self.v_change
    speed *= self.push

    self.rect = self.rect.move(speed * secs, 0)

    # Bound the x (if it hits either though it dies, which will
    # be detected in the colission method of main class when x < 0)
    if self.rect.x < 10+170:
      self.rect.x = -10
    if self.rect.x > 490+125:
      self.rect.x = -10
