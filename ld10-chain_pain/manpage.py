# AKA Instructions
import pygame
from pygame.locals import *
from os import path
from sys import exit
from menu import Menu

class Man(Menu): # Need draw text function

  def __init__(self, screen):
    
    s_width, s_height = screen.get_size()

    f = open(path.join('data','man.txt'))
    file = [e.replace('\n', '') for e in f.readlines()] # No \ns!
    font = pygame.font.Font(path.join('data', 'cour.ttf'), 25)

    line_width, line_height = font.size(file[0]) # Longest line
    t_img = pygame.Surface((line_width+20, len(file)*(line_height+len(file))))
    t_rect = t_img.get_rect()
    t_rect = t_rect.move(10, s_height)
    speed = -80 #pps
    self.screen = t_img # For draw_text()

    for i in range(len(file)):
      self.draw_text(file[i], font, (0,i * line_height + line_height),\
          (255,255,255) )

    clock = pygame.time.Clock()
    while 1:
      secs = clock.tick(30) / 1000.0

      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          break

      screen.fill( (0,0,0) )
      screen.blit(t_img, t_rect)
      
      t_rect = t_rect.move(0, speed * secs)
      pygame.display.update()
      
      if t_rect.bottom < 0:
        break
