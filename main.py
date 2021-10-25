import pygame
import random as rnd
import numpy as np
import sys

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
pygame.display.set_caption('Escape')
clock = pygame.time.Clock()

WIDTH = 1800
HEIGHT = 800
GRAVITY = 10
player_width = 60
player_height = 80

#Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Creating player class
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		img = pygame.image.load('images/ghost_right.png')
		self.image = pygame.transform.scale(img, (player_width,player_height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vel_y = 0
		self.jumped = False
	
	def is_aabb_collision(self, other):
		# Axis Aligned Bounding Box
		x_collision = (np.fabs(self.rect.x - other.x)*2) < (player_width + other.width)
		y_collision = (np.fabs(self.rect.y - other.y) * 2) < (player_height + other.height)
		return (x_collision and y_collision)
	
	def update(self):
		dx = 0
		dy = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] and self.jumped == False:
			self.vel_y = -22
			self.jumped = True
		if key[pygame.K_SPACE] == False:
			self.jumped = False
		if key[pygame.K_LEFT]:
			img = pygame.image.load('images/ghost_left.png')
			self.image = pygame.transform.scale(img, (player_width,player_height))
			dx -= 10
		elif key[pygame.K_RIGHT]:
			img = pygame.image.load('images/ghost_right.png')
			self.image = pygame.transform.scale(img, (player_width,player_height))
			dx += 10

		
		# Add gravity
		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y
		
		# Check for collision
		for object in objects:
			#check for collision on the left
			if object.rect.colliderect(self.rect.x + dx, self.rect.y, player_width, player_height):
				dx = 0
			#check for collision in y direction
			if object.rect.colliderect(self.rect.x, self.rect.y + dy, player_width, player_height):
				if self.vel_y < 0:
					dy = object.rect.bottom - self.rect.top
					self.vel_y = 0
				elif self.vel_y >= 0:
					dy = object.rect.top - self.rect.bottom
					self.vel_y = 0
		
		# Update player position
		self.rect.x += dx
		self.rect.y += dy
		dy += GRAVITY
		#Check if the player reaches the borders
		if (self.rect.x < 0):
			self.rect.x = 0
		elif (self.rect.x > WIDTH - player_width):
			self.rect.x = WIDTH - player_width

		screen.blit(self.image, self.rect)




class BKG_objet(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, img_path):
		pygame.sprite.Sprite.__init__(self)
		self.width = width
		self.height = height
		img = pygame.image.load(img_path)
		self.image = pygame.transform.scale(img, (width,height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	
	def draw(self):
		screen.blit(self.image, self.rect)

class Pumpkin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('images/pumpkin.png')
		self.image = pygame.transform.scale(img, (50,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	
	def draw(self):
		screen.blit(self.image, self.rect)

player = Player(200,520)
objects = [] 
objects.append(BKG_objet(0, 600, WIDTH, 200, 'images/block.png'))
objects.append(BKG_objet(600,400, 100, 200, 'images/block.png'))
objects.append(BKG_objet(1300, 200, 100, 100, 'images/block.png'))
pumpkins = []
pumpkins.append(Pumpkin(1350, 150))
pumpkin_ctr = 0
pumpkin_token = Pumpkin(10,10)

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	screen.fill('pink')	
	for object in objects:
		object.draw()

	player.update()
	pumpkin_token.draw()

	for pumpkin in pumpkins:
		if pygame.Rect.colliderect(player.rect, pumpkin.rect):
			pumpkin.rect.y = 900
			pumpkin_ctr += 1
		text = myfont.render(': {}'.format(pumpkin_ctr), False, 'black')
		screen.blit(text, (57, 20))	
		pumpkin.draw()

	
	pygame.display.update()

	# Set the FPS
	clock.tick(30)

pygame.quit()
