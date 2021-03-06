import pygame, sys, math
from pygame.locals import *
from enum import IntEnum
from starship_game_functions import *
from starships import *
from projectiles import *
#from survival import *

class Weapon(object):
	def __init__(self):
		self.cooldownTime = 10

	def release(self, locX, locY, direction, game):
		pass
		#n = len(game.objectList)
		#game.objectList.append(Projectile(locX, locY, direction, n))


class BasicCannon(Weapon):
	def __init__(self):
		self.cooldownTime = 10

	def release(self, locX, locY, direction, game):
		game.projectileList.append(BasicProjectile(locX, locY, direction))


class LightCannon(Weapon):
	def __init__(self):
		self.cooldownTime = 5

	def release(self, locX, locY, direction, game):
		game.projectileList.append(LightProjectile(locX, locY, direction))


class HeavyCannon(Weapon):
	def __init__(self):
		self.cooldownTime = 20

	def release(self, locX, locY, direction, game):
		game.projectileList.append(HeavyProjectile(locX, locY, direction))

class CustomCannon(Weapon):
	def __init__(self):
		self.cooldownTime = 10
		self.projectileSpeed = 5
		self.projectileDamage = 10

	def release(self, locX, locY, direction, game):
		newProjectile = BasicProjectile(locX, locY, direction)
		newProjectile.velocity = self.projectileSpeed
		newProjectile.damage = self.projectileDamage
		game.projectileList.append(newProjectile)
