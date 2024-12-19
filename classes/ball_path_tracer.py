# from pygame import Vector2
# from classes.pool_table import PoolTable
# from config import pygame, math
# from classes.draw_mode import DrawMode
# from classes.pool_ball import PoolBall

# # class PathTrace(pygame.sprite.Sprite):
# #     def __init__(self):
# #         pygame.sprite.Sprite.__init__(self)
    
# #         # self.surface = pygame.Surface(size, pygame.SRCALPHA)
# #         self.rect = None
# #         self.mask = None
# #         self.image = None

# #     def update(self, start_point, end_point):
# #         max_path_line = pygame.draw.aaline(self.image, 'black', start_point, end_point)
# #         self.mask = pygame.mask.from_surface(self.image)

# #     def draw(self, surface: pygame.Surface):
# #         self.surface.fill((255,0,0))

# #         msurf = self.mask.to_surface()
# #         self.surface.blit(msurf, (0, 0))
# #         # self.surface.blit(self.image, (0, 0))
        
# #         self.surface.blit(self.image, (0, 0))
        
# #         surface.blit(self.surface, (0, 0))


# class BallPathTracer():
#     def __init__(self, size, pool_table: PoolTable):
#         self.draw_mode = DrawMode.WIREFRAME
#         self.size = size
#         self.ball_origin = None
#         self.pool_table = pool_table
#         self.ball_origin_ring_radius = 18
#         self.ball_origin_ring_color = pygame.Color('black')
#         self.path_angle = 0
#         self.WIREFRAME_outline_width = 3

#         self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
#         self.rect = self.surface.get_rect()
#         self.ball_origin_ring_surface = pygame.Surface((self.ball_origin_ring_radius*2, self.ball_origin_ring_radius*2), pygame.SRCALPHA)
#         self.path_color = pygame.Color('white')
#         self.path_thickness = 3
#         # self.path_max_distance = 500
#         self.path_trace = PathTrace()
#         # self.orig_path_surface = pygame.Surface((100, self.path_thickness))#, pygame.SRCALPHA)
#         # self.path_surface = pygame.Surface((self.path_thickness, self.path_thickness))#, pygame.SRCALPHA)
#         self.setup_visuals()
#         self.mouse_position = None
#         self.mouse_distance = self.path_thickness
#         self.mouse_angle = 0
#         self.origin_ring_position = None
#         self.ball_position = None
#         self.path_line_end_point = None
#         self.path_line_start_point = None
#         self.final_path_line_end_point = None
#         self.final_path_line_start_point = None

#     def set_ball(self, ball: PoolBall):
#         self.ball_origin = ball

#     def setup_visuals(self):
#         if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
#             outline_width = 0
#             if self.draw_mode in DrawMode.WIREFRAME:
#                 outline_width = self.WIREFRAME_outline_width

#             center = (self.ball_origin_ring_radius, self.ball_origin_ring_radius)
#             pygame.draw.circle(self.ball_origin_ring_surface, self.ball_origin_ring_color, center, self.ball_origin_ring_radius, outline_width)

#     def on_event(self, event: pygame.event.Event):
#         if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
#             return
        
#         self.mouse_position = event.pos

#     def update(self):
#         if not self.ball_origin:
#             return
    
#         self.ball_position = (self.ball_origin.position[0] + self.pool_table.rect.left, self.ball_origin.position[1] + self.pool_table.rect.top)

#         # if self.mouse_position:
#         #     dx = self.mouse_position[0] - self.ball_position[0]
#         #     dy = self.mouse_position[1] - self.ball_position[1]
#         #     self.mouse_distance = math.sqrt(dx*dx + dy*dy)
#         #     self.mouse_angle = math.atan2(dy, dx)

#         self.origin_ring_position = (self.ball_position[0] - self.ball_origin_ring_radius, self.ball_position[1] - self.ball_origin_ring_radius)

#         max_length = self.size[0] # assuming the width is longer than the height
#         self.path_line_start_point = self.ball_origin.position
#         ending_x = self.path_line_start_point[0] + math.cos(self.mouse_angle) * max_length
#         ending_y = self.path_line_start_point[1] + math.sin(self.mouse_angle) * max_length
#         self.path_line_end_point = Vector2(ending_x, ending_y)
        
#         # clipped_line = None
#         # use_clipped_start_position = True

