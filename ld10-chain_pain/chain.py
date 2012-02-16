# Chains
import pygame
from os import path

class Chain:

  def __init__(self, pos, screen):

    self.state = 0 # Initial state 

    self.screen = screen
    self.chain_link = pygame.image.load(\
        path.join('data','chainlink.png')).convert_alpha()
#<rect(94, 436, 64, 64)> master1 rect
#<rect(706, 436, 64, 64)> master2 rect
#<rect(642, 436, 64, 64)> new better master2 rect

    st_y = 436+32
    suby = -10
    if pos == 'left':
      st_x = 94+60 #start x
      subx = -10 # "subtractor", to offset chains in x
    else:
      st_x = 642-5
      subx = 10
    
    pt_list1 = [ (st_x,st_y), (st_x-subx,st_y), \
        (st_x-subx*2,st_y-suby), (st_x-subx*2,st_y-suby*2) ]
    pt_list2 = [ (st_x,st_y), (st_x,st_y+suby), (st_x,st_y+suby*2), \
        (st_x+subx,st_y+suby*3), (st_x+subx*2,st_y+suby*4), \
        (st_x+subx*3,st_y+suby*5), (st_x+subx*4,st_y+suby*6), \
        (st_x+subx*5,st_y+suby*7), (st_x+subx*6,st_y+suby*7), \
        (st_x+subx*7,st_y+suby*8), (st_x+subx*8,st_y+suby*8), \
        (st_x+subx*9,st_y+suby*7), (st_x+subx*10,st_y+suby*6), \
        (st_x+subx*11,st_y+suby*5), (st_x+subx*12,st_y+suby*4), \
        (st_x+subx*12,st_y+suby*3), (st_x+subx*12,st_y+suby*2), \
        (st_x+subx*13,st_y+suby) ]
    pt_list3 = [ (st_x,st_y), (st_x,st_y+suby), (st_x,st_y+suby*2), \
        (st_x-subx,st_y+suby*3), (st_x-subx*2,st_y+suby*4), \
        (st_x-subx*3,st_y+suby*4), (st_x-subx*4,st_y+suby*5), \
        (st_x-subx*5,st_y+suby*5), (st_x-subx*6,st_y+suby*6), \
        (st_x-subx*7,st_y+suby*6), (st_x-subx*8,st_y+suby*7), \
        (st_x-subx*9,st_y+suby*7) ]
    pt_list4 = [ (st_x,st_y), (st_x-subx,st_y+suby), (st_x-subx*2,st_y+suby),\
        (st_x-subx*3,st_y+suby*2), (st_x-subx*4,st_y+suby*2), \
        (st_x-subx*5,st_y+suby*3), (st_x-subx*6,st_y+suby*3), \
        (st_x-subx*7,st_y+suby*4), (st_x-subx*8,st_y+suby*4), \
        (st_x-subx*9,st_y+suby*4), (st_x-subx*10,st_y+suby*5), \
        (st_x-subx*11,st_y+suby*5), (st_x-subx*12,st_y+suby*5), \
        (st_x-subx*13,st_y+suby*6), (st_x-subx*14,st_y+suby*6), \
        (st_x-subx*15,st_y+suby*6), (st_x-subx*16,st_y+suby*6), \
        (st_x-subx*17,st_y+suby*7), (st_x-subx*18,st_y+suby*7), \
        (st_x-subx*19,st_y+suby*7), (st_x-subx*20,st_y+suby*7), \
        (st_x-subx*21,st_y+suby*7), (st_x-subx*22,st_y+suby*8) ]

    self.points = [pt_list1, pt_list2, pt_list3, pt_list4]

  def change(self):
    self.state += 1
    if self.state == 4:
      self.state = 0
    #self.redraw_chain()

  def redraw_chain(self):
    pt_list = self.points[self.state]
    for pt in pt_list:
      self.screen.blit(self.chain_link, pt)
    #pygame.display.update()
