from globals import *

class Wall(BaseSprite):

  def __init__(self):
    BaseSprite.__init__(self)

    self.image = pygame.image.load(join('data', 'lavawall.png')).convert()
    self.rect = self.image.get_rect()
    self.rect.topright = 1, CEIL_Y

    self.lava_tile = pygame.image.load(join('data', 'lavatile.png')).convert()

    self.old_speed = 0
    self.speed = 1
    self.acc = .007 # The name's Bond. James Bond.
    self.max_speed = 10

  def update(self):
    self.rect = self.rect.move(self.speed, 0)

    self.speed += self.acc
    if self.speed > self.max_speed: self.speed = self.max_speed

    if rand(0, 10*int(self.max_speed-self.speed)) and 1==2:
      self.groups()[0].add(LavaTile(self.lava_tile, self.rect))

class LavaTile(BaseSprite):
  # Decided not to do these.

  def __init__(self, img, lava_rect):
    BaseSprite.__init__(self)

    self.image = img
    self.rect = self.image.get_rect()
    self.rect.x = lava_rect.x
    self.rect.y = rand(lava_rect.top, 3*lava_rect.bottom/4)

  def update(self):
    pass # should travel in a parabola then hit ground/player
