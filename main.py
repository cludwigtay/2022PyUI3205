from networktables import NetworkTables
import pygame
import numpy as np
from pygame.locals import *
import sys
import random
import math

class main:
    def __init__(self):
        pygame.init()
        self.SCRN_DIMS = (927, 458)
        self.FIELD_DIMS = (16.46, 8.23)
        self.ROBOT_DIMS = (32 * 2.54 / 100, 38 * 2.54 / 100)
        self.RAD = 0.12
        
        self.table = NetworkTables.getTable('balls')
        self.state_table = NetworkTables.getTable('State')
        
        
    def update(self):
        heading = self.state_table.getNumber("heading", 0)
        x = self.state_table.getNumber("x_pos", 0)
        y = self.state_table.getNumber("y_pos", 0)
        
        
        self.DISPLAY = pygame.display.set_mode(self.SCRN_DIMS)
        self.background()
        #self.draw_ball( pos = (random.random() * 4, random.random() * 4))
        self.draw_all_balls()
        
        self.draw_self_robot( pos = (x, y), heading = heading)
        pygame.display.update()
        self.exit()
        
    def background(self):
        image = pygame.image.load("images/background2.jpg")
        image = pygame.transform.scale(image, self.SCRN_DIMS)
        rect = image.get_rect()
        self.DISPLAY.blit(image, rect)
        
    def draw_all_balls(self):
        
        for c in range(40):
            pos_str = "pos_" + str(c)
            vel_str = "vel_" + str(c)
            g_str = "gstate_" + str(c)
            pos = self.state_table.getNumberArray(pos_str, [0, 0, 0])
            vel = self.state_table.getNumberArray(vel_str, [0, 0, 0])
            g_state = self.state_table.getNumberArray(g_str, [0, 0, 0, 0])
            if (round(g_state[0]) != 0):
                if (round(g_state[2]) == 0):
                    col = "r"
                else:
                    col = "b"
                self.draw_ball((pos[0], pos[1]), col = col)
                
            
        
    def draw_ball(self, pos = (1,1),col = "r"):
        #Translate dist to screen pos
        m2p_dist = self.SCRN_DIMS[0]/self.FIELD_DIMS[0]
        x = round(pos[0] * m2p_dist + (self.SCRN_DIMS[0]/2))
        y = round((self.SCRN_DIMS[1]/2) - pos[1] * m2p_dist)
        rad = round(self.RAD * m2p_dist)
        
        if col == "r":
            pygame.draw.circle(self.DISPLAY, (255,0,0), (x, y), rad)
        else:
            pygame.draw.circle(self.DISPLAY, (0,0,255), (x, y), rad)
    
    def draw_self_robot(self, pos = (1,1), heading = (3.14 / 4)):
        m2p = self.SCRN_DIMS[0]/self.FIELD_DIMS[0]
        image = pygame.image.load("images/robot.png")        
        p_size = (round(m2p * self.ROBOT_DIMS[0]), round(m2p * self.ROBOT_DIMS[1]))
        image = pygame.transform.scale(image, p_size)
        image = pygame.transform.rotate(image, heading * 180 / np.pi)
        rect = image.get_rect()
        
        
        x = round(pos[0] * m2p + (self.SCRN_DIMS[0]/2))
        y = round((self.SCRN_DIMS[1]/2) - pos[1] * m2p)
        rect.center=(x, y)
        self.DISPLAY.blit(image, rect)
        
        
    def exit(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
if __name__ == "__main__":
    m = main()
    while True:
        m.update()