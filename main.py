import pygame
from src import *
from pygame.locals import *
from random import randint

class Game():
    def __init__(self):
        self.reset()

    def reset(self):
        self.play= False
        self.flip_card= False
        self.timer= pygame.time.Clock()
        self.cards_on_the_table= [back_card, back_card2]
        self.player= Player([Card(0,0, "rock_card.png", 3),
                    Card(0,0, "paper_card.png", 3),
                    Card(0,0, "scissors_card.png", 3)])

        self.bot= Player([Card(0,0, "rock_card.png", 3),
                        Card(0,0, "paper_card.png", 3),
                        Card(0,0, "scissors_card.png", 3)])

    def new_card(self):
        card_types=["rock_card.png","paper_card.png","scissors_card.png"]
        card= Card(0, 0, card_types[randint(0, len(card_types)-1)],3)
        return card

    def verify_cards(self):
        if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
            self.cards_on_the_table.clear()
            self.bot.cards.append(self.new_card())
            self.player.get_card_from_the_deck= True

        elif self.cards_on_the_table[0].type == "rock" and self.cards_on_the_table[1].type == "scissors":   
            self.bot.cards.append(self.new_card())
            self.player.round_points.append(True)
            self.bot.round_points.append(False)

        elif self.cards_on_the_table[0].type == "paper" and self.cards_on_the_table[1].type == "rock":      
            self.bot.cards.append(self.new_card())
            self.player.round_points.append(True)
            self.bot.round_points.append(False)

        elif self.cards_on_the_table[0].type == "scissors" and self.cards_on_the_table[1].type == "paper":  
            self.bot.cards.append(self.new_card())
            self.player.round_points.append(True)
            self.bot.round_points.append(False)

        else:
            self.player.get_card_from_the_deck= True
            self.player.round_points.append(False)
            self.bot.round_points.append(True)
            
    def draw_HUD(self):
        screen.blit(hud_player.img, (hud_player.x, hud_player.y))
        screen.blit(hud_bot.img, (hud_bot.x, hud_bot.y))

        padx=0
        for value in self.player.round_points:
            if value: screen.blit(rect_round_win.img,(hud_player.x + padx, 130))
            else: screen.blit(rect_round.img,(hud_player.x + padx, 130))
            padx+=15 + rect_round.w

        padx2=screen_w - rect_round.w
        for value in self.bot.round_points:
            if value: screen.blit(rect_round_win.img,(padx2, 130))
            else: screen.blit(rect_round.img,(padx2, 130))
            padx2-=15 + rect_round.w

    def interface(self):
        if self.play:
            self.draw_HUD()
            #Deck
            if deck_card.mouse_up:
                deck_card.y= screen_h/2 - deck_card.h/2 - 10
                screen.blit(deck_card.img, (deck_card.x, deck_card.y))
                screen.blit(rect_deck_card.img, (deck_card.x-6, deck_card.y-6))
                #+1 card
                if deck_card.mouse_pressed and len(self.player.cards) <5:
                    if self.player.get_card_from_the_deck:
                        self.player.cards.append(self.new_card())
                        self.player.get_card_from_the_deck= False
            else:
                deck_card.x= screen_w/2 - deck_card.w/2
                deck_card.y= screen_h/2 - deck_card.h/2
                screen.blit(deck_card.img, (deck_card.x, deck_card.y))
            deck_card.update()

            #Player.cards
            for card in self.player.cards:
                self.player.update_cards(screen_w, 4 + card.w + 4, screen_h - card.h -10)
                screen.blit(card.img, (card.x, card.y))

                if card.mouse_up:
                    screen.blit(rect_pos_card.img, (card.x-6, card.y-6))
                    if not self.player.get_card_from_the_deck:
                        if not self.player.chosen_card:
                                if card.mouse_pressed and card.y < screen_h - card.h -10:
                                    self.cards_on_the_table[0]= self.player.select_card(card)

            #Bot.cards
            for card in self.bot.cards:
                self.bot.update_cards(screen_w, 2 + back_card_bot.w + 2, 20)
                screen.blit(back_card_bot.img, (card.x, card.y))

                if self.player.chosen_card and not self.bot.chosen_card:
                    self.cards_on_the_table[1]= self.bot.select_card(self.bot.cards[randint(0, len(self.bot.cards)-1)])

            #Cards on the table
            for card in self.cards_on_the_table:
                self.cards_on_the_table[0].x=screen_w/2 - screen_w/4 - card.w/2
                self.cards_on_the_table[1].x=screen_w/2 + screen_w/4 - card.w/2
                self.cards_on_the_table[0].y=screen_h/2 - card.h/2
                self.cards_on_the_table[1].y=screen_h/2 - card.h/2
                card.update()
                
                if self.player.chosen_card and self.bot.chosen_card:
                    if self.flip_card:
                        screen.blit(card.img, (card.x, card.y))
                        if pygame.mouse.get_pressed()[0]:
                            self.verify_cards()
                            self.cards_on_the_table= [back_card, back_card2]
                            self.player.chosen_card= False
                            self.bot.chosen_card= False
                            self.flip_card= False

                    else:
                        if card.y < screen_h- card.h -20:
                            screen.blit(back_card.img, (card.x, card.y))
                            if card.mouse_up and pygame.mouse.get_pressed()[2]:
                                self.flip_card= True

                    if self.flip_card and pygame.mouse.get_pressed()[0]:
                        self.verify_cards()

                        self.cards_on_the_table= [back_card, back_card2]
                        self.player.chosen_card= False
                        self.bot.chosen_card= False
                        self.flip_card= False
                screen.blit(rect_pos_card.img, (card.x-6, card.y-6))
                if pygame.key.get_pressed()[K_r]:
                    self.reset()
        else:
            #Menu Inicial
            screen.blit(icon, (screen_w/2 - icon.get_width()/2, screen_h/2 - icon.get_height()/2 - btn_play.h/2))
            btn_play.x= screen_w/2 - icon.get_width()/2
            btn_play.y= screen_h/2 + btn_play.h/2+55
            btn_play.update()

            if btn_play.mouse_up:
                screen.blit(btn_play.img, (btn_play.x, btn_play.y))
                if btn_play.mouse_pressed: 
                    self.play= True

            else: screen.blit(btn_play_down.img, (btn_play.x, btn_play.y))
        screen.blit(mouse, pygame.mouse.get_pos())

    def main(self):
        while True:
            screen.fill(BG)
            self.interface()
            self.timer.tick(60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    game= Game()
    game.main()
