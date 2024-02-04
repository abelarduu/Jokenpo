import pygame
from src import *
from pygame.locals import *
from random import randint


class Game():
    def __init__(self):
        self.play= False
        self.flip_card= False
        self.timer= pygame.time.Clock()
        self.cards_on_the_table= [back_card, back_card2]
    def reset(self):
        pass

    def verify_cards(self):
        if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
            bot.cards.append(self.cards_on_the_table.pop(1))
            player.cards.append(self.cards_on_the_table.pop(0))

        elif self.cards_on_the_table[0].type == "rock" and self.cards_on_the_table[1].type == "scissors":   
            bot.cards.append(self.cards_on_the_table.pop(1))
            player.win.append(True)
            bot.win.append(False)

        elif self.cards_on_the_table[0].type == "paper" and self.cards_on_the_table[1].type == "rock":      
            bot.cards.append(self.cards_on_the_table.pop(1))
            player.win.append(True)
            bot.win.append(False)

        elif self.cards_on_the_table[0].type == "scissors" and self.cards_on_the_table[1].type == "paper":  
            bot.cards.append(self.cards_on_the_table.pop(1))
            player.win.append(True)
            bot.win.append(False)

        else:
            player.cards.append(self.cards_on_the_table.pop(0))
            bot.win.append(True)
            player.win.append(False)

    def interface(self):
        if self.play:
            #Deck
            deck_card.x= screen_w/2 - deck_card.w/2
            deck_card.y= screen_h/2 - deck_card.h/2
            screen.blit(deck_card.img, (deck_card.x, deck_card.y))

            #Player.cards
            for card in player.cards:
                player.update_cards(screen_w, 4 + card.w + 4, screen_h - card.h -10)
                screen.blit(card.img, (card.x, card.y))

                if card.mouse_up:
                    screen.blit(rect_pos_card.img, (card.x-6, card.y-6))

                    if not player.chosen_card:
                        if card.mouse_pressed and card.y < screen_h - card.h -10:
                            self.cards_on_the_table[0]= player.select_card(card)

            #Bot.cards
            for card in bot.cards:
                bot.update_cards(screen_w, 2 + back_card_bot.w + 2, 10)
                screen.blit(back_card_bot.img, (card.x, card.y))

                if player.chosen_card and not bot.chosen_card:
                    self.cards_on_the_table[1]= bot.select_card(bot.cards[randint(0, len(bot.cards)-1)])

            #Cards on the table
            for card in self.cards_on_the_table:
                self.cards_on_the_table[0].x=screen_w/2 - screen_w/4 - card.w/2
                self.cards_on_the_table[1].x=screen_w/2 + screen_w/4 - card.w/2
                self.cards_on_the_table[0].y=screen_h/2 - card.h/2
                self.cards_on_the_table[1].y=screen_h/2 - card.h/2

                if player.chosen_card and bot.chosen_card:
                    if self.flip_card:
                        screen.blit(card.img, (card.x, card.y))
                        if pygame.mouse.get_pressed()[0]:
                            self.verify_cards()
                            self.cards_on_the_table= [back_card, back_card2]
                            player.chosen_card= False
                            bot.chosen_card= False
                            self.flip_card= False

                    else:
                        if card.y < screen_h- card.h -20:
                            screen.blit(back_card.img, (card.x, card.y))
                            if pygame.mouse.get_pressed()[2]:
                                self.flip_card= True

                    if self.flip_card and pygame.mouse.get_pressed()[0]:
                        self.verify_cards()

                        self.cards_on_the_table= [back_card, back_card2]
                        player.chosen_card= False
                        bot.chosen_card= False
                        self.flip_card= False
                screen.blit(rect_pos_card.img, (card.x-6, card.y-6))
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
        #MOUSE
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