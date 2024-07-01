from src import *

class Game():
    def __init__(self):
        self.reset()

    def reset(self):
        self.play= False
        self.tutorial= False
        self.flip_card= False
        self.check_card= False
        self.mouse_released= False
        self.timer= pygame.time.Clock()
        self.cards_on_the_table= [back_card, back_card2]
        self.player= Player([Card(0,0, (172,0,40,68), 3),
                             Card(0,0, (214,0,40,68), 3),
                             Card(0,0, (257,0,40,68), 3)])

        self.bot= Player([Card(0,0, (172,0,40,68), 2),
                          Card(0,0, (214,0,40,68), 2),
                          Card(0,0, (257,0,40,68), 2)])

    def bot_win_round(self):
        self.player.get_card_from_the_deck= True
        self.player.round_points.append(False)
        self.bot.round_points.append(True)

    def player_win_round(self):
        self.bot.cards.append(self.new_card(scale=2))
        self.player.round_points.append(True)
        self.bot.round_points.append(False)

    def new_card(self, scale) -> Card:
        cards_coordinates=[(172,0,40,68),(214,0,40,68),(257,0,40,68)]
        card= Card(0, 0, cards_coordinates[randint(0, len(cards_coordinates)-1)], scale)
        return card

    def verify_cards(self):
        if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
            self.bot.cards.append(self.new_card(scale=2))
            self.player.get_card_from_the_deck= True
        elif self.cards_on_the_table[0].type == "rock" and self.cards_on_the_table[1].type == "scissors": self.player_win_round()
        elif self.cards_on_the_table[0].type == "paper" and self.cards_on_the_table[1].type == "rock": self.player_win_round()
        elif self.cards_on_the_table[0].type == "scissors" and self.cards_on_the_table[1].type == "paper": self.player_win_round()
        else: self.bot_win_round()

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

    def check_victory(self, player, img_victory_ribbon ,img_victory):
        player.wins=[value for value in player.round_points if value]
        if self.flip_card and not self.check_card:
            if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
                screen.blit(tie_ribbon.img,(screen_w/2 - tie_ribbon.w/2, self.cards_on_the_table[1].h-40))
            else:
                 if len(player.round_points) >0 and player.round_points[-1]:
                    screen.blit(img_victory_ribbon.img,(screen_w/2 - img_victory_ribbon.w/2, self.cards_on_the_table[1].h-40))

        if len(player.wins) ==3: 
            screen.blit(img_victory.img,(screen_w/2 - img_victory.w/2, screen_h/2 - img_victory.h/2 - btn_home.h/2))
            btn_home.pos.x= screen_w/2 - img_victory.w/2+105
            btn_home.pos.y= screen_h/2 + btn_home.h/2+55
            btn_home.update()

            if btn_home.mouse_up:
                screen.blit(btn_home.img, btn_home.pos)
                if self.mouse_released: 
                    self.reset()
                    
            else: screen.blit(btn_home_down, btn_home.pos)

    def interface(self):
        if self.tutorial:
            screen.blit(tutorial_ribbon.img,(screen_w/2 - tutorial_ribbon.w/2, tutorial_ribbon.h))
            screen.blit(tip1.img, (screen_w/3 - tip1.w/2, screen_h/2 - tip1.h/2))
            screen.blit(tip2.img, (screen_w/3 + screen_w/3 - tip2.w/2, screen_h/2 - tip2.h/2))
            screen.blit(tutorial_text.img, (screen_w/2 - tutorial_text.w/2, screen_h/2 +  screen_h/3 - tutorial_text.h/2))

            if self.mouse_released: 
                self.tutorial=False
                self.play= True

        elif self.play:
            self.draw_HUD()
            deck_card.pos.x= screen_w/2 - deck_card.w/2
            deck_card.pos.y= screen_h/2 - deck_card.h/2
            deck_card.update()

            screen.blit(deck_card.img, deck_card.pos)
            if deck_card.mouse_up:
                screen.blit(rect_deck_card.img, deck_card.pos-(6,6))
                if deck_card.mouse_pressed:
                    if self.player.get_card_from_the_deck:
                        self.player.cards.append(self.new_card(scale=3))
                        self.player.get_card_from_the_deck= False

            #Player.cards
            for card in self.player.cards:
                self.player.update_cards(screen_w, 4 + card.w + 4, screen_h - card.h -10)
                screen.blit(card.img, card.pos)

                if card.mouse_up:
                    screen.blit(rect_pos_card.img, card.pos - (6,6))
                    if not self.player.get_card_from_the_deck:
                        if not self.player.chosen_card:
                            if card.mouse_pressed and card.pos.y < screen_h - card.h -10:
                                self.cards_on_the_table[0]= self.player.select_card(card)

            #Bot.cards
            for card in self.bot.cards:
                self.bot.update_cards(screen_w, 2 + back_card_bot.w + 2, 20)
                screen.blit(back_card_bot.img, card.pos)

                if self.player.chosen_card and not self.bot.chosen_card:
                    card_bot= self.bot.select_card(self.bot.cards[randint(0, len(self.bot.cards)-1)])
                    self.cards_on_the_table[1]= Card(0, 0, card_bot.img_coordinates,3)
                    
            #Cards on the table
            for card in self.cards_on_the_table:
                self.cards_on_the_table[0].pos.x=screen_w/2 - screen_w/4 - card.w/2
                self.cards_on_the_table[1].pos.x=screen_w/2 + screen_w/4 - card.w/2
                self.cards_on_the_table[0].pos.y=screen_h/2 - card.h/2
                self.cards_on_the_table[1].pos.y=screen_h/2 - card.h/2
                card.update()

                if self.player.chosen_card and self.bot.chosen_card:
                    if self.flip_card:
                        screen.blit(card.img, card.pos)

                        if self.check_card:
                            self.verify_cards()
                            self.check_card= False
                        if pygame.mouse.get_pressed()[0]:
                            self.cards_on_the_table= [back_card, back_card2]
                            self.player.chosen_card= False
                            self.bot.chosen_card= False
                            self.flip_card= False

                    else:
                        screen.blit(back_card.img, card.pos)
                        if card.mouse_up and pygame.mouse.get_pressed()[2]:
                            self.flip_card= True
                            self.check_card= True

                screen.blit(rect_pos_card.img, card.pos-(6,6))
                if self.player.get_card_from_the_deck:
                    screen.blit(more_one_card_text.img, (screen_w/2 - more_one_card_text.w/2, screen_h/2 - more_one_card_text.h/2 - btn_home.h/2-72))

                self.check_victory(self.bot, bot_victory_ribbon, bot_victory)
                self.check_victory(self.player, player_victory_ribbon, player_victory)
        else:
            #Menu Inicial
            screen.blit(icon, (screen_w/2 - icon.get_width()/2, screen_h/2 - icon.get_height()/2 - btn_play.h/2))
            btn_play.pos.x= screen_w/2 - icon.get_width()/2
            btn_play.pos.y= screen_h/2 + btn_play.h/2+55
            btn_play.update()

            if btn_play.mouse_up:
                screen.blit(btn_play.img, btn_play.pos)
                if self.mouse_released: 
                    self.tutorial= True
                    self.mouse_released= False

            else: screen.blit(btn_play_down, btn_play.pos)
        screen.blit(mouse, pygame.mouse.get_pos())

    def run(self):
        while True:
            screen.fill(BG)
            self.interface()
            self.timer.tick(60)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    self.mouse_released= True
                else: self.mouse_released= False

                if event.type == QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    game= Game()
    game.run()
