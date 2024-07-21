
import pygame
from src.cards import Card

class Player:
    def __init__(self,  cards: list):
        self.cards = cards
        self.round_points = []
        self.chosen_card =False
        self.get_card_from_the_deck = False
        self.wins = []

    def update_cards(self, screen_w, padx, pady):
        """Atualiza as cartas do deck do jogador na interface e verifica as interações com cada carta."""
        X = screen_w/2 - (padx/2 *len(self.cards))
        for card in self.cards:
            card.pos.x = X
            card.pos.y = pady
            card.update()
            X += padx

    def select_card(self, card) -> Card:
        """Remove e retorna a carta selecionada do deck do jogador."""
        if not self.chosen_card:
            self.cards.remove(card)
            self.chosen_card = True
            return card