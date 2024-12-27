from config import pygame

def draw_poly_points_around_rect(surface, rect: pygame.Rect, color, radius, offset=(0,0)):
    points = [
        (offset[0] + radius/2, offset[1] + radius/2),
        (offset[0] + rect.width - radius/2, offset[1] + radius/2),
        (offset[0] + rect.width - radius/2, offset[1] + rect.height - radius/2),
        (offset[0] + radius/2, offset[1] + rect.height - radius/2)
    ]
    draw_poly_points(surface, points, color, radius)

def draw_poly_points(surface, points, color, radius):
    for point in points:
        pygame.draw.circle(surface, color, point, radius)


def aspect_scale(img, size):
    bx = size[0]
    by = size[1]
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (sx,sy))

def scale_poly_points(scale, poly_points):
    sized_poly_points = []
    for point in poly_points:
        resized = (point[0] * scale[0], point[1] * scale[1])
        sized_poly_points.append(resized)

    return sized_poly_points
