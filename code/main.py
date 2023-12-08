import pygame
import os
import time
import random

# covert the to class approch from function approch


# Time_font = pygame.font.SysFont("comicsans", 30)
# VEL_font = pygame.font.SysFont("comicsans", 40)

WIDTH ,HEIGHT = 800, 600

# SPACESHIP_VEL = 6
# FPS = 60
# BOMB_WIDTH, BOMB_HEIGHT = 6, 14
# BASE_BOMB_VEL=3
# BOMB_NUM = 5
# MAX_BOMBS = 26
# SPACESHIP_x, SPACESHIP_Y = 40, 60

class Spaceship:
    FPS = 60
    SPACESHIP_VEL = 6
    def __init__(self, x, y, width, height, vel, img):
        self.x = x #not sure yet
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.img = img
        # Bomb section
        self.bomb_width, self.bomb_height = 6, 14
        self.bomb_vel = 3
        self.bomb_num = 5 # number of bomb added in one time
        self.max_bomb = 26

        #Graphics section
        self.win=pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Game")
        self.bg_space = pygame.transform.scale(pygame.image.load(self.assets+"bg.jpeg"), (WIDTH, HEIGHT))
        self.ship = pygame.transform.scale(pygame.image.load(
            self.assets+"Space-Invaders-Ship.png"), (self.spaceship_x, self.spaceship_y ))
        bombTemp=pygame.transform.rotate(pygame.image.load(self.assets+"bomb2.png"), 180)
        self.bomb = pygame.transform.scale(bombTemp, (self.bomb_width+5, self.bomb_height+15))

        # spaceship section
        self.spaceship_x, self.spaceship_y = 40, 60

        # Assets section
        self.assets="assets/"
        self.Time_font = pygame.font.SysFont("comicsans", 30)
        self.VEL_font = pygame.font.SysFont("comicsans", 40)

        # function calling
        self.check_assets()
        pygame.font.init()

        #TUNING VARIABLE shouhd be 0 in for standard state
        self.FORWARD_TIME=0 #in second should be 0 in for standard state
        self.REDUCE_INCREMENT_TIME=0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def check_assets(self):
        # check current directory if its has chid directory assets or it parent directory has assets
        if not os.path.isdir(assets):
            if os.path.isdir("../"+assets):
                assets="../"+assets
                print("assets directory found in parent directory")
            else:
                print("assets directory not found")
        else:
            print("assets directory found in current directory")
        




# Graphics section


def draw_opInfo(bomb_vel=0,ship_vel=0):
        
        bomb_vel = VEL_font.render(
                f"Bomb vel : {bomb_vel:2>.2f}" , True, "white")
        WIN.blit(bomb_vel, (WIDTH-bomb_vel.get_width(), 5))
        ship_vel = VEL_font.render(
                    f"ship vel : {ship_vel:2>.2f}" , True, "white")
        WIN.blit(ship_vel, (WIDTH-ship_vel.get_width(), bomb_vel.get_height()))
        Count_bomb = VEL_font.render(
                    f"BOMB COUNT : {count_bomb:4}", True, "white")
        WIN.blit(Count_bomb, (WIDTH-Count_bomb.get_width(),Count_bomb.get_height()+ bomb_vel.get_height()))
        pygame.display.update()

def draw(spaceship_rect, elapsed_time, bombs):
    time_text = Time_font.render(
        f"Time : {round(elapsed_time) }", True, "white")
    WIN.blit(time_text, (5, 5))
    WIN.blit(SPACESHIP, (spaceship_rect.x, spaceship_rect.y))
    for bomb in bombs:
        WIN.blit(BOMB, (bomb.x, bomb.y))

    pygame.display.update()

# MAIN GAME

def main():
    run = True
    clock = pygame.time.Clock()
    curr_time = time.time() - FORWARD_TIME
    elapsed_time = 0
    bomb_increment = 2000-REDUCE_INCREMENT_TIME
    bomb_add_time = 1500  # last star added to game
    bombs = []
    global count_bomb
    count_bomb=0

    hit = False

    spaceship_rect = pygame.Rect(
        WIDTH//2-SPACESHIP_x//2, HEIGHT-SPACESHIP_Y, SPACESHIP_x, SPACESHIP_Y)

    while run:

        bomb_add_time += clock.tick(FPS)
        elapsed_time = time.time() - curr_time
        # elapsed_time=len(bombs)
        bomb_vel=min(8.5,BASE_BOMB_VEL+elapsed_time*.03)
        spaceship_vel=min(7.5,SPACESHIP_VEL+elapsed_time*.01)

        

        if bomb_add_time > bomb_increment and len(bombs) < MAX_BOMBS:
            for _ in range(BOMB_NUM):
                starX = random.randint(0, WIDTH)
                starY = random.randint(0, 200)
                bomb = pygame.Rect(starX, -starY, BOMB_WIDTH, BOMB_HEIGHT)
                bombs.append(bomb)

            bomb_add_time = 0
            bomb_increment = max(300, bomb_increment-50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and spaceship_rect.x > 0:
            spaceship_rect.x -= spaceship_vel
        if keys_pressed[pygame.K_RIGHT] and spaceship_rect.x + spaceship_rect.width < WIDTH:
            spaceship_rect.x += spaceship_vel

    # moving stars
        for bomb in bombs:
            bomb.y += bomb_vel
            if bomb.y > HEIGHT:
                bombs.remove(bomb)
                count_bomb+=1
            elif bomb.y + bomb.height >= spaceship_rect.y and bomb.colliderect(spaceship_rect):
                bombs.remove(bomb)
                hit = True
                break

        if hit:
            lost_text =Time_font.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        #DRAWING staf
        WIN.blit(SPACE, (0, 0))
        draw_opInfo(bomb_vel,spaceship_vel)
        draw(spaceship_rect, elapsed_time, bombs)

        

    main()


if __name__ == "__main__":
    main()
