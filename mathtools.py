import pygame


def rect_lines(rect):
    vertices = [pygame.math.Vector2(vertex) for vertex in
                (rect.topleft, rect.topright, rect.bottomright, rect.bottomleft)]
    for index, point in enumerate(vertices):
        yield (point, vertices[(index+1) % 4])


def does_intersect(line, ray):
    line_start, line_end = line
    vector_along_line = line_end - line_start
    ray_start, ray_direction = ray
    cross = ray_direction.cross(vector_along_line)
    if cross == 0:
        return False
    diff = line_start - ray_start
    intersection_on_ray = diff.cross(vector_along_line) / cross
    intersection_on_line = diff.cross(ray_direction) / cross

    if intersection_on_ray > 0 and 0 < intersection_on_line < 1:
        return True
    return False


def intersects(line, ray):
    line_start, line_end = line
    vector_along_line = line_end-line_start
    ray_start, ray_direction = ray
    cross = ray_direction.cross(vector_along_line)
    if cross == 0:
        return None
    diff = line_start - ray_start
    intersection_on_ray = diff.cross(vector_along_line) / cross
    intersection_on_line = diff.cross(ray_direction) / cross

    if intersection_on_ray > 0 and 0 < intersection_on_line < 1:
        return line_start + intersection_on_line * vector_along_line


def line_to_ray(line):
    start_line, end_line = line
    return start_line, (end_line - start_line).normalize()
