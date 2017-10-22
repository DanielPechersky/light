import pygame
import pygame.gfxdraw
import config
import threading
import queue
import light_sim


class Simulation(threading.Thread):
    def __init__(self, queue, light_sources, interacting_objects, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.queue = queue
        self.light_sources = light_sources
        self.interacting_objects = interacting_objects

        self._stop_event = threading.Event()

    def run(self):
        for ray in light_sim.simulate(self.light_sources, self.interacting_objects):
            self.queue.put(ray)
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

    def redraw(self):
        self.screen.fill(color=pygame.Color(0,0,0))

    def start_simulating(self, light_sources, interacting_objects):
        if hasattr(self, 'simulation'):
            self.simulation.stop()

        self.queue = queue.Queue()
        self.simulation = Simulation(self.queue, light_sources, interacting_objects)
        self.simulation.run()
        self.redraw()

    def wavelength_to_rgb(wavelength):
        H = ((270 * (wavelength - 620)) / (-170))
        color = pygame.Color(0,0,0)
        color.hsva = (H, 100,100, 20)
        return color

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and pygame.key.get_pressed() == pygame.K_ESCAPE:
                running = False

    def drawNewRays(self):
        try:
            for _ in range(config.max_frame_lines):
                for points, wavelength in queue.Queue.get_nowait():
                    drawingSurface = pygame.Surface((self.dimension.width, self.dimension.height))
                    colour = (self.wavelength_to_rgb(wavelength))  # 460 to 620
                    for index in range(len(points) - 1):
                        p_x, p_y = points[index]
                        pnext_x, pnext_y = points[index + 1]
                        pygame.gfxdraw.line(drawingSurface, p_x, p_y, pnext_x, pnext_y, colour)

                    self.screen.blit(drawingSurface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        except queue.Empty():
            pass

    def draw(self):
        # ds = pygame.Surface((self.dimension.width, self.dimension.height))
        # def truncate(ray):
        #     intercepts = list(filter(lambda x: x is not None, (mathtools.intersects(line, ray) for line in rlines)))
        #     intercepts.sort(key=lambda intercept: ray[0].distance_squared_to(intercept))
        #     return intercepts[0]
        #
        #
        # longLine=((0,0), (20000,20000))
        # pygame.draw.line(ds, (200,200,200), longLine[0], truncate(longLine[1]), 1)
        #
        # #pygame.draw.line(ds,(200,200,200), (0, 0), (20000, 20000), 1)
        #
        # circleLayer = pygame.Surface((width, height))
        # col = pygame.Color(200, 10, 40, 100)

        pygame.display.flip()

    def update(self):
        while self.running:
            self.update_events()
            self.draw()
            self.clock.tick(20)

if __name__ == "__main__":
    app = AppWindow()
    app.start_simulating(config.getLightSources(), config.getInteractingObjects())
