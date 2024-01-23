import pygame
from pygame.locals import *
from random import randint

class Object:
    def __init__(self, x:int, y:int , img:str, scale: int):
        self.x= x
        self.y= y
        self.scale= scale
        self.pre_img= pygame.image.load(img)
        self.img= pygame.transform.scale(self.pre_img, (self.pre_img.get_width() * self.scale, self.pre_img.get_height()*self.scale))
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
        self.defeats= 0
        self.cards= cards
        self.chosen_card=False

    def update_cards(self, screen, padx, pady):
        x=int((screen.get_size()[0]/2-padx) -(padx/2))
        for card in self.cards:
            card.update()
            if card.mouse_up and card.y>20:
                card.y = screen.get_size()[1] - card.h -20
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
        self.screen_w, self.screen_h= self.screen.get_size()
        pygame.display.set_caption("Jokenpô")
        pygame.mouse.set_visible(False)

        #Interface Objects
        self.play = False
        self.flip_card= False
        self.img= pygame.image.load("assets/icon.png")
        self.icon= pygame.transform.scale(self.img, (self.img.get_width()*5, self.img.get_height()*5))
        self.mouse= Object(0,0, "assets/mouse.png",2)
        self.btn_play= Object(0,0,"assets/btn_up.png",5)
        self.btn_play_down= Object(0,0,"assets/btn_down.png",5)

        #Cards
        self.deck= Object(0,0, "assets/deck_card.png", 3)
        self.back_card= Object(0,0, "assets/back_card.png",3)
        self.back_card2= Object(0,0, "assets/back_card.png",3)
        self.back_card_bot= Object(0,0, "assets/back_card.png",2)
        self.rect_pos_card= Object(0,0, "assets/rect_pos_card.png",3)
        self.cards_on_the_table= [self.back_card, self.back_card2]

        self.player= Player([Object(0,0, "assets/rock_card.png",3),
                             Object(0,0, "assets/paper_card.png",3),
                             Object(0,0, "assets/scissors_card.png",3)])
            
        self.bot= Player([Object(0,0, "assets/rock_card.png",3),
                             Object(0,0, "assets/paper_card.png",3),
                             Object(0,0, "assets/scissors_card.png",3)])

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
            #Deck
            self.deck.x=self.screen_w/2 - self.deck.w/2
            self.deck.y=self.screen_h/2 - self.deck.h/2
            self.screen.blit(self.deck.img, (self.deck.x, self.deck.y))

            #Player.cards
            for card in self.player.cards:
                self.player.update_cards(self.screen, card.w + 4 * len(self.player.cards), self.screen_h - card.h -10)
                self.screen.blit(card.img, (card.x, card.y))

                if card.mouse_up:
                    self.screen.blit(self.rect_pos_card.img, (card.x-6, card.y-6))

                    if card.mouse_pressed and card.y < self.screen_h - card.h -10:
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
                self.cards_on_the_table[0].x=self.screen_w/2 - self.screen_w/4 -card.w/2
                self.cards_on_the_table[1].x=self.screen_w/2 + self.screen_w/4 - card.w/2
                self.cards_on_the_table[0].y=self.screen_h/2 - card.h/2
                self.cards_on_the_table[1].y=self.screen_h/2 - card.h/2
                
                if self.player.chosen_card and self.bot.chosen_card:
                    if self.flip_card: 
                        self.screen.blit(card.img, (card.x, card.y))
                    else:
                        if card.y < self.screen_h-192-20:
                            self.screen.blit(self.back_card.img, (card.x, card.y))
                        if pygame.mouse.get_pressed()[2]:
                            self.flip_card= True

                    if self.flip_card and pygame.mouse.get_pressed()[0]:
                        self.verify_cards()
                        self.cards_on_the_table= [self.back_card, self.back_card2]
                        self.player.chosen_card= False
                        self.bot.chosen_card= False
                        self.flip_card= False

                self.screen.blit(self.rect_pos_card.img, (card.x-6, card.y-6))
                card.update()
        
        else:
            #Menu Inicial
            self.screen.blit(self.icon, (self.screen_w/2 - self.icon.get_width()/2, self.screen_h/2 - self.icon.get_height()/2 - self.btn_play.h/2))
            self.btn_play.x= self.screen_w/2 - self.icon.get_width()/2
            self.btn_play.y= self.screen_h/2 + self.btn_play.h/2+55
            self.btn_play.update()

            if self.btn_play.mouse_up:
                self.screen.blit(self.btn_play.img, (self.btn_play.x, self.btn_play.y))
                if self.btn_play.mouse_pressed: 
                    self.play= True
            else: self.screen.blit(self.btn_play_down.img, (self.btn_play.x, self.btn_play.y))

    def main(self):
        while True:
            self.screen.fill((112,198,169))
            self.draw_interface()
            self.screen.blit(self.mouse.img, (pygame.mouse.get_pos()))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type== QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    game=Game()
    game.main()