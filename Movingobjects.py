#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
import math

class Movingobject(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.gravity = Vector2D(0,2)
		self.maxspeed = 5
		self.pos = Vector2D(SCREEN_X/2 - 22, SCREEN_Y/2 - 22)
		self.direction = Vector2D(0,-1)

	def rotate(self):
		"""The math behind finding the new direction with an angle"""
		x = self.direction.x * math.cos(math.radians(-self.angle)) - self.direction.y * math.sin(math.radians(-self.angle))
		y = self.direction.x * math.sin(math.radians(-self.angle)) + self.direction.y * math.cos(math.radians(-self.angle))
		new_speed = Vector2D(x, y)

		return new_speed

	def update_sprite(self, img):
		oldrect = self.rect
		self.image = pygame.image.load(img).convert_alpha()
		self.image = pygame.transform.scale(self.image,(30,30))
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center) # Reposition sprite to its center

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __init__(self, uid):
		super().__init__()
		self.uid = uid
		self.image = pygame.image.load("sprites/ship.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.engineOn = False
		self.turnLeft = False
		self.turnRight = False
		self.refuel = False
		self.fuel = 1000
		self.maxfuel = 1000
		self.score = 0
		self.angle = 0
		self.shots = []
		if self.uid == 1:
			self.spawn = Vector2D(300,350)
			self.pos = self.spawn
		elif self.uid == 2:
			self.spawn = Vector2D(1075, 210)
			self.pos = self.spawn


	def logic(self, screen):
		"""Logic method of rocket"""
		self.speed_limit()
		self.move()
		self.screen_wrap()
		self.fule()
		#Hitbox for bugtesting
		#pygame.draw.rect(screen,RED,(self.rect.x,self.rect.y,self.rect.height,self.rect.width))

	def move(self):
		"""move method of rocket"""

		if self.turnLeft:
			self.angle += 4
		if self.turnRight:
			self.angle -= 4

		#Reset angle if it goes over 360 back to 0
		if self.angle > 360:
			self.angle = 0
		if self.angle < -360:
			self.angle = 0
		
		new_speed = self.rotate()

		#Movement if engine is on
		if self.engineOn and self.fuel>0:
			self.update_sprite("sprites/ship_engine_on.png")
			self.direction *= 1.5
			if self.refuel is False:
				self.pos += new_speed #+ self.gravity/2
			self.rect.center = (self.pos.x, self.pos.y)
			self.refuel = False
			self.fuel -=1
			
			#set fuel not to go under 0
			if self.fuel <= 0:
				self.fuel = 0
		else:
			self.update_sprite("sprites/ship.png")
			if self.direction.magnitude() > 0.5 and self.refuel is False:
				self.direction /= 1.04
				self.pos += new_speed + self.gravity
			else:
				self.pos += self.gravity
			self.rect.center = (self.pos.x, self.pos.y)

			#Rotate slowly back to 0 deg if engine is off
			if 1 < self.angle < -1:
				self.angle = 0
			else:
				if self.angle < 0:
					self.angle += 1
				if self.angle > 0:
					self.angle -= 1

	def speed_limit(self):
		"""Speed_limit method of rocket"""
		if self.direction.magnitude() > self.maxspeed:
			self.direction = self.direction.normalized() * self.maxspeed

	def shoot(self):
		"""Shoot method of rocket"""
		return Bullet(self.rect, self.rotate(), self.uid)

	def screen_wrap(self):
		"""Screen_wrap method of rocket"""
		#Left
		if self.pos.x <= 0:
			self.pos.x = SCREEN_X - 1
		#Right
		if self.pos.x >= SCREEN_X:
			self.pos.x = 1
		#Bottom
		if self.pos.y >= SCREEN_Y:
			self.pos.y = 1
		#Top
		if self.pos.y <= 0:
			self.pos.y = SCREEN_Y

	def fule(self):
		if self.fuel > self.maxfuel:
			self.fuel = self.maxfuel
		if self.refuel and self.fuel < self.maxfuel:
			self.fuel += 1

class Bullet(Movingobject):
	"""The bullet class"""
	def __init__(self, rect, direc, uid):
		super().__init__()
		self.uid = uid
		self.dir = direc
		self.image = pygame.image.load("sprites/bullet.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.pos.x = rect.center[0] - self.rect.width/2
		self.pos.y = rect.center[1]

	def move(self):
		self.pos += self.dir.normalized() * 15
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def logic(self):
		self.move()