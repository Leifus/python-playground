from config import pygame
from classes.draw_mode_enum import DrawModeEnum


cue_power_bar_max_power = 2000000
cue_power_bar_default_power = cue_power_bar_max_power - cue_power_bar_max_power / 3
cue_power_bar_size = (50, 400)
cue_power_bar_draw_mode = DrawModeEnum.Rich
cue_power_bar_DM_WIREFRAME_thickness = 2
cue_power_bar_DM_RAW_color = pygame.Color('white')
cue_power_bar_DM_RICH_media = 'UI/spr_UI_Powerbar.png'
cue_power_bar_overlay_DM_RICH_media = 'UI/spr_UI_Powerbar_Overlay.png'
cue_power_bar_cue_DM_RICH_media = 'UI/spr_UI_Powerbar_Cue.png'
cue_power_bar_cue_button_DM_RAW_color = pygame.Color('blue')
