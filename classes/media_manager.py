from config import pygame
import config


class MediaManager():
    def __init__(self):
        self.root_path = config.media_root_path
        self.media = dict()

    def get(self, path, convert=False, convert_alpha=False):
        full_path = f'{self.root_path}/{path}'

        cached_media = self.media.get(full_path)
        if cached_media is not None:
            return cached_media

        loaded_media = pygame.image.load(full_path)
        if convert:
            loaded_media = loaded_media.convert()
        elif convert_alpha:
            loaded_media = loaded_media.convert_alpha()
            
        self.media[full_path] = loaded_media
        return loaded_media