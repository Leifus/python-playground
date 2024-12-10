from config import pygame
import config


class MediaManager():
    def __init__(self):
        self.root_path = config.media_root_path
        self.media = dict()

    def get_image(self, path, convert=False, convert_alpha=False):
        full_path = f'{self.root_path}/{path}'
        img_surface = pygame.image.load(full_path)
        if convert:
            img_surface = img_surface.convert()
        elif convert_alpha:
            img_surface = img_surface.convert_alpha()
            
        return img_surface