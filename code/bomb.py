import pygame.sprite

class Bomb(pygame.sprite.Sprite):
    def __init__(self,surface,win_rect,pos,speed,imageLoc):
        super().__init__()
        self.surface = surface
        self.win_rect = win_rect
        self.width, self.height = 6, 14
        self.rect = pygame.Rect(*pos, self.width, self.height)
        self.speed = speed
        bombTemp=pygame.transform.rotate(pygame.image.load(imageLoc).convert_alpha(), 180) 
        self.image = pygame.transform.scale(bombTemp, (self.rect.width+5, self.rect.height+15)) #bomb image size bigger than bomb rect size
        self.damage=25

        # print("Bomb object created")
    
    def check_inside(self):
        if self.rect.y > self.win_rect.height:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.check_inside()
