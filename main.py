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

        self.bot= Player([Card(0,0, "rock_card.png", 2),
                        Card(0,0, "paper_card.png", 2),
                        Card(0,0, "scissors_card.png", 2)])

    def new_card(self, scale):
        card_types=["rock_card.png","paper_card.png","scissors_card.png"]
        card= Card(0, 0, card_types[randint(0, len(card_types)-1)], scale)
        return card

    def verify_cards(self):
        if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
            self.cards_on_the_table.clear()
            self.bot.cards.append(self.new_card(scale=2))
            self.player.get_card_from_the_deck= True

        elif self.cards_on_the_table[0].type == "rock" and self.cards_on_the_table[1].type == "scissors":   
            self.bot.cards.append(self.new_card(scale=2))
            self.player.round_points.append(True)
            self.bot.round_points.append(False)
            screen.blit(player_victory_ribbon.img, (screen_w/2 - player_victory_ribbon.w/2, 170))

        elif self.cards_on_the_table[0].type == "paper" and self.cards_on_the_table[1].type == "rock":      
            self.bot.cards.append(self.new_card(scale=2))
            self.player.round_points.append(True)
            self.bot.round_points.append(False)
            screen.blit(player_victory_ribbon.img, (screen_w/2 - player_victory_ribbon.w/2, 170))

        elif self.cards_on_the_table[0].type == "scissors" and self.cards_on_the_table[1].type == "paper":  
            self.bot.cards.append(self.new_card(scale=2))
            self.player.round_points.append(True)
            self.bot.round_points.append(False)
            screen.blit(player_victory_ribbon.img, (screen_w/2 - player_victory_ribbon.w/2, 170))
        
        else:
            self.player.get_card_from_the_deck= True
            self.player.round_points.append(False)
            self.bot.round_points.append(True)
            screen.blit(bot_victory_ribbon.img, (screen_w/2 - bot_victory_ribbon.w/2, 170))
            
    def draw_HUD(self):
        screen.blit(hud_player.img, (hud_player.pos.x, hud_player.pos.y))
        screen.blit(hud_bot.img, (hud_bot.pos.x, hud_bot.pos.y))

        padx=0
        for value in self.player.round_points:
            if value: screen.blit(rect_round_win.img,(hud_player.pos.x + padx, 130))
            else: screen.blit(rect_round.img,(hud_player.pos.x + padx, 130))
            padx+=15 + rect_round.w

        padx2=screen_w - rect_round.w
        for value in self.bot.round_points:
            if value: screen.blit(rect_round_win.img,(padx2, 130))
            else: screen.blit(rect_round.img,(padx2, 130))
            padx2-=15 + rect_round.w

    def interface(self):
        if self.play:
            self.draw_HUD()
            deck_card.pos.x= screen_w/2 - deck_card.w/2
            deck_card.pos.y= screen_h/2 - deck_card.h/2
            deck_card.update()

            screen.blit(deck_card.img, (deck_card.pos.x, deck_card.pos.y))
            if deck_card.mouse_up:
                screen.blit(rect_deck_card.img, (deck_card.pos.x-6, deck_card.pos.y-6))
                if deck_card.mouse_pressed and len(self.player.cards) <5:
                    if self.player.get_card_from_the_deck:
                        self.player.cards.append(self.new_card(scale=3))
                        self.player.get_card_from_the_deck= False

            #Player.cards
            for card in self.player.cards:
                self.player.update_cards(screen_w, 4 + card.w + 4, screen_h - card.h -10)
                screen.blit(card.img, (card.pos.x, card.pos.y))

                if card.mouse_up:
                    screen.blit(rect_pos_card.img, (card.pos.x-6, card.pos.y-6))
                    if not self.player.get_card_from_the_deck:
                        if not self.player.chosen_card:
                                if card.mouse_pressed and card.pos.y < screen_h - card.h -10:
                                    self.cards_on_the_table[0]= self.player.select_card(card)

            #Bot.cards
            for card in self.bot.cards:
                self.bot.update_cards(screen_w, 2 + back_card_bot.w + 2, 20)
                screen.blit(back_card_bot.img, (card.pos.x, card.pos.y))

                if self.player.chosen_card and not self.bot.chosen_card:
                    card_bot= self.bot.select_card(self.bot.cards[randint(0, len(self.bot.cards)-1)])
                    self.cards_on_the_table[1]= Card(0, 0, f"{card_bot.type}_card.png",3)
                    
            #Cards on the table
            for card in self.cards_on_the_table:
                self.cards_on_the_table[0].pos.x=screen_w/2 - screen_w/4 - card.w/2
                self.cards_on_the_table[1].pos.x=screen_w/2 + screen_w/4 - card.w/2
                self.cards_on_the_table[0].pos.y=screen_h/2 - card.h/2
                self.cards_on_the_table[1].pos.y=screen_h/2 - card.h/2
                card.update()
                
                if self.player.chosen_card and self.bot.chosen_card:
                    if self.flip_card:
                        screen.blit(card.img, (card.pos.x, card.pos.y))
                        if pygame.mouse.get_pressed()[0]:
                            self.verify_cards()
                            self.cards_on_the_table= [back_card, back_card2]
                            self.player.chosen_card= False
                            self.bot.chosen_card= False
                            self.flip_card= False

                    else:
                        if card.pos.y < screen_h- card.h -20:
                            screen.blit(back_card.img, (card.pos.x, card.pos.y))
                            if card.mouse_up and pygame.mouse.get_pressed()[2]:
                                self.flip_card= True

                screen.blit(rect_pos_card.img, (card.pos.x-6, card.pos.y-6))
                if pygame.key.get_pressed()[K_r]:
                    self.reset()
        else:
            #Menu Inicial
            screen.blit(icon, (screen_w/2 - icon.get_width()/2, screen_h/2 - icon.get_height()/2 - btn_play.h/2))
            btn_play.pos.x= screen_w/2 - icon.get_width()/2
            btn_play.pos.y= screen_h/2 + btn_play.h/2+55
            btn_play.update()

            if btn_play.mouse_up:
                screen.blit(btn_play.img, (btn_play.pos.x, btn_play.pos.y))
                if btn_play.mouse_pressed: 
                    self.play= True

            else: screen.blit(btn_play_down.img, (btn_play.pos.x, btn_play.pos.y))
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