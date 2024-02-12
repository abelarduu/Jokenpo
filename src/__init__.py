import pygame
from src import assets
from src.cards import Card
from src.player import Player

#INIT
pygame.init()
screen= pygame.display.set_mode()
screen_w, screen_h= screen.get_size()
pygame.display.set_caption("Jokenpô")
mouse= assets.get_image("mouse.png",3)
pygame.mouse.set_visible(False)
BG= (112, 198, 169)
FPS= 60

#MENU
icon= assets.get_image("icon.png",5)
btn_play= Card(0,0,"btn_up.png",5)
btn_play_down= Card(0,0,"btn_down.png",5)

#HUD
rect_round= Card(0,0,"rect_round.png",3)
rect_round_win= Card(0,0,"rect_round_win.png",3)
hud_player= Card(0,0,"hud_player.png",3)
hud_bot= Card(0,0,"hud_bot.png",3)
hud_bot.pos.x= screen_w - hud_bot.w       

#Cards
deck_card= Card(0,0, "deck_card.png", 3)
back_card= Card(0,0, "back_card.png", 3)
back_card2= Card(0,0, "back_card.png", 3)
back_card_bot= Card(0,0, "back_card.png", 2)
rect_pos_card= Card(0,0, "rect_pos_card.png", 3)
rect_deck_card= Card(0,0, "rect_deck_card.png", 3)

#Sounds
sound_mouse_up=assets.get_sound("mouse_up.mp3")
music=assets.get_music("music.mp3")
pygame.mixer.music.play(-1)