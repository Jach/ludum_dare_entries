from globals import *

class Menu:

  def __init__(self, screen):
    self.screen = screen

    self.play_btn = pygame.Surface((400, 50))
    self.quit_btn = pygame.Surface((400, 50))

    self.selected_bg_col = (0xab, 0xcd, 0xef)
    self.selected_font_col = (180, 20, 75)
    self.deselected_bg_col = self.selected_font_col
    self.deselected_font_col = self.selected_bg_col

    self.font = pygame.font.Font(join('data', 'cour.ttf'), 30)

    self.selected = 'play'

  def display_menu(self):
    self.screen.fill((35, 35, 35))
    clock = pygame.time.Clock()
    self.need_update = 1

    self.draw_title_and_instructions()
    while 1:
      clock.tick(10)

      for event in pygame.event.get():
        if event.type == QUIT:
          return 0
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            return 0
          if event.key == K_UP or event.key == K_DOWN:
            self.selected = 'quit' if self.selected == 'play' else 'play'
            self.need_update = 1
            sounds['menu_select'].play()
          if event.key == K_RETURN:
            return 1 if self.selected == 'play' else 0

      self.draw_items()
      pygame.display.flip()

  def draw_items(self):
    if self.need_update:
      if self.selected == 'play':
        border_btn = self.play_btn
        play_bg_col = self.selected_bg_col
        play_font_col = self.selected_font_col
        quit_bg_col = self.deselected_bg_col
        quit_font_col = self.deselected_font_col
      elif self.selected == 'quit':
        border_btn = self.quit_btn
        play_bg_col = self.deselected_bg_col
        play_font_col = self.deselected_font_col
        quit_bg_col = self.selected_bg_col
        quit_font_col = self.selected_font_col

      self.play_btn.fill(play_bg_col)
      self.quit_btn.fill(play_font_col)

      pygame.draw.rect(border_btn, (0, 255, 255), border_btn.get_rect(), 5)
      draw_text(self.play_btn, 'Play', self.font, (170, 6), play_font_col)
      draw_text(self.quit_btn, 'Quit', self.font, (170, 6), quit_font_col)

      self.screen.fill((35, 35, 35), (0, 440, 800, 160))
      self.screen.blit(self.play_btn, (200, 450))
      self.screen.blit(self.quit_btn, (200, 525))

      self.need_update = 0

  def draw_title_and_instructions(self):
    small_font = pygame.font.Font(join('data', 'cour.ttf'), 24)
    big_font = pygame.font.Font(join('data', 'cour.ttf'), 72)

    draw_text(self.screen, 'LAVA FLEE', big_font, (SCR_SIZE[0]/2, 50), (255, 0, 0), 1)
    import Blocks as bl
    b1 = bl.Block(pos=(10, 100))
    b2 = bl.Block(reflect=1, pos=(10, 160))
    b3 = bl.Block(unbreakable=1, pos=(10, 220))
    b4 = bl.Spike(pos=(10, 280))
    b5 = bl.Rock(pos=(10, 340))
    blocks = b1, b2, b3, b4, b5
    for b in blocks: self.screen.blit(b.image, b.rect)
    w = (255,255,255)
    draw_text(self.screen, '- Shoot these with x.', small_font, (70, 100), w)
    draw_text(self.screen, '- These reflect your shots.', small_font, (70, 160), w)
    draw_text(self.screen, '- Jump around these with z.', small_font, (70, 220), w)
    draw_text(self.screen, '- Avoid touching these.', small_font, (70, 280), w)
    draw_text(self.screen, '- Don\'t let one of these fall on you.', small_font, (70, 340), w)
    draw_text(self.screen, 'Move with arrows, press p to pause.', small_font, (50, 400), w)
