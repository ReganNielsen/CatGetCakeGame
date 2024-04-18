import pygame
from random import randint

screen_height = 500
screen_width = 400

screen = pygame.display.set_mode((screen_height, screen_width))

#Background -->

background_image = pygame.image.load("resources/background.png")
background_rec = background_image.get_rect(center = [screen_width//2,screen_height//2])

background_x = 0
background_y = 0

#Cat Sprite -->

cat_right = [pygame.image.load("resources/cat_r1.png"),
             pygame.image.load("resources/cat_r2.png"),
             pygame.image.load("resources/cat_r3.png")]
cat_left = [pygame.image.load("resources/cat_left1.png"),
             pygame.image.load("resources/cat_left2.png"),
             pygame.image.load("resources/cat_left3.png")]
cat_up = [pygame.image.load("resources/cat_up1.png"),
             pygame.image.load("resources/cat_up2.png"),
             pygame.image.load("resources/cat_up3.png")]
cat_down = [pygame.image.load("resources/cat_down1.png"),
             pygame.image.load("resources/cat_down2.png"),
             pygame.image.load("resources/cat_down3.png")]

cur_direction = "down"
cur_cat = cat_down

cat_rect = cat_right[0].get_rect()

cat_rect.x = 218
cat_rect.y = 168

#Movement Values -->

speed = 1

frame_rate = 10

current_frame = 0

clock = pygame.time.Clock()

#Cake Sprite -->

point_image = pygame.image.load("resources/cake.png")

point_rect = point_image.get_rect()

x_point_rect = 100
y_point_rect = 100

#Main loop -->

running = True
while running:
    for event in pygame.event.get(): #Quit
        if event.type == pygame.QUIT:
            running = False

    #Collision with cake -->
    if point_rect.colliderect(cat_rect):
        print("Yippie")

    keys = pygame.key.get_pressed() #Keyboard input movements for cat
    if keys[pygame.K_UP]:
        cur_direction = "up"
        cur_cat = cat_up
        current_frame += 0.2
        cat_rect.y -= speed
    if keys[pygame.K_DOWN]:
        cur_direction = "down"
        cur_cat = cat_down
        current_frame += 0.2
        cat_rect.y += speed
    if keys[pygame.K_LEFT]:
        cur_direction = "left"
        cur_cat = cat_left
        current_frame += 0.2
        cat_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        cur_direction = "right"
        cur_cat = cat_right
        current_frame += 0.2
        cat_rect.x += speed

    screen.fill((0, 0, 0))

    if current_frame >= len(cur_cat): #Animation reset 
        current_frame = 0
    if current_frame == 4:
        current_frame = 0

    #Screen settings/blits

    screen.blit(background_image, [background_x, background_y])

    pygame.draw.rect(screen, (0, 0, 0), cat_rect)
    pygame.draw.rect(screen, (0, 0, 0), point_rect)

    screen.blit(point_image, [x_point_rect, y_point_rect])
    screen.blit(cur_cat[int(current_frame)], cat_rect)

    pygame.display.flip()
    clock.tick(60)