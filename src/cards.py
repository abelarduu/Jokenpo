import pygame
from pygame.math import Vector2
from src.assets import get_image

class Card():
    def __init__(self, x:int, y:int , img_coordinates:tuple, scale: int):
        self.pos= Vector2(x,y)
        self.img_coordinates= img_coordinates
        self.img= get_image(img_coordinates, scale)
        self.img_rect= self.img.get_rect(center=(self.pos.x + self.img.get_width()/2, self.pos.y + self.img.get_height()/2))
        self.w= self.img.get_width()
        self.h= self.img.get_height()
        self.mouse_up= False
        self.mouse_pressed= False

        if self.img_coordinates == (172,0,40,68): self.type="rock"
        elif self.img_coordinates == (214,0,40,68): self.type="paper"
        elif self.img_coordinates == (257,0,40,68): self.type="scissors"
        else: self.type= "deck"

    def update(self):
        self.img_rect= self.img.get_rect(center= (self.pos.x + self.img.get_width()/2, self.pos.y + self.img.get_height()/2))
        #Mouse Up
        if self.img_rect.collidepoint(pygame.mouse.get_pos()):
            self.pos.y = (self.pos.y-10)
            self.mouse_up= True
            
            #Mouse Pressed
            if pygame.mouse.get_pressed()[0]:self.mouse_pressed= True
            else: self.mouse_pressed= False
        else: self.mouse_up= False