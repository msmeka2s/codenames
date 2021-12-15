import sys 
import os
sys.path.append(os.path.join(sys.path[0],'..','lib'))
import pygame
pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("First Game")

imgPath = "../images/"

walkRight = [pygame.image.load(imgPath + 'R1.png'),pygame.image.load(imgPath + 'R2.png'),pygame.image.load(imgPath + 'R3.png'),pygame.image.load(imgPath + 'R4.png'),pygame.image.load(imgPath + 'R5.png'),pygame.image.load(imgPath + 'R6.png'),pygame.image.load(imgPath + 'R7.png'),pygame.image.load(imgPath + 'R8.png'),pygame.image.load(imgPath + 'R9.png')]
walkLeft = [pygame.image.load(imgPath + 'L1.png'),pygame.image.load(imgPath + 'L2.png'),pygame.image.load(imgPath + 'L3.png'),pygame.image.load(imgPath + 'L4.png'),pygame.image.load(imgPath + 'L5.png'),pygame.image.load(imgPath + 'L6.png'),pygame.image.load(imgPath + 'L7.png'),pygame.image.load(imgPath + 'L8.png'),pygame.image.load(imgPath + 'L9.png')]
bg = pygame.image.load(imgPath + 'bg.jpg')
char = pygame.image.load(imgPath + 'standing.png')

clock = pygame.time.Clock()

class Player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False 
        self.jumpCount = 10
        self.left = False 
        self.right = False 
        self.walkCount = 0
        self.standing = True 
    
    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else: 
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x,self.y))

class Enemy(object):
    walkRight = [pygame.image.load(imgPath + 'R1E.png'), pygame.image.load(imgPath + 'R2E.png'), pygame.image.load(imgPath + 'R3E.png'), pygame.image.load(imgPath + 'R4E.png'), pygame.image.load(imgPath + 'R5E.png'), pygame.image.load(imgPath + 'R6E.png'), pygame.image.load(imgPath + 'R7E.png'), pygame.image.load(imgPath + 'R8E.png'), pygame.image.load(imgPath + 'R9E.png'), pygame.image.load(imgPath + 'R10E.png'), pygame.image.load(imgPath + 'R11E.png')]
    walkLeft = [pygame.image.load(imgPath + 'L1E.png'), pygame.image.load(imgPath + 'L2E.png'), pygame.image.load(imgPath + 'L3E.png'), pygame.image.load(imgPath + 'L4E.png'), pygame.image.load(imgPath + 'L5E.png'), pygame.image.load(imgPath + 'L6E.png'), pygame.image.load(imgPath + 'L7E.png'), pygame.image.load(imgPath + 'L8E.png'), pygame.image.load(imgPath + 'L9E.png'), pygame.image.load(imgPath + 'L10E.png'), pygame.image.load(imgPath + 'L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        
    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel 
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else: 
            if self.x - self.vel > self.path[0]:
                self.x += self.vel 
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

class Projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius 
        self.color = color
        self.facing = facing 
        self. vel = 8 * facing 

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
    
def redrawGameWindow():
    win.blit(bg,(0,0))
    goblin.draw(win)
    player.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()

player = Player(300,400,64,64)
goblin = Enemy(100,410,64,64,450)
bullets = []
# main loop
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else: 
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if player.left:
            facing = -1
        else: 
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(player.x + player.width // 2, round(player.y + player.height // 2),6,(0,0,0),facing))
    
    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False
    elif keys[pygame.K_RIGHT] and player.x < 500 - player.width - player.vel:
        player.x += player.vel
        player.left = False
        player.right = True
        player.standing = False
    else: 
        player.standing = True
        player.walkCount = 0
        
        

    if not player.isJump:    
        if keys[pygame.K_UP]:
            player.isJump = True
            player.left = False 
            player.right = False 
            
    else:
        if player.jumpCount >= -10:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount**2) * 0.5 * neg 
            player.jumpCount -= 1    

        else:
            player.isJump = False
            player.jumpCount = 10
    
    redrawGameWindow()    
     
    
pygame.quit()