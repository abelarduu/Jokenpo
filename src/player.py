
import pygame

class Player:
    def __init__(self,  cards: list):
        self.cards= cards
        self.round_points= []
        self.chosen_card=False

    def update_cards(self,screen_w ,padx, pady):
        x= screen_w/2 - (padx/2 *len(self.cards))
        for card in self.cards:
            card.x= x
            x+= padx

            if card.mouse_up and card.y>20: 
                card.y = pady -20
            else: card.y= pady
            card.update()

    def select_card(self, card):
        if not self.chosen_card:
            self.cards.remove(card)
            self.chosen_card= True
            return card