#Import modules
import pygame
import random

# Initialize Pygame
pygame.init()

#Set up the screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat Protect Cake")

#Background
bgi = pygame.image.load("background.png").convert()

#Sound import // function // collision & game over
pygame.mixer.init()
munch = pygame.mixer.Sound("assets/munch.mp3")
gameover = pygame.mixer.Sound("assets/gameover.mp3")

#Defined colors
BLACK = (0, 0, 0)

#Cat class for player
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Import sprite for each animation // Scale each sprite
        self.cat_down = [pygame.transform.scale(pygame.image.load("resources/cat_down1.png"), (80, 80)),
                         pygame.transform.scale(pygame.image.load("resources/cat_down2.png"), (80, 80)),
                         pygame.transform.scale(pygame.image.load("resources/cat_down3.png"), (80, 80))]
        self.cat_up = [pygame.transform.scale(pygame.image.load("resources/cat_up1.png"), (80, 80)),
                       pygame.transform.scale(pygame.image.load("resources/cat_up2.png"), (80, 80)),
                       pygame.transform.scale(pygame.image.load("resources/cat_up3.png"), (80, 80))]
        self.cat_left = [pygame.transform.scale(pygame.image.load("resources/cat_left1.png"), (80, 80)),
                         pygame.transform.scale(pygame.image.load("resources/cat_left2.png"), (80, 80)),
                         pygame.transform.scale(pygame.image.load("resources/cat_left3.png"), (80, 80))]
        self.cat_right = [pygame.transform.scale(pygame.image.load("resources/cat_r1.png"), (80, 80)),
                          pygame.transform.scale(pygame.image.load("resources/cat_r2.png"), (80, 80)),
                          pygame.transform.scale(pygame.image.load("resources/cat_r3.png"), (80, 80))]
        self.image = self.cat_down[0]  #Set Idle Image
        self.rect = self.image.get_rect() #Cat sprite placed on rect
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) #Cat Position
        self.animation_index = 0  #Track current frame // Stored in index
        self.direction = 'down'   #Starting Direction

    #Update animation function for user key input -> movement animation
    def update(self, cat_x=0, cat_y=0):
        if cat_x != 0 or cat_y != 0:
            if cat_x > 0:
                self.direction = 'right'
                self.image = self.cat_right[self.animation_index]
            elif cat_x < 0:
                self.direction = 'left'
                self.image = self.cat_left[self.animation_index]
            elif cat_y > 0:
                self.direction = 'down'
                self.image = self.cat_down[self.animation_index]
            elif cat_y < 0:
                self.direction = 'up'
                self.image = self.cat_up[self.animation_index]

            #Update animation index to loop through frames
            self.animation_index = (self.animation_index + 1) % len(self.cat_down)

        self.rect.x += cat_x
        self.rect.y += cat_y

#Rat class for rat object moving around screen
class Rat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rat = pygame.image.load("resources/rat.png").convert_alpha()  #Load the sprite image
        self.image = pygame.transform.scale(self.rat, (35,45))  #Scale image
        self.rect = self.image.get_rect()
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])
        self.spawn_away_from_bomb()

    #Rat object cant spawn near bomb rect area
    def spawn_away_from_bomb(self):
        bomb_rect = pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50), (100, 100))
        while True:
            self.rect.center = (random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100))
            if not bomb_rect.colliderect(self.rect):
                break

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

#Bomb class -> place in middle
class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cake = pygame.image.load("resources/cake.png").convert_alpha()
        self.image = pygame.transform.scale(self.cake, (35, 35)) 
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main game loop
clock = pygame.time.Clock()
running = True
cat = Cat()
rat = Rat()  #Create the first Rat object
rat2 = Rat()  #Create the second Rat object
bomb = Bomb()
all_sprites = pygame.sprite.Group(cat, rat, rat2, bomb)  #Add both Rats to the sprite group
score = 0

# Font for the score display
font = pygame.font.Font(None, 36)

# Main loop for running the game
running = True
while running:
    #Reset game variables
    cat.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    rat.spawn_away_from_bomb()
    rat2.spawn_away_from_bomb()
    inner_running = True

    #Inner game loop --> Keep running game will window is not closed by user
    while inner_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inner_running = False
                running = False  #Ensure the outer loop also breaks

        #Arrow keys as user input
        keys = pygame.key.get_pressed()
        cat_x = 0
        cat_y = 0
        if keys[pygame.K_LEFT]:
            cat_x = -5
        if keys[pygame.K_RIGHT]:
            cat_x = 5
        if keys[pygame.K_UP]:
            cat_y = -5
        if keys[pygame.K_DOWN]:
            cat_y = 5

        cat.update(cat_x, cat_y)

        #Check collisions
        if pygame.sprite.collide_rect(rat, cat):
            score += 1
            rat.spawn_away_from_bomb()  #Respawn the first Rat away from the bomb
            munch.play() #Play sound if rat is eatten
        if pygame.sprite.collide_rect(rat2, cat):
            score += 1
            rat2.spawn_away_from_bomb()  #Respawn the second Rat away from the bomb
            munch.play() #Play sound if rat is eatten
        if pygame.sprite.collide_rect(rat, bomb) or pygame.sprite.collide_rect(rat2, bomb):
            inner_running = False
            gameover.play() #Play sound if rat touched the cake

        #Update sprites
        all_sprites.update()

        #Clear the screen
        screen.blit(bgi, (0, 0))

        #Draw sprites
        all_sprites.draw(screen)

        #Render, update and display score
        score_text = font.render("Score: " + str(score), True, BLACK)
        score_rect = score_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        screen.blit(score_text, score_rect)

        pygame.display.flip()
        clock.tick(60)

    #Game over screen
    game_over_text = font.render("Game Over!", True, BLACK)
    game_over_rect = game_over_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))  # Position at the center top
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

    #Wait for a few seconds before starting a new game
    pygame.time.wait(3000)

#Close game when the outer loop ended by user
pygame.quit()