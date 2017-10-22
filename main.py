import pygame
import pygame.gfxdraw
import config
import threading
from queue import Queue
import light_sim
pygame.init()


class Simulator(threading.Thread):
    def __init__(self, queue, light_sources, interacting_objects, *args, **kwargs):
        threading.Thread.__init__(*args, **kwargs)
        self.queue: Queue = queue
        self.light_sources = light_sources
        self.interacting_objects = interacting_objects

    def run(self):
        for ray in light_sim.simulate(self.light_sources, self.interacting_objects)
            self.queue.put(ray)

class AppWindow:
    pass
running=True

(width, height)=(1366,768)
#screen=pygame.display.set_mode((width, height), pygame.FULLSCREEN)
screen=pygame.display.set_mode((width, height))
clock = pygame.time.Clock()



def wavelength_to_rgb(wavelength):
    H = ((270 * (wavelength - 620)) / (-170))
    color = pygame.Color(0,0,0)
    color.hsva = (H, 100,100, 20)
    return color



while running:

    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and pygame.key.get_pressed() == pygame.K_ESCAPE:
            running = False

    rlines = mathtools.rect_lines(pygame.Rect(0, 0, width, height))

    ds = pygame.Surface((width, height))
    def truncate(ray):
        intercepts = list(filter(lambda x: x is not None, (mathtools.intersects(line, ray) for line in rlines)))
        intercepts.sort(key=lambda intercept: ray[0].distance_squared_to(intercept))
        return intercepts[0]


    longLine=((0,0), (20000,20000))
    pygame.draw.line(ds, (200,200,200), longLine[0], truncate(longLine[1]), 1)

    #pygame.draw.line(ds,(200,200,200), (0, 0), (20000, 20000), 1)

    circleLayer = pygame.Surface((width, height))
    col = pygame.Color(200, 10, 40, 100)


    """if event.type == pygame.MOUSEBUTTONDOWN and event.type!=pygame.MOUSEMOTION:
        x, y = pygame.mouse.get_pos()
        drag=True
        pygame.gfxdraw.filled_circle(circleLayer,int(x), int(y), 20, col)
        #pygame.gfxdraw.filled_trigon(circleLayer, int(x), int(y), 20, col)
        pygame.display.update()
        screen.blit(circleLayer, (0, 0), special_flags=pygame.BLEND_MAX)

    if event.type == pygame.MOUSEBUTTONUP:
        drag=False

        #pygame.gfxdraw.filled_circle(circleLayer,int(x), int(y), int(timer.get_time()/2), col)

        # THREAD here"""

    for points,wavelength in test2.test():
        drawingSurface = pygame.Surface((width, height))
        colour = (wavelength_to_rgb(wavelength))  # 460 to 620
        points = [(min(max(int(x),0),width), min(max(int(y),0),height)) for x, y in points]
        for index in range(len(points)-1):
            p_x, p_y = points[index]
            pnext_x, pnext_y = points[index + 1]
            pygame.gfxdraw.line(drawingSurface, p_x, p_y, pnext_x, pnext_y, colour)

        screen.blit(drawingSurface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    pygame.display.flip()
#timer.set_timer(0)
try:
    for _ in range(config.max_frame_lines):
        pass
    """
            #THREAD here
    try:
        for _ in range(config.max_frame_lines):
            drawingSurface = pygame.Surface((width, height))
            points, wavelength = queue.pop()
            colour = wavelength_to_rgb(460) #460 to 620
            # for index, point in enumerate(points):
            #     p_x, p_y = point
            #     pnext_x, pnext_y = points[index+1]
            #     pygame.gfxdraw.line(drawingSurface, p_x, p_y, pnext_x, pnext_y)
            # screen.blit(myNewSurface1, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

except queue.Empty:
    pass





