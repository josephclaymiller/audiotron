import sys
import math
import threading
import random
import gc

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Point3
from pandac.PandaModules import Vec3
from pandac.PandaModules import CollisionHandlerEvent
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionPlane
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import Plane
from pandac.PandaModules import BitMask32
from pandac.PandaModules import NodePath, PandaNode

import config
import CollisionBitMasks
from WiimoteManager import WiimoteManager
from WiimoteEmulator import WiimoteEmulator
from Enemy import Enemy
from EnemyManager import EnemyManager
from EnemyData import enemyData, levelData
from Player import Player
from tunnel import Tunnel
from music import MusicController
from hud import HUD

#trial delete
from pandac.PandaModules import DirectionalLight, AmbientLight #needed to setup lighting
from pandac.PandaModules import VBase3, VBase4


class World (DirectObject):

	def __init__(self):
		self.wiimoteManager = WiimoteManager()
		self.wiimoteManager.setDaemon(True)
		
		if config.EMULATE_WIIMOTE:
			self.wiimoteEmulator = WiimoteEmulator(self.wiimoteManager)
		
		self.accept('escape', sys.exit)
		#self.accept('m', self.garbageDebug)
		#self.accept('e', self.spawnMoreEnemy)
	
	
	def garbageDebug(self):
		#print gc.get_objects()
		#self.musicController.debugPrint()
		render.ls()
			
	def spawnMoreEnemy(self, task):
		time = globalClock.getRealTime()
		
		if (self.enemyManager.level == len(levelData)):
			return Task.done
			
		elif (time > self.nextSpawnTime):
			currentEnemies = self.enemyManager.getCurrentEnemyTypes()
			unlockedEnemies = self.enemyManager.getUnlockedEnemyTypes()
			
			if (len(unlockedEnemies) == 0 or random.random() < 0.6):
				typeToSpawn = random.choice(currentEnemies)
			else:
				typeToSpawn = random.choice(unlockedEnemies)
			
			level = self.enemyManager.level
			numFormations = 1 #random.randint(1, 1 + level / 2)
			
			for i in range(numFormations):
			
				numToSpawn = random.randint(3 + math.floor(level / 2), 5 + level)	
				formation = random.randint(0, 2)
				pos = Point3(random.uniform(-2.5, 2.5), 0, random.uniform(-2.5, 2.5))
				
				if formation == 0:
					handle = self.enemyManager.spawnCircle(typeToSpawn, numToSpawn, random.uniform(0.5, 2.5), startPos = pos)
				elif formation == 1:
					handle = self.enemyManager.spawnSpiral(typeToSpawn, numToSpawn, random.uniform(0.5, 2.5), random.choice((-1, 1)), startPos = pos)
				else:
					if (numToSpawn % 3 == 0):
						cols = 3
					elif (numToSpawn % 2 == 0 or numToSpawn > 5):
						cols = 2
					else:
						cols = 1
						
					handle = self.enemyManager.spawnRect(typeToSpawn, int(math.floor(numToSpawn / cols)), cols, startPos = pos)
				
				movement = random.randint(0, 1)
				if movement == 0:
					self.enemyManager.moveForward(handle)
				elif movement == 1:
					self.enemyManager.moveSpiral(handle, random.choice((-1, 1)))
			
			self.nextSpawnTime += self.spawnRate
		
		return Task.cont
		
		
	def start(self):
		base.setBackgroundColor(0,0,0) #set the background color to black
		self.playerHandle=NodePath(PandaNode("PlayerHandle"))
		self.setupCollision()
		self.musicController = MusicController()
		self.HUD = HUD(self.playerHandle)
		self.player = Player(self.playerHandle, self.wiimoteManager, self.musicController, self.HUD)
		self.enemyManager = EnemyManager(self.musicController, self.HUD, self.player)
		self.tunnel = Tunnel(self.musicController)
		
		self.spawnRate = self.musicController.secondsPerSixteenth * 16
		self.nextSpawnTime = globalClock.getRealTime() + self.spawnRate
		taskMgr.add(self.spawnMoreEnemy, "spawnMoreEnemy")
		
		self.accept('r', self.player.hitByEnemy)
		
		if config.EMULATE_WIIMOTE:
			taskMgr.add(self.wiimoteEmulator.update, "updateEmulator")
		else:
			self.wiimoteManager.start()
	
	def setupCollision(self):
		self.cHandler = CollisionHandlerEvent()
		self.cHandler.setInPattern("%fn-into-%in")
		base.cHandler = self.cHandler

		self.cTrav = CollisionTraverser()
		base.cTrav = self.cTrav
		
		enemyKillPlane = CollisionPlane(Plane(Vec3(0, 1, 0), Point3(0, -10, 0)))
		cKillPlaneNode = CollisionNode('cEnemyKillPlane')
		cKillPlaneNode.setFromCollideMask(BitMask32.allOff())
		cKillPlaneNode.setIntoCollideMask(CollisionBitMasks.enemyMask)
		cKillPlaneNode.addSolid(enemyKillPlane)
		cNodePath = render.attachNewNode(cKillPlaneNode)
		cNodePath.show()
		base.cTrav.addCollider(cNodePath, base.cHandler)
	
