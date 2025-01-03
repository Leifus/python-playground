from classes.actor.cow_actor import CowActor
from classes.configs.game_mode_config import GameModeConfig
from classes.configs.game_space_config import GameSpaceConfig
from classes.common.game_sprite import GameSprite
from classes.configs.game_time_config import GameTimeConfig
from classes.enums.game_mode_enum import GameModeEnum
from classes.food_source import FoodSource
from classes.water_source import WaterSource
from config import pymunk, pygame, random
from globals import media_manager


#TODO: Make and Use a PhysicalGameSprite (with base space params and methods)
class Sandbox(GameSprite):
    def __init__(self, size, position):
        super(Sandbox, self).__init__()

        self.size = size
        self.position = position
        self.space: pymunk.Space = None
        space_config: GameSpaceConfig = GameSpaceConfig(1.0 / 60, 1, 10, (0, 0), 0.23, 0.5)
        time_config: GameTimeConfig = GameTimeConfig(60)
        self.game_config = GameModeConfig(GameModeEnum.Default, time_config, space_config)
        self.actors_group = pygame.sprite.Group()
        self.sources_groups = pygame.sprite.Group()
        self.mouse_position: pygame.Vector2 = None
        self.cow: CowActor = None
        self.clock = pygame.time.Clock()
        self.time_lapsed = 0

        self.create_default_surface()
        self.create_visuals()
        self.create_physical_space()
        self.redraw()

    def create_visuals(self):
        # Temp Background
        media = 'terrain_tiles/DirtTile.png'
        self.orig_image = media_manager.get(media, convert=True)

    def redraw(self):
        self.image = pygame.transform.scale(self.orig_image, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)
        
    def on_event(self, event: pygame.event.Event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            mouse_x, mouse_y = event.pos
            self.mouse_position = pygame.Vector2(mouse_x-self.rect.left, mouse_y-self.rect.top)
            # print('mouse', (mouse_x, mouse_y), self.mouse_position)

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     buttons_pressed = pygame.mouse.get_pressed()
        #     if buttons_pressed[0]:
        #         self.cow.move_to_new_position(self.mouse_position)



    def create_physical_space(self):
        space = pymunk.Space()
        space_config = self.game_config.space_config
        space.iterations = space_config.iterations
        space.gravity = space_config.gravity
        space.damping = space_config.damping
        space.sleep_time_threshold = space_config.sleep_time_threshold
        self.space = space

    def add_food_sources(self):
        food_source_count = 20
        size = (50, 40)

        food_source_bodies = []
        food_source_shapes = []
        for i in range(food_source_count):
            rand_x = random.randint(size[0]/2, self.rect.width-size[0]/2)
            rand_y = random.randint(size[1]/2, self.rect.height-size[1]/2)
            position = (rand_x, rand_y)
            food_source = FoodSource(size, position)
            food_source_bodies.append(food_source.body)
            food_source_shapes.append(food_source.shape)
            self.sources_groups.add(food_source)
            food_source.is_active = True

        self.space.add(*food_source_bodies, *food_source_shapes)

    def add_water_source(self):
        vectors = [
            (-90, 57), 
            (11, 72), 
            (108, -40), 
            (-37, -71)
        ]
        position = (400, 400)
        size = (200, 200)
        water_source = WaterSource(size, position, vectors)
        water_source.is_active = True
        self.space.add(water_source.body, water_source.shape)
        self.sources_groups.add(water_source)

        
    def add_cow_actor(self):
        cow = CowActor(birth_date=self.time_lapsed)

        rand_x = random.randint(cow.rect.width/2, self.rect.width - cow.rect.width/2)
        rand_y = random.randint(cow.rect.height/2, self.rect.height - cow.rect.height/2)
        cow.update_position((rand_x, rand_y))

        rand_angle = random.randint(0, 360)
        cow.update_angle(degrees=rand_angle)

        self.space.add(cow.body, cow.shape)
        cow.is_active = True
        self.actors_group.add(cow)
        self.cow = cow

        # self.cow.test_steering_behaviour_set_initial_velocity()

    def update(self, *args, **kwargs):
        self.time_lapsed = pygame.time.get_ticks()
        self.clock.tick(self.game_config.time_config.fps)

        for _ in range(self.game_config.space_config.dt_steps):
            self.space.step(self.game_config.space_config.dt / self.game_config.space_config.dt_steps)
        
        self.sources_groups.update(self.time_lapsed)
        self.actors_group.update(self.time_lapsed, self.mouse_position)

        return super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        
        self.surface.blit(self.image, (0,0))
        self.sources_groups.draw(self.surface)
        # self.actors_group.draw(self.surface)

        for actor in self.actors_group:
            actor: CowActor
            actor.draw(self.surface)

        #     if actor.destination_position is None:
        #         continue

        #     #Draw line towards destination point
        #     color = pygame.Color('blue')
        #     pygame.draw.line(self.surface, color, actor.position, actor.destination_position)

        #     #Draw destination point
        #     pygame.draw.circle(self.surface, color, actor.destination_position, 5, 1)

        # self.space.debug_draw(pymunk.pygame_util.DrawOptions(self.surface))

        surface.blit(self.surface, self.rect)
        