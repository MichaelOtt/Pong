import pygame, sys, random, socket
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

port=9029
myIP="127.0.0.1"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((myIP, 9028))

def connectToServer(ip, sock):
	sock.sendto("ready".encode(), (ip, 9029))
	while True:
		data, addr = sock.recvfrom(1024)
		if(data.decode()=="ready"):
			break
	serverIP=ip
	print ("Connected!")
	
def sendInfo(mousey, ip):
	sock.sendto(str(int(mousey)).encode(), (ip, port))
def receiveInfo():
	#return p1y, p2y, ballx, bally, p1points, p2points
	infostring, addr=sock.recvfrom(1024)
	values=infostring.decode().split(":")
	return int(values[0]), int(values[1]), int(values[2]), int(values[3]), int(values[4]), int(values[5])

def draw(surface, p1, p2, ballx, bally, radius, p1points, p2points):
	surface.fill((0,0,0))
	textsurface = myfont.render(str(p1points), False, (255,255,255))
	surface.blit(textsurface, (width/2-100,20))
	textsurface = myfont.render(str(p2points), False, (255,255,255))
	surface.blit(textsurface, (width/2+100,20))
	pygame.draw.rect(surface, (255,255,255), p1)
	pygame.draw.rect(surface, (255,255,255), p2)
	pygame.draw.circle(surface, (255,255,255), (int(ballx), int(bally)), ballradius)
	
ip=input("What is the IP of the server?")
connectToServer(ip, sock)
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 24)
COMEVENT = pygame.USEREVENT+2
pygame.time.set_timer(COMEVENT, int(1000/100))
DISPLAYSURF = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pong!')
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEMOTION:
			_, mousey = pygame.mouse.get_pos()
		if event.type == COMEVENT:
			sendInfo(mousey, ip)
			p1y, p2y, ballx, bally, p1points, p2points = receiveInfo()
			p1.top = p1y
			p2.top = p2y
	draw(DISPLAYSURF, p1, p2, ballx, bally, ballradius, p1points, p2points)
	pygame.display.update()
