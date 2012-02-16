from globals import *

class Camera:
  # Thanks to Pixelman3 (I think) for a lurvly Camera class base from which I've based further
  # ones.

  def __init__(self, screen, world_rect, sprite_to_center_on):
    self.screen = screen
    self.rect = screen.get_rect()
    self.world_rect = world_rect
    self.sprite = sprite_to_center_on
    
    self.scroll_speed = 5

  def update(self):
    if self.sprite.rect.centerx > self.rect.centerx + self.scroll_speed:
      self.rect.centerx = self.sprite.rect.centerx - self.scroll_speed
    if self.sprite.rect.centerx < self.rect.centerx - self.scroll_speed:
      self.rect.centerx = self.sprite.rect.centerx + self.scroll_speed
    if self.sprite.rect.centery > self.rect.centery + self.scroll_speed:
      self.rect.centery = self.sprite.rect.centery - self.scroll_speed
    if self.sprite.rect.centery < self.rect.centery - self.scroll_speed:
      self.rect.centery = self.sprite.rect.centery + self.scroll_speed
    self.rect.clamp_ip(self.world_rect)
        
  def update_grps(self, *grps):
    for grp in grps:
      for sprite in grp.sprites():
        if sprite.is_static:
          grp.update()
          break
        elif sprite.rect.left <= self.rect.right and sprite.rect.right >= self.rect.left and \
                sprite.rect.top <= self.rect.bottom and sprite.rect.bottom >= self.rect.top or \
                'Wall' in str(sprite) or 'LavaTile' in str(sprite):
          sprite.update()

  def draw_grps(self, *grps):
    for grp in grps:
      for sprite in grp.sprites():
        if sprite.is_static:
          grp.draw(self.screen)
          break
        elif sprite.rect.left <= self.rect.right and sprite.rect.right >= self.rect.left and \
                sprite.rect.top <= self.rect.bottom and sprite.rect.bottom >= self.rect.top:
          self.screen.blit(sprite.image, self.sprite_rect(sprite))
            
  def sprite_rect(self, sprite):
    return pygame.Rect(sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y, sprite.rect.w, sprite.rect.h)
