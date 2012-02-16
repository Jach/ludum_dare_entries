from globals import *

block_imgs = {}

class Block(BaseSprite):
  def __init__(self, **args):
    BaseSprite.__init__(self)
    global block_imgs
    if len(block_imgs) == 0:
      block_imgs = {
          'unbreakable_block.png': pygame.image.load(join('data', 'unbreakable_block.png')).convert(),
          'mirror_block.png': pygame.image.load(join('data', 'mirror_block.png')).convert(),
          'breakable_block.png': pygame.image.load(join('data', 'breakable_block.png')).convert(),
          'spikes.png': pygame.image.load(join('data', 'spikes.png')).convert_alpha(),
          'rock.png': pygame.image.load(join('data', 'rock.png')).convert_alpha()
        }

    if 'unbreakable' in args: img = 'unbreakable_block.png'; self.unbreakable = 1; self.reflect = 0
    elif 'reflect' in args: img = 'mirror_block.png'; self.unbreakable = 0; self.reflect = 1
    else: img = 'breakable_block.png'; self.unbreakable = 0; self.reflect = 0

    if 'pos' in args: pos = args['pos']
    else: pos = (-100, -100)

    self.image = block_imgs[img]
    self.rect = self.image.get_rect()
    self.rect = self.rect.move(pos)
  
  def update(self):
    pass

class Spike(BaseSprite):
  def __init__(self, **args):
    BaseSprite.__init__(self)

    if 'pos' in args: pos = args['pos']
    else: pos = (-100, -100)

    self.image = block_imgs['spikes.png']
    self.rect = self.image.get_rect()
    self.rect = self.rect.move(pos)

  def update(self):
    pass

class Rock(BaseSprite):
  def __init__(self, **args):
    BaseSprite.__init__(self)

    if 'pos' in args: pos = args['pos']
    else: pos = (-100, -100)

    self.image = block_imgs['rock.png']
    self.rect = self.image.get_rect()
    self.rect = self.rect.move(pos)

    self.start_falling = 0
    self.speed = 20
    self.done = 0

  def update(self):
    if not self.start_falling:
      if self.rect.centerx - self.player.rect.centerx < 100:
        self.start_falling = 1
    else:
      self.rect = self.rect.move(0, self.speed)
      if self.rect.top > self.ground.rect.top:
        self.speed = 0
        self.done = 1
