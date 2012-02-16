from globals import *

imgs = {
    'cavewall': pygame.image.load(join('data', 'cavewall.png')).convert(),
    'stalactite': pygame.image.load(join('data', 'stalactite.png')).convert_alpha(),
    'stalagmite': pygame.image.load(join('data', 'stalagmite.png')).convert_alpha(),
    'gate': pygame.image.load(join('data', 'gate.png')).convert(),
    'collectible': pygame.image.load(join('data', 'collectible.png')).convert_alpha()
    }

class Block(pygame.sprite.Sprite):

  def __init__(self, pos, img=None, needed=0):
    pygame.sprite.Sprite.__init__(self)

    self.type = img
    self.image = imgs[img]
    self.rect = self.image.get_rect()
    self.rect = self.rect.move(pos)

    if self.type == 'collectible':
      self.image = pygame.image.load(join('data', 'collectible.png')).convert_alpha() # needs its own
      self.rect = self.rect.move(((TILE_SIZE - self.rect.width)/2, (TILE_SIZE - self.rect.height)/2))
    if self.type == 'gate':
      self.image = pygame.image.load(join('data', 'gate.png')).convert() # needs its own
      self.needed = needed
      draw_text(self.image, str(needed), pygame.font.Font(join('data','cour.ttf'),20), color=(255,0,0), pos=(18,15))
      

  def update(self):
    pass
