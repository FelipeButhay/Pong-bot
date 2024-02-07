import pygame
import tkinter as tk
import math
import random
import pong_bot as bot

resolution_screen = tk.Tk()
screen_x = resolution_screen.winfo_screenwidth()
screen_y = resolution_screen.winfo_screenheight()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_x, screen_y))

class ball_c:
    def __init__(self):
        self.exist = False
        self.v = 0
        self.vx = 0 
        self.vy = 0
        self.a = 0
        self.rect = pygame.Rect((-1000, -1000, .025*screen_x, .025*screen_x))
        self.rect.center = screen_x*.5, screen_y*.5
        
    def move(self, pong, pong_target):
        if  self.rect.y < 0:
            self.a = abs(self.a-360)
            self.rect.y = 0
            print(pong_target)
        if  self.rect.y + self.rect.h > screen_y:
            self.a = abs(self.a-360)
            self.rect.y = screen_y - self.rect.h
            print(pong_target)
        
        if ball.rect.colliderect(pong.rect):
            d = -((pong.rect.y + pong.rect.h/2)-self.rect.centery)/(pong.rect.h/2)
            self.v = (screen_x*10)/1920
            if self.a < 90 or self.a > 270:
                self.a = 180 - d*50
                self.rect.right = pong.rect.left
            else:
                self.a = (d*50)%360
                self.rect.left  = pong.rect.right
                
        self.vx = self.v*math.cos(self.a/57.29578)
        self.vy = self.v*math.sin(self.a/57.29578)
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self):
        if self.exist:
            pygame.draw.rect(screen, "white", (*self.rect.topleft, *self.rect.size))

class pong_c:
    def __init__(self, position):
        self.points = 0
        self.rect = pygame.Rect((*position, .01*screen_x, .15*screen_y))
        
    def wpoints(self, pos):
        font = pygame.font.Font(None, int(screen_y*.15))
        if self.points < 10:
            img = font.render("0"+str(self.points), True, "white")
        else:
            img = font.render(str(self.points), True, "white")
        screen.blit(img, img.get_rect(center = pos))
        
    def limit(self):
        if  self.rect.y < 0:
            self.rect.y = 0
        if  self.rect.y + self.rect.h > screen_y:
            self.rect.y = screen_y - self.rect.h
            
    def draw(self):
        pygame.draw.rect(screen, "white", self.rect)

ball = ball_c()
left_pong = pong_c([.02*screen_x, .45*screen_y])
right_pong = pong_c([.97*screen_x, .45*screen_y])

pong_target = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if ball.rect.x + ball.rect.w < 0:
        ball.exist = False
        right_pong.points += 1
    
    if ball.rect.x > screen_x:
        ball.exist = False
        left_pong.points += 1

    if not ball.exist:
        ball.rect.center = screen_x*.5, screen_y*.5
        ball.exist = True
        ball.v = (screen_x*5)/1920
        if random.randint(0,1)==0:
            ball.a = random.randint(-70, 70)%360
        else:
            ball.a = 180 + random.randint(-70, 70)
        
    for x in (left_pong, right_pong):
        ball.move(x, pong_target)

    screen.fill("black")
    for x in range(0, 10):
        pygame.draw.rect(screen, "white", (screen_x*.495, screen_y*.05*2*x + screen_y*.025, screen_x*.01, screen_y*.05))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_pong.rect.y -= .015 * screen_y
    if keys[pygame.K_s]:
        left_pong.rect.y += .015 * screen_y
        
    if ball.vx < 0:
        if .5*screen_y + .01*screen_y < right_pong.rect.centery:
            right_pong.rect.y -= .015 * screen_y
        elif .5*screen_y - .01*screen_y > right_pong.rect.centery:
            right_pong.rect.y += .015 * screen_y
    else:
        pong_target = bot.get_inter(ball.rect.center, ball.vx, ball.vy, screen_y, right_pong.rect.left)
        if pong_target + .01*screen_y < right_pong.rect.centery:
            right_pong.rect.y -= .015 * screen_y
        elif pong_target - .01*screen_y > right_pong.rect.centery:
            right_pong.rect.y += .015 * screen_y
        
    left_pong.limit()
    right_pong.limit()
    
    left_pong.wpoints((screen_x*.25, screen_y*.15))
    right_pong.wpoints((screen_x*.75, screen_y*.15))
    
    if ball.exist:
        ball.draw()
    left_pong.draw()
    right_pong.draw()
        
    pygame.display.update()
    clock.tick(60)
