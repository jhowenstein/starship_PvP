import pygame, sys, math, time
from pygame.locals import *
from enum import IntEnum
from starships import *
from weapons import *
from projectiles import *
import numpy as np



class Game(object):
	def __init__(self, numberPlayers):
		self.status = True # Defines whether the game is currenty active and valid
		self.numberPlayers = numberPlayers
		
		self.objectList = []
		self.projectileList = []
		self.objectGarbage = []
		self.projectileGarbage = []
		self.impactList = []
		#self.commandList = []
		
		if self.numberPlayers == 1:
			self.player1 = Player("Player One")
			self.level = None
		elif self.numberPlayers == 2:
			self.player1 = Player("Player One")
			self.player2 = Player("Player Two")
			
		self.AI = False

		self.WINDOWHEIGHT = 600
		self.WINDOWWIDTH = 1000
		
		self.incidenceMap = np.zeros((self.WINDOWHEIGHT, self.WINDOWWIDTH))
		
		self.DISPLAYSURF = 0 # Display surface to be initialize prior to game loop
		
		self.BG_COLOR = (0, 0, 0) # Default = Black
		
		self.endCondition = 0
		
		self.counter = 0
		
class Player(object):
	def __init__(self, name):
		self.name = name
		self.ship = None
		self.status = True

		self.userControl = Control.Keyboard_A
		
		self.keyDown = np.zeros(6)
		self.keyUp = np.zeros(6)
		
		
