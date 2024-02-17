import pygame
from os import listdir
from os.path import abspath, dirname

def files_dir(folder_name:str):
    return abspath(dirname(__file__)+ f"/{folder_name}")
    
def get_files(file_extension:str, folder_name:str) ->list:
    files= listdir(files_dir(folder_name))
    for file in files:
        if not file_extension in file:
            files.remove(file)
    return files

def get_image(rect: type(pygame.Rect), scale:int):
    TILESET= pygame.image.load(f"{files_dir("images")}/tileset.png")
    img_cut= TILESET.subsurface(rect)
    img_scale=pygame.transform.scale(img_cut, (img_cut.get_width()*scale, img_cut.get_height()*scale))
    return img_scale

def get_sound(name_file:str):
    pygame.mixer.init()
    if name_file in get_files("mp3", "sounds"):
        sound= pygame.mixer.Sound(f"{files_dir("sounds")}/{name_file}")
        return sound

def get_music(name_file:str):
    pygame.mixer.init()
    if name_file in get_files("mp3", "sounds"):
        music= pygame.mixer.music.load(f"{files_dir("sounds")}/{name_file}")
        return music