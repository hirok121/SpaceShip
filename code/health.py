import pygame

class HealthBar(pygame.sprite.Sprite):
    def __init__(self,surface,win_rect,max_health,assets):
        super().__init__()
        self.surface = surface
        self.win_rect = win_rect
        self.assets = assets
        self.max_health=max_health
        self.topleft = (55,39)
        self.width = 152
        self.height = 4
        self.rect = pygame.Rect((20,10), (self.width,self.height))
        self.image = pygame.image.load(self.assets+"health_bar.png").convert_alpha()

    def update(self,current_health=150):
        current_health_ratio = current_health / self.max_health
        current_bar_width = self.width * current_health_ratio
        health_bar_rect = pygame.Rect(self.topleft, (current_bar_width, self.height))
        pygame.draw.rect(self.surface, '#dc4949', health_bar_rect)


