#!/usr/bin/env python

from globals import * # pygame, etc.

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Bat Cave Adventures! -- By Jach")

from menu import Menu
from bat import Bat
from mapdata import *
from blocks import *

class Game:

  def __init__(self):
    
    self.bigfont = pygame.font.Font(join('data', 'cour.ttf'), 22)
    self.font = pygame.font.Font(join('data', 'cour.ttf'), 12)
    self.world = [0] * 9
    self.map_sprites = [0] * 9
    self.world_frame = 4
    self.generate_panels()

    self.player = Bat((SIZE[0]/2, SIZE[1]/2), self.map_sprites)
    #self.player.collectibles = 10
    self.player.world_frame = self.world_frame

    self.player_sprites = SPRITE_GRP(self.player)

    self.draw_panel()
    self.loop()
    
  def draw_panel(self):
      self.bg = self.world[self.world_frame]
      screen.blit(self.bg, (0,0))
      pygame.display.update()

  def generate_panels(self):
    bg = pygame.image.load(join('data', 'bg.png')).convert()
    for k,v in enumerate(self.world):
      surf = pygame.Surface(SIZE)
      surf.blit(bg, (0,0))
      """col = ( rand(0,255), rand(0,255), rand(0,255) )
      oppcol = map(lambda x: 255 - x, col)
      surf.fill(col)
      draw_text(surf, str(k), self.bigfont, (SIZE[0]/2,SIZE[1]/2), oppcol, 1)"""
      self.map_sprites[k] = SPRITE_GRP()
      self.prepare_map_sprites(k)
      self.map_sprites[k].draw(surf)
      self.world[k] = surf

  def prepare_map_sprites(self, frame):
    map = eval("map%d" % frame)
    rows = len(map)
    cols = len(map[0])
    for y in range(rows):
      for x in range(cols):
        cell = map[y][x]
        pos = TILE_SIZE * x, TILE_SIZE * y
        if cell == '.': continue
        elif cell == '#':
          self.map_sprites[frame].add(Block(pos, 'cavewall'))
        elif cell == 'v':
          self.map_sprites[frame].add(Block(pos, 'stalactite'))
        elif cell == '^':
          self.map_sprites[frame].add(Block(pos, 'stalagmite'))
        elif cell == '*':
          self.map_sprites[frame].add(Block(pos, 'collectible'))
        elif cell in '0123456789abcdef':
          self.map_sprites[frame].add(Block(pos, 'gate', int(cell, 16)))

  def loop(self):
    self.clock = pygame.time.Clock()
    self.keep_going = 1
    while self.keep_going:
      self.clock.tick(40)

      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.keep_going = 0

      self.player_sprites.clear(screen, self.bg)

      try:
        self.player_sprites.update()
      except Exception, msg:
        if msg.args[0] == 'killed':
          self.death()
          self.world_frame = 4
          self.player.world_frame = self.world_frame
          self.player.rect.center = SIZE[0]/2, SIZE[1]/2
          self.draw_panel()
        elif msg.args[0] == 'itemgot':
          self.player.collectibles += 1
          item = msg.args[1]
          col = self.bg.get_at(map(lambda x: x - 1, item.rect.topleft))
          item.image.fill(col)
          self.bg.blit(item.image, item.rect)
          screen.blit(item.image, item.rect)
          pygame.display.update(item.rect)
          item.kill()
          if self.player.collectibles == 11:
            self.win()
            self.keep_going = 0
        else:
          exit(msg.args)


      self.check_bounds()

      dirties = self.player_sprites.draw(screen)

      pygame.display.update(dirties)

  def check_bounds(self):
    shifted = 1
    off = 5
    r = self.player.rect
    if r.bottom < r.height/2 - off: # go up
      self.world_frame -= 3
      self.player.rect.top = SIZE[1] - r.height/2 - off
    elif r.right < r.width/2 - off: # go left
      self.world_frame -= 1
      self.player.rect.left = SIZE[0] - r.width/2 - off
    elif r.top > SIZE[1] - r.height/2 + off: # go down
      self.world_frame += 3
      self.player.rect.bottom = r.height/2 + off
    elif r.left > SIZE[0] - r.width/2 + off: # go right
      self.world_frame += 1
      self.player.rect.right = r.width/2 + off
    else:
      shifted = 0

    if shifted:
      self.player.world_frame = self.world_frame
      self.fancy_panel_transition()
      self.draw_panel()

  def fancy_panel_transition(self):
    bk = 0,0,0
    which = rand(1, 3)
    if which == 1:
      for x in range(0, SIZE[0], 100):
        for y in range(0, SIZE[1], 100):
          screen.fill(bk, (x,y,100,100))
          pygame.display.update((x,y,100,100))
          self.clock.tick(40)
    elif which == 2:
      for y in range(0, SIZE[1], 100):
        for x in range(0, SIZE[0], 100):
          screen.fill(bk, (x,y,100,100))
          pygame.display.update((x,y,100,100))
          self.clock.tick(40)
    elif which == 3:
      for y in range(0, SIZE[1], 100):
        for x in range(0, SIZE[0], 100):
          if int(str(x)[0]) % 2 != 0 and int(str(y)[0]) %2 == 0:
            continue
          if int(str(y)[0]) % 2 != 0 and int(str(x)[0]) % 2 == 0:
            continue
          screen.fill(bk, (x,y,100,100))
          pygame.display.update((x,y,100,100))
          self.clock.tick(20)
  
  def death(self):
    self.blank_scr('Be careful! You impaled yourself!\n\nNow you\'re back in the main cavern.')

  def win(self):
    self.blank_scr('Well. You win. I guess I should\ngive you a prize or something.\n\nI know! Enter this code:\n\nbe121740bf988b2225a313fa1f107ca1\n\nIn the never-to-be-made\nsequel and I\'ll give you a special prize.\n\n...\n\nNo seriously, this is it. Sorry?')
        
  def blank_scr(self, txt):
    screen.fill((0,0,0))
    texts = txt.split('\n')
    lines = len(texts)
    for i in xrange(lines):
      draw_text(screen, texts[i], self.bigfont, (SIZE[0]/2, 3*SIZE[1]/5 - 25*(lines - i)), (255,255,255), 1)
    draw_text(screen, 'Press any key to continue', self.font, (SIZE[0]/2, 4*SIZE[1]/5), (255,255,255), 1)
    while 1:
      self.clock.tick(10)
      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          return
      pygame.display.update()

if __name__ == '__main__':
  pygame.mixer.init()
  bg_music = pygame.mixer.Sound(join('data', 'bg_music.wav'))
  bg_music.play(-1)
  menu = Menu(screen)
  menu.redraw()
  go = menu.loop()
  while go:
    g = Game()
    menu.redraw()
    go = menu.loop()
