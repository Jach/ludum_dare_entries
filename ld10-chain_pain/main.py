#!/usr/bin/python
from sys import exit # If this fails.. They REALLY suck.
try:
  import pygame
  from pygame.locals import *
  from os import environ, path
  from random import randint

  # Actual game classes
  from menu import Menu
  from blood import Blood
  from master import Master
  from bar import Bar
  from timer import Timer
  from manpage import Man
  from besttime import BestTime
  from chain import Chain
except:
  print 'Could not import everything! You suck.'
  exit()
FPS = 60

class Game(Menu): # Need draw_text()

  def __init__(self, start=1):
    if start:
      pygame.init()

      environ['SDL_VIDEO_CENTERED'] = '1'
      self.scr_size = (800, 600)
      self.screen = pygame.display.set_mode(self.scr_size)
      pygame.display.set_caption('Chain Pain - By Jach')
    
    while 1:
      cont = self.load_menu()
      if cont == 'play':
        self.load_crap()
        self.play()
        break
      elif cont == 'time':
        self.high_time()
      elif cont == 'man':
        self.instructions()
      else:
        exit()

  def load_menu(self):
    m = Menu(self.screen)
    return m.load()

  def high_time(self): # Display highest time
    self.screen.fill( (0,0,0) ) # Kill menu
    best_time = BestTime(self.screen)

  def instructions(self):
    self.screen.fill( (0,0,0) ) # Kill menu
    manual = Man(self.screen)

  def play(self):

    self.screen.fill( (0,0,0) )
    self.clock = pygame.time.Clock()
    self.time_passed = 0
    self.manlinesses = 2 # Lives
    self.masters_allowed = 0 # To update
    self.time_since_whip = 0
    self.master_chosen = 0
    while 1:
      self.secs = self.clock.tick(FPS) / 1000.0
      self.time_passed += self.secs

      self.events()
      self.update_crap() # Updates, no more no less
      self.draw_crap() # Erases too
      self.collision_crap()

  def load_crap(self):
    # Loads all images, makes objects if applicable, adds any images and
    # rects to all_sprites{}
    # Now also loads all sounds at the very top!

    self.sounds = {'gasp' : self.load_sound('gasp.ogg'),\
        'ugh' : self.load_sound('ugh.ogg'),\
        'ow' : self.load_sound('ow.ogg'),\
        'ahh' : self.load_sound('ahh.ogg'),\
        'cry' : self.load_sound('cry.ogg'),\
        'whip' : self.load_sound('whip.ogg'),\
        'music' : self.load_sound('music1.ogg'),\
        'haha' : self.load_sound('haha.ogg')}
    self.sounds['music'].play(-1)

    self.all_sprites = {}

    self.bg_img = pygame.image.load(\
        path.join('data','background.png')).convert_alpha()

    playerimg=pygame.image.load(path.join('data', 'player.png')).convert_alpha()
    player_pos = [370,384] # Does not move?
    self.all_sprites['player'] = [playerimg,player_pos]

    self.master1 = Master('left', self.screen)
    self.master2 = Master('right', self.screen)
    self.all_sprites['master1'] = [self.master1.image, self.master1.rect]
    self.all_sprites['master2'] = [self.master2.image, self.master2.rect]

    big_bar = pygame.image.load(path.join('data','big_bar.png')).convert_alpha()
    big_bar_pos = (400-250, 500) # 500 bottom? 10 top? Edit background for bot
    self.all_sprites['big_bar'] = [big_bar, big_bar_pos]

    self.bar = Bar(self.sounds) # Moving bar
    self.all_sprites['moving_bar'] = [self.bar.image, self.bar.rect]

    self.timer = Timer() #Clock so player knows how long they've gone
    self.all_sprites['timer'] = [self.timer.image, self.timer.rect]

    manliness = pygame.image.load(\
        path.join('data','manliness.png')).convert_alpha()
    manliness1pos = (65, 1)
    manliness2pos = (100, 1)
    self.all_sprites['man1'] = [manliness, manliness1pos]
    self.all_sprites['man2'] = [manliness, manliness2pos]

    self.blood = Blood(self.screen, player_pos)
    self.all_sprites['blood'] = [self.blood.image, self.blood.rect]

  def draw_crap(self):
    # Erase everything first (yeah yeah optimization later)
    self.screen.blit(self.bg_img, (0,0) )
    for key in sorted(self.all_sprites):
      self.screen.blit(self.all_sprites[key][0], self.all_sprites[key][1])
    # Note: if I need something to blit on top of something else, give
    # it a z first letter or something.
    self.master1.chain.redraw_chain()
    self.master2.chain.redraw_chain()

    pygame.display.update()

  def update_crap(self):
    
    self.bar.update(self.secs) # Update bar
    self.all_sprites['moving_bar'][1] = self.bar.rect # Update rect

    self.timer.update(self.time_passed) # Update clock
    self.all_sprites['timer'][0] = self.timer.image # update image

    if not self.masters_allowed and randint(1, 70) == 1:
      self.masters_allowed = 1

    if self.masters_allowed and randint(1,5) == 1: # Rand used to slow down
      # Masters can update
      if not self.master_chosen:
        self.master_chosen = randint(1, 3)
      if self.master_chosen == 1:
        self.master1.update()
        self.all_sprites['master1'][0] = self.master1.image
      if self.master_chosen == 2:
        self.master2.update()
        self.all_sprites['master2'][0] = self.master2.image
      if self.master_chosen == 3:
        self.master1.update()
        self.master2.update()
        self.all_sprites['master1'][0] = self.master1.image
        self.all_sprites['master2'][0] = self.master2.image

      self.clock.tick(FPS)
      if self.master1.state == 0 and self.master2.state == 0: # Done animating
        self.masters_allowed = 0
        self.master_chosen = 0
        self.blood.image = self.blood.blank_image
        self.all_sprites['blood'][0] = self.blood.image
    else: # masters can't update, still need to draw chain
      pass

  def events(self):
    
    for event in pygame.event.get():

      if event.type == QUIT:
        exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          exit()
        if event.key == K_LEFT:
          self.bar.push = -1
        if event.key == K_RIGHT:
          self.bar.push = 1

  def collision_crap(self):
    if self.bar.rect.x < 0: # Class bounds it
      self.manlinesses -= 1
      self.sounds['haha'].play()
      if self.manlinesses == 0:
        self.gameover()
      else:
        self.all_sprites.pop('man2')
        self.bar = Bar(self.sounds) # Moving bar
        self.all_sprites['moving_bar'] = [self.bar.image, self.bar.rect]
        self.bar.v_change = -20
        self.all_sprites['player'][0] = pygame.image.load(\
            path.join('data','deadplayer.png')).convert_alpha()

    # Whip on player?
    if self.master1.state == 3: # Final chain
      self.bar.v_change = 200
      self.sounds['whip'].play()
      self.bar.play_sound()
      self.time_since_whip = self.time_passed
    if self.master2.state == 3:
      self.bar.v_change = 200
      self.sounds['whip'].play()
      self.bar.play_sound()
    if self.master1.state == 3 and self.master2.state == 3:
      self.bar.v_change = 400
    if (self.master1.state == 0 or self.master2.state == 0) and \
        self.time_passed - self.time_since_whip >= 0.5:
      self.bar.v_change = 0
    if self.master1.state == 2 or self.master2.state == 2:
      self.blood.render_blood()
      self.all_sprites['blood'][0] = self.blood.image

  def load_sound(self, sound):
    file = pygame.mixer.Sound(path.join('data',sound))
    return file

  def gameover(self):

    for e in self.sounds.itervalues():
      e.stop()

    self.sounds['cry'].play()
    self.all_sprites['player'][0] = pygame.image.load(\
        path.join('data','superdeadplayer.png')).convert_alpha()
    self.draw_crap()
    pygame.display.update()
    pygame.time.wait(700) # wait half a sec so they can see their death

    self.screen.fill( (0,0,0) )
    # Grab time
    mins = '%02d' % (self.time_passed / 60)
    secs = '%02d' % (self.time_passed % 60)

    font = pygame.font.Font(path.join('data','cour.ttf'), 50)
    font2 = pygame.font.Font(path.join('data','digib.ttf'), 70)
    font.set_underline(1)
    self.draw_text('Final Time', font, (5,0), (255,255,255) )
    font.set_underline(0)
    self.draw_text(mins + ':' + secs, font2, (5, 100), (255,255,255) )

    # Check if it was a high score
    f = open(path.join('data', 'best_time.txt'), 'r')
    line = f.next().replace('\n', '').split(' ')[1].split(':')

    beaten = 0
    if int(line[0]) * 60 + int(line[1]) < int(self.time_passed):
      self.draw_text('Congrats!', font,\
          (5, 200), (255,255,255))
      self.draw_text('You beat the best time!', font, (5,300), (255,255,255))
      self.draw_text('Enter your initials:', font, (5,400), (255,255,255))
      f.close()
      beaten = 1

    pygame.display.update()

    if not beaten:
      while 1:
        self.clock.tick(10)
        for event in pygame.event.get():
          if event.type == QUIT:
            exit()
          if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_RETURN:
              self.screen.fill( (0,0,0) )
              pygame.display.update()
              self.__init__(0)
    else:
      self.enter_initials(mins, secs, font)

  def enter_initials(self, mins, secs, font):
    font.set_underline(1)

    letters = 0
    initials = ''
    pygame.event.clear()
    while 1:
      self.clock.tick(10)
      if letters > 2:
        break
      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN and letters < 3:
          letters += 1
          self.draw_text(event.unicode.upper(), font,\
              (letters * 50, 500), (255,255,255))
          initials += event.unicode.upper()
      
    f = open(path.join('data', 'best_time.txt'), 'w')
    f.write(initials + ' ' + mins + ':' + secs)
    f.close()
    self.screen.fill( (0,0,0) )
    pygame.display.update()
    self.__init__(0)

if __name__ == '__main__':
  g = Game()
