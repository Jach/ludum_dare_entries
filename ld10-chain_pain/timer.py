# Timer is a big clock
import pygame
from os import path 
from menu import Menu
class Timer(Menu): # Inherits menu for draw_text() function.

  def __init__(self):

    self.font = pygame.font.Font(path.join('data', 'digib.ttf'), 20)
    self.minute = '00'
    self.second = '00'
    min_width, min_height = self.font.size(self.minute)

    self.image = pygame.Surface( (2*min_width+15, min_height) )
    self.screen = self.image
    self.rect = self.image.get_rect()
    self.rect = self.rect.move(2, 2)

    self.min_pos = (5,0)
    self.col_pos = (min_width+5,0) # Colon:
    self.sec_pos = (min_width+10,0)

    self.color = (0, 0, 255)
    self.draw_text(self.minute, self.font, self.min_pos, self.color)
    self.draw_text(':', self.font, self.col_pos, self.color)
    self.draw_text(self.second, self.font, self.sec_pos, self.color)

  def update(self, time): # Time in secs
    self.minute = "%02d" % (time/60)
    self.second = "%02d" % (time%60)
    self.image.fill( (0,0,0) )
 
    self.draw_text(self.minute, self.font, self.min_pos, self.color)
    self.draw_text(':', self.font, self.col_pos, self.color)
    self.draw_text(self.second, self.font, self.sec_pos, self.color)