class Command(IntEnum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4
	PRIMARY = 5
	SECONDARY = 6

class Control(IntEnum):
	Keyboard_A = 1
	Keyboard_B = 2
	Controller_A = 3
	Controller_B = 4
	
class Ship(IntEnum):
	Basic = 1
	Light = 2
	Heavy = 3

'''	
def createShip(game, shipType, location):
	if shipType == Ship.Basic:
		game.objectList.append(BasicShip(location[0],location[1]))
	elif shipType == Ship.Light:
		game.objectList.append(LightShip(location[0],location[1]))
	elif shipType == Ship.Heavy:
		game.objectList.append(HeavyShip(location[0],location[1]))
'''


def processInput(game):
	# Process input player 1
	
	if game.player1.userControl == Control.Keyboard_A:
		eventList = pygame.event.get()
		for event in eventList:
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			handleKeyboard(game.player1, event)
			'''
			if event.type == KEYDOWN:
				if event.key == K_UP:
					game.player1.keyDown[0] = 1
				elif event.key == K_DOWN:
					game.player1.keyDown[1] = 1
				elif event.key == K_LEFT:
					game.player1.keyDown[2] = 1
				elif event.key == K_RIGHT:
					game.player1.keyDown[3] = 1
				elif event.key == K_SPACE:
					game.player1.keyDown[4] = 1
				elif event.key == K_x:
					game.player1.keyDown[5] = 1
			elif event.type == KEYUP:
				if event.key == K_UP:
					game.player1.keyUp[0] = 1
				elif event.key == K_DOWN:
					game.player1.keyUp[1] = 1
				elif event.key == K_LEFT:
					game.player1.keyUp[2] = 1
				elif event.key == K_RIGHT:
					game.player1.keyUp[3] = 1
				elif event.key == K_SPACE:
					game.player1.keyUp[4] = 1
				elif event.key == K_x:
					game.player1.keyUp[5] = 1
			'''
	elif game.userControl == Control.Controller:
		print("Controller not yet supported")
		pygame.quit()
		sys.exit()
	
	translateCommands(game.player1)
	'''
	if game.player1.keyDown[0]:
		game.player1.ship.commandList.append(Command.UP)
	if game.player1.keyDown[1]:
		game.player1.ship.commandList.append(Command.DOWN)
	if game.player1.keyDown[2]:
		game.player1.ship.commandList.append(Command.LEFT)
	if game.player1.keyDown[3]:
		game.player1.ship.commandList.append(Command.RIGHT)
	if game.player1.keyDown[4]:
		game.player1.ship.commandList.append(Command.PRIMARY)
	if game.player1.keyDown[5]:
		game.player1.ship.commandList.append(Command.SECONDARY)
		
	for i in range(game.player1.keyDown.size):
		if game.player1.keyUp[i] == 1:
			game.player1.keyDown[i] = 0
			
	game.player1.keyUp = np.zeros(6)
	'''

def updateGame(game):
	game.counter += 1
	game.DISPLAYSURF.fill(game.BG_COLOR)
	game.incidenceMap = np.zeros((game.WINDOWHEIGHT, game.WINDOWWIDTH))
	
	if len(game.impactList) > 0:
		handleImpact(game)
	
	game.player1.status = game.player1.ship.update(game)
	
	#statusPlayer2 = game.player2.ship.update(game)
	
	if game.AI == True:
		game.level.updateAI(game, game.counter)
		
	i = 0
	while (i < len(game.objectList)):
		alive = game.objectList[i].update(game)
		if alive == False:
			game.objectGarbage.append(i)
		i += 1

	i = 0
	while (i < len(game.projectileList)):
		alive = game.projectileList[i].update(game)
		if alive == False:
			game.projectileGarbage.append(i)
		i += 1
		
	if len(game.objectGarbage) > 0:
		for i in range(len(game.objectGarbage)-1, -1, -1):
			game.objectList.pop(game.objectGarbage[i])

	if len(game.projectileGarbage) > 0:
		for i in range(len(game.projectileGarbage)-1, -1, -1):
			game.projectileList.pop(game.projectileGarbage[i])

	game.objectGarbage = []
	game.projectileGarbage = []
	
	game.status = gameStatus(game)

def handleImpact(game):
	for impact in game.impactList:
		if impact.locID == 1:
			game.player1.ship.damageList.append(impact.damage)
		elif impact.locID == 2:
			game.player2.ship.damageList.append(impact.damage)
		else:
			for entity in game.objectList:
				if entity.ID == impact.locID:
					entity.damageList.append(impact.damage)
	
	game.impactList = []
	
def gameStatus(game):
	#print(len(game.objectList))
	if game.numberPlayers == 1:
		if game.player1.status == False:
			game.endCondition = -1
			return False
		elif len(game.objectList) == 0:
			game.endCondition = 1
			return False
	elif game.numberPlayers == 2:
		if game.player1.status == False and game.player2.status == False:
			game.endCondition = -1 # Should be own error code
			return False
		elif game.player1.status == False:
			game.endCondition = 2
			return False
		elif game.player2.status == False:
			game.endCondition = 1
			return False
			
	return True
	
def finalScreen(game):
	if game.endCondition == -1:
		# Game Over
		game.DISPLAYSURF.fill(game.BG_COLOR)
		fontObj = pygame.font.Font('freesansbold.ttf',48)
		textSurfaceObj = fontObj.render('GAME OVER!', True, (255,255,255))
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (500,300)
		game.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
		pygame.display.update()
		time.sleep(5)
	elif game.endCondition == 1:
		# Player 1 Wins
		game.DISPLAYSURF.fill(game.BG_COLOR)
		fontObj = pygame.font.Font('freesansbold.ttf',48)
		textSurfaceObj = fontObj.render('PLAYER 1 WINS!', True, (255,255,255))
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (500,300)
		game.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
		pygame.display.update()
		time.sleep(5)
	elif game.endCondition == 2:
		# Player 2 Wins
		game.DISPLAYSURF.fill(game.BG_COLOR)
		fontObj = pygame.font.Font('freesansbold.ttf',48)
		textSurfaceObj = fontObj.render('PLAYER 2 WINS!', True, (255,255,255))
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (500,300)
		game.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
		pygame.display.update()
		time.sleep(5)
	elif game.endCondition == 0:
		# Error! Unexpected Game Exit
		game.DISPLAYSURF.fill(game.BG_COLOR)
		fontObj = pygame.font.Font('freesansbold.ttf',48)
		textSurfaceObj = fontObj.render('Error. Unexpected Game Exit', True, (255,255,255))
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (500,300)
		game.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
		pygame.display.update()
		time.sleep(5)
	
def handleKeyboard(player, event):
	if player.userControl = Control.Keyboard_A:
		if event.type == KEYDOWN:
			if event.key == K_UP:
				player.keyDown[0] = 1
			elif event.key == K_DOWN:
				player.keyDown[1] = 1
			elif event.key == K_LEFT:
				player.keyDown[2] = 1
			elif event.key == K_RIGHT:
				player.keyDown[3] = 1
			elif event.key == K_SPACE:
				player.keyDown[4] = 1
			elif event.key == K_x:
				player.keyDown[5] = 1
		elif event.type == KEYUP:
			if event.key == K_UP:
				player.keyUp[0] = 1
			elif event.key == K_DOWN:
				player.keyUp[1] = 1
			elif event.key == K_LEFT:
				player.keyUp[2] = 1
			elif event.key == K_RIGHT:
				player.keyUp[3] = 1
			elif event.key == K_SPACE:
				player.keyUp[4] = 1
			elif event.key == K_x:
				player.keyUp[5] = 1
	if player.userControl = Control.Keyboard_B:
		if event.type == KEYDOWN:
			if event.key == K_w:
				player.keyDown[0] = 1
			elif event.key == K_s:
				player.keyDown[1] = 1
			elif event.key == K_a:
				player.keyDown[2] = 1
			elif event.key == K_d:
				player.keyDown[3] = 1
			elif event.key == K_q:
				player.keyDown[4] = 1
			elif event.key == K_e:
				player.keyDown[5] = 1
		elif event.type == KEYUP:
			if event.key == K_w:
				player.keyUp[0] = 1
			elif event.key == K_s:
				player.keyUp[1] = 1
			elif event.key == K_a:
				player.keyUp[2] = 1
			elif event.key == K_d:
				player.keyUp[3] = 1
			elif event.key == K_q:
				player.keyUp[4] = 1
			elif event.key == K_e:
				player.keyUp[5] = 1

def translateCommands(player):
	if player.keyDown[0]:
		player.ship.commandList.append(Command.UP)
	if player.keyDown[1]:
		player.ship.commandList.append(Command.DOWN)
	if player.keyDown[2]:
		player.ship.commandList.append(Command.LEFT)
	if player.keyDown[3]:
		player.ship.commandList.append(Command.RIGHT)
	if player.keyDown[4]:
		player.ship.commandList.append(Command.PRIMARY)
	if player.keyDown[5]:
		player.ship.commandList.append(Command.SECONDARY)
		
	for i in range(player.keyDown.size):
		if player.keyUp[i] == 1:
			player.keyDown[i] = 0
			
	player.keyUp = np.zeros(6)

			
				
