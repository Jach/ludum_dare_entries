#!/usr/bin/python
try:
  import psyco
  psyco.full()
except ImportError:
  print "Aww, you don't have Pysco. Oh well."

# I don't think you'll -need- psyco, but it's here anyway.
# Yes I'm doing some crazy stuff to justify it to save me some thinking time.

from globals import *

# Game classes

from Menu import *
from Statics import *
from MapData import *
from Camera import *
from Player import *
from Blocks import *
from Wall import *

class Game:

  def __init__(self, screen):
    self.screen = screen
    self.map_rows = len(map)
    self.map_cols = len(map[0])
    self.world_rect = pygame.Rect(0, 0, TILE_SIZE*(self.map_cols+1), SCR_SIZE[1])
    self.bg_col = (0x69, 0x50, 0x36)
    self.lives = 4 # should be in player class but whatever
    self.big_font = pygame.font.Font(join('data', 'cour.ttf'), 72)
    self.font = pygame.font.Font(join('data', 'cour.ttf'), 30)

    self.load_grps()
    self.load_data()

  def load_grps(self):
    self.static_sprites = SPRITE_GRP()
    self.wall_sprites = SPRITE_GRP()
    self.player_sprites = SPRITE_GRP()
    self.block_sprites = SPRITE_GRP()

    self.all = self.block_sprites, self.player_sprites, self.wall_sprites,\
                self.static_sprites
    
  def load_data(self):
    # Static stuff first
    self.ceil = Ceil()
    self.ceil.player_lives = self.lives
    self.ground = Ground()
    self.static_sprites.add(self.ceil, self.ground)

    # Wall stuff
    self.wall = Wall()
    self.wall_sprites.add(self.wall)

    # Player stuff
    self.player = Player()
    self.player_sprites.add(self.player, self.player.bullet)
    self.player.add_collision_grps(*self.all)

    # Block stuff
    self.map_var = 1
    self.render_blocks(0, self.map_cols/4)

  def render_blocks(self, start, end):
    for y in xrange(self.map_rows):
      for x in xrange(start, end):
        xx, yy = TILE_SIZE * x, TILE_SIZE * y + CEIL_Y
        cell = map[y][x]
        pos = xx, yy
        if cell == '.': continue
        elif cell == '#':
          self.block_sprites.add(Block(pos=pos, unbreakable=1))
        elif cell == '0':
          self.block_sprites.add(Block(pos=pos, reflect=1))
        elif cell == '*':
          self.block_sprites.add(Block(pos=pos))
        elif cell == '^':
          self.block_sprites.add(Spike(pos=pos))
        elif cell == '@':
          r = Rock(pos=pos)
          r.player = self.player
          r.ground = self.ground
          self.block_sprites.add(r)


  def start(self):
    self.clock = pygame.time.Clock()
    self.keep_going = 1
    self.camera = Camera(screen, self.world_rect, self.player)
    self.blank_scr("OMFG A WALL\nOF LAVA!\nRUN AWAY!")

    while self.keep_going:
      self.clock.tick(FRAME_RATE)
      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.keep_going = 0
          """if event.key == K_z: # jump # handled in player class now
            if not self.player.states.jumping in self.player.state_lst and not self.player.states.falling in self.player.state_lst:
              self.player.state_lst.append(self.player.states.jumping)"""
          if event.key == K_x: # attack
            if not self.player.states.attacking in self.player.state_lst:
              self.player.state_lst.append(self.player.states.attacking)
              sounds['fire'].play()
          if event.key == K_f:
            print "FPS:", self.clock.get_fps()
          if event.key == K_p:
            self.blank_scr('PAUSED')

      self.screen.fill(self.bg_col, (0, CEIL_Y, SCR_SIZE[0], SCR_SIZE[1] - 2*CEIL_Y))
      self.camera.update()
      self.camera.update_grps(*self.all)
      self.check_some_collisions()
      self.camera.draw_grps(*self.all)
      if self.keep_going:
        pygame.display.flip()
    sounds['lava'].stop()

  def check_some_collisions(self):
    # like player with edges of world
    if self.player.rect.left < 0: self.player.rect.left = 0
    if self.player.rect.right > self.world_rect.right: self.player.rect.right = self.world_rect.right
    # and bullets against blocks
    for sprite in self.player_sprites.sprites():
      if 'Bullet' in str(sprite):
        for block in self.block_sprites.sprites():
          if abs(sprite.rect.centerx - block.rect.centerx) >= sprite.max_distance:
            continue
          if block.rect.collidepoint(sprite.rect.center):
            if 'Block' in str(block):
              if block.reflect: sprite.dir *= -1
              elif block.unbreakable: sprite.done = 1; break
              else: sprite.done = 1; self.block_sprites.remove(block); break
            else:
              sprite.done = 1; break
    # and if player is dead
    # and to revive the player if the death animation is done
    if self.player.dead:
      if self.player in self.player_sprites:
        self.lives -= 1
        self.ceil.player_lives = self.lives
        self.wall.old_speed = self.wall.speed
        self.wall.speed = 0
        self.death_animation()
      else:
        for ball in self.player_sprites.sprites():
          if ball.done and 'DeathBall' in str(ball):
            self.player_sprites.empty()
            self.player_sprites.add(self.player, self.player.bullet)
            self.player.dead = 0
            self.player.rect.top = CEIL_Y
            self.player.rect.left += TILE_SIZE/2
            self.wall.speed = self.wall.old_speed
            self.player.state_lst = [self.player.states.standing]
            if self.lives <= 0:
              self.blank_scr('GAME OVER')
            break
    # and to remove any blocks the wall hits (speeds up game over time!)
    for block in self.block_sprites.sprites():
      if block.rect.right - self.wall.rect.right < 0:
        self.block_sprites.remove(block)
    # and to render more blocks
    f = 1.0 * self.player.rect.right / self.world_rect.right
    if abs(f - 1./4) <= .1 and self.map_var == 1:
      self.map_var += 1
      self.kill_some_blocks()
      self.render_blocks(self.map_cols/4, 2*self.map_cols/4)
    elif abs(f - 2/4.) <= .1 and self.map_var == 2:
      self.map_var += 1
      self.kill_some_blocks()
      self.render_blocks(2*self.map_cols/4, 3*self.map_cols/4)
    elif abs(f - 3/4.) <= .1 and self.map_var == 3:
      self.map_var += 1
      self.kill_some_blocks()
      self.render_blocks(3*self.map_cols/4, 4*self.map_cols/4)
    # and to check victory
    if self.world_rect.right - self.player.rect.right < TILE_SIZE: # win!
      if self.lives == 4: txt = 'WOW!\nCongratumalations!\nYou beat it\nwith all lives!'
      elif self.lives == 3: txt = 'Congratumalations!\nYou only died\nonce!'
      elif self.lives == 2: txt = 'No shame in\nthis win!'
      elif self.lives == 1: txt = 'Phew...\nBarely won.'
      self.keep_going = 0
      self.blank_scr(txt)

  def kill_some_blocks(self):
      for block in self.block_sprites.sprites():
        if self.player.rect.right - block.rect.right > SCR_SIZE[0]/2 + TILE_SIZE: 
          self.block_sprites.remove(block)

  def death_animation(self):
    sounds['death'].play()
    self.player_sprites.remove(self.player)
    for i in xrange(8):
      ball = DeathBall(i)
      ball.rect.center = self.player.rect.center
      self.player_sprites.add(ball)

  def blank_scr(self, txt):
    sounds['lava'].stop()
    if txt == 'GAME OVER': self.keep_going = 0
    self.screen.fill((0,0,0))
    texts = txt.split('\n')
    lines = len(texts)
    for i in xrange(lines):
      draw_text(self.screen, texts[i], self.big_font, (SCR_SIZE[0]/2, 3*SCR_SIZE[1]/5 - 72*(lines - i)), (255,255,255), 1)
    draw_text(self.screen, 'Press any key to continue', self.font, (SCR_SIZE[0]/2, 4*SCR_SIZE[1]/5), (255,255,255), 1)
    while 1:
      self.clock.tick(10)
      for event in pygame.event.get():
        if event.type == QUIT:
          exit()
        if event.type == KEYDOWN:
          if self.keep_going: sounds['lava'].play(-1)
          return
      pygame.display.flip()

if __name__ == '__main__':

  #pygame.init()
  screen = pygame.display.set_mode(SCR_SIZE, (DOUBLEBUF|HWSURFACE) )
  pygame.display.set_caption('Flee the Lava of Doom! -- By Jach')
  pygame.mouse.set_visible(0)

  menu = Menu(screen)
  go = menu.display_menu()

  while go:
    game = Game(screen)
    game.start()
    go = menu.display_menu()

