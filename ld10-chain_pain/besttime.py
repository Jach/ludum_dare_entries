import pygame
from pygame.locals import *
from os import path
from sys import exit
from menu import Menu
class BestTime(Menu): # Need draw_text()

  def __init__(self, screen):
    self.screen = screen

    f = open(path.join('data', 'best_time.txt'))
    score = f.next().replace('\n', '')
    score = score.replace(' ', ' '*15)

    font = pygame.font.Font(path.join('data','digib.ttf'), 72)
    font2 = pygame.font.Font(path.join('data', 'cour.ttf'), 74)
    font2.set_underline(1)

    header = 'Player  Time'
    self.draw_text(header, font2, (5,5), (255,255,255))
    self.draw_text(score, font, (5,100), (255,255,255))

    escape = 0 # Delay
    clock = pygame.time.Clock()
    while not escape:
      clock.tick(10)

      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            escape = 1
          if event.key == K_RETURN:
            escape = 1
      pygame.display.update()

    self.screen.fill( (0,0,0) )
    pygame.display.update()
