import pygame
import pygame.gfxdraw
import config
import threading
import queue
pygame.init()

class AppWindow:
    pass
running=True

(width, height)=(1366,768)
screen=pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
timer = pygame.time.Clock()

def wavelength_to_rgb(wavelength):
    H = ((270 * (wavelength - 620)) / (-170))
    color = pygame.Color(0,0,0)
    color.hsva = (H, 100,100, 20)
    return color

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and pygame.key.get_pressed() == pygame.K_ESCAPE:
            running = False


    circleLayer = pygame.Surface((width, height))
    col = pygame.Color(200, 10, 40, 255)


    #b = mouse.get_pressed()

    if event.type == pygame.MOUSEBUTTONDOWN:
        timer.tick()
        x, y = pygame.mouse.get_pos()
        pygame.gfxdraw.filled_circle(circleLayer,int(x), int(y), int(timer.get_time()/2), col)
        pygame.display.update()
    screen.blit(circleLayer, (0, 0))

    try:
        for _ in range(config.max_frame_lines):
            pass
            """
            #THREAD here
            drawingSurface = pygame.Surface((width, height))
            wavelength, points=queue.pop()
            colour=(wavelength_to_rgb(460)) #460 to 620
            for index, point in enumerate(points):
                if index == len(points):
                    pass
                else:
                    p_x, p_y = point
                    pnext_x, pnext_y = points[index+1]
                    pygame.gfxdraw.line(drawingSurface, p_x, p_y, pnext_x, pnext_y)
                    
            screen.blit(myNewSurface1, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
            """

    except queue.Empty:
        pass




    pygame.display.flip()
