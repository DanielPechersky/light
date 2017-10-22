

class LineSegmentSurface:
    def __init__(self, line):
        self.line = line
        self.normal = self.line.normalize().rotate(90)

    def get_intersection(self, ray):
        line_start = self.line[0]
        # vector along line
        ray_start, ray_direction = ray
        cross = self.vector_along_line.cross(ray_direction)
        if cross == 0:
            return None
        diff = line_start - ray_start
        intersection_on_line = diff.cross(ray_direction)
        intersection_on_ray = diff.cross(self.vector_along_line)

        if intersection_on_ray > 0 and 0 < intersection_on_line < 1:
            return ray_start + intersection_on_ray * ray_direction

    @property
    def vector_along_line(self):
        return self.line[1]-self.line[0]

    @property
    def ends(self):
        return self.line.copy()


class CircleSegmentSurface:
    def __init__(self, side, radius, concave):
        self.side = side
        self.radius = radius
        self.cut = side * 1 if concave else -1

        side_start, side_end = side
        chord_distance = (radius**2-(side_start.distance_squared_to(side_end)/4))**.5
        halfway = side_start.lerp(side_end)
        self.position = halfway + (side_end - halfway).rotate_ip(90).scale_to_length(chord_distance)

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
        intersections = [ray_start+intersection_on_line for intersection_on_line in
                         (-b+sqrt_disc/(2*a), -b-sqrt_disc/(2*a))
                         if intersection_on_line >= 0 and self.cut.cross(ray_start+intersection_on_line) >= 0]
        if list(intersections) == 0:
            return None
        intersections.sort(key=lambda intersect: ray[0].distance_squared_to(intersect))
        intersection = intersections[0]
        return intersection, self.get_normal(intersection)

    @property
    def ends(self):
        return self.side.copy()


class Lens:
    def __init__(self, surfaces):
        # Sides point clockwise to the next
        self.surfaces = surfaces

    def get_collision(self, ray, inside):
        intersects_and_normals = [(intersect, surface.get_normal(intersect)) for intersect, surface in
                                  filter(lambda x: x[0] is not None,
                                         (surface.get_intersection(ray), surface for surface in self.surfaces))]
        intersects_and_normals.sort(key=lambda intersect_and_normal: ray[0].distance_squared_to(intersect_and_normal[0]))
        """
        if inside and there is an even number of intercepts,
        get second because ray intersects something it already intersected
        Otherwise get first
        """
        return intersects_and_normals[(1-(len(intersects_and_normals) % 2))*inside],

