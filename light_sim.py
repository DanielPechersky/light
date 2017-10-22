import mathtools
import config


def simulate(light_sources, interacting_objects):
    for light_source in light_sources:
        yield simulate_ray(light_source.get_light_rays_by_color(), interacting_objects)


def simulate_ray(ray, interacting_objects):
    points = []
    wavelength = ray
    for object in interacting_objects:
        for line in object.bounding_box():
            if mathtools.does_intersect(line, ray):
                ray, inside = object.interact(ray=ray[0], wavelength=ray[1], inside=False)
                points.append(ray[0])
                if len(points) == config.max_interactions:
                    return points, wavelength
                while inside:
                    ray, inside = object.interact(ray=ray[0], wavelength=ray[1], inside=True)
                    points.append(ray[0])
                    if len(points) == config.max_interactions:
                        return points, wavelength