#         # how the feck is my line a sprite to check???
#         # its NOT!!!!!

#         # a sprite-surface we need YES?

#         start_point = (self.path_line_start_point[0] + self.pool_table.rect.left, self.path_line_start_point[1] + self.pool_table.rect.top)
#         end_point = (self.path_line_end_point[0] + self.pool_table.rect.left, self.path_line_end_point[1] + self.pool_table.rect.top)
#         self.path_trace.update(start_point, end_point)
#         # max_path_line = pygame.draw.aaline(self.path_surface, 'black', start_point, end_point)
        
#         mask_collide = pygame.sprite.spritecollide(self.path_trace, self.pool_table.balls, False, pygame.sprite.collide_mask)
#         if mask_collide:
#             print('mask_collide', mask_collide)
#         else:
#             print('NO COLLIDE')



#         # #check balls
#         # for ball in self.pool_table.balls:
#         #     if ball is self.ball_origin:
#         #         continue
            
#         #     clipped_line = ball.rect.clipline(self.path_line_start_point, self.path_line_end_point)
#         #     if clipped_line:
#         #         break

#         # #check cushions
#         # if not clipped_line:
#         #     for cushion in self.pool_table.cushions:
#         #         clipped_line = cushion.rect.clipline(self.path_line_start_point, self.path_line_end_point)
#         #         if clipped_line:
#         #             break

#         # #check pockets
#         # if not clipped_line:
#         #     for pocket in self.pool_table.pockets:
#         #         clipped_line = pocket.rect.clipline(self.path_line_start_point, self.path_line_end_point)
#         #         if clipped_line:
#         #             use_clipped_start_position = False
#         #             break

#         # if len(clipped_line) > 0:
#         #     start, end = clipped_line
#         #     x1, y1 = start
#         #     x2, y2 = end
#         #     self.final_path_line_end_point = start
#         #     if not use_clipped_start_position:
#         #         self.final_path_line_end_point = end
#         # else:
#         #     self.final_path_line_end_point = self.path_line_end_point
        
            
        
#         #NOPE!


#         # # Build up the line length up
#         # line_length_check = 10
#         # actual_length = 0
#         # collidepoint = False
#         # xx = math.ceil(max_length / line_length_check)
        
#         # # .normalize()
#         # for length_iter in range(xx):
#         #     actual_length += line_length_check
#         #     ending_x = self.ball_origin.position[0] + math.cos(self.mouse_angle) * actual_length
#         #     ending_y = self.ball_origin.position[1] + math.sin(self.mouse_angle) * actual_length
#         #     end_point = (ending_x, ending_y)

#         #     # Find collision points of touched objects
#         #     for ball in self.pool_table.balls:
#         #         if ball is self.ball_origin or ball.identifier != '9':
#         #             continue
                
#         #         # Check rect collision.
#         #         collidepoint = ball.rect.collidepoint(end_point)
#         #         print('ball collide', ball.identifier, collidepoint, ball.rect, end_point)
#         #         if collidepoint:
#         #             break
#         #         # if ball.identifier == '9':
#         #         #     print('ball collide', ball.identifier, collidepoint, ball.rect, end_point)

#         # ending_x = self.ball_position[0] + math.cos(self.mouse_angle) * actual_length
#         # ending_y = self.ball_position[1] + math.sin(self.mouse_angle) * actual_length
#         # end_point = (ending_x, ending_y)

#         # self.path_line_endpoint = end_point

#     def draw(self, surface: pygame.Surface):
#         self.surface.fill((0,0,0,0))

#         self.surface.blit(self.ball_origin_ring_surface, self.origin_ring_position)

#         self.path_trace.draw(self.surface)

#         # start_point = (self.path_line_start_point[0] + self.pool_table.rect.left, self.path_line_start_point[1] + self.pool_table.rect.top)
#         # end_point = (self.path_line_end_point[0] + self.pool_table.rect.left, self.path_line_end_point[1] + self.pool_table.rect.top)
#         # max_path_line = pygame.draw.aaline(self.surface, 'black', start_point, end_point)
        
#         # end_point = (self.final_path_line_end_point[0] + self.pool_table.rect.left, self.final_path_line_end_point[1] + self.pool_table.rect.top)
#         # true_path_line = pygame.draw.line(self.surface, self.path_color, start_point, end_point, 3)
        


#         surface.blit(self.surface, self.rect)
        
    