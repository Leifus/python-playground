from classes.draw_mode_enum import DrawModeEnum
from classes.game_space_config import GameSpaceConfig
from classes.game_tables.game_table import GameTable
from config import pool_table_config, pygame
from globals import media_manager

class SnookerGameTable(GameTable):
    def __init__(self, size, position, space_config: GameSpaceConfig, draw_mode: DrawModeEnum):
        super(SnookerGameTable, self).__init__(size=size, position=position, space_config=space_config, draw_mode=draw_mode)
        
        self.rich_media_path = pool_table_config.pool_table_DM_RICH_media
        
        self.setup_visuals()
        self.redraw()

    def setup_visuals(self):
        # Table
        self.orig_image = media_manager.get(self.rich_media_path, convert_alpha=True)
        if not self.orig_image:
            print('SnookerGameTable: No table img', self.rich_media_path)
            return
        