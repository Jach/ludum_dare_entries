from globals import *

class Bat(pygame.sprite.Sprite):

  def __init__(self, start, map_sprites):
    pygame.sprite.Sprite.__init__(self)

    self.map_sprites = map_sprites

    self.image = pygame.image.load(join('data', 'bat.png')).convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.center = start

    self.speed = 10
    self.got_blood = pygame.mixer.Sound(join('data', 'got_blood.wav'))

    self.collectibles = 0

  def update(self):
    vector = CVector()

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
      vector -= self.speed*1j
    if keys[K_DOWN]:
      vector += self.speed*1j
    if keys[K_LEFT]:
      vector -= self.speed
    if keys[K_RIGHT]:
      vector += self.speed

    vector = CVector(self.speed * vector.normal()) # proper movement
    if tuple(vector) == (0,0):
      return

    # Check collisions with cave walls and stuff
    for v in [vector.vector.real+0j, vector.vector.imag*1j]:
      # need to run this once for dx and once for dy (thanks pymike!)
      self.rect.x += v.real
      self.rect.y += v.imag
      for sprite in self.map_sprites[self.world_frame]:
        if self.rect.colliderect(sprite.rect):
          if sprite.type == 'gate' and sprite.needed <= self.collectibles:
            continue
          if sprite.type == 'collectible':
            self.got_blood.play()
            raise Exception('itemgot', sprite)
          if v.real > 0: # hit left side of wall
            self.rect.right = sprite.rect.left
          if v.real < 0: # hit right side of wall
            self.rect.left = sprite.rect.right
          if v.imag > 0: # hit top side of wall
            self.rect.bottom = sprite.rect.top
            if sprite.type == 'stalagmite':
              raise Exception('killed')
          if v.imag < 0: # hit bottom side of wall
            self.rect.top = sprite.rect.bottom
            if sprite.type == 'stalactite':
              raise Exception('killed')
