import pygame
from src import assets
from src.cards import Card
from src.player import Player

#INIT
pygame.init()
screen= pygame.display.set_mode()
screen_w, screen_h= screen.get_size()
pygame.display.set_caption("Jokenpô")
mouse= assets.get_image((264,86,20,30), 3)
pygame.mouse.set_visible(False)
BG= (112, 198, 169)
FPS= 60

#MENU
icon= assets.get_image((0,0,128,68), 5)
btn_play= Card(0,0, (0,105,128,35), 5)
btn_play_down= Card(0,0, (0,70,128,35), 5)

#HUD
player_victory_ribbon= Card(0,0, (130,153,150,19), 3)
bot_victory_ribbon= Card(0,0, (130,174,150,19), 3)
rect_round_win= Card(0,0,(280,70,14,14), 3)
rect_round= Card(0,0,(264,70,14,14), 3)
hud_player= Card(0,0,(299,0,104,41),3)
hud_bot= Card(0,0,(299,43,104,41),3)
hud_bot.pos.x= screen_w - hud_bot.w   

#Cards
deck_card= Card(0,0, (130,70,40,80), 3)
back_card= Card(0,0, (130,0,40,68), 3)
back_card2= Card(0,0, (130,0,40,68), 3)
back_card_bot= Card(0,0, (130,0,40,68), 2)
rect_pos_card= Card(0,0, (218,70,44,68), 3)
rect_deck_card= Card(0,0, (172,70,44,80), 3)

#Sounds
sound_mouse_up=assets.get_sound("mouse_up.mp3")
music=assets.get_music("music.mp3")
pygame.mixer.music.play(-1)