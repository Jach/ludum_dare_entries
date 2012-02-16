#!/usr/bin/python
import pygame
from pygame.locals import *
from sys import exit
from os.path import join
from random import randint as rand

from menu import Menu
from turret import * # tower, turret, laser
from enemies import *

pygame.init()
SIZE = (800,600)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Femme Tower -- By Jach')

class Ground(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface((SIZE[0], 50))
    self.image.fill((0x3d,0xa4,0x2c))
    self.rect = self.image.get_rect()
    self.rect.topleft = (0, SIZE[1]-50)

  def update(self):
    pass

class Integrity(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface( (100,10) )
    self.image.fill((0,255,0))
    self.rect = self.image.get_rect()
    self.rect.topleft = (10, 10)

    self.life = 100
    self.oldlife = 100
  
  def update(self):
    if self.life != self.oldlife:
      self.oldlife = self.life
      self.image.fill((255,0,0))
      if self.life > 0:
        pygame.draw.rect(self.image, (0,255,0), (0,0,self.life,10))

class ThingsLeft(pygame.sprite.Sprite):

  def __init__(self, peeps=100): # peeps being, uh, enemies
    pygame.sprite.Sprite.__init__(self)

    self.peeps = peeps
    self.oldpeeps = 0
    self.font = pygame.font.Font(join('data', 'cour.ttf'), 20)

    self.image = pygame.Surface((200,30))
    self.trans = (22,38,111) # random color
    self.image.fill(self.trans)
    self.image.set_colorkey(self.trans)
    self.rect = self.image.get_rect()
    self.rect.topleft = (125, 5)

  def update(self):
    if self.oldpeeps != self.peeps:
      self.oldpeeps = self.peeps
      if self.peeps == 1: mess = ' kill left'
      else: mess = ' kills left'
      n = self.font.render(str(self.peeps) + mess, 1, (0,0,0))
      self.image.fill(self.trans)
      self.image.blit(n, (0,0))

class Game:

  def __init__(self):

    # Load sounds

    self.sounds = {}
    self.sounds['lightning'] = pygame.mixer.Sound(join('data','lightning.wav'))
    self.sounds['laser'] = pygame.mixer.Sound(join('data', 'laser.wav'))
    self.sounds['crap'] = pygame.mixer.Sound(join('data', 'crap.wav'))
    self.sounds['bg'] = pygame.mixer.Sound(join('data', 'bg.wav'))
    self.sounds['bg'].set_volume(0.5)
    self.sounds['bg'].play(-1)

    # Load backgrounds

    self.sky_col = (0x2c, 0x84, 0xa4)
    self.bg = pygame.Surface(SIZE)
    self.bg.fill(self.sky_col)


    self.go()

  def go(self):
    # stats
    self.kills = 0
    self.victory = 0

    # bg sprites
    cloud1 = Cloud()
    cloud2 = Cloud()
    cloud3 = Cloud()
    self.bg_sprites = pygame.sprite.OrderedUpdates(cloud1, cloud2, cloud3)


    # player sprites
    self.tower = Tower()
    self.turret = Turret()
    self.player_sprites = pygame.sprite.OrderedUpdates(self.tower, self.turret)

    # enemy sprites
    self.enemy_sprites = pygame.sprite.OrderedUpdates()

    # menu sprites
    self.ground = Ground()
    self.integ = Integrity()
    self.things = ThingsLeft()
    self.menu_sprites = pygame.sprite.OrderedUpdates(self.ground, self.integ, self.things)

    self.opening() # opening plot thingy
    self.reallystart()

  def reallystart(self):

    self.clock = pygame.time.Clock()
    self.keep_going = 1

    while self.keep_going and not self.victory:
      self.clock.tick(40)

      for event in pygame.event.get():

        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.keep_going = 0
          if event.key == K_SPACE:
            # fire the laser!
            self.fire_laser(self.turret.dir)

      self.check_collisions()
      self.add_enemies()
      
      # blit
      self.bg_sprites.clear(screen, self.bg)
      self.player_sprites.clear(screen, self.bg)
      self.enemy_sprites.clear(screen, self.bg)
      self.menu_sprites.clear(screen, self.bg)

      self.bg_sprites.update()
      self.player_sprites.update()
      self.enemy_sprites.update()
      self.menu_sprites.update()

      dirty_rects = []
      dirty_rects.append(self.bg_sprites.draw(screen))
      dirty_rects.append(self.player_sprites.draw(screen))
      dirty_rects.append(self.enemy_sprites.draw(screen))
      dirty_rects.append(self.menu_sprites.draw(screen))
      all_dirt = dirty_rects[0] + dirty_rects[1] + dirty_rects[2] + dirty_rects[3]
      pygame.display.update(all_dirt)

    self.closing()

  def opening(self):
    font = pygame.font.Font(join('data', 'cour.ttf'), 25)
    mess = (
        '',
        'For some reason, 100 various knights, owls,',
        'and angry clouds are attacking a tower full',
        'of women! Defend with the Tamtuff Turret!',
        'Left and right rotate, space shoots the red',
        'laser.',
        '',
        'Press Enter to start.'
        )
    labs = []
    for line in mess:
      tmp = font.render(line, 1, (255,255,255))
      labs.append(tmp)

    clock = pygame.time.Clock()
    keep_going = 1
    while keep_going:
      clock.tick(10)
      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          if event.key == K_RETURN:
            keep_going = 0
      screen.fill((0,0,0))
      for i in range(len(labs)):
        screen.blit(labs[i], (50, 30*i))
      pygame.display.update()
    
    screen.blit(self.bg, (0,0))
    pygame.display.update()
  
  def closing(self):
    self.sounds['bg'].stop()
    font = pygame.font.Font(join('data', 'cour.ttf'), 25)
    win = font.render('You win!', 1, (255,255,255))
    lose = font.render('You lose!', 1, (255,255,255))
    screen.fill((0,0,0))
    if self.victory:
      screen.blit(win, (100,100))
    else:
      screen.blit(lose, (100,100))
    pygame.display.update()
    pygame.time.wait(1000)

  def add_enemies(self):
    if rand(1, 200) == 32: # ANGRY CLOUD
      ac = AngryCloud()
      self.enemy_sprites.add(ac)
    if rand(1, 50) == 2: # Knight
      k = Knight()
      self.enemy_sprites.add(k)
    if rand(1, 150) == 3: # Owl
      o = Owl()
      self.enemy_sprites.add(o)

  def check_collisions(self):
    # check lasers against edge of world or ground
    for sprite in self.player_sprites.sprites():
      if 'Laser' in str(sprite):
        r = sprite.rect
        if r.colliderect(self.ground.rect) or r.right < 0 or r.left > SIZE[0] \
            or r.bottom < 0:
          self.player_sprites.remove(sprite)
        # check laser against enemies
        for enemy in self.enemy_sprites.sprites():
          if enemy.rect.colliderect(sprite.rect):
            enemy.hit()
            self.player_sprites.remove(sprite)
            if enemy.hp <= 0:
              self.enemy_sprites.remove(enemy)
              self.things.peeps -= 1

    # check for collision with knights
    for sprite in self.enemy_sprites.sprites():
      if 'Knight' in str(sprite):
        if sprite.rect.colliderect(self.tower.rect.inflate(-20,-20)):
          self.integ.life -= 2
          self.enemy_sprites.remove(sprite)
      if 'AngryCloud' in str(sprite):
        if sprite.attack:
          L = Lightning(sprite.rect.center)
          self.enemy_sprites.add(L)
          self.sounds['lightning'].play()
          self.integ.life -= 10
          sprite.attack_pause = 0
      if 'Lightning' in str(sprite):
        if sprite.done:
          self.enemy_sprites.remove(sprite)
      if 'Owl' in str(sprite):
        if sprite.attack:
          C = Bowlmb(sprite.rect.center)
          self.enemy_sprites.add(C)
          self.sounds['crap'].play()
      if 'Bowlmb' in str(sprite):
        if sprite.rect.colliderect(self.tower.rect.inflate(-50,-50)):
          self.integ.life -= 3
          self.enemy_sprites.remove(sprite)

    if self.integ.life <= 0:
      print 'You lose'
      self.keep_going = 0
    elif self.things.peeps <= 0:
      print 'You win!'
      self.victory = 1


  def fire_laser(self, dir): # RAAAAAAAAR!
    # contra3-style laser
    las = Laser(dir)
    self.player_sprites.add(las)
    self.sounds['laser'].play()

if __name__ == '__main__':
  menu = Menu(screen)
  cont = menu.start()
  while cont:
    g = Game()
    cont = menu.start()
