import pygame.sprite

class Bomb(pygame.sprite.Sprite):
    def __init__(self,surface,win_rect,pos,imageLoc):
        super().__init__()
        self.surface = surface
        self.win_rect = win_rect
        self.width, self.height = 6, 14
        self.rect = pygame.Rect(*pos, self.width, self.height)
        self.speed = 3
        bombTemp=pygame.transform.rotate(pygame.image.load(imageLoc), 180) 
        self.image = pygame.transform.scale(bombTemp, (self.rect.width+5, self.rect.height+15)) #bomb image size bigger than bomb rect size
        self.start_time = pygame.time.get_ticks()

        print("Bomb object created")

    def increse_speed(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time)//1000
        self.speed=min(7.5,self.speed+elapsed_time*0.03)
    
    def check_inside(self):
        if self.rect.y > self.win_rect.height:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.increse_speed()
        self.check_inside()
