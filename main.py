#Import modules
import pygame
import sprite_sheet
pygame.init()

#Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat Get Cake")


#Import Background
bg_image = pygame.image.load('resources/bg.png')


#Import image (sprite sheet) 
cat = pygame.image.load('resources/cat.png').convert_alpha()
sprite_sheet = sprite_sheet.SpriteSheet(cat)
cat_x = 1
cat_y = 1

move_right = False
move_left = False
move_down = False
move_up = False

#Color variables
# BG = (50, 50, 50)
BLACK = (0, 0, 0)

#Animation list for images
animation_list = []
animation_steps = [3, 3, 3, 3, 1]
action = 4
#Timer -> draw next image to create animation
last_update = pygame.time.get_ticks()
animation_cooldown = 250
frame = 0 #Animation start
step_counter = 0

#Image in frame function -> Loop through them 3 times (pull image from step counter)
#Temp list part of master list -> Image will change based on action (user input taken)
for animation in animation_steps:
    temp_image_list = []
    for _ in range (animation):
        temp_image_list.append(sprite_sheet.get_image(step_counter, 32, 32, 3, BLACK)) #Extract image in frame and append to animation list
        step_counter += 1
    animation_list.append(temp_image_list)

#Infinite loop
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Update background
    # screen.fill(BG)
    screen.blit(bg_image, (0, 0))

    #Update animation -> current time / check which image is in animation
    current_time = pygame.time.get_ticks()
    #Compare to last update
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        #Reset animation after it ran through last frame
        if frame >= len(animation_list[action]):
            frame = 0

    #Event Handler
    for event in pygame.event.get():
        #Key is pressed down for movement
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RIGHT):
                move_right = True
                action = 0
                frame = 0
            if(event.key == pygame.K_LEFT):
                move_left = True
                action = 3
                frame = 0
            if(event.key == pygame.K_DOWN):
                move_down = True
                action = 2
                frame = 0
            if(event.key == pygame.K_UP):
                move_up = True
                action = 1
                frame = 0
        elif(event.type == pygame.KEYUP):
            if(event.key == pygame.K_RIGHT):
                move_right = False
                action = 4
                frame = 0
            if(event.key == pygame.K_LEFT):
                move_left = False
                action = 4
                frame = 0
            if(event.key == pygame.K_DOWN):
                move_down = False
                action = 4
                frame = 0
            if(event.key == pygame.K_UP):
                move_up = False
                action = 4
                frame = 0

    if(move_right == True):
        cat_x += 0.09
    if(move_left == True):
        cat_x -= 0.09
    if(move_up == True):
        cat_y -= 0.09
    if(move_down == True):
        cat_y += 0.09

    #Display frame image
    #screen.blit(cat_obj, (Cat.x, Cat.y))
    screen.blit(animation_list[action][frame], (cat_x, cat_y))

    pygame.display.update()
pygame.quit()