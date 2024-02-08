import pygame
from src.assets import get_image

class Card():
    def __init__(self, x:int, y:int , img:str, scale: int):
        self.x= x
        self.y= y
        self.img= get_image(img, scale)
        self.img_rect= self.img.get_rect(center=(self.x + self.img.get_width()/2, self.y + self.img.get_height()/2))
        self.w= self.img.get_width()
        self.h= self.img.get_height()
        self.mouse_up= False
        self.mouse_pressed= False

        if "rock" in img:self.type="rock"
        elif "paper" in img:self.type="paper"
        elif "scissors" in img:self.type="scissors"
        else: self.type= "deck"

    def update(self):
        self.img_rect= self.img.get_rect(center= (self.x + self.img.get_width()/2, self.y + self.img.get_height()/2))
        #Mouse Up
        if self.img_rect.collidepoint(pygame.mouse.get_pos()):
            self.y = (self.y-10)
            self.mouse_up= True
            
            #Mouse Pressed
            if pygame.mouse.get_pressed()[0]:self.mouse_pressed= True
            else: self.mouse_pressed= False
        else: self.mouse_up= False

