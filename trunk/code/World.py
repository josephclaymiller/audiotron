import sys
import math
import threading
from random import random
from random import uniform
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
		if (len(self.enemyManager.enemies) == 0 and self.enemyManager.level < len(levelData) and task.frame % 1000 == 0):
			sublevels = self.enemyManager.sublevels
			if (len(sublevels) == 1):
				type = levelData[self.enemyManager.level][sublevels[0]][0]
				print "Spawning type '", type, "'"
				self.enemyManager.spawnCircle(type, 8)
			else:
				type1 = levelData[self.enemyManager.level][sublevels[0]][0]
				type2 = levelData[self.enemyManager.level][sublevels[1]][0]
				print "Spawning types '", type1, "' and '", type2, "'"
				self.enemyManager.spawnCircle(type1, 8, 2, Point3(0.5, 17, 0.5))
				self.enemyManager.spawnCircle(type2, 8, 2, Point3(-0.5, 23, -0.5))
			
		#self.enemyManager.spawnCircle()
		#for enemy in self.enemyManager.enemies:
		#	enemy.destroy()
			
		#if (task.frame % 100 == 0):
		#	self.enemyManager.spawnSpiral()
		#elif ((task.frame + 50) % 100 == 0):
		#	self.enemyManager.spawnCircle()
		
		#if (len(self.enemyManager.enemies) > 0):
		#	for i in range(2):
		#		index = int(uniform(0, len(self.enemyManager.enemies)))
		#		print "Delete enemy ", index
		#		self.enemyManager.enemies[index].destroy()
		
		return Task.cont
		
	def start(self):
		base.setBackgroundColor(0,0,0) #set the background color to black
		self.setupCollision()
		self.musicController = MusicController()
		self.player = Player(self.wiimoteManager, self.musicController)
		self.enemyManager = EnemyManager(self.musicController)
		self.tunnel = Tunnel(self.musicController)
		
		self.enemyHandle3 = self.enemyManager.spawnCircle('pyramid_hon', 5, 2)
		#self.enemyManager.moveForward(self.enemyHandle3)
			
		
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
	
