import pygame
import os
import time
import random

from SpaceShip import SpaceShip
from bomb import Bomb



WIDTH ,HEIGHT = 800, 600


class Game:
    FPS = 60
    def __init__(self, win_width, win_height, spaceship_vel=6 ):
        self.win_width =win_width #window width
        self.win_height = win_height #window height
        self.win_rect = pygame.Rect(0, 0, self.win_width, self.win_height)
        self.hit = False

        # function calling
        pygame.font.init()

        # Assets section
        self.assets="assets/"
        self.check_assets()
        self.Time_font = pygame.font.SysFont("comicsans", 30)
        self.VEL_font = pygame.font.SysFont("comicsans", 40)

        #TUNING VARIABLE shouhd be 0 in for standard state
        self.FORWARD_TIME=3000 #in second should be 0 in for standard state
        self.REDUCE_INCREMENT_TIME=0

        #Time section
        self.clock = pygame.time.Clock()
        self.start_time = time.time() - self.FORWARD_TIME
        self.elapsed_time = 0

        # Bomb section
        self.bomb_img=self.assets+"bomb2.png"
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

    def check_assets(self):
        # check current directory if its has chid directory assets or it parent directory has assets
        if not os.path.isdir(self.assets):
            if os.path.isdir("../"+self.assets):
                self.assets="../"+self.assets
                print("assets directory found in parent directory")
            else:
                print("assets directory not found")
        else:
            print("assets directory found in current directory")


    def draw(self):
        """draw all the object on screen
        """
        self.win.blit(self.bg_space, (0, 0))
        self.time_text = self.Time_font.render(
        f"Time : {round(self.elapsed_time) }", True, "white")
        self.win.blit(self.time_text, (5, 5))
        self.bombs.draw(self.win)
        self.spaceship.draw(self.win)
        self.draw_opInfo()

        pygame.display.update()
        # print("draw function called")
        
    def draw_opInfo(self):
        """draw operation info on screen
        read the current value of bomb_vel,ship_vel,bomb_passed and draw on screen
        """
        #get number of in bombs sprite group
        if len(self.bombs.sprites())>0:
            self.bomb_vel = self.bombs.sprites()[0].speed
        else:
            self.bomb_vel = 0
        self.spaceship_vel = self.spaceship.sprite.speed
        self.bomb_present = len(self.bombs.sprites())

        self.bomb_vel_text = self.VEL_font.render(
                f"Bomb vel : {self.bomb_vel:2>.2f}" , True, "white")
        self.win.blit(self.bomb_vel_text, (self.win_rect.width-self.bomb_vel_text.get_width(), 5))
        self.ship_vel_text = self.VEL_font.render(
                    f"ship vel : {self.spaceship_vel:2>.2f}" , True, "white")
        self.win.blit(self.ship_vel_text, (self.win_rect.width-self.ship_vel_text.get_width(), self.bomb_vel_text.get_height()))
        self.bomb_passed_text = self.VEL_font.render(
                    f"BOMB COUNT : {self.bomb_present:4}", True, "white")
        self.win.blit(self.bomb_passed_text, (self.win_rect.width-self.bomb_passed_text.get_width(),self.bomb_passed_text.get_height()+ self.bomb_vel_text.get_height()))
        pygame.display.update()

        # print("draw_opInfo function called")

    def add_bombs(self):
        self.bomb_add_time += self.clock.tick(Game.FPS) #self.clock.tick(FPS) return the time in ms since the last call
        if self.bomb_add_time > self.bomb_increment_time and len(self.bombs) < self.max_bomb:
            for _ in range(self.bomb_num):
                pos=(random.randint(0, self.win_width),-random.randint(0, 200))
                bomb=Bomb(self.win,self.win_rect,pos,self.bomb_img) #surface,win_rect,pos,imageLoc
                self.bombs.add(bomb)
                
            self.bomb_add_time = 0
            self.bomb_increment_time = max(500, self.bomb_increment_time-50)
    
    def space_ship_movement(self):
        pass

    def check_collision(self):
        ship=self.spaceship.sprite
        if pygame.sprite.spritecollide(ship, self.bombs, True):
            ship.get_hit()
            self.hit=True
    
    def level(self):
        self.elapsed_time = time.time() - self.start_time #time.time() return the time in second since the epoch
        self.add_bombs()
        self.check_collision()

        # Update sprites
        self.spaceship.update()
        self.bombs.update()

        #Draw sprite
        self.draw()


    def Run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            # print("section 3")

            # moving bombs
            # for bomb in self.bombs:
            #     if bomb.y > HEIGHT:
            #         self.bomb_passed+=1
            #     elif bomb.y + bomb.height >= self.spaceship_rect.y and bomb.colliderect(self.spaceship_rect):
            #         self.bombs.remove(bomb)
            #         self.hit = True
            #         break

            # print("section 4")

            self.level()

            if self.hit:
                lost_text =self.Time_font.render("You Lost!", 1, "white")
                self.win.blit(lost_text, (self.win_width/2 - lost_text.get_width()/2, self.win_height/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2000)
                break

            #DRAWING staf
            # self.draw_opInfo()
            # self.draw()

            # print("section 5")

if __name__ == "__main__":
    Obj=Game(WIDTH,HEIGHT)
    Obj.Run()
