import materials
import pygame
import interacting_objects
import config

max_frame_lines = 20
max_interactions = 20
screen_dims = 1300, 700


class CustomMaterials(materials.Material):
    K_CROWN = ((1.1273555, 0.124412303, 0.827100531), (0.00720341707, 0.0269835916, 100.384588))


start = pygame.math.Vector2(500, 500)


def getLightSources():
    return [interacting_objects.PointSource(position=start, rays_per_color=500,

                                            wavelengths=[620, 555])]
def getInteractingObjects():
    sides = [pygame.math.Vector2(0, 0), pygame.math.Vector2(20, 0), pygame.math.Vector2(20, 20), pygame.math.Vector2(0, 20)]
    sides_offset = [side + start + pygame.math.Vector2(20, 0) for side in sides]
    sides_objects = [
        interacting_objects.CircleSegmentSurface((sides_offset[0], sides_offset[1]), 20, True),
        interacting_objects.LineSegmentSurface((sides_offset[1], sides_offset[2])),
        interacting_objects.CircleSegmentSurface((sides_offset[2], sides_offset[3]), 20, True),
        interacting_objects.LineSegmentSurface((sides_offset[3], sides_offset[0]))
    ]
    lens = interacting_objects.Lens(sides_objects, material=config.CustomMaterials.K_CROWN)
    return [lens]

