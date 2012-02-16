import pygame
from pygame.locals import *
from os import path
class Menu:

  def __init__(self, screen):
    
    self.screen = screen
    self.ss = size = screen.get_size()
    self.title =pygame.image.load(path.join('data','title.png')).convert_alpha()
    self.tit_pos = (self.ss[0]/2 - 150, 20)

    self.pointer = pygame.image.load(\
        path.join('data','cherry.png')).convert_alpha()
    self.point_pos = [ (size[0]/20, size[1]/5),\
        (size[0]/20, 2*size[1]/5),\
        (size[0]/20, 3*size[1]/5),\
        (size[0]/20, 4*size[1]/5) ]
    # Possible pointer positions

    self.load_choices()
    self.selected = 'play'
    self.sound = pygame.mixer.Sound(path.join('data','music2.ogg'))
    self.sound.play()

  def load(self):
    self.screen.blit(self.title, self.tit_pos)

    clock = pygame.time.Clock()
    black = (0,0,0)
    while 1:
      clock.tick(10)

      for event in pygame.event.get():
        if event.type == QUIT:
          return 'quit'
        if event.type == KEYDOWN:
          if event.key == K_DOWN:
            if self.selected == 'play':
              self.selected = 'time' # highest time
              self.screen.fill(black, (self.point_pos[0], (78,78)))
            elif self.selected == 'time':
              self.selected = 'man' # manual
              self.screen.fill(black, (self.point_pos[1],(78,78)))
            elif self.selected == 'man':
              self.selected = 'quit'
              self.screen.fill(black, (self.point_pos[2], (78,78)))
            elif self.selected == 'quit':
              self.selected = 'play'
              self.screen.fill(black, (self.point_pos[3],(78,78)))
          if event.key == K_UP:
            if self.selected == 'play':
              self.selected = 'quit'
              self.screen.fill(black, (self.point_pos[0],(78,78)))
            elif self.selected == 'quit':
              self.selected = 'man'
              self.screen.fill(black, (self.point_pos[3],(78,78)))
            elif self.selected == 'time':
              self.selected = 'play'
              self.screen.fill(black, (self.point_pos[1],(78,78)))
            elif self.selected == 'man':
              self.selected = 'time'
              self.screen.fill(black, (self.point_pos[2],(78,78)))
          if event.key == K_RETURN:
            self.sound.stop()
            return self.selected
      # Draw pointer
      if self.selected == 'play':
        self.screen.blit(self.pointer, self.point_pos[0])
      if self.selected == 'time':
        self.screen.blit(self.pointer, self.point_pos[1])
      if self.selected == 'man':
        self.screen.blit(self.pointer, self.point_pos[2])
      if self.selected == 'quit':
        self.screen.blit(self.pointer, self.point_pos[3])

      pygame.display.update()

  def draw_text(self, text, font, pos, color):
    t_im = font.render(text, 1, color)
    t_rect = t_im.get_rect()
    t_rect = t_rect.move(pos)
    self.screen.blit(t_im, t_rect)
    pygame.display.update(t_rect)

  def load_choices(self):
    """Play
       Best Time
       Instructions
       Quit"""
    # Also draws pointer

    font = pygame.font.Font(path.join('data','cour.ttf'), 20)
    color = (228,28,0)

    self.draw_text('Play', font, (self.ss[0]/5,self.ss[1]/5), color)
    self.draw_text('Best Time', font, (self.ss[0]/5,2*self.ss[1]/5), color)
    self.draw_text('Instructions', font, (self.ss[0]/5,3*self.ss[1]/5), color)
    self.draw_text('Quit', font, (self.ss[0]/5,4*self.ss[1]/5), color)

    # Draw pointer
    self.screen.blit(self.pointer, self.point_pos[0])

