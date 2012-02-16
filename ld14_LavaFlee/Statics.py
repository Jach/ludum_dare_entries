from globals import *

class Ceil(BaseSprite):
  
  def __init__(self):
    BaseSprite.__init__(self)

    self.tile = pygame.image.load(join('data', 'ceil_floor_tile.png')).convert()
    self.image = pygame.Surface((800, 100))
    for i in xrange(16):
      self.image.blit(self.tile, (i*TILE_SIZE, 0))
      self.image.blit(self.tile, (i*TILE_SIZE, TILE_SIZE))

    self.rect = self.image.get_rect()

    self.is_static = 1

    self.player_lives = 0
    self.old_lives = 0
    self.font = pygame.font.Font(join('data', 'cour.ttf'), 30)

  def update(self):
    if self.old_lives != self.player_lives:
      # erase area
      for i in xrange(3, 5):
        self.image.blit(self.tile, (i*TILE_SIZE, 0))
      # redraw lives
      draw_text(self.image, "Lives: %d" % self.player_lives, self.font, (3.5*TILE_SIZE, 25), (255,255,255), 1)
      self.old_lives = self.player_lives

class Ground(Ceil):

  def __init__(self):
    Ceil.__init__(self)
    self.rect = self.rect.move(0, GROUND_Y)
