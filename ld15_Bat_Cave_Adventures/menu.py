import pygame
from pygame.locals import *
from os import path
join = path.join

class Selector(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((30,10))
    self.rect = self.image.get_rect()

  def update(self):
    pass

class Menu:
  
  def __init__(self, screen):
    self.screen = screen
    self.font1 = pygame.font.Font(join('data','cour.ttf'), 30)
    self.font2 = pygame.font.Font(join('data','cour.ttf'), 22)

    self.bg = pygame.image.load(join('data', 'bg.png')).convert()#(0x8B, 0x69, 0x14) # brownish
    self.white = (255,255,255)

    self.choice = 1 # 1 play, 0 quit
    self.selector = Selector()
    self.sel_grp = pygame.sprite.Group(self.selector)

    self.play = self.font2.render("Play", 1, self.white)
    self.quit = self.font2.render("Quit", 1, self.white)

    self.pos = [ (600, 400), (400, 400), (550, 410), (350, 410) ] # quit, play

  def redraw(self):
    title = self.font1.render("Bat Cave Adventures!", 1, self.white)
    helper = self.font2.render("Collect blood to win!", 1, self.white)

    self.screen.blit(self.bg, (0,0))
    self.screen.blit(title, (200, 200))
    self.screen.blit(helper, (300, 300))
    self.screen.blit(self.play, self.pos[1])
    self.screen.blit(self.quit, self.pos[0])
    self.screen.blit(self.selector.image, self.pos[1+2])
    pygame.display.update()

  def loop(self):
    keep_going = 1
    clock = pygame.time.Clock()
    while keep_going:
      clock.tick(10)

      r1 = self.pos[self.choice+2], self.selector.rect.bottomright
      for event in pygame.event.get():
        if event.type == QUIT:
          return 0
        if event.type == KEYDOWN:
          if event.key == K_RIGHT or event.key == K_LEFT:
            self.choice ^= 1
          elif event.key == K_RETURN:
            return self.choice
          elif event.key == K_ESCAPE:
            return 0

      self.sel_grp.clear(self.screen, self.bg)
      self.selector.rect.topleft = self.pos[self.choice+2]
      self.sel_grp.draw(self.screen)
      r2 = self.pos[self.choice+2], self.selector.rect.bottomright
      pygame.display.update((r1, r2))
