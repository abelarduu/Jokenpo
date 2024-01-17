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

        if "rock" in img:self.type="rock"
        elif "paper" in img:self.type="paper"
        elif "scissors" in img:self.type="scissors"
        else: self.type= "deck"

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
        self.chosen_card=False

    def update_cards(self, screen, padx, pady):
        x=int((screen.get_size()[0]/2-padx) -(padx/2))
        for card in self.cards:
            card.update()
            if card.mouse_up and card.y>20:card.y = screen.get_size()[1] - card.h -20
            else: card.y= pady
            card.x= x
            x+=padx

    def select_card(self, card):
        if not self.chosen_card:
            self.cards.remove(card)
            self.chosen_card= True
            return card

class Game:
    def __init__(self):
        pygame.init()
        self.screen= pygame.display.set_mode()
        pygame.display.set_caption("Jokenpô")
        self.play = True
        self.flip_card= False

        self.rock_card= Card(0,0, "assets/rock_card.png",3)
        self.paper_card= Card(0,0, "assets/paper_card.png",3)
        self.scissors_card= Card(0,0, "assets/scissors_card.png",3)

        self.rock_card2= Card(0,0, "assets/rock_card.png",3)
        self.paper_card2= Card(0,0, "assets/paper_card.png",3)
        self.scissors_card2= Card(0,0, "assets/scissors_card.png",3)

        self.back_card= Card(0,0, "assets/back_card.png",3)
        self.back_card_bot= Card(0,0, "assets/back_card.png",2)
        self.deck= Card(0,0, "assets/deck.png", 3)

        self.player= Player([self.rock_card, self.paper_card, self.scissors_card])
        self.bot= Player([self.rock_card2, self.paper_card2, self.scissors_card2])
        self.cards_on_the_table= [self.deck, self.deck]

    def verify_cards(self):
        if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
            self.bot.cards.append(self.cards_on_the_table.pop(1))
            self.player.cards.append(self.cards_on_the_table.pop(0))

        elif self.cards_on_the_table[0].type == "rock" and self.cards_on_the_table[1].type == "scissors":   self.bot.cards.append(self.cards_on_the_table.pop(1))
        elif self.cards_on_the_table[0].type == "paper" and self.cards_on_the_table[1].type == "rock":      self.bot.cards.append(self.cards_on_the_table.pop(1))
        elif self.cards_on_the_table[0].type == "scissors" and self.cards_on_the_table[1].type == "paper":  self.bot.cards.append(self.cards_on_the_table.pop(1))
        else:self.player.cards.append(self.cards_on_the_table.pop(0))

    def draw_interface(self):            
        if self.play:
            #Player.cards
            for card in self.player.cards:
                self.player.update_cards(self.screen, card.w + 4 * len(self.player.cards), self.screen.get_size()[1] - card.h -10)
                self.screen.blit(card.img, (card.x, card.y))
                
                if card.mouse_pressed and card.y <self.screen.get_size()[1] - card.h -10:
                    if not self.player.chosen_card:
                        self.cards_on_the_table[0]= self.player.select_card(card)
                   
            #Bot.cards
            for card in self.bot.cards:
                self.bot.update_cards(self.screen, self.back_card_bot.w + 2 * len(self.bot.cards), 10)
                self.screen.blit(self.back_card_bot.img, (card.x, card.y))

                if self.player.chosen_card and not self.bot.chosen_card:
                    self.cards_on_the_table[1]= self.bot.select_card(self.bot.cards[randint(0, len(self.bot.cards)-1)])

            #Cards on the table
            for card in self.cards_on_the_table:
                if self.flip_card: self.screen.blit(card.img, (card.x, card.y))
                else:
                    if card.y < self.screen.get_size()[1]-192-20:
                        self.screen.blit(self.back_card.img, (card.x, card.y))
                card.update()

                if self.player.chosen_card and self.bot.chosen_card:
                    self.cards_on_the_table[0].x=self.screen.get_size()[0]/2 - self.screen.get_size()[0]/4 -card.w/2
                    self.cards_on_the_table[0].y=self.screen.get_size()[1]/2 - card.h/2
                    
                    self.cards_on_the_table[1].x=self.screen.get_size()[0]/2 + self.screen.get_size()[0]/4 - card.w/2
                    self.cards_on_the_table[1].y=self.screen.get_size()[1]/2 - card.h/2

                    if pygame.mouse.get_pressed()[2]:
                        self.flip_card= True

                    if self.flip_card and pygame.mouse.get_pressed()[0]:
                        self.verify_cards()
                        self.cards_on_the_table= [self.deck, self.deck]
                        self.player.chosen_card= False
                        self.bot.chosen_card= False
                        self.flip_card= False

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