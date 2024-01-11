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

        if "pedra" in img:self.type="pedra"
        if "papel" in img:self.type="papel"
        if "tesoura" in img:self.type="tesoura"

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

    def update_cards(self, screen, padx, pady):
        x=int((screen.get_size()[0]/2-padx) -(padx/2))
        for card in self.cards:
            card.update()
            if card.mouse_up and card.y>20:card.y = screen.get_size()[1] - card.h -20
            else: card.y= pady
            card.x= x
            x+=padx



class Game:
    def __init__(self):
        pygame.init()
        self.screen= pygame.display.set_mode()
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
        self.deck= Card(0,0, "assets/baralho.png", 3)

        self.player= Player([self.stone_card, self.paper_card, self.scissors_card])
        self.bot= Player([self.stone_card2, self.paper_card2, self.scissors_card2])
        self.cards_on_the_table= [self.deck, self.deck]

    def draw_interface(self):
        if self.play:

            #Player.cards
            for card in self.player.cards:
                self.player.update_cards(self.screen, self.player.cards[0].w + 4 * len(self.player.cards), self.screen.get_size()[1] - self.player.cards[0].h -10)
                self.screen.blit(card.img, (card.x, card.y))
                
                if not self.player.select_card:
                    if card.mouse_pressed:
                        self.cards_on_the_table[0]= card
                        self.player.cards.remove(self.cards_on_the_table[0])
                        self.player.select_card= True

            #Bot.cards
            for card in self.bot.cards:
                self.bot.update_cards(self.screen, self.back_card_bot.w + 2 * len(self.bot.cards), 10)
                self.screen.blit(self.back_card_bot.img, (card.x, card.y))

                if self.player.select_card and not self.bot.select_card:
                    try: self.cards_on_the_table[2]= self.bot.cards[randint(0, len(self.bot.cards))]
                    except: 
                        try: self.cards_on_the_table[1]= self.bot.cards[randint(0, len(self.bot.cards))]
                        except: self.cards_on_the_table[1]= self.bot.cards[randint(0, len(self.bot.cards))]
                    self.bot.cards.remove(self.cards_on_the_table[1])
                    self.bot.select_card=True   

            #Cards on the table
            for card in self.cards_on_the_table:
                self.screen.blit(card.img, (card.x, card.y))
                card.update()

                if self.player.select_card and self.bot.select_card:
                    self.cards_on_the_table[0].x=self.screen.get_size()[0]/2 - self.screen.get_size()[0]/4 -self.cards_on_the_table[0].w/2
                    self.cards_on_the_table[0].y=self.screen.get_size()[1]/2 - self.cards_on_the_table[0].h/2
                    
                    self.cards_on_the_table[1].x=self.screen.get_size()[0]/2 + self.screen.get_size()[0]/4 - self.cards_on_the_table[1].w/2
                    self.cards_on_the_table[1].y=self.screen.get_size()[1]/2 - self.cards_on_the_table[1].h/2

                    if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
                        pass
                        '''self.player.cards.append(self.cards_on_the_table.pop())
                        self.bot.cards.append(self.cards_on_the_table.pop())
                        self.player.select_card= False
                        self.bot.select_card= False'''

            #Deck
            self.deck.x=self.screen.get_size()[0]/2 - self.deck.w/2
            self.deck.y=self.screen.get_size()[1]/2 - self.deck.h/2
            self.screen.blit(self.deck.img, (self.deck.x, self.deck.y))

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
