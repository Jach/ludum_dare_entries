from os.path import join
from random import randint as rand
import pygame
from pygame.locals import *
import menu, tank, cars, misc

pygame.init()
SIZE = (640, 480)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("The Hunt for Pepsi Blue")
pygame.mouse.set_visible(0)
FPS = 50

class Game(object):
  
  def __init__(self):
    self.load_crap()
    self.sounds('start')

    self.start_game()
  
  def load_crap(self):
    self.level = 1 # of 10
    self.map = pygame.image.load(join('data', 'map.png')).convert()
    self.mapfont = pygame.font.Font(join('data', 'cour.ttf'), 18)

    # Load music and other sounds
    self.music = {'music1' : pygame.mixer.Sound(join('data', 'music1.ogg')),
        'music2' : pygame.mixer.Sound(join('data', 'music2.ogg')),
        'music3' : pygame.mixer.Sound(join('data', 'music3.ogg')),
        'explosion' : pygame.mixer.Sound(join('data', 'shell.ogg')),
        'death' : pygame.mixer.Sound(join('data', 'death.ogg')),
        'cheer' : pygame.mixer.Sound(join('data', 'cheer.ogg')),
        'clap' : pygame.mixer.Sound(join('data', 'clap.ogg')),
        'excellent' : pygame.mixer.Sound(join('data', 'excellent.ogg'))
        }
    self.music['cheer'].set_volume(.2)
    self.music['clap'].set_volume(.8)

    self.clock = pygame.time.Clock()
    self.not_done = 1
    self.background = pygame.image.load(join('data', \
        'background.png')).convert()
    screen.blit(self.background, (0,0))
    pygame.display.update()

    # player related sprites (add Shell(s) later)
    self.player = tank.Tank()
    self.player_sprites = pygame.sprite.OrderedUpdates(self.player)

    # enemy related sprites. (none atm, types are car, bus, and van)
    self.enemy_sprites = pygame.sprite.OrderedUpdates()

    # misc sprites like Available Pepsi, People Remaining, cars parked, etc.
    self.pepsi_left = misc.Pepsi() # health, basically
    self.people_left = misc.People() # tells player how many more he must stop
    self.cars_parked = misc.Parked()
    # when a car gets through, Parked.cars gains a member that contains its
    # type and cell (1,2,3). Then it chooses which stall in that cell to
    # put it in.
    self.misc_sprites = pygame.sprite.OrderedUpdates(self.pepsi_left, \
        self.people_left, self.cars_parked)

    self.level_animation()

  def start_game(self):

    while self.not_done:
      self.clock.tick(FPS)

      self.events()
      self.updates()
      self.collisions()
      self.draw()

  def events(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.sounds('stop')
        self.not_done = 0
        pygame.event.post(pygame.event.Event(QUIT))
      elif event.type == KEYDOWN:
        if event.key == K_SPACE:
          if len(self.player_sprites.sprites()) < 6:
            # One sprite for player, 5 maximum shells...apparently
            shell = tank.Shell(self.player)
            self.player_sprites.add(shell)
        # Player class handles arrow keys for events by itself.
        if event.key == K_i:
          self.pepsi_left.life = 100
        if event.key == K_s:
          self.people_left.people = 0

  def updates(self):

    # Check if we need to move on to next level, or if we have a game ovah.
    if self.pepsi_left.life > 0 and self.people_left.people == 0 and not \
        self.enemy_sprites.sprites():
      self.load_level()

    if self.pepsi_left.life <= 0:
      self.game_over()

    self.player_sprites.update()
    self.enemy_sprites.update()
    self.misc_sprites.update()

  def collisions(self):
    "Collisions also handles adding/removing entities from the groups."

    # Check for any shells hitting enemies, or if they're at their dest.
    for shell in self.player_sprites.sprites():
      if 'Shell' in str(shell):
        if shell.at_dest:
          self.player_sprites.remove(shell)
        hit_cars = pygame.sprite.spritecollide(shell, self.enemy_sprites, 0)
        if hit_cars:
          self.player_sprites.remove(shell)
          for car in hit_cars:
            car.hit('shell')
            self.music['explosion'].play()

    # Check for any enemies hitting player.
    hit_cars = pygame.sprite.spritecollide(self.player, self.enemy_sprites, 0)
    if hit_cars:
      for car in hit_cars:
        car.hit('ram')
        self.pepsi_left.life -= 2 # 2 hp blow for ramming...
        # Move the car and player out of the way so no overlapping...
        # Does it by getting the vector between them and moving <s>each</s>one
        # in the opposite direction. Not great but it works.
        vec = [self.player.rect.centerx - car.rect.centerx, \
            self.player.rect.centery - car.rect.centery]
        #self.player.rect.centerx += vec[0]
        #self.player.rect.centery += vec[1]
        car.rect.centerx -= vec[0]/2
        car.rect.centery -= vec[1]/2

    # Check for enemies hitting enemies.
    hit_cars = pygame.sprite.groupcollide(self.enemy_sprites, \
        self.enemy_sprites, 0, 0)
    if hit_cars:
      for car in hit_cars: # iters keys
        if len(hit_cars[car]) > 1: # collision
          for the_car in hit_cars[car]: # move each one
            the_car.rect = the_car.rect.move(the_car.speed * rand(-1,1), \
                the_car.speed * rand(-1,1))


    # Remove enemies at their dest or if they're dead, add them to the stalls.
    for enemy in self.enemy_sprites.sprites():
      if enemy.at_dest:
        self.enemy_sprites.remove(enemy)
        self.cars_parked.set_filled(enemy.stall)
        if 'Car' in str(enemy):
          self.pepsi_left.life -= 5
        elif 'Van' in str(enemy):
          self.pepsi_left.life -= 10
        elif 'Bus' in str(enemy):
          self.pepsi_left.life -= 15
      elif enemy.health <= 0:
        self.enemy_sprites.remove(enemy)

    # Randomly add enemies!
    diff = self.level # difficulty
    factor = 200
    people = self.people_left.people
    if rand(1, 150) == 1 and people > 0: # was factor/diff
      # reg car
      car = cars.Car()
      self.enemy_sprites.add(car)
      people -= 1
      self.people_left.people -= 1
    if rand(1, 3*150) == 1 and people > 0 and self.level > 1:
      # van comes a third as often as car.
      van = cars.Van()
      self.enemy_sprites.add(van)
      people -= 1
      self.people_left.people -= 1
    if rand(1, 4*150) == 1 and people > 0 and self.level > 2:
      # bus comes a fourth as often as car.
      bus = cars.Bus()
      self.enemy_sprites.add(bus)
      people -= 1
      self.people_left.people -= 1

  def draw(self):
    
    self.player_sprites.clear(screen, self.background)
    self.enemy_sprites.clear(screen, self.background)
    self.misc_sprites.clear(screen, self.background)

    dirties = []
    dirties.append(self.player_sprites.draw(screen))
    dirties.append(self.enemy_sprites.draw(screen))
    dirties.append(self.misc_sprites.draw(screen))

    all_dirt = dirties[0] + dirties[1] + dirties[2]
    pygame.display.update(all_dirt)

  def load_level(self):
    # Basically just does the cheering if level is > 1 and draws stuff to
    # map, then waits around a bit.
    # Other stuff: resets player, resets life, changes people left.
    self.level += 1
    self.player_sprites.empty()
    self.player = tank.Tank()
    self.player_sprites.add(self.player)
    self.pepsi_left.life = 100
    self.people_left.people = self.level * 5
    self.cars_parked.reset()

    if self.level < 11:
      self.level_animation()
    else: # they won!
      self.winner()

  def level_animation(self):
    # Blits the map and lags, cheers, etc. What load_level should have done
    # but doesn't do.
    self.sounds('stop')
    # Add something to the map depending on the level.
    lev = self.level
    blk = (0,0,0)
    if lev == 1:
      txt = "Olympia, WA"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (80,40), 5)
      self.map.blit(txt, (86, 34) )
    elif lev == 2:
      txt = "Carson City, NV"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (150, 180), 5)
      pygame.draw.line(self.map, blk, (80,40), (150,180) )
      self.map.blit(txt, (156, 174) )
    elif lev == 3:
      txt = "Phoenix, AZ"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (190, 330), 5)
      pygame.draw.line(self.map, blk, (150, 180), (190, 330) )
      self.map.blit(txt, (196, 324) )
    elif lev == 4:
      txt = "Houston, TX"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (280, 430), 5)
      pygame.draw.line(self.map, blk, (190, 330), (280, 430) )
      self.map.blit(txt, (286, 424) )
    elif lev == 5:
      txt = "Dallas, TX"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (330, 380), 5)
      pygame.draw.line(self.map, blk, (280, 430), (330, 380) )
      self.map.blit(txt, (336, 374) )
    elif lev == 6:
      txt = "Omaha, NE"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (360, 190), 5)
      pygame.draw.line(self.map, blk, (330, 380), (360, 190) )
      self.map.blit(txt, (366, 184) )
    elif lev == 7:
      txt = "Louisville, KY"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (480, 260), 5)
      pygame.draw.line(self.map, blk, (360, 190), (480, 260) )
      self.map.blit(txt, (486, 254) )
    elif lev == 8:
      txt = "Tampa, FL"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (530, 430), 5)
      pygame.draw.line(self.map, blk, (480, 260), (530, 430) )
      self.map.blit(txt, (536, 424) )
    elif lev == 9:
      txt = "Albany, NY"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (520, 100), 5)
      pygame.draw.line(self.map, blk, (530, 430), (520, 100) )
      self.map.blit(txt, (526, 94) )
    elif lev == 10:
      txt = "Orem, UT"
      txt = self.mapfont.render(txt, 1, blk)
      pygame.draw.circle(self.map, blk, (230, 230), 5)
      pygame.draw.line(self.map, blk, (520, 100), (230, 230) )
      self.map.blit(txt, (236, 224) )

    if lev > 1:
      self.music['cheer'].play()
      self.music['clap'].play()
      self.music['excellent'].play()

    m = lev % 3
    if m == 1:
      music = 'music1'
    elif m == 0:
      music = 'music2'
    elif m == 2:
      music = 'music3'

    screen.blit(self.map, (0,0) )
    pygame.display.update()
    for i in xrange(50): # 50 frames at 10 fps = 5 secs
      self.clock.tick(10)
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.event.post(pygame.event.Event(QUIT))
          return

    screen.blit(self.background, (0,0) )
    pygame.display.update()
    self.sounds('start', music)

  def game_over(self):
    self.sounds('stop')
    self.music['death'].play()
    print 'you lose!'
    self.not_done = 0

  def winner(self):
    print 'you win!'
    self.not_done = 0

  def sounds(self, action, music='music1'):
    if action == 'stop':
      for sound in self.music:
        self.music[sound].stop()
    elif action == 'start':
      # Play music. Defaults to default game music.
      self.music[music].play(-1)

def main():
  intro = menu.Menu()
  cont = intro.start() # returns 1 if they select play, 0 if quit
  while cont:
    game = Game()
    cont = intro.start()

if __name__ == '__main__':
  main()
