import pygame
from pygame.locals import *
from random import randint

class Card:
    '''def __new__(cls, *args):
        new_card= object.__new__(cls, args)
        return new_card'''
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

    def destroy(self):
        pass

class Player:
    def __init__(self,  listCards: list):
        self.scores= 0
        self.cards= listCards

        def select_cards(self):
            pass
        def drop_cards(self):
            pass

class Game:
    def __init__(self):
        pygame.init()

        self.screen= pygame.display.set_mode((600,600))
        pygame.display.set_caption("Jokenpô")
        self.play = False

        self.stone_card= Card(0,400, "assets/carta_pedra.png",3)
        self.paper_card= Card(0,400, "assets/carta_papel.png",3)
        self.scissors_card= Card(0,400, "assets/carta_tesoura.png",3)
        self.scissors_card= Card(0,400, "assets/carta_tesoura.png",3)
 
        self.stone_card2= Card(0,10, "assets/carta_pedra.png",3)
        self.paper_card2= Card(0,10, "assets/carta_papel.png",3)
        self.scissors_card2= Card(0,10, "assets/carta_tesoura.png",3)
        self.scissors_card2= Card(0,10, "assets/carta_tesoura.png",3)

        self.back_card= Card(0,10, "assets/carta_verso.png",3)
        self.back_card_bot= Card(0,10, "assets/carta_verso.png",2)


        self.player= Player([self.stone_card, self.paper_card, self.scissors_card])
        self.bot= Player([self.stone_card2, self.paper_card2, self.scissors_card2])
        self.cards_on_the_table= [self.stone_card, self.stone_card2]

        x1=115
        for card in self.player.cards:
            card.x+= x1
            x1+=125
        
        x2= int((600/2-82) -(82/2))#177
        for card in self.bot.cards:
            card.scale=1
            card.x+= x2
            x2+=83

    def interface(self):
        for card in self.player.cards:
            self.screen.blit(card.img, (card.x, card.y))
            card.update()

            #MOUSE_UP
            if card.mouse_up: 
                card.y = 395
                #MOUSE_PRESSED
                if card.mouse_pressed:
                    self.cards_on_the_table[0]= self.back_card
                    self.player.cards.remove(card)
                    try:
                        self.cards_on_the_table[1]= self.bot.cards[int(randint(0, len(self.bot.cards)))]
                        self.bot.cards.remove(self.cards_on_the_table[1])
                    except:
                        self.cards_on_the_table[1]= self.bot.cards[int(randint(0, len(self.bot.cards)))]
                        self.bot.cards.remove(self.cards_on_the_table[1])
            else: card.y=400

        for card in self.bot.cards:
            self.screen.blit(self.back_card_bot.img, (card.x, card.y))
            card.update()

            if self.cards_on_the_table[0]== self.back_card:
                self.cards_on_the_table[1]= self.back_card
                #self.cards_on_the_table[1]= self.bot.cards[randint(0, len(self.bot.cards))]
                #self.bot.cards.remove(self.cards_on_the_table[1])

            if not self.cards_on_the_table[0] in self.player.cards:
                self.screen.blit(self.cards_on_the_table[0].img, (150, 171))

            if not self.cards_on_the_table[1] in self.bot.cards:
                self.screen.blit(self.cards_on_the_table[1].img, (330, 171))


    def main(self):
        while True:
            self.screen.fill((0,0,0))
            self.interface()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type== QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    game=Game()
    game.main()