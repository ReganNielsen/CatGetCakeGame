import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

    #Use Sprite Sheet
    #Select Image based off w/h on sheet ->
    #Allocate frame -> 
    #Position (blit on screen) -> 
    #Scale -> Background of sprite = transparent
    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= 3
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += 3
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= 3
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += 3
            self.facing = 'down'
        
