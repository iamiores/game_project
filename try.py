import pygame
pygame.init()

W, H = 800, 600

window = pygame.display.set_mode((W, H))

background_image = pygame.image.load('bg.jpg')
background_rect = background_image.get_rect()

font = pygame.font.Font(None, 20)

background_x = 0
background_y = 0

speed = 7
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if keys[pygame.K_LEFT]:
        background_x += speed
    if keys[pygame.K_RIGHT]:
        background_x -= speed
    if keys[pygame.K_UP]:
        background_y += speed
    if keys[pygame.K_DOWN]:
        background_y -= speed

    text = font.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, pygame.color.Color('white'))
    #window
    window.fill((0, 0, 0))

    window.blit(background_image, (background_x, background_y))
    window.blit(text, (10, 10))
    pygame.display.update()
    clock.tick(30)
