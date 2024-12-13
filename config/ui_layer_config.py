from config import pygame
from classes.draw_mode import DrawMode

# ----------------------------------------------------
# FLOOR CONFIG
# ----------------------------------------------------

ui_layer_draw_mode = DrawMode.RICH
ui_layer_DM_WIREFRAME_outline_width = 2

ui_layer_housing_DM_RAW_color = (0, 0, 0, 100)
ui_layer_housing_DM_RICH_media = 'UI/spr_UI_Housing.png'

ui_layer_options_button_size = (50, 50)
ui_layer_options_button_position = (30, 30)
ui_layer_options_button_label = 'MENU'
ui_layer_options_button_DM_RAW_font_family = 'freesansbold.ttf'
ui_layer_options_button_DM_RAW_font_size = 14
ui_layer_options_button_DM_RAW_font_color = pygame.Color('black')
ui_layer_options_button_DM_RAW_color = pygame.Color('white')
ui_layer_options_button_DM_RICH_media = 'UI/Menu UI/spr_UI_Button_Options.png'