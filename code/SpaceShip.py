import pygame

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,surface,win_rect,assets,speed=6):
        super().__init__()
        # Define attributes for the spaceship
        self.surface = surface
        self.win_rect = win_rect
        self.assets = assets
        self.speed = speed
        self.spaceship_height, self.spaceship_width = 40, 60 #define it by rect object
        #spaceship pos bottom center
        self.rect = pygame.Rect( 
            self.win_rect.width//2-self.spaceship_height//2, self.win_rect.height-self.spaceship_width, self.spaceship_height, self.spaceship_width)
        self.image = pygame.transform.scale(pygame.image.load(
            self.assets+"Space-Invaders-Ship.png"), self.rect.size)
        
        self.start_time = pygame.time.get_ticks()
        self.direction = pygame.math.Vector2(0,0)

        # life management
        self.life=3
        self.hit=False
        self.invincibility_duration = 500
        self.invincible = False
        self.hurt_time = 0
    
    def get_input(self):
        # Add your spaceship input code here
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.direction.x = -1
        elif keys_pressed[pygame.K_RIGHT] and self.rect.x + self.rect.width < self.win_rect.width:
            self.direction.x = 1
        elif keys_pressed[pygame.K_UP] and self.rect.y > 0:
            self.direction.y = -1
        elif keys_pressed[pygame.K_DOWN] and self.rect.y + self.rect.height < self.win_rect.height:
            self.direction.y = 1
        else:
            self.direction = pygame.math.Vector2(0,0)

    def get_status(self):
        pass

    def get_hit(self):
        if not self.invincible:
            self.life-=1
            self.hit=True
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            # self.hit_sound.play()

    def add_life(self):
        self.life+=1

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False
                self.hit=False
    
    def increse_speed(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time)//1000
        self.speed=min(7.5,self.speed+elapsed_time*.01)

    def movement(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        # Add your spaceship update code here
        self.get_input()
        # print("get_input() called")
        self.increse_speed()
        # print("increse_speed() called")
        self.movement()
        # print("movement() called")
        self.get_hit()
        # print("get_hit() called")
        self.add_life()
        # print("add_life() called")
        self.invincibility_timer()
        # print("invincibility_timer() called")
