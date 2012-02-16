from globals import *

class Player(BaseSprite):

  def __init__(self):
    BaseSprite.__init__(self)

    # States
    self.states = Struct(standing=0, moving=1, jumping=2, falling=3, attacking=4)
    self.state_lst = [self.states.standing]
    self.dead = 0

    # Movement
    self.speed = 10
    self.dir = 0
    self.facing = 1 # right

    # Gravity vars
    self.init_fall_speed = .3
    self.fall_speed = self.init_fall_speed
    self.g = .4
    self.max_fall_speed = 15

    self.init_jump_speed = -7
    self.jump_speed = self.init_jump_speed

    # Animation stuff
    self.frame = 0
    self.delay = 10
    self.pause = 0

    # Sprites

    self.frames = 3 # no of sprites
    self.load_sprites()
    self.image = self.sprites[self.frame]
    self.rect = self.image.get_rect()
    self.rect.bottomleft = 200, GROUND_Y

    self.bullet = Bullet()

  def load_sprites(self):
    self.sprites = []
    for i in xrange(1, self.frames+1):
      img = pygame.image.load(join('data', 'player%.2d.png' % i)).convert_alpha()
      self.sprites.append(img)
    # jumping sprites?

  def reload_player(self, img=None):
    if img:
      self.image = img
    else:
      self.image = self.sprites[self.frame]
    if self.facing == -1:
      self.image = pygame.transform.flip(self.image, 1, 0)
    center = self.rect.center
    self.rect = self.image.get_rect()
    self.rect.center = center

  def update(self):
    # Gravity!
    vector = CVector()
    self.fall_speed = self.max_fall_speed if self.fall_speed >= self.max_fall_speed else self.fall_speed + self.g
    vector += self.fall_speed*1j

    # Jumping
    if self.states.jumping in self.state_lst:
      vector -= self.fall_speed*1j # undo gravity
      vector += self.jump_speed*1j
      self.jump_speed += self.g # apply gravity
      if self.jump_speed >= 0:
        self.jump_speed = 0
        self.state_lst.append(self.states.falling)
        self.state_lst.remove(self.states.jumping)

    # Attacking
    if self.states.attacking in self.state_lst:
      pos = self.rect.centerx, self.rect.centery
      self.bullet.rect.topleft = pos
      self.bullet.dir = self.facing
      self.bullet.speed = self.bullet.init_speed
      self.bullet.distance = 0
      self.bullet.done = 0

      self.state_lst.remove(self.states.attacking)

    # Horizontal movement etc
    keys = pygame.key.get_pressed()
    move = 0
    if keys[K_LEFT]:
      move = 1
      self.dir = -1
      if self.facing == 1:
        self.facing = -1
        self.reload_player()
    elif keys[K_RIGHT]:
      move = 1
      self.dir = 1
      if self.facing == -1:
        self.facing = 1
        self.reload_player()
    if keys[K_z]:
      if not self.states.jumping in self.state_lst and not self.states.falling in self.state_lst:
        self.state_lst.append(self.states.jumping)
        sounds['jump'].play()
    else:
      if self.states.jumping in self.state_lst:
        self.jump_speed = 0
    if not keys[K_LEFT] and not keys[K_RIGHT] and self.states.moving in self.state_lst:
      move = 0
      self.dir = 0
      self.state_lst.append(self.states.standing)
      self.state_lst.remove(self.states.moving)

    if move:
      vector += self.speed * self.dir
      if self.states.moving not in self.state_lst:
        self.state_lst.append(self.states.moving)
        self.state_lst.remove(self.states.standing)

    if self.states.standing in self.state_lst \
        and self.states.moving not in self.state_lst:
      self.pause = 0
      self.frame = 0
      self.reload_player()

    # Animation
    if self.states.moving in self.state_lst and self.states.jumping not in self.state_lst \
        and self.states.falling not in self.state_lst:
      self.pause +=1
      if self.pause % (self.delay / self.frames) == 0:
        self.frame +=1
        if self.frame == self.frames:
          self.frame = 0
        if self.pause >= self.delay:
          self.pause = 0
        self.reload_player()

    if self.states.jumping in self.state_lst or self.states.falling in self.state_lst:
      self.reload_player(self.sprites[0]) # first image is jumping one

    self.rect = self.rect.move(tuple(vector))
    self.check_collisions(vector)

  def check_collisions(self, vector):
    has_collided = 0
    for grp in self.collision_grps:
      for sprite in grp.sprites():
        if 'Bullet' in str(sprite):
          if sprite.done:
            sprite.rect.topleft = (-200, -200)
            sprite.speed = 0
        elif 'Ground' in str(sprite) or 'Ceil' in str(sprite):
          if self.rect.bottom >= GROUND_Y:
            has_collided = 1
            self.rect.bottom = GROUND_Y
            self.fall_speed = self.init_fall_speed
            if self.states.falling in self.state_lst:
              self.state_lst.remove(self.states.falling)
              self.jump_speed = self.init_jump_speed
              self.frame = 0
              self.pause = 0
              self.reload_player()
          if self.rect.top <= CEIL_Y:
            has_collided = 1
            self.rect.top = CEIL_Y
            if self.states.jumping in self.state_lst:
              self.state_lst.remove(self.states.jumping)
              self.state_lst.append(self.states.falling)
        elif 'Wall' in str(sprite) or 'LavaTile' in str(sprite):
          if self.rect.colliderect(sprite.rect):
            self.dead = 1
            has_collided = 1
        elif abs(self.rect.centerx - sprite.rect.centerx) >= self.bullet.max_distance:
          continue
        elif 'Block' in str(sprite):
          if self.rect.colliderect(sprite.rect):
            has_collided = 1
            if TILE_SIZE/2 > self.rect.bottom - sprite.rect.top > 0:
              if self.states.falling in self.state_lst:
                self.state_lst.remove(self.states.falling)
                self.jump_speed = self.init_jump_speed
                self.frame = 0
                self.pause = 0
                self.reload_player()
              self.rect.bottom = sprite.rect.top
            elif TILE_SIZE/2 > sprite.rect.bottom - self.rect.top > 0:
              if not self.states.falling in self.state_lst:
                self.state_lst.append(self.states.falling)
              self.rect.top = sprite.rect.bottom
            elif TILE_SIZE/2 > self.rect.right - sprite.rect.left > 0:
              self.rect.right = sprite.rect.left
            elif TILE_SIZE/2 > sprite.rect.right - self.rect.left > 0:
              self.rect.left = sprite.rect.right

        elif 'Spike' in str(sprite) or 'Rock' in str(sprite):
          if self.rect.colliderect(sprite.rect.inflate(-10, -10)):
            has_collided = 1
            self.dead = 1
    if not has_collided and not self.states.falling in self.state_lst: # Must be falling.
      self.state_lst.append(self.states.falling)


class Bullet(BaseSprite):

  def __init__(self):
    BaseSprite.__init__(self)

    self.image = pygame.image.load(join('data', 'bullet.png')).convert_alpha()
    self.rect = self.image.get_rect()

    self.dir = 1
    self.init_speed = 20
    self.speed = self.init_speed
    self.distance = 0
    self.max_distance = 600

    self.done = 0

  def update(self):
    self.rect = self.rect.move(self.speed * self.dir, 0)
    self.distance += self.speed
    if self.distance >= self.max_distance: self.done = 1

class DeathBall(BaseSprite):

  def __init__(self, dir):
    BaseSprite.__init__(self)

    self.image = pygame.image.load(join('data', 'deathball.png')).convert_alpha()
    self.rect = self.image.get_rect()

    self.speed = 10
    self.dir = dir * 2*PI / 8
    self.done = 0
    self.distance = 0
    self.max_distance = 200

  def update(self):
    x = self.speed * cos(self.dir)
    y = -self.speed * sin(self.dir)
    self.rect = self.rect.move(x, y)

    self.distance += sqrt(x**2 + y**2)
    if self.distance >= self.max_distance:
      self.done = 1
