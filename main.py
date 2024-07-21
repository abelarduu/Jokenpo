from src import *

class Game():
    def __init__(self):
        self.reset()

    def reset(self):
        self.play = False
        self.tutorial = False
        self.flip_card = False
        self.check_card = False
        self.mouse_released = False
        self.timer = pygame.time.Clock()
        self.cards_on_the_table = [back_card, back_card2]

        # Criando Jogadores
        self.player = Player([Card(0, 0, (172, 0, 40, 68), 3),
                              Card(0, 0, (214, 0, 40, 68), 3),
                              Card(0, 0, (257, 0, 40, 68), 3)])

        self.bot = Player([Card(0, 0, (172, 0, 40, 68), 2),
                           Card(0, 0, (214, 0, 40, 68), 2),
                           Card(0, 0, (257, 0, 40, 68), 2)])

    def new_card(self, scale) -> Card:
        """Gera e retorna uma nova carta aleatoria (Pedra, papel ou tesoura)."""
        CARDS_COORDINATES = [(172, 0, 40, 68),
                             (214, 0, 40, 68),
                             (257, 0, 40, 68)]

        card = Card(0, 0, CARDS_COORDINATES[randint(0, len(CARDS_COORDINATES) - 1)], scale)
        return card

    def player_win_round(self):
        """Padroniza as ações após a vitoria do Player."""
        self.bot.cards.append(self.new_card(scale= 2))
        self.player.round_points.append(True)
        self.bot.round_points.append(False)
    
    def bot_win_round(self):
        """Padroniza as ações após a vitoria do Bot."""
        self.player.get_card_from_the_deck = True
        self.player.round_points.append(False)
        self.bot.round_points.append(True)

    def verify_cards(self):
        """Verifica as cartas escolhidas dos jogadores a cada round."""
        card1_type = self.cards_on_the_table[0].type
        card2_type = self.cards_on_the_table[1].type

        # Verificação de cartas iguais
        if card1_type == card2_type:
            self.bot.cards.append(self.new_card(scale= 2))
            self.player.get_card_from_the_deck = True
        else:
            
            # Verificação de cartas diferentes:
            # Pedra e tesoura
            if (card1_type == "rock" and
                card2_type == "scissors"):
                self.player_win_round()
            
            # Papel e pedra
            elif (card1_type == "paper" and
                card2_type == "rock"):
                self.player_win_round()
            
            # Tesoura e papel
            elif (card1_type == "scissors" and
             card2_type == "paper"):
                self.player_win_round()
        
            # Senão, bot Ganha a rodada
            else: 
                self.bot_win_round()

    def draw_HUD(self):
        """Desenha e atualiza o HUD de pontos dos jogadores."""
        screen.blit(hud_player.img, (hud_player.pos.x, hud_player.pos.y))
        screen.blit(hud_bot.img, (hud_bot.pos.x, hud_bot.pos.y))

        # Pontuação do player
        PADX = 0
        for value in self.player.round_points:
            if value:
                screen.blit(rect_round_win.img,(hud_player.pos.x + PADX, 130))
            else: 
                screen.blit(rect_round.img,(hud_player.pos.x + PADX, 130))
            PADX += 15 + rect_round.w

        # Pontuação do Bot
        PADX2 = screen_w - rect_round.w
        for value in self.bot.round_points:
            if value: 
                screen.blit(rect_round_win.img,(PADX2, 130))
            else: 
                screen.blit(rect_round.img,(PADX2, 130))
            PADX2 -= 15 + rect_round.w

    def check_victory(self, player, img_victory_ribbon ,img_victory):
        """Padronização da Verificação de vitoria entre as cartas escolhidas entre os jogadores."""
        player.wins = [value for value in player.round_points if value]

        # Se virou as cartas da mesa e
        # Se ainda não checou as cartas
        if self.flip_card and not self.check_card:

            # Se as cartas são iguais:
            # Adiciona na tela  a fita de "Empate"
            if self.cards_on_the_table[0].type == self.cards_on_the_table[1].type:
                screen.blit(tie_ribbon.img,(screen_w/2 - tie_ribbon.w/2, self.cards_on_the_table[1].h-40))
            else:
                 if (len(player.round_points) > 0 and player.round_points[-1]):
                    screen.blit(img_victory_ribbon.img,(screen_w/2 - img_victory_ribbon.w/2, self.cards_on_the_table[1].h-40))

        # Se o Jogador Vencer
        if len(player.wins) == 3: 
            screen.blit(img_victory.img,(screen_w/2 - img_victory.w/2, screen_h/2 - img_victory.h/2 - btn_home.h/2))
            btn_home.pos.x = screen_w/2 - img_victory.w/2 + 105
            btn_home.pos.y = screen_h/2 + btn_home.h/2 + 55
            btn_home.update()

            # Resetar para o menu
            if btn_home.mouse_up:
                screen.blit(btn_home.img, btn_home.pos)
                if self.mouse_released: 
                    self.reset()
            else:
                screen.blit(btn_home_down, btn_home.pos)

    def interface(self):
        """Atualiza a interface e todos os seus elementos."""
        if self.tutorial:
            screen.blit(tutorial_ribbon.img,(screen_w/2 - tutorial_ribbon.w/2, tutorial_ribbon.h))
            screen.blit(tip1.img, (screen_w/3 - tip1.w/2, screen_h/2 - tip1.h/2))
            screen.blit(tip2.img, (screen_w/3 + screen_w/3 - tip2.w/2, screen_h/2 - tip2.h/2))
            screen.blit(tutorial_text.img, (screen_w/2 - tutorial_text.w/2, screen_h/2 +  screen_h/3 - tutorial_text.h/2))

            # Finaliza o tutorial e começa a gameplay
            if self.mouse_released: 
                self.tutorial = False
                self.play = True

        elif self.play:
            CENTERED_DECK_X = screen_w/2 - deck_card.w/2
            CENTERED_DECK_y = screen_h/2 - deck_card.h/2
            deck_card.pos.x = CENTERED_DECK_X
            deck_card.pos.y = CENTERED_DECK_y
            deck_card.update()

            screen.blit(deck_card.img, deck_card.pos)
            self.draw_HUD()
            
            if deck_card.mouse_up:
                if deck_card.mouse_pressed:
                    if self.player.get_card_from_the_deck:
                        self.player.cards.append(self.new_card(scale= 3))
                        self.player.get_card_from_the_deck = False

                screen.blit(rect_deck_card.img, deck_card.pos - (6, 6))

            # Player.cards
            for card in self.player.cards:
                self.player.update_cards(screen_w, 4 + card.w + 4, screen_h - card.h - 10)
                screen.blit(card.img, card.pos)

                if card.mouse_up:
                    screen.blit(rect_pos_card.img, card.pos - (6, 6))
                    if not self.player.get_card_from_the_deck:
                        if not self.player.chosen_card:
                            if (card.mouse_pressed and card.pos.y < screen_h - card.h - 10):
                                self.cards_on_the_table[0] = self.player.select_card(card)

            # Bot.cards
            for card in self.bot.cards:
                self.bot.update_cards(screen_w, 2 + back_card_bot.w + 2, 20)
                screen.blit(back_card_bot.img, card.pos)

                if (self.player.chosen_card and not self.bot.chosen_card):
                    card_bot = self.bot.select_card(self.bot.cards[randint(0, len(self.bot.cards) - 1)])
                    self.cards_on_the_table[1] = Card(0, 0, card_bot.img_coordinates, 3)
                    
            # Cards on the table
            for card in self.cards_on_the_table:
                CENTER_CART1_X = screen_w/2 - screen_w/4 - card.w/2
                CENTER_CART1_Y = screen_w/2 + screen_w/4 - card.w/2
                CENTER_CART2_X = screen_h/2 - card.h/2
                CENTER_CART2_Y = screen_h/2 - card.h/2
                self.cards_on_the_table[0].pos.x = CENTER_CART1_X
                self.cards_on_the_table[1].pos.x = CENTER_CART1_Y
                self.cards_on_the_table[0].pos.y = CENTER_CART2_X
                self.cards_on_the_table[1].pos.y = CENTER_CART2_Y
                card.update()

                if self.player.chosen_card and self.bot.chosen_card:
                    if self.flip_card:
                        screen.blit(card.img, card.pos)

                        if self.check_card:
                            self.verify_cards()
                            self.check_card = False
                        if pygame.mouse.get_pressed()[0]:
                            self.cards_on_the_table = [back_card, back_card2]
                            self.player.chosen_card = False
                            self.bot.chosen_card = False
                            self.flip_card = False

                    else:
                        screen.blit(back_card.img, card.pos)
                        if card.mouse_up and pygame.mouse.get_pressed()[2]:
                            self.flip_card = True
                            self.check_card = True

                screen.blit(rect_pos_card.img, card.pos - (6, 6))
                if self.player.get_card_from_the_deck:
                    screen.blit(more_one_card_text.img, (screen_w/2 - more_one_card_text.w/2, screen_h/2 - more_one_card_text.h/2 - btn_home.h/2 - 72))

            self.check_victory(self.bot, bot_victory_ribbon, bot_victory)
            self.check_victory(self.player, player_victory_ribbon, player_victory)
        else:
            # Menu Inicial
            screen.blit(icon, (screen_w/2 - icon.get_width()/2, screen_h/2 - icon.get_height()/2 - btn_play.h/2))
            btn_play.pos.x = screen_w/2 - icon.get_width()/2
            btn_play.pos.y = screen_h/2 + btn_play.h/2 + 55
            btn_play.update()

            if btn_play.mouse_up:
                screen.blit(btn_play.img, btn_play.pos)
                if self.mouse_released:
                    self.tutorial = True
                    self.mouse_released = False
            else: 
                screen.blit(btn_play_down, btn_play.pos)
        
        screen.blit(mouse, pygame.mouse.get_pos())

    def run(self):
        """Loop infinito do game."""
        while True:
            screen.fill(BG)
            self.interface()
            self.timer.tick(60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    self.mouse_released = True
                else: 
                    self.mouse_released = False
                if event.type == QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    game = Game()
    game.run()
