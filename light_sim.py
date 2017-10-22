import mathtools
import config


out_of_frame_distance = 1000


def simulate(light_sources, interacting_objects):
    for light_source in light_sources:
        for ray, wavelength in light_source.get_light_rays_by_color():
            yield simulate_ray(ray, wavelength, interacting_objects), wavelength


def simulate_ray(ray, wavelength, interacting_objects):
    points = [ray[0]]
    for object in interacting_objects:
        for line in mathtools.rect_lines(object.bounding_box):
            if mathtools.does_intersect(line, ray):
                results = object.interact(ray=ray, wavelength=wavelength, inside=False)
                if results is not None:
                    ray, inside = results
                    points.append(ray[0])
                    if len(points) == config.max_interactions:
                        return points
                    while inside:
                        results = object.interact(ray=ray, wavelength=wavelength, inside=False)
                        if results is not None:
                            ray, inside = results
                            points.append(ray[0])
                            if len(points) == config.max_interactions:
                                return points
            else:
                points.append(ray[0]+(ray[1]-ray[0])*out_of_frame_distance)
                return points
