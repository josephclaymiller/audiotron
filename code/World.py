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
from pandac.PandaModules import CollisionHandlerEvent
from pandac.PandaModules import CollisionTraverser

import config
from WiimoteManager import WiimoteManager
from WiimoteEmulator import WiimoteEmulator
from Enemy import Enemy
from EnemyManager import EnemyManager
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
		
		print "\n***\nEnemies\n****"
		for enemy in self.enemyManager.enemies:
			print gc.get_referents(enemy)
			
		print "\n***\nModels\n****"
		for enemy in self.enemyManager.enemies:
			print gc.get_referents(enemy.model)
			
	def spawnMoreEnemy(self, task):
		#self.enemyManager.spawnCircle()
		#self.garbageDebug()
		#for enemy in self.enemyManager.enemies:
		#	enemy.shotByPlayer(enemy.uid)
		#self.garbageDebug()
			
	#	if (task.frame % 100 == 0):
	#		self.enemyManager.spawnSpiral()
	#	elif ((task.frame + 50) % 100 == 0):
	#		self.enemyManager.spawnCircle()
	#	
	#	if (len(self.enemyManager.enemies) > 0):
	#		for i in range(2):
	#			index = int(uniform(0, len(self.enemyManager.enemies)))
	#			print "Delete enemy ", index
	#			self.enemyManager.enemies[index].shotByPlayer()
		return Task.cont
		
	def start(self):
		base.setBackgroundColor(0,0,0) #set the background color to black
		self.setupCollision()
		self.player = Player(self.wiimoteManager)
		self.enemyManager = EnemyManager()
		self.musicController = MusicController()
		self.tunnel = Tunnel(self.musicController)
		
		self.enemyHandle = self.enemyManager.spawnCircle()
		
		#TEST DELETE*************************************************
		#create lighting
		alight = AmbientLight('alight')
		alight.setColor(VBase4(.5, 0, 0, 1))
		alnp = self.enemyHandle.attachNewNode(alight)
		self.enemyHandle.setLight(alnp)
		
		dlight = DirectionalLight('dlight')
		dlight.setColor(VBase4(0, 0, .75, 1))
		dlnp = self.enemyHandle.attachNewNode(dlight)
		dlnp.setHpr(0, -60, 0)
		self.enemyHandle.setLight(dlnp)
		
		dlight = DirectionalLight('dlight')
		dlight.setColor(VBase4(1, 1, 1, 1))
		dlnp = self.enemyHandle.attachNewNode(dlight)
		dlnp.setHpr(0, 60, 0)
		self.enemyHandle.setLight(dlnp)
		
		#create pulse
		pulse = [x*4 for x in range(self.musicController.numSixteenths/4)]
		self.musicController.addPulsingElement(self.enemyHandle, pulse)
		#TRIAL DELETE END**************************************************************
		
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

	
