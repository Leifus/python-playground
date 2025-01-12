from config import pygame, os
import config


class MediaManager():
    def __init__(self):
        self.root_path = f'{os.getcwd()}/{config.media_root_path}'
        self.media = dict()

    #TODO Allow the media manager to determine the convert
    def get(self, path, convert=False, convert_alpha=False):
        file_path = f'{self.root_path}/{path}'

        if not os.path.exists(file_path):
            return None

        cached_media = self.media.get(file_path)
        if cached_media is not None:
            return cached_media
        
        loaded_media = pygame.image.load(file_path)
        if convert:
            loaded_media = loaded_media.convert()
        elif convert_alpha:
            loaded_media = loaded_media.convert_alpha()
            
        self.media[file_path] = loaded_media
        return loaded_media