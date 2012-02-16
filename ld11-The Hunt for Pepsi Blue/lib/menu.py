import pygame
from pygame.locals import *
from os.path import join

class Menu(object):
  """Displays menu and gives introduction."""

  def __init__(self):
    f = open(join('data', 'man.txt'))
    self.man = [e.replace('\n', '') for e in f.readlines()]
    self.man_voice = pygame.mixer.Sound(join('data', 'man_voice.ogg'))
    self.beat = pygame.mixer.Sound(join('data', 'menu_beat.ogg'))
    self.map = pygame.image.load(join('data', 'map.png')).convert()
    self.screen = pygame.display.get_surface()
    self.size = self.screen.get_width(), self.screen.get_height()
    self.headerfont = pygame.font.Font(join('data', 'courbd.ttf'), 35)
    self.headerfont.set_underline(1)
    self.itemfont = pygame.font.Font(join('data', 'courbd.ttf'), 30)
    self.manfont = pygame.font.Font(join('data', 'courbd.ttf'), 25)
    self.color = (0,0,128)

  def start(self):
    if pygame.event.peek(QUIT):
      return
    self.beat.play(-1)

    header = self.headerfont.render("The Hunt for Pepsi Blue", 1, self.color)
    start = self.itemfont.render("1: Start", 1, self.color)
    man = self.itemfont.render("2: Instructions", 1, self.color)
    quit = self.itemfont.render("3: Quit", 1, self.color)

    self.clock = pygame.time.Clock()
    while 1:
      self.clock.tick(5)
      for event in pygame.event.get():
        if event.type == QUIT:
          return 0
        if event.type == KEYDOWN:
          if event.key == K_1:
            self.beat.stop()
            return 1
          elif event.key == K_2:
            cont = self.manpage()
            if not cont:
              return 0
          elif event.key == K_3:
            self.beat.stop()
            return 0

      self.screen.blit(self.map, (0,0))
      self.screen.blit(header, (self.size[0]/10, self.size[1]/7) )
      self.screen.blit(start, (self.size[0]/8, 3*self.size[1]/7) )
      self.screen.blit(man, (self.size[0]/8, 4*self.size[1]/7) )
      self.screen.blit(quit, (self.size[0]/8, 5*self.size[1]/7) )

      pygame.display.update()

  def manpage(self):
    # Make a big surface for the font to be on, and move it down each frame.
    lw, lh = self.manfont.size(self.man[-3]) # longest line
    fh = len(self.man) * (lh + len(self.man)) # file height
    img = pygame.Surface( (lw+20, fh) )
    rect = img.get_rect()
    rect = rect.move(20, self.size[1])

    # Render text onto it.
    white = (255,255,255)
    black = (0,0,0)
    for i in range(len(self.man)):
      line = self.manfont.render(self.man[i], 1, white)
      img.blit(line, (0, i * lh + lh))
    
    # Animate!
    self.man_voice.play()
    speed = 55 # pixels per second
    not_done = 1
    self.clock.tick()
    while not_done:
      secs = self.clock.tick(45) / 1000.0

      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.event.post(pygame.event.Event(QUIT))
          return 0
        elif event.type == KEYDOWN:
          return 1

      if rect.bottom <= 3*lh:
        not_done = 0
        return 1

      self.screen.fill(black)
      self.screen.blit(img, rect)
      rect = rect.move(0, -speed*secs)
      pygame.display.update()

