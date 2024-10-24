from tkinter import CURRENT
import pygame, sys, math, random
#Setup
pygame.init()
clock = pygame.time.Clock()

#Custom Event to Spawn Enemies
SPAWNENEMIES = pygame.USEREVENT + 1

#Backgrounds
bg_1 = pygame.image.load("room_1.png")
bg_2 = pygame.image.load("Room_2.png")
bg_3 = pygame.image.load("room_3.png")
bg_4 = pygame.image.load("room_4.png")
bg_5 = pygame.image.load("Room_5.png")

#Player
player = pygame.Rect(50,50,50,50)
player.x = 100
player.y = 100
player_health = 400

current_background = bg_1

#Bullet Class
class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos() #Finds the x and y positions of the mouse where the mouse was clicked
        self.dir = (mx - player.x, my - player.y)
        self.speed = 4
        self.damage = 50
        length = math.hypot(*self.dir) #Finds the hypontenuse between the location of the player and the location of the mouse click
        self.bullet = pygame.Surface((15, 15)).convert_alpha()
        self.bullet.fill((0,255,0)) #Bullet colour
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
    
    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed, self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)
      
#Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, scale_factor=0.5):
        super().__init__()
        self.image = enemy_surface
        self.image = pygame.transform.scale_by(self.image, scale_factor)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1
        self.direction = pygame.math.Vector2(0, 0)
        self.health = 100
        self.damage = 0.3
        
    def update(self, player_rect, bullets):
        target_vector = pygame.math.Vector2(player_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        direction = target_vector - enemy_vector
        if direction.magnitude() > 0:
            self.direction = direction.normalize()
        #Enemy Movement & Speed
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        #Checking for bullet collisions
        for bullet in bullets[:]:
            if self.rect.collidepoint(bullet.pos):
                self.health -= bullet.damage
                bullets.remove(bullet)
                if self.health <= 0:
                    enemy_grp.remove(self)
                    self.kill
        if self.rect.colliderect(player_rect):
            global player_health
            player_health -= self.damage
      
    def draw(self, screen):
        screen.blit(self.image, self.rect)

#Colours
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Display
screen = pygame.display.set_mode((1920,1020))
pygame.display.set_caption("Bullet Hell")

#Movement
movement_speed = 2

enemy_surface = pygame.image.load("01-01.jpg").convert_alpha()
enemy_surface = pygame.transform.scale_by(enemy_surface, 0.2)

#Bullet List
bullets = []

enemy_grp = pygame.sprite.Group()
pygame.time.set_timer(SPAWNENEMIES, 1000)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(Bullet(player.x + 25, player.y + 25))
        if event.type == SPAWNENEMIES:
            enemy = Enemy(random.randrange(500,1410),random.randrange(25,935), enemy_surface, 2) #Spawns an enemy anywhere on the map
            enemy_grp.add(enemy)



    #Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= movement_speed
    if keys[pygame.K_s]:
        player.y += movement_speed
    if keys[pygame.K_a]:
        player.x -= movement_speed
    if keys[pygame.K_d]:
        player.x += movement_speed

    screen.fill((0,0,0))    
    screen.blit(current_background, (500, 25))

    #Level navigation
    if current_background == bg_1 and player.x <= 500 and player.y == 480: 
        current_background = bg_2
        player.x = 1390
        player.y = 480
    if current_background == bg_2 and player.x >= 1410 and player.y == 480:
        current_background = bg_1
        player.x = 520
        player.x = 480
    if current_background == bg_1 and player.x >= 1410 and player.y == 480:
        current_background = bg_3
        player.x = 520
        player.y = 480
    if current_background == bg_3 and player.x <= 500 and player.y == 480:
        current_background = bg_1
        player.x = 1390
        player.y = 480
    if current_background == bg_1 and 

    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)
        if not screen.get_rect().collidepoint(bullet.pos): #Deletes the bullet if it leaves the bounds of the screen
            bullets.remove(bullet)

    enemy_grp.update(player, bullets)
    enemy_grp.draw(screen)

    #List Checking
    #print(len(bullets))
    #print(player_health)

    #Collision
    if player.x < 500:
        player.x = 500
    if player.y < 25:
        player.y = 25
    if player.x > 1410:
        player.x = 1410
    if player.y > 935:
        player.y = 935

    pygame.draw.rect(screen, blue, player)
    #Empty Health Bar
    pygame.draw.rect(screen, red, (50, 50, 400, 30))
    #Full Health Bar
    pygame.draw.rect(screen, green, (50, 50, player_health, 30))
    pygame.display.flip()
       
#Frames & Screen Updates
clock.tick(60)