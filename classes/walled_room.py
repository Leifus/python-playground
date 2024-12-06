from config import pymunk, app_cfg

class WalledRoom:
    def __init__(self, space, display_size, radius=4):
        self.radius = radius
        x0, y0 = (0, 0)
        x1, y1 = display_size
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(space.static_body, pts[i], pts[(i+1) % 4], radius)
            segment.elasticity = app_cfg.wall_elasticity
            segment.friction = app_cfg.wall_friction
            space.add(segment)