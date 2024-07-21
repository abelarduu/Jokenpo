import pygame
from os import listdir
from os.path import abspath, dirname

def files_dir(folder_name:str) -> str:
    """Retorna o caminho do determinado diretorio especificado."""
    return abspath(dirname(__file__) + f"/{folder_name}")
    
def get_files(file_extension:str, folder_name:str) -> list:
    """Retorna uma lista de arquivos especificos atraves da sua extensão e de sua determinada pasta dentro dos 'assets'."""
    files = listdir(files_dir(folder_name))
    for file in files:
        if not file_extension in file:
            files.remove(file)
    return files

def get_image(rect: type(pygame.Rect), scale:int) -> pygame.Surface:
    """Retorna uma parte da imagem 'tileset.png' com uma determinada escala aplicada."""
    TILESET = pygame.image.load(f"{files_dir("images")}/tileset.png")
    img_cut = TILESET.subsurface(rect)
    img_scale = pygame.transform.scale(img_cut, (img_cut.get_width()*scale, img_cut.get_height()*scale))
    return img_scale

def get_sound(name_file:str) -> pygame.mixer.Sound:
    """Retorna o determinado arquivo de som especificado como um 'pygame.mixer.Sound()'."""
    pygame.mixer.init()
    if name_file in get_files("mp3", "sounds"):
        sound = pygame.mixer.Sound(f"{files_dir("sounds")}/{name_file}")
        return sound

def get_music(name_file:str) -> pygame.mixer.music:
    """Retorna o determinado arquivo de som especificado como um 'pygame.mixer.music()'."""
    pygame.mixer.init()
    if name_file in get_files("mp3", "sounds"):
        music = pygame.mixer.music.load(f"{files_dir("sounds")}/{name_file}")
        return music