import sys 
import os
sys.path.append(os.path.join(sys.path[0],'..','lib'))
import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

imgPath = "../images/"

walkRight = [pygame.image.load(str.join(imgPath,'R1.png')),pygame.image.load(str.join(imgPath,'R2.png')),pygame.image.load(str.join(imgPath,'R3.png')),pygame.image.load(str.join(imgPath,'R4.png')),pygame.image.load(str.join(imgPath,'R5.png')),]
walkLeft = [pygame.image.load(str.join(imgPath,'L1.png')),pygame.image.load(str.join(imgPath,'L2.png')),pygame.image.load(str.join(imgPath,'L3.png')),pygame.image.load(str.join(imgPath,'L4.png')),pygame.image.load(str.join(imgPath,'L5.png')),]
bg = pygame.image.load(str.join(imgPath,'standing.png'))
char = pygame.image.load(str.join(imgPath,'standing.png'))

x = 50
y = 50
width = 40
height = 60
vel = 5

isJumping = False
jumpCount = 10
left = False 
right = False 

run = True

while run:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel

    if keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x += vel

    if not isJumping:    
        if keys[pygame.K_SPACE]:
            isJumping = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount**2) * 0.5 * neg 
            jumpCount -= 1    

        else:
            isJumping = False
            jumpCount = 10
    
    win.fill((0,0,0))  # Fills the screen with black
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.display.update() 
    
pygame.quit()