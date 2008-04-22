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
		self.accept('m', self.garbageDebug)
		taskMgr.add(self.spawnMoreEnemy, "spawnMoreEnemy")
	
	def garbageDebug(self):
		#print gc.get_objects()
		#self.musicController.debugPrint()
		render.ls()
			
	def spawnMoreEnemy(self, task):
		if (self.enemyManager.level == len(levelData)):
			return Task.done
			
		elif (task.frame % self.spawnRate == 0):
			validEnemies = self.enemyManager.getValidEnemyTypes()
			numValid = len(validEnemies)
			
			if (numValid >= 3):
				if (random.random() < 0.5):
					typeToSpawn = validEnemies[random.randint(numValid - 2, numValid - 1)]
				else:
					typeToSpawn = validEnemies[random.randint(0, numValid - 3)]
					
			elif (numValid == 2):
				typeToSpawn = validEnemies[random.randint(0, 1)]
			
			else:
				typeToSpawn = validEnemies[0]
				
			handle = self.enemyManager.spawnCircle(typeToSpawn, random.randint(3, 8))
			self.enemyManager.moveForward(handle)
		
		return Task.cont
		
	def start(self):
		base.setBackgroundColor(0,0,0) #set the background color to black
		self.setupCollision()
		self.musicController = MusicController()
		self.HUD = HUD()
		self.player = Player(self.wiimoteManager, self.musicController, self.HUD)
		self.enemyManager = EnemyManager(self.musicController)
		self.tunnel = Tunnel(self.musicController)
		
		self.spawnRate = 100
		
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
	
