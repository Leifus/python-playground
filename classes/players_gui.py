from classes.__helpers__ import aspect_scale
from config import pygame
from classes.game_sprite import GameSprite
from globals import media_manager

class PlayersGui(GameSprite):
    def __init__(self, size, position):
        super(GameSprite, self).__init__()

        self.size = size
        self.position = position
        self.players = []
        self.player_surfaces = []
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        self.player_overlay_orig_image: pygame.Surface = None
        self.player_housing_orig_image: pygame.Surface = None
        self.player_avatar_orig_image: pygame.Surface = None

        self.setup_visuals()

    def setup_visuals(self):
        # Player Housing
        media = 'UI/spr_UI_Popup.png'
        img = media_manager.get(media)
        self.player_housing_orig_image = aspect_scale(img, self.size)

        # Player Overlay
        media = 'UI/spr_UI_Player_Bar.png'
        img = media_manager.get(media)
        self.player_overlay_orig_image = aspect_scale(img, self.size)

        # Player Avatar
        media = 'UI/Menu UI/spr_UI_Player_Icon.png'
        img = media_manager.get(media)
        self.player_avatar_orig_image = aspect_scale(img, self.size)


    def setup_players(self, players):
        self.players = players
        self.redraw()

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def redraw(self):
        self.image.fill((0,0,0,0))

        avatar_size = (38, 38)
        player_gui_spacing = 30
        player_gui_width = (self.rect.width - avatar_size[0]/2 - player_gui_spacing) / len(self.players)
        player_gui_height = 50

        for i, player in enumerate(self.players):
            player_iter = i+1

             # Player Overlay
            size = (player_gui_width, player_gui_height)
            overlay_image = pygame.transform.scale(self.player_overlay_orig_image, size)
            width, height = overlay_image.get_size()
            
            # Positioning
            x = player_gui_width/2*player_iter + player_gui_width/2*i + avatar_size[0]/2 + player_gui_spacing*i
            y = self.rect.height/2 + height/2
            position = (x, y)
            overlay_rect = overlay_image.get_rect(center=position)

            # Player Housing
            margin = 10
            size = (overlay_rect.width-margin, overlay_rect.height-margin)
            housing_image = pygame.transform.scale(self.player_housing_orig_image, size)
            housing_rect = housing_image.get_rect(center=position)

            # Housing Highlight
            if player.is_playing:
                size = (housing_rect.width-margin, housing_rect.height-margin)
                highlight_image = pygame.Surface(size, pygame.SRCALPHA)
                highlight_image.fill((255,255,0,30), special_flags=pygame.BLEND_RGBA_MAX)
                # highlight_image.get_rect(center=housing_rect.center)
                housing_image.blit(highlight_image, (margin/2,margin/2))


            # Player Avatar
            position = (overlay_rect.left, overlay_rect.centery)
            avatar_image = pygame.transform.scale(self.player_avatar_orig_image, avatar_size)
            avatar_rect = avatar_image.get_rect(center=position)

            # Player Name
            font_family = 'freesansbold.ttf'
            font_size = 15
            default_font_color = pygame.Color('gray80')
            active_font_color = pygame.Color('goldenrod1')
            font_color = default_font_color
            font = pygame.font.Font(font_family, font_size)

            if player.is_playing:
                font_color = active_font_color

            # Text
            text = font.render(player.name, True, font_color)
            margin_x = 3
            size = text.get_size()
            position = (margin_x + size[0]/2 + avatar_rect.width/2, housing_rect.height/2)
            text_rect = text.get_rect(center=position)

            # Text Shadow
            if player.is_playing:
                offset_x, offset_y = (-2,-2)
                position = (text_rect.centerx - offset_x, text_rect.centery - offset_y)
                color = (0,0,0,100)
                text_shadow = font.render(player.name, True, color)
                text_shadow_rect = text.get_rect(center=position)
                housing_image.blit(text_shadow, text_shadow_rect)

            housing_image.blit(text, text_rect)

            self.image.blit(housing_image, housing_rect)
            self.image.blit(overlay_image, overlay_rect)
            self.image.blit(avatar_image, avatar_rect)


    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)