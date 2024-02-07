import pygame
from src import assets
from src.cards import Card
from src.player import Player

#INIT
pygame.init()
screen= pygame.display.set_mode()
screen_w, screen_h= screen.get_size()
pygame.display.set_caption("Jokenpô")
mouse= assets.get_image("mouse.png",2)
pygame.mouse.set_visible(False)
BG= (112, 198, 169)
FPS= 60

#MENU
icon= assets.get_image("icon.png",5)
btn_play= Card(0,0,"btn_up.png",5)
btn_play_down= Card(0,0,"btn_down.png",5)

#Cards
rock_card= Card(0,0, "rock_card.png", 3)
paper_card= Card(0,0, "paper_card.png", 3)
scissors_card= Card(0,0, "scissors_card.png", 3)

back_card= Card(0,0, "back_card.png", 3)
back_card2= Card(0,0, "back_card.png", 3)
back_card_bot= Card(0,0, "back_card.png", 2)
deck_card= Card(0,0, "deck_card.png", 3)
rect_pos_card= Card(0,0, "rect_pos_card.png", 3)
rect_deck_card= Card(0,0, "rect_deck_card.png", 3)

#Sounds
sound_mouse_up=assets.get_sound("mouse_up.mp3")

#Players
player= Player([Card(0,0, "rock_card.png", 3),
                Card(0,0, "paper_card.png", 3),
                Card(0,0, "scissors_card.png", 3)])

bot= Player([Card(0,0, "rock_card.png", 3),
                Card(0,0, "paper_card.png", 3),
                Card(0,0, "scissors_card.png", 3)])