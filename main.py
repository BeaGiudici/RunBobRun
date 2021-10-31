import pygame
import random as rnd
import numpy as np
import sys

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
GameOverfont = pygame.font.SysFont('Comic Sans MS', 100)
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
	def __init__(self):
		img = pygame.image.load('images/ghost_right.png')
		self.image = pygame.transform.scale(img, (player_width,player_height))
		self.rect = self.image.get_rect()
		#self.rect.x = x
		#self.rect.y = y
		self.vel_y = 0
		self.jumped = False
	
	def update(self):
		dx = 0
		dy = 0
		key = pygame.key.get_pressed()
		if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jumped == False:
			self.vel_y = -20
			self.jumped = True
		if key[pygame.K_SPACE] == False:
			self.jumped = False
		if key[pygame.K_LEFT]:
			img = pygame.image.load('images/ghost_left.png')
			self.image = pygame.transform.scale(img, (player_width,player_height))
			dx -= 5
		elif key[pygame.K_RIGHT]:
			img = pygame.image.load('images/ghost_right.png')
			self.image = pygame.transform.scale(img, (player_width,player_height))
			dx += 5

		
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
		#elif (self.rect.x > WIDTH - player_width):
		#	self.rect.x = WIDTH - player_width

		screen.blit(self.image, self.rect)




class Objet(pygame.sprite.Sprite):
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

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, x_min, x_max):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('images/unicorn_right.png')
		self.image = pygame.transform.scale(img, (70, 50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = 'right'	
		self.xmin = x_min
		self.xmax = x_max

	def update(self):
		if self.direction == 'right':
			dx = 2
		elif self.direction == 'left':
			dx = -2
		#Check if there are collision with objects or boundaries
		for object in objects:
			if (object.rect.colliderect(self.rect.x + dx, self.rect.y, 70, 50) and self.direction == 'right') or (self.rect.x + 70 + dx >= self.xmax):
				self.direction = 'left'
				img = pygame.image.load('images/unicorn_left.png')
				self.image = pygame.transform.scale(img, (70, 50))
				dx = 0
			elif (object.rect.colliderect(self.rect.x + dx, self.rect.y, 70, 50) and self.direction == 'left') or (self.rect.x + dx <= self.xmin):
				self.direction = 'right'
				img = pygame.image.load('images/unicorn_right.png')
				self.image = pygame.transform.scale(img, (70, 50))
				dx = 0

		self.rect.x += dx
		screen.blit(self.image, self.rect)
		
player = Player()
objects = pygame.sprite.Group()
pumpkins = pygame.sprite.Group()
enemies = pygame.sprite.Group()
pumpkins.add(Pumpkin(10,10)) # just a token for points tracking purpose
pumpkin_ctr = 0

levels = ['']

level1 = [
	'XXXXXXXXXXXXXXXXXX',
	'                  ',
	'               P  ',
	'           EXXXXX ',
	'         XXXX     ',
	'                  ',
	'G                 ',
	'XXXXXXXXXXXXXXXXXX'
]

#levels.append(level1)

level2 = [
	'XXXXXXXXXXXXXXXXXX',
	'                  ',
	'     XXXP         ',
	'       XX         ',
	'                  ',
	'            XX    ',
	'G           XX    ',
	'XXXXXXXXXXXXXXXXXX'
]

levels.append(level2)

level3 = [
	'XXXXXXXXXXXXXXXXXX',
	'                  ',
	'     XXXPX        ',
	'       XXX        ',
	'                  ',
	'            XX    ',
	'G      XE   XX    ',
	'XXXXXXXXXXXXXXXXXX'
]

levels.append(level3)

def setup_level(level):
	for j in range(len(level)):
		for i in range(len(level[j])):
			c = level[j][i]
			screen_x = 100*i
			screen_y = 100*j
			if c == 'X':
				objects.add(Objet(screen_x, screen_y, 100, 100, 'images/block.png'))
			if c == 'P':
				pumpkins.add(Pumpkin(screen_x + 50, screen_y + 50)) # add 50 so that the pumpkin stays on the ground
			if c == 'G':
				player.rect.x = screen_x + 10
				player.rect.y = screen_y + 10
			if c == 'E':
				enemies.add(Enemy(screen_x, screen_y + 50, screen_x - 200, screen_x + 200))

def destroy_level(objects, pumpkins, enemies):
	objects.empty()
	pumpkins.empty()
	enemies.empty()
		

def setup_initial_screen(level):
	pumpkins.add(Pumpkin(10,10)) # just a token for points tracking purpose
	setup_level(level)

setup_initial_screen(level1)
pumpkin_ctr = 0

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	screen.fill('pink')
	
	for level in levels:
		if player.rect.x + player_width / 2.0 >= WIDTH:
			destroy_level(objects, pumpkins, enemies)
			setup_initial_screen(level)
			pygame.display.update()
		
		else:
			for object in objects:
				object.draw()

			for enemy in enemies:
				# Check for collisions with the player
				if pygame.Rect.colliderect(player.rect, enemy.rect):
					screen.fill('pink')
					destroy_level(objects, pumpkins, enemies)
					run = False
				enemy.update()

			player.update()

			for pumpkin in pumpkins:
				if pygame.Rect.colliderect(player.rect, pumpkin.rect):
					pumpkin.rect.y = 10
					pumpkin.rect.x = 10
					pumpkin_ctr += 1
				text = myfont.render(': {}'.format(pumpkin_ctr), False, 'black')
				screen.blit(text, (57, 20))	
				pumpkin.draw()

			pygame.display.update()
		
	# Set the FPS
	clock.tick(30)

pygame.quit()
