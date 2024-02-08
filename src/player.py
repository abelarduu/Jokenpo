
import pygame

class Player:
    def __init__(self,  cards: list):
        self.cards= cards
        self.round_points= []
        self.chosen_card=False
        self.get_card_from_the_deck= False

    def update_cards(self,screen_w ,padx, pady):
        x= screen_w/2 - (padx/2 *len(self.cards))
        for card in self.cards:
            card.x= x
            card.y= pady
            card.update()
            x+= padx

    def select_card(self, card):
        if not self.chosen_card:
            self.cards.remove(card)
            self.chosen_card= True
            return card