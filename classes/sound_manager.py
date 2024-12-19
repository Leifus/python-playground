from config import pygame, os
import config


class SoundManager():
    def __init__(self):
        self.root_path = config.sounds_root_path
        self.sounds = dict()
        pygame.mixer.init(channels=16)
        self.curr_channel = 0

    def play_sound(self, path, volume):
        file_path = f'{self.root_path}/{path}'

        if not os.path.exists(file_path):
            return
        
        sound = None
        cached_sound = self.sounds.get(file_path)
        if cached_sound is not None:
            sound = cached_sound
        else:
            sound = pygame.mixer.Sound(file_path)
            self.sounds[file_path] = sound

        sound.set_volume(volume)

        #first step in sound management
        #find a free channel and play
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(sound)

        return sound.get_length()