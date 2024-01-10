import pygame
from pygame.locals import *
from random import randint

class Card:
    def __init__(self, x:int, y:int , img:str, scale: int):
        self.x= x
        self.y= y
        self.scale= scale
        self.pre_img= pygame.image.load(img)
        self.img= pygame.transform.scale(self.pre_img, (self.pre_img.get_width()*self.scale, self.pre_img.get_height()*self.scale))
        self.img_rect= self.img.get_rect(center=(self.x + self.img.get_width()/2, self.y + self.img.get_height()/2))
        self.w= self.img.get_width()
        self.h= self.img.get_height()

        self.mouse_up= False
        self.mouse_pressed= False

    def update(self):

        self.img_rect= self.img.get_rect(center=(self.x + self.img.get_width()/2, self.y + self.img.get_height()/2))
        #Mouse Up
        if self.img_rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_up= True

            #Mouse Pressed
            if pygame.mouse.get_pressed()[0]:self.mouse_pressed= True
            else: self.mouse_pressed= False
        else: self.mouse_up= False


class Player:
    def __init__(self,  cards: list):
        self.scores= 0
        self.cards= cards
        self.select_card=False

    def draw_cards(self, screen, padx, pady):
        x=int((screen.get_size()[0]/2-padx) -(padx/2))
        for card in self.cards:
            card.x= x
            card.y= pady
            x+=padx

class Game:
    def __init__(self):
        pygame.init()

        self.screen= pygame.display.set_mode((600,600), RESIZABLE)
        pygame.display.set_caption("Jokenpô")
        self.play = True

        self.stone_card= Card(0,0, "assets/carta_pedra.png",3)
        self.paper_card= Card(0,0, "assets/carta_papel.png",3)
        self.scissors_card= Card(0,0, "assets/carta_tesoura.png",3)

        self.stone_card2= Card(0,0, "assets/carta_pedra.png",3)
        self.paper_card2= Card(0,0, "assets/carta_papel.png",3)
        self.scissors_card2= Card(0,0, "assets/carta_tesoura.png",3)


        self.back_card= Card(0,0, "assets/carta_verso.png",3)
        self.back_card_bot= Card(0,0, "assets/carta_verso.png",2)

        self.player= Player([self.stone_card, self.paper_card, self.scissors_card])
        self.bot= Player([self.stone_card2, self.paper_card2, self.scissors_card2])
        self.cards_on_the_table= [self.stone_card, self.stone_card]

    def draw_interface(self):
        if self.play:
            self.player.draw_cards(self.screen, 125, self.screen.get_size()[1] - self.player.cards[0].h -10)
            self.bot.draw_cards(self.screen, 82, 10)
       
            for card in self.player.cards:
                self.screen.blit(card.img, (card.x, card.y))
                card.update()
                
                if not self.player.select_card:
                    #MOUSE_UP
                    if card.mouse_up: 
                        card.y = self.screen.get_size()[1] - card.h -20
                        #MOUSE_PRESSED
                        if card.mouse_pressed:
                            if not self.player.select_card:
                                self.cards_on_the_table[0]= card
                                self.player.cards.remove(self.cards_on_the_table[0])
                                self.player.select_card= True
                    else: card.y=400

            for card in self.bot.cards:
                self.screen.blit(self.back_card_bot.img, (card.x, card.y))
                card.update()

                if self.player.select_card and not self.bot.select_card:
                    try: self.cards_on_the_table[1]= self.bot.cards[(randint(0, len(self.bot.cards)))]
                    except: self.cards_on_the_table[1]= self.bot.cards[(randint(0, len(self.bot.cards)))]
                    self.bot.cards.remove(self.cards_on_the_table[1])
                    self.bot.select_card=True   

            for card in self.cards_on_the_table:
                if self.player.select_card and self.bot.select_card:
                    self.cards_on_the_table[0].x=self.screen.get_size()[0]/2 - self.screen.get_size()[0]/5 -card.w/2
                    self.cards_on_the_table[0].y=self.screen.get_size()[1]/2 - card.h/2-30
                    
                    self.cards_on_the_table[1].x=self.screen.get_size()[0]/2 + self.screen.get_size()[0]/5 - card.w/2
                    self.cards_on_the_table[1].y=self.screen.get_size()[1]/2 - card.h/2-30
                    self.screen.blit(card.img, (card.x, card.y))
                    card.update()
                

    def main(self):
        while True:
            self.screen.fill((0,0,0))
            self.draw_interface()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type== QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    game=Game()
    game.main()