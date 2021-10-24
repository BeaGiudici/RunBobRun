import pygame
import random as rnd
import numpy as np
import sys

pygame.init()
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
	
	def is_aabb_collision(self, other):
		# Axis Aligned Bounding Box
		x_collision = (np.fabs(self.rect.x - other.x)*2) < (player_width + other.width)
		y_collision = (np.fabs(self.rect.y - other.y) * 2) < (player_height + other.height)
		return (x_collision and y_collision)
	
	def update(self):
		dx = 0
		dy = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			img = pygame.image.load('images/ghost_left.png')
			self.image = pygame.transform.scale(img, (player_width,player_height))
			dx -= 10
			dy = 0
		elif key[pygame.K_RIGHT]:
			img = pygame.image.load('images/ghost_right.png')
			self.image = pygame.transform.scale(img, (player_width,player_height))
			dx += 10
			dy = 0
		elif key[pygame.K_UP]:
			dx = 0
			dy -= 24
		elif key[pygame.K_DOWN]:
			dx = 0
			dy += 24
	
		# Check for collision


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
	def __init__(self, x, y, width, height, color='white'):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
	
	def draw(self):
		pygame.draw.rect(screen, self.color, self.rect)


player = Player(200,520)
objects = [] 
objects.append(BKG_objet(0, 600, WIDTH, 200, color='gold'))
objects.append(BKG_objet(0,0, WIDTH, 600, color='white'))


run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	for object in objects:
		object.draw()
	
	player.update()
	
	for object in objects:
		if player.is_aabb_collision(object):
			if player.rect.x + player_width < object.x:
			# Player is to the left
				player.rect.x = object.x - object.width/2.0 - player_width/2.0
			elif player.rect.y + player_height < object.y:
				# Player is above
				player.dy = 0
				player.rect.y = object.y - object.height / 2.0 - player_height/2.0
	
	pygame.display.flip()

	# Set the FPS
	clock.tick(30)

pygame.quit()
