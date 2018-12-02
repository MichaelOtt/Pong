import pygame, sys, random, socket, threading
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
dx = 0
dy = 0
p1points = 0
p2points = 0

myIP='0.0.0.0'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

p2center=0

def connectToClient():#needs to be blocking

	sock.bind((myIP, 9029))
	while True:
		data, addr = sock.recvfrom(1024)
		if(data.decode()=="ready"):
			break
	sock.sendto("ready".encode(), addr)
	t=threading.Thread(target=receiveThread)
	t.start()

	print ("Connected!")
	return addr
	
	
def sendInfo(p1y, p2y, ballx, bally, p1points, p2points, clientAddress):
	infoString=str(int(p1y))+":"+str(int(p2y))+":"+str(int(ballx))+":"+str(int(bally))+":"+str(int(p1points))+":"+str(int(p2points))
	sock.sendto(infoString.encode(), clientAddress)
def receiveInfo():
	data, addr = sock.recvfrom(1024)
	return int(data.decode())
def receiveThread():
	global p2center
	while True:
		p2center= receiveInfo()
def resetBall():
	ballx = width/2
	bally = height/2
	dx = random.random()*5+1
	if (random.random() < 0.5):
		dx *= -1
	dy = random.random()*10-5
	return ballx, bally, dx, dy

def updateState(ballx, bally, ballradius, dx, dy, p1points, p2points, p1, p2):
	ballx += dx
	bally += dy
	if (bally <= 0):
		bally *= -1
		dy *= -1
	elif (bally >= height):
		bally = 2*height-bally
		dy *= -1
	if (ballx <= 0):
		ballx, bally, dx, dy = resetBall()
		p2points+=1
	elif (ballx >= width):
		ballx, bally, dx, dy = resetBall()
		p1points+=1
	ballrect = pygame.Rect(ballx-ballradius/2, bally-ballradius/2, ballradius, ballradius)
	if (ballrect.colliderect(p1)):
		ballx = p1.right+ballradius/2+1
		dx *= -1
	if (ballrect.colliderect(p2)):
		ballx = p2.left-ballradius/2-1
		dx *= -1
	return ballx, bally, dx, dy, p1points, p2points, p1, p2

def draw(surface, p1, p2, ballx, bally, radius, p1points, p2points):
	surface.fill((0,0,0))
	textsurface = myfont.render(str(p1points), False, (255,255,255))
	surface.blit(textsurface, (width/2-100,20))
	textsurface = myfont.render(str(p2points), False, (255,255,255))
	surface.blit(textsurface, (width/2+100,20))
	pygame.draw.rect(surface, (255,255,255), p1)
	pygame.draw.rect(surface, (255,255,255), p2)
	pygame.draw.circle(surface, (255,255,255), (int(ballx), int(bally)), ballradius)
	
clientAddress=connectToClient()
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 24)
UPDATEEVENT = pygame.USEREVENT+1
COMEVENT = pygame.USEREVENT+2
pygame.time.set_timer(UPDATEEVENT, int(1000/120))
pygame.time.set_timer(COMEVENT, int(1000/100))
DISPLAYSURF = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pong!')
ballx, bally, dx, dy = resetBall()
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEMOTION:
			_, mousey = pygame.mouse.get_pos()
			p1.center = (p1.left+p1.width/2, mousey)
		if event.type == UPDATEEVENT:
			ballx, bally, dx, dy, p1points, p2points, p1, p2 = updateState(ballx, bally, ballradius, dx, dy, p1points, p2points, p1, p2)
		if event.type == COMEVENT:
			sendInfo(p1.top, p2.top, ballx, bally, p1points, p2points, clientAddress)
			p2.center = (p2.left+p2.width/2, p2center)
	draw(DISPLAYSURF, p1, p2, ballx, bally, ballradius, p1points, p2points)
	pygame.display.update()
