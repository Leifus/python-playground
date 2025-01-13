from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from classes.media_folder import MediaFolder
from classes.media_item import MediaItem
from config import pygame, os
from globals import media_manager


class MediaExplorer(GameSprite):
    def __init__(self, size, position):
        super(MediaExplorer, self).__init__()

        self.size = size
        self.position = position
        self.padding = 12
        self.is_active = False
        self.is_hovered = False
        self.hovered_button: Button = None
        self.media_listing = []
        self.allowed_image_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.webp']
        self.excluded_media_folders = ['/icons']
        self.media_folders = pygame.sprite.Group()
        self.folder_indent = 10
        self.folder_gap = 15
        self.selected_media_item: MediaItem = None

        self.add_button_image: pygame.Surface = None
        self.add_button: Button = None
        self.buttons_group = pygame.sprite.Group()
        self.button_size = (20, 20)

        self.relative_mouse_position = None
        self.show_media_buttons = False
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW

        self.add_selected_media = False

        self.create_default_surface()
        self.setup_visuals()
        self.setup_media_buttons()
        self.setup_media_listing()
        self.setup_media_items()
        self.redraw()

    def setup_visuals(self):
        # Housing
        color = pygame.Color('gray90')
        self.orig_image.fill(color)

        # Housing Edge
        color = pygame.Color('gray70')
        width = 2
        start_pos = (self.size[0]-width, 0)
        end_pos = (self.size[0]-width, self.size[1])
        pygame.draw.line(self.orig_image, color, start_pos, end_pos, width)

        # Button
        button_bg_color = pygame.Color('gray92')
        button_surface = pygame.Surface(self.button_size, pygame.SRCALPHA)
        button_surface.fill(button_bg_color)

        # Add Button
        image = media_manager.get('icons/add_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size[0]*icon_scale, self.button_size[1]*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size[0]/2, self.button_size[1]/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.add_button_image = button_image

    def on_event(self, event: pygame.event.Event):
        self.is_hovered = False
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW

        if not self.is_active:
            return

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            mouse_x, mouse_y = event.pos
            self.relative_mouse_position = pygame.Vector2(mouse_x - self.rect.left, mouse_y - self.rect.top)

            is_in_x = self.relative_mouse_position.x >=0 and self.relative_mouse_position.x <= self.rect.right
            is_in_y = self.relative_mouse_position.y >=0 and self.relative_mouse_position.y <= self.rect.bottom
            self.is_hovered = is_in_x and is_in_y

        if self.is_hovered:
            hovered_item = None
            self.hovered_button = None
            for folder in self.media_folders:
                folder: MediaFolder
                folder.on_event(self.relative_mouse_position, event)

                if folder.hovered_item:
                    hovered_item = folder.hovered_item

            # if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and hovered_item:
            self.selected_media_item = hovered_item

            if self.selected_media_item:
                for button in self.buttons_group:
                    button: Button
                    button.on_event(self.relative_mouse_position, event)
                    if button.is_hovered:
                        self.hovered_button = button

            if self.hovered_button:
                self.mouse_cursor = pygame.SYSTEM_CURSOR_HAND
            
            self.show_media_buttons = hovered_item is not None

        else:
            if self.selected_media_item:
                self.selected_media_item.is_hovered = False
                self.selected_media_item.redraw()
                self.selected_media_item = None
            self.show_media_buttons = False

    def redraw(self):
        # Housing
        self.image = pygame.transform.scale(self.orig_image, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, *args, **kwargs):
        if self.is_active:
            if self.selected_media_item:
                self.set_media_buttons_to_selected_item()

            self.buttons_group.update()

        return super().update(*args, **kwargs)
    
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        if self.is_active:
            self.surface.blit(self.image, (0,0))

            for folder in self.media_folders:
                folder: MediaFolder
                folder.draw(self.surface)

            if self.show_media_buttons:
                self.buttons_group.draw(self.surface)
        
        surface.blit(self.surface, self.rect)


    def on_add_media_button_press(self, button):
        self.add_selected_media = True

    def setup_media_buttons(self):
        # Add to Main Space Button
        x = self.rect.width - self.button_size[0]
        y = 10
        position = (x,y)
        value = 1,
        on_hover = None
        on_press = self.on_add_media_button_press
        on_release = None
        self.add_button = Button(self.add_button_image, position, value, on_hover, on_press, on_release, tooltip='Add media')
        self.buttons_group.add(self.add_button)

    def set_media_buttons_to_selected_item(self):
        self.show_media_buttons = True
        self.add_button.set_position((self.add_button.position[0], self.selected_media_item.rect.centery))

    def setup_media_items(self):
        x_pos = self.folder_indent
        y_pos = 40
        housing_width = self.rect.width-self.folder_indent
        line_gap = 5
        for folder, files in self.media_listing:
            folder: str
            media_folder = MediaFolder(folder, (x_pos, y_pos), housing_width)

            y_pos += media_folder.rect.height + line_gap
            x_pos_indent = folder.count('/') * self.folder_indent
            for file in files:
                media_item = MediaItem(folder, file, (x_pos + x_pos_indent, y_pos), housing_width - x_pos_indent)
                media_folder.media_items.add(media_item)
                y_pos += media_item.rect.height + line_gap

            self.media_folders.add(media_folder)
            y_pos += self.folder_gap

    def setup_media_listing(self):
        self.media_listing.clear()

        for root, subdirs, files in os.walk(media_manager.root_path):
            media_list = []
            relative_root = root.replace(media_manager.root_path, '')
            if relative_root == '':
                relative_root = '/'

            if relative_root in self.excluded_media_folders: # Deny listing of exluded folder
                continue

            # print('--\nroot = ' + relative_root)
            
            # for subdir in subdirs:
                # print('\t- /' + subdir)

            for filename in files:
                file_path = os.path.join(root, filename)
                splitext = os.path.splitext(file_path)
                
                if len(splitext) == 1:  # no file extension
                    continue
                
                extension = splitext[1]
                if extension not in self.allowed_image_formats: # not a recognised image format
                    # print('\t exclude: ', filename)
                    continue

                media_list.append(filename)

                # print('\t- ', filename)

            if len(media_list) > 0:
                media_list.sort()
                self.media_listing.append((relative_root, media_list))
