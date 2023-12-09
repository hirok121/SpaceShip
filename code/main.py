import pygame
import os
import time
import random

from SpaceShip import SpaceShip
from bomb import Bomb
from support import *

class Game:
    def __init__(self, win_width, win_height, spaceship_vel=6 ):
        self.win_width =win_width #window width
        self.win_height = win_height #window height
        self.win_rect = pygame.Rect(0, 0, self.win_width, self.win_height)

        # function calling
        pygame.font.init()
        # Assets section
        self.assets=check_assets()
        self.Score = pygame.font.SysFont("comicsans", 20)
        self.VEL_font = pygame.font.SysFont("comicsans", 10)

        #TUNING VARIABLE shouhd be 0 in for standard state
        self.FORWARD_TIME=0 #in second should be 0 in for standard state
        self.REDUCE_INCREMENT_TIME=0 #in ms should be 0 in for standard state

        #Time section
        self.clock = pygame.time.Clock()
        self.start_time = time.time() - self.FORWARD_TIME #time.time() return the time in second since the epoch
        self.elapsed_time = 0
        self.start_time_ms = pygame.time.get_ticks() - self.FORWARD_TIME

        # Bomb section
        self.bomb_img=self.assets+"bomb2.png"
        self.bomb_speed=3
        self.bomb_num = 5 # number of bomb added in one time
        self.max_bomb = 26
        self.bomb_increment_time = 2000-self.REDUCE_INCREMENT_TIME # time interval to add new bomb (in ms) 
        self.bomb_add_time = 0  # last time bomb added to game
        self.bomb_passed=0
        self.bombs =pygame.sprite.Group() # list of bomb rect object

        #Graphics section
        self.win=pygame.display.set_mode(self.win_rect.size)
        pygame.display.set_caption("Space Game")
        self.bg_space = pygame.transform.scale(pygame.image.load(self.assets+"bg.jpeg"), self.win_rect.size)

        # spaceship section
        self.spaceship=pygame.sprite.GroupSingle()
        sprite=SpaceShip(self.win,self.win_rect,self.assets)
        self.spaceship.add(sprite)
        # print("Object created")

    
    def score_count(self):

        current_time = pygame.time.get_ticks()
        elapsed_time_ms = (current_time - self.start_time_ms)*0.75
        score=int(elapsed_time_ms)
        self.Score_text = self.Score.render(
        f"Score : {score}", True, "white")
        self.win.blit(self.Score_text, (45, 60))


    def draw(self):
        """draw all the object on screen
        """
        self.win.blit(self.bg_space, (0, 0))
        self.score_count()
        self.bombs.draw(self.win)
        self.spaceship.draw(self.win)
        self.spaceship.sprite.health_bar.draw(self.win)
        self.spaceship.sprite.health_bar.update(self.spaceship.sprite.health)
        self.draw_opInfo()

        pygame.display.update() #! update the screen
        
    def draw_opInfo(self):
        """draw operation info on screen
        read the current value of bomb_vel,ship_vel,bomb_passed and draw on screen
        """
        #get number of in bombs sprite group

        self.spaceship_vel = self.spaceship.sprite.speed
        self.bomb_present = len(self.bombs.sprites())

        self.bomb_vel_text = self.VEL_font.render(
                f"Bomb v {self.bomb_speed:2>.2f}" , True, "white")
        self.win.blit(self.bomb_vel_text, (self.win_rect.width-self.bomb_vel_text.get_width(), 5))
        self.ship_vel_text = self.VEL_font.render(
                    f"ship v : {self.spaceship_vel:2>.2f}" , True, "white")
        self.win.blit(self.ship_vel_text, (self.win_rect.width-self.ship_vel_text.get_width(), self.bomb_vel_text.get_height()))
        self.bomb_passed_text = self.VEL_font.render(
                    f"BOMB COUNT : {self.bomb_present:4}", True, "white")
        self.win.blit(self.bomb_passed_text, (self.win_rect.width-self.bomb_passed_text.get_width(),self.bomb_passed_text.get_height()+ self.bomb_vel_text.get_height()))
        pygame.display.update()

        # print("draw_opInfo function called")

    def increse_speed(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time_ms)//1000
        self.bomb_speed=min(8.5,3+elapsed_time*0.04)

    def add_bombs(self):
        self.bomb_add_time += self.clock.tick(FPS) #self.clock.tick(FPS) return the time in ms since the last call
        if self.bomb_add_time > self.bomb_increment_time and len(self.bombs) < self.max_bomb:
            for _ in range(self.bomb_num):
                pos=(random.randint(0, self.win_width),-random.randint(0, 200))
                bomb=Bomb(self.win,self.win_rect,pos,self.bomb_speed, self.bomb_img) #surface,win_rect,pos,imageLoc
                self.bombs.add(bomb)
                
            self.bomb_add_time = 0
            self.bomb_increment_time = max(500, self.bomb_increment_time-50)
    
    def space_ship_movement(self):
        pass

    def check_collision(self):
        ship=self.spaceship.sprite
        if pygame.sprite.spritecollide(ship, self.bombs, True):
            ship.get_hit(self.bombs.sprites()[0].damage)
        
    def game_over(self):
        if not self.spaceship.sprite.alive:
            lost_text =self.Score.render("Game Over!", 1, "white")
            self.win.blit(lost_text, (self.win_width/2 - lost_text.get_width()/2, self.win_height/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            
    
    def level(self):
        self.elapsed_time = time.time() - self.start_time #time.time() return the time in second since the epoch
        self.add_bombs()
        self.increse_speed()
        self.check_collision()

        # Update sprites
        self.spaceship.update()
        self.bombs.update()

        #Draw sprite
        self.draw()

        self.game_over()


    def Run(self):
        run=True
        while run and self.spaceship.sprite.alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            self.level()


if __name__ == "__main__":
    Obj=Game(WIDTH,HEIGHT)
    Obj.Run()
