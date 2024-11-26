import pygame, sys, math, random
#Setup
pygame.init()
clock = pygame.time.Clock()

#Display
screen = pygame.display.set_mode((1920,1020))
pygame.display.set_caption("Bullet Hell")

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
player.x = 960
player.y = 480
player_health = 400

current_background = bg_1

keys_collected = False

flash_timer = 0
flash_duration = 5

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
        self.bullet.fill((0,255,0))
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)

    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed, self.pos[1]+self.dir[1]*self.speed) #Updates the position of the bullet using the direction is was fired in and setting the speed

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)
     
#Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, scale_factor=0.15):
        super().__init__()
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, scale_factor) #Scaling the enemy image down to an appropriate size
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1.8
        self.direction = pygame.math.Vector2(0, 0)
        self.health = 100
        self.damage = 0.5

    def update(self, player_rect, bullets):
        target_vector = pygame.math.Vector2(player_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        direction = target_vector - enemy_vector
        if direction.magnitude() > 0:
            self.direction = direction.normalize() #Normalising the vector to make the enemy speed consistent
        #Enemy Movement & Speed
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        #Checking for bullet collisions
        for bullet in bullets[:]:
            if self.rect.collidepoint(bullet.pos): #Checking if a bullet from the bullet list collides with an enemy
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
        
#Key Class
class KeyItem(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, background):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.background = background
        self.collected = False
        
    def update(self, player_rect):
        if self.rect.colliderect(player_rect) and self.collected == False and current_background == self.background: #Checks if the key is already collected and if the player is in the correct room
            self.collected = True
            
    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

#Key Collectables
key_1 = KeyItem("key_1.png", 640, 250, bg_2)
key_2 = KeyItem("key_2.png", 1206, 450, bg_3)
key_3 = KeyItem("key_3.png", 560, 780, bg_4)

#Colours
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Display
screen = pygame.display.set_mode((1920,1020))
pygame.display.set_caption("Bullet Hell")

#Text
font = pygame.font.SysFont('Arial', 75, bold=True)
death_text = font.render("YOU DIED", True, (255, 255, 255))
victory_text = font.render("YOU WON", True, (255, 255, 255))
restart_text = font.render("Will You Try Again? Press Q", True, (255, 255, 255))

#Movement
movement_speed = 2

#Bullet List
bullets = []

#Key Group
key_items = pygame.sprite.Group()
key_items.add(key_1, key_2, key_3)

#Enemy Group and Spawn Event
enemy_grp = pygame.sprite.Group()
pygame.time.set_timer(SPAWNENEMIES, 1000) #Spawns an enemy every second

left_exit = (500, 480)
right_exit = (1410, 480)
north_exit = (962, 25)
south_exit = (962, 935)

#Game Loop
dead = False
victory = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: #Spawns a bullet on the player's position when the mouse is clicked
            bullets.append(Bullet(player.x + 25, player.y + 25))
            flash_timer = flash_duration
        if event.type == SPAWNENEMIES:
            enemy = Enemy(random.randrange(500,1410),random.randrange(25,935), 2) #Spawns an enemy anywhere on the map
            enemy_grp.add(enemy)

    #Making keys visible and interactable in their corresponding backgrounds
    key_items.update(player)
    for KeyItem in key_items:
        if current_background == KeyItem.background:
            screen.blit(KeyItem.image, KeyItem.rect)

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
        
    #Reset button that resets key collectables, player position and player health
    if keys[pygame.K_q] and (dead or victory):
        dead = False
        victory = False
        player_health = 400
        current_background = bg_1
        player.x = 960
        player.y = 480
        key_1.collected = False
        key_2.collected = False
        key_3.collected = False

    screen.fill((0,0,0))    

    #Level navigation
    if dead == False and victory == False:
        screen.blit(current_background, (500, 25))
        if flash_timer > 0:
            flash_rect = player.copy()
            pygame.draw.rect(screen, green, flash_rect)
            flash_timer -= 1
        else:
            pygame.draw.rect(screen, blue, player)
        #Empty Health Bar
        pygame.draw.rect(screen, red, (50, 50, 400, 30))
        #Full Health Bar
        pygame.draw.rect(screen, green, (50, 50, player_health, 30))
        enemy_grp.update(player, bullets)
        enemy_grp.draw(screen)
        if current_background == bg_1 and (player.x, player.y) == left_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_2
            player.x = 1390
            player.y = 480
        if current_background == bg_2 and (player.x, player.y) == right_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_1
            player.x = 520
            player.x = 480
        if current_background == bg_1 and (player.x, player.y) == right_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_3
            player.x = 520
            player.y = 480
        if current_background == bg_3 and (player.x, player.y) == left_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_1
            player.x = 1390
            player.y = 480
        if current_background == bg_1 and (player.x, player.y) == south_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_4
            player.x = 962
            player.y = 45
        if current_background == bg_4 and (player.x, player.y) == north_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_1
            player.x = 962
            player.y = 915
        if current_background == bg_1 and (player.x, player.y) == north_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_5
            player.x = 962
            player.y = 915
        if current_background == bg_5 and (player.x, player.y) == south_exit:
            enemy_grp.empty()
            bullets.clear()
            current_background = bg_1
            player.x = 962
            player.y = 45
        if current_background == bg_5 and (player.x, player.y) == north_exit and keys_collected == True:
            enemy_grp.empty()
            bullets.clear()
            victory = True

    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)
        if not screen.get_rect().collidepoint(bullet.pos): #Deletes the bullet if it leaves the bounds of the screen
            bullets.remove(bullet)
   
    #Player Collision
    if player.x < 500:
        player.x = 500
    if player.y < 25:
        player.y = 25
    if player.x > 1410:
        player.x = 1410
    if player.y > 935:
        player.y = 935

    #Victory Feature
    if victory == True:
        screen.blit(victory_text, (760, 40))
        screen.blit(restart_text, (625, 600))
        enemy_grp.empty()
        
    #Checking if the player is dead and resets the player's inventory
    if player_health <= 0:
        dead = True
        player_health = 0
        screen.blit(death_text, (760, 40))
        screen.blit(restart_text, (625, 600))
        enemy_grp.empty()
        key_1.collected = False
        key_2.collected = False
        key_3.collected = False
    
    #Key Display/Inventory
    key_display = pygame.Rect(50, 100, 350, 750)
    pygame.draw.rect(screen, (255, 255, 255), key_display, 2)
    key_display_text = font.render("Keys:", True, (255, 255, 255))
    screen.blit(key_display_text, (75, 125))
    
    if key_1.collected:
        screen.blit(key_1.image, (180, 250))
    if key_2.collected:
        screen.blit(key_2.image, (190, 450))
    if key_3.collected:
        screen.blit(key_3.image, (200, 650))
        
    if key_1.collected == True and key_2.collected == True and key_3.collected == True:
        keys_collected = True

    if current_background == bg_2 and dead == False and victory == False:
        key_1.draw(screen)
    if current_background == bg_3 and dead == False and victory == False:
        key_2.draw(screen)
    if current_background == bg_4 and dead == False and victory == False:
        key_3.draw(screen)

    pygame.display.flip()
       
#Frames & Screen Updates
clock.tick(60)
