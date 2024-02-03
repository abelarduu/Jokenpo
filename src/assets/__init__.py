import pygame
from os import listdir
from os.path import abspath, dirname

def image_dir():
    return abspath(dirname(__file__)+"/images")

def get_image(name_file:str, scale:int):
    if name_file  in get_images():
        img=pygame.image.load(f"{image_dir()}/{name_file}")
        img_scale=pygame.transform.scale(img, (img.get_width()*scale, img.get_height()*scale))
        return img_scale

def get_images() ->list:
    images= listdir(image_dir())
    for file in images:
        if not ".png" in file:
            images.remove(file)
    return images