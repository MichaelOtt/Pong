import pygame, sys, random
from pygame.locals import *

paddleheight = 50
paddlewidth = 10
ballradius = 5
width = 800
height = 600
p1 = pygame.Rect(10, height/2-paddleheight/2, paddlewidth, paddleheight)
p2 = pygame.Rect(width-10-paddlewidth, height/2-paddleheight/2, paddlewidth, paddleheight)
ballx = 0
bally = 0
p1points = 0
p2points = 0
mousey = height/2

def sendInfo(mousey):
	garbage = 0
def receiveInfo():
	#return p1y, p2y, ballx, bally, p1points, p2points
	return 0, 0, 0, 0, 0, 0

def draw(surface, p1, p2, ballx, bally, radius, p1points, p2points):
	surface.fill((0,0,0))
	textsurface = myfont.render(str(p1points), False, (255,255,255))
	surface.blit(textsurface, (width/2-100,20))
	textsurface = myfont.render(str(p2points), False, (255,255,255))
	surface.blit(textsurface, (width/2+100,20))
	pygame.draw.rect(surface, (255,255,255), p1)
	pygame.draw.rect(surface, (255,255,255), p2)
	pygame.draw.circle(surface, (255,255,255), (int(ballx), int(bally)), ballradius)
	
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 24)
COMEVENT = pygame.USEREVENT+2
pygame.time.set_timer(COMEVENT, int(1000/10))
DISPLAYSURF = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pong!')
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEMOTION:
			mousey = pygame.mouse.get_pos()
		if event.type == COMEVENT:
			sendInfo(mousey)
			p1y, p2y, ballx, bally, p1points, p2points = receiveInfo()
			p1.top = p1y
			p2.top = p2y
	draw(DISPLAYSURF, p1, p2, ballx, bally, ballradius, p1points, p2points)
	pygame.display.update()