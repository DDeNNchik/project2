import pygame
from map1 import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()


wind_w, wind_h = 1400, 1000
window = pygame.display.set_mode((wind_w, wind_h))
pygame.display.set_caption("test")

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        window.blit(self.image, (self.rect.x-camera.rect.x, self.rect.y))

player_images_stand = [pygame.image.load(f"img/adventBoy_stand{i}.png") for i in range(1, 3)]
player_images_stand = [pygame.transform.scale(img, (100, 100)) for img in player_images_stand]  # Scale images

class Player(Sprite):
    def __init__(self, x, y, w, h, images_right, images_jump, images_stand, speed):
        super().__init__(x, y, w, h, images_right[0])
        self.images_right = images_right
        self.images_left = [pygame.transform.flip(img, True, False) for img in images_right]
        self.images_jump_right = images_jump
        self.images_jump_left = [pygame.transform.flip(img, True, False) for img in images_jump]
        self.images_stand_right = images_stand
        self.images_stand_left = [pygame.transform.flip(img, True, False) for img in images_stand]
        self.speed = speed
        self.is_jumping = False
        self.jump_count = 10
        self.walk_count = 0
        self.walk_frame_count = 0  # Counter for slowing down the walking animation
        self.stand_count = 0
        self.stand_frame_count = 0  # Counter for slowing down the standing animation
        self.direction = 'right'
        
    
    def move(self, a, d):
        keys = pygame.key.get_pressed()
        if keys[d]:
            if self.rect.right < wind_w:
                self.rect.x += self.speed
                self.walk_frame_count += 1
                if self.walk_frame_count >= 5:  # Adjust this value to make the walking animation slower or faster
                    self.walk_count = (self.walk_count + 1) % len(self.images_right)
                    self.walk_frame_count = 0
                self.image = self.images_right[self.walk_count]
                self.direction = 'right'
                #print(f"Moving right: walk_count={self.walk_count}")
        elif keys[a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
                self.walk_frame_count += 1
                if self.walk_frame_count >= 5:  # Adjust this value to make the walking animation slower or faster
                    self.walk_count = (self.walk_count + 1) % len(self.images_left)
                    self.walk_frame_count = 0
                self.image = self.images_left[self.walk_count]
                self.direction = 'left'
                #print(f"Moving left: walk_count={self.walk_count}")
        else:
            self.walk_count = 0
            self.stand_frame_count += 1
            if self.stand_frame_count >= 10:  # Adjust this value to make the standing animation slower or faster
                self.stand_count = (self.stand_count + 1) % len(self.images_stand_right)
                self.stand_frame_count = 0
            if self.direction == 'right':
                self.image = self.images_stand_right[self.stand_count]
            else:
                self.image = self.images_stand_left[self.stand_count]

    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                if self.direction == 'right':
                    self.image = self.images_jump_right[0]  # Set jumping image for right direction
                else:
                    self.image = self.images_jump_left[0]  # Set jumping image for left direction
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

    def fire(self, target_pos):
        direction_vector = pygame.math.Vector2(target_pos) - pygame.math.Vector2(self.rect.center)
        direction_vector = direction_vector.normalize() * 15  # Normalize and scale the vector
        bullets.append(Bullet(self.rect.centerx, self.rect.centery, 25, 50, bullet_img, direction_vector))

class Bullet(Sprite):
    def __init__(self, x, y, w, h, image, velocity):
        super().__init__(x, y, w, h, image)
        self.velocity = velocity
    
    def move(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.rect.y <= 0 or self.rect.y >= wind_h or self.rect.x <= 0 or self.rect.x >= wind_w:
            bullets.remove(self)

class Obstacle(Sprite):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h, image)
        
class Camera:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        
    def move(self, player):
        if player.rect.x >= ((self.rect.x + self.rect.w)*0,7):
            self.rect.x += self.speed
        
        
camera = Camera(0, 0, wind_w, wind_h, 3)

blocks = []
block_size = 25

block_x = 0
block_y = 0
block_img = pygame.image.load("wall.png")

for row in lvl1:
    for tile in row:
        if tile == "1":
            blocks.append(Sprite(block_x, block_y, block_size, block_size, block_img))
            print(block_x, block_y)
        block_x += block_size
    block_x = 0
    block_y += block_size

bullet_img = pygame.image.load("img/bullet.png")
bullets = []

# Load walking animation frames
player_images_right = [pygame.image.load(f"img/adventBoy_walk{i}.png") for i in range(1, 4)]
player_images_right = [pygame.transform.scale(img, (100, 100)) for img in player_images_right]  # Scale images 3 times

# Load jumping animation frames
player_images_jump = [pygame.image.load("img/adventBoy_jump.png")]
player_images_jump = [pygame.transform.scale(img, (100, 100)) for img in player_images_jump]  # Scale images 3 times

player = Player(50, 850, 100, 100, player_images_right, player_images_jump, player_images_stand, 5)  # Update player size



game = True
while game:
    window.fill((0, 100, 50))
    for bullet in bullets:
        bullet.draw()
        bullet.move()
    player.draw()
    player.move(pygame.K_a, pygame.K_d)
    player.jump()

    for b in blocks:
        b.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.is_jumping:
                player.is_jumping = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                player.fire(event.pos)

    pygame.display.update()
    clock.tick(FPS)