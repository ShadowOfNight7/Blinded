import math, time, os, random, statistics, pygame

pygame.init()
screen_scale = 1
screen_x, screen_y = 1280 * screen_scale, 720 * screen_scale
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

FPS = 60

running = True

while running:
    screen.fill("black")
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
                    break
    
    pygame.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), 20)


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()