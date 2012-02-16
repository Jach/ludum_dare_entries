import pygame
from pygame.locals import *
from os.path import join

class Menu:

  def __init__(self, screen):

    self.screen = screen
    self.size = screen.get_size()

    self.bg = pygame.image.load(join('data', 'title.png')).convert()
    
    self.ifont = pygame.font.Font(join('data', 'cour.ttf'), 28)
    self.ifont.set_bold(1)
    self.fcolor = (0x12,0x27,0x5b)

    self.mi = menu_items = 6 # play, quit (+1 *2)
    self.pointer = pygame.Surface((25,25))
    pygame.draw.circle(self.pointer, self.fcolor, (13,13), (13))
    self.pointer.set_colorkey((0,0,0))
    self.pointer_pos = [
        (11*self.size[0]/15, (menu_items-2)*self.size[1]/menu_items),
        (11*self.size[0]/15, (menu_items-1.5)*self.size[1]/menu_items)
        ]

  
  def start(self):

    self.screen.blit(self.bg, (0,0))
    self.load_stuff()

    self.selected = 'play'
    clock = pygame.time.Clock()

    while 1:
      clock.tick(10)

      for event in pygame.event.get():
        if event.type == QUIT:
          return 0
        if event.type == KEYDOWN:
          if event.key == K_DOWN:
            if self.selected == 'play':
              self.selected = 'quit'
              self.erase(self.pointer_pos[0])
            elif self.selected == 'quit':
              self.selected = 'play'
              self.erase(self.pointer_pos[1])
          if event.key == K_UP:
            if self.selected == 'play':
              self.selected = 'quit'
              self.erase(self.pointer_pos[0])
            elif self.selected == 'quit':
              self.selected = 'play'
              self.erase(self.pointer_pos[1])
          if event.key == K_RETURN:
            if self.selected == 'play':
              return 1
            elif self.selected == 'quit':
              return 0
          if event.key == K_ESCAPE:
            return 0
      # draw pointer
      if self.selected == 'play':
        self.screen.blit(self.pointer, self.pointer_pos[0])
      elif self.selected == 'quit':
        self.screen.blit(self.pointer, self.pointer_pos[1])

      pygame.display.update()

  def load_stuff(self):

    col = self.fcolor
    menu_items = self.mi
    self.draw_text('Play', self.ifont, \
        (12*self.size[0]/15, (menu_items-2)*self.size[1]/menu_items), col)
    self.draw_text('Quit', self.ifont, \
        (12*self.size[0]/15, (menu_items-1.5)*self.size[1]/menu_items), col)

    # pointer
    self.screen.blit(self.pointer, self.pointer_pos[0])

  def draw_text(self, text, font, pos, color):
    t_im = font.render(text, 1, color)
    t_rect = t_im.get_rect()
    t_rect = t_rect.move(pos)
    self.screen.blit(t_im, t_rect)
    pygame.display.update(t_rect)
    
  def erase(self, pos): # for pointer (inefficient?) (cheat, fill with bg)
    """rect = pygame.Rect(pos, (25,25))
    part = self.bg.subsurface(rect)
    self.screen.blit(part, pos)"""
    self.screen.fill( (0x2c, 0x84, 0xa4), (pos, (25,25)))
