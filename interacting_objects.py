import pygame
import functools
import math
import numpy as np
import mathtools


class LineSegmentSurface:
    def __init__(self, line):
        self.line = line
        self.normal = self.line[0].normalize().rotate(90)

        line_start, line_end = line
        self.bounding_box = pygame.Rect(line_start, line_end-line_start)
        self.bounding_box.normalize()

    def get_intersection(self, ray):
        intersect = mathtools.intersects(self.line, ray)
        if intersect is not None:
            return intersect, self.normal

    @property
    def vector_along_line(self):
        return self.line[1]-self.line[0]

    @property
    def ends(self):
        return self.line.copy()


class CircleSegmentSurface:
    def __init__(self, side, radius, concave):
        self.side = tuple(pygame.math.Vector2(p) for p in side)
        self.radius = radius
        self.cut = tuple(pygame.math.Vector2(v) for v in self.side)
        if not concave:
            self.cut[0], self.cut[1] = self.cut[1], self.cut[0]

        side_start, side_end = self.side
        chord_distance = (radius**2-(side_start.distance_squared_to(side_end)/4))**.5
        halfway = side_start.lerp(side_end, .5)
        self.position = halfway + (side_end - halfway).rotate(90)
        self.position.scale_to_length(chord_distance)

        self.bounding_box = pygame.Rect(self.position-pygame.math.Vector2((radius/2,)*2), (radius,)*2)

    def get_normal(self, point):
        return point - self.position

    def get_intersection(self, ray):
        ray_start, ray_direction = ray
        a = ray_direction * ray_direction
        b = 2 * ray_direction * (ray_start-self.position)
        c = ray_start * ray_start + self.position * self.position - 2 * ray_start * self.position - self.radius**2
        disc = b**2 - 4 * a * c
        if disc < 0:
            return None
        sqrt_disc = disc ** .5
        intersections = [ray_start+intersection_on_line*ray_direction for intersection_on_line in
                         (-b+sqrt_disc/(2*a), -b-sqrt_disc/(2*a))
                         if intersection_on_line >= 0 and
                         self.vector_along_cut.angle_to(ray_start+intersection_on_line*ray_direction-self.cut[0]) >= 0]
        if len(intersections) == 0:
            return None
        intersections.sort(key=lambda intersect: ray[0].distance_squared_to(intersect))
        intersection = intersections[0]
        return intersection, self.get_normal(intersection)

    @property
    def vector_along_cut(self):
        return self.cut[1] - self.cut[0]

    @property
    def ends(self):
        return [pygame.math.Vector2(v) for v in self.side]


class Lens:
    def __init__(self, surfaces, material):
        # Sides point clockwise to the next
        self.surfaces = surfaces
        self.material = material

        self.bounding_box = functools.reduce(
            lambda rect1, rect2: rect1.union(rect2),
            map(lambda surface: surface.bounding_box, surfaces))

    def get_collision(self, ray, inside):
        intersects_and_normals = list(filter(lambda x: x is not None,
                                        (surface.get_intersection(ray) for surface in self.surfaces)))
        if len(intersects_and_normals) == 0:
            return None
        intersects_and_normals.sort(key=lambda intersect_and_normal: ray[0].distance_squared_to(intersect_and_normal[0]))
        """
        if inside and there is an even number of intercepts,
        get second because ray intersects something it already intersected
        Otherwise get first
        """
        return intersects_and_normals[(1-(len(intersects_and_normals) % 2))*inside]

    def interact(self, ray, wavelength, inside):
        n1 = 1
        n2 = self.material.n(wavelength)
        if inside:
            n1, n2 = n2, n1

        collision = self.get_collision(ray, inside)
        if collision is None:
            return None
        intersection, normal = collision
        _ray_start, ray_direction = ray
        result = (intersection, pygame.math.Vector2(1, 0).rotate(math.asin(math.sin(ray_direction.as_polar()[1])*n1/n2)))
        # if result[1] > 1 ray is still inside
        return result, result[1].as_polar()[1] > 1


class PointSource:
    def __init__(self, position, rays_per_color, wavelengths, start_angle=0, end_angle=360):
        self.position = position
        self.rays_per_color = rays_per_color
        self.wavelengths = wavelengths
        self.start_angle = start_angle
        self.end_angle = end_angle

    @property
    def angle_of_view(self):
        return self.end_angle - self.start_angle

    @property
    def _step_angle(self):
        return self.angle_of_view/self.rays_per_color

    def get_light_rays_by_color(self):
        for wavelength in self.wavelengths:
            for angle in np.arange(self.start_angle, self.end_angle, self._step_angle):
                yield (pygame.math.Vector2(self.position), pygame.math.Vector2(1, 0).rotate(angle)), wavelength

    def get_light_rays_by_angle(self):
        for angle in np.arange(self.start_angle, self.end_angle, self._step_angle):
            for wavelength in self.wavelengths:
                yield (pygame.math.Vector2(self.position), pygame.math.Vector2(1, 0).rotate(angle)), wavelength


