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
    
    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else: 
            win.blit(char, (self.x,self.y))

def redrawGameWindow():
    win.blit(bg,(0,0))
    
    player.draw(win)
    
    pygame.display.update()

player = Player(300,400,64,64)
# main loop
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
    elif keys[pygame.K_RIGHT] and player.x < 500 - player.width - player.vel:
        player.x += player.vel
        player.left = False
        player.right = True
    else: 
        player.right = False
        player.left = False 
        walkCount = 0

    if not player.isJump:    
        if keys[pygame.K_SPACE]:
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