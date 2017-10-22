import pygame
import pygame.gfxdraw
import config
import threading
import queue
import light_sim
import mathtools


class Simulation(threading.Thread):
    def __init__(self, queue, light_sources, interacting_objects, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.queue = queue
        self.light_sources = light_sources
        self.interacting_objects = interacting_objects

        self._stop_event = threading.Event()

    def run(self):
        for ray_points, wavelength in light_sim.simulate(self.light_sources, self.interacting_objects):
            self.queue.put((ray_points, wavelength))
            if self._stop_event.is_set():
                self.join()

    def stop(self):
        self._stop_event.set()


class AppWindow:
    def __init__(self):
        pygame.init()
        self.running=True

        self.clock = pygame.time.Clock()

        width, height = config.screen_dims
        self.dimension = pygame.Rect(0, 0, width, height)
        self.screen = pygame.display.set_mode((width, height))

        self.start_simulating(config.getLightSources(), config.getInteractingObjects())

        self.update()

    def redraw(self):
        self.screen.fill(color=pygame.Color(0,0,0))

    @property
    def is_simulating(self):
        return hasattr(self, 'simulation') and self.simulation is not None

    def start_simulating(self, light_sources, interacting_objects):
        if self.is_simulating:
            self.simulation.stop()

        self.queue = queue.Queue()
        self.simulation = Simulation(self.queue, light_sources, interacting_objects)
        self.simulation.run()
        self.redraw()

    def wavelength_to_rgb(self, wavelength):
        H = ((270 * (wavelength - 620)) / (-170))
        color = pygame.Color(0,0,0)
        color.hsva = (H, 100,100, 20)
        return color

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and pygame.key.get_pressed() == pygame.K_ESCAPE:
                self.running = False

    def truncate(self, ray):
        intercepts = list(filter(lambda x: x is not None, (mathtools.intersects(line, ray)
                                                           for line in mathtools.rect_lines(self.dimension))))
        intercepts.sort(key=lambda intercept: ray[0].distance_squared_to(intercept))
        if len(intercepts) == 0:
            return ray[0]
        return intercepts[0]

    def draw_new_rays(self):
        if self.is_simulating:
            try:
                for _ in range(config.max_frame_lines):
                    points, wavelength = self.queue.get_nowait()
                    drawingSurface = pygame.Surface((self.dimension.width, self.dimension.height))
                    colour = self.wavelength_to_rgb(wavelength)  # 460 to 620
                    for index in range(len(points) - 2):
                        p_x, p_y = map(int, points[index])
                        pnext_x, pnext_y = map(int, points[index + 1])
                        pygame.gfxdraw.line(drawingSurface, p_x, p_y, pnext_x, pnext_y, colour)
                    line_start, line_end = pygame.math.Vector2(points[-2]), pygame.math.Vector2(points[-1])
                    line_end = self.truncate(mathtools.line_to_ray((line_start, line_end)))
                    p_x, p_y = map(int, line_start)
                    pnext_x, pnext_y = map(int, line_end)
                    pygame.gfxdraw.line(drawingSurface, p_x, p_y, pnext_x, pnext_y, colour)

                    self.screen.blit(drawingSurface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                    pygame.display.flip()
            except queue.Empty:
                pass

    #def draw(self):
        # ds = pygame.Surface((self.dimension.width, self.dimension.height))

        #
        #
        # longLine=((0,0), (20000,20000))
        # pygame.draw.line(ds, (200,200,200), longLine[0], truncate(longLine[1]), 1)
        #
        # #pygame.draw.line(ds,(200,200,200), (0, 0), (20000, 20000), 1)
        #
        # circleLayer = pygame.Surface((width, height))
        # col = pygame.Color(200, 10, 40, 100)



    def update(self):
        while self.running:
            self.update_events()
            self.draw_new_rays()
            self.clock.tick(20)


if __name__ == "__main__":
    app = AppWindow()
