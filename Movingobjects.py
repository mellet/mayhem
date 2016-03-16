#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
import math

class Movingobject(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.gravity = Vector2D(0,2)
		self.maxspeed = 10
		self.pos = Vector2D(SCREEN_X/2 - 22, SCREEN_Y/2 - 22)
		self.direction = Vector2D(0,-1)

	def rotate(self):
		"""The math behind finding the new direction with an angle"""
		x = self.direction.x * math.cos(math.radians(-self.angle)) - self.direction.y * math.sin(math.radians(-self.angle))
		y = self.direction.x * math.sin(math.radians(-self.angle)) + self.direction.y * math.cos(math.radians(-self.angle))
		new_speed = Vector2D(x, y)

		return new_speed

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("sprites/ship.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.engineOn = False
		self.turnLeft = False
		self.turnRight = False
		self.fuel = 1000
		self.angle = 0
		self.shots = []


	def logic(self, screen):
		self.speed_limit()
		self.move()
		#pygame.draw.rect(screen,RED,(self.pos.x,self.pos.y,45,45))

	def move(self):
		if self.turnLeft:
			self.angle += 4
		if self.turnRight:
			self.angle -= 4
		
		new_speed = self.rotate()

		if self.engineOn and self.fuel>0:
			self.image = pygame.image.load("sprites/ship_engine_on.png").convert_alpha()
			self.image = pygame.transform.rotate(self.image, self.angle)
			self.rect = self.image.get_rect()
			self.direction *= 1.3
			self.pos += new_speed + self.gravity
			self.rect.center = (self.pos.x + 22, self.pos.y + 22)
			self.fuel -=1
			
			#set fuel not to go under 0
			if self.fuel <= 0:
				self.fuel = 0
		else:
			self.image = pygame.image.load("sprites/ship.png").convert_alpha()
			self.image = pygame.transform.rotate(self.image, self.angle)
			self.rect = self.image.get_rect()
			self.direction /= 1.1
			self.pos += new_speed + self.gravity
			self.rect.center = (self.pos.x + 22, self.pos.y + 22)


	def speed_limit(self):
		if self.direction.magnitude() > self.maxspeed:
			self.direction = self.direction.normalized() * self.maxspeed

	def shoot(self):
		return Bullet(self.rect, self.rotate())
		#self.shots.append(Bullet(self.pos, self.rotate()))
			
	def refule(self):
		pass

class Bullet(Movingobject):
	"""The bullet class"""
	def __init__(self, rect, direc):
		super().__init__()
		self.dir = direc
		self.image = pygame.image.load("sprites/bullet.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.pos.x = rect.center[0] - self.rect.width/2
		self.pos.y = rect.center[1]

	def move(self):
		self.pos += self.dir.normalized() * 20
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def logic(self):
		self.move()
		#pygame.draw.circle(screen, RED, (int(self.pos.x),int(self.pos.y)), self.radius)