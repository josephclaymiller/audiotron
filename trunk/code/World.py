import sys
import math
import threading

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
#from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Point3
from pandac.PandaModules import CollisionHandlerEvent
from pandac.PandaModules import CollisionTraverser

import config
from WiimoteManager import WiimoteManager
from WiimoteEmulator import WiimoteEmulator
from Enemy import Enemy, spawnCircle, spawnSpiral
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
		
		self.enemyUID=0
		
	def start(self):
		
		base.setBackgroundColor(0,0,0) #set the background color to black
		
		self.setupCollision()
		
	#	self.enemyHandle = NodePath(PandaNode("EnemyHandle"))
	#	self.enemyHandle.reparentTo(render)
	#	self.enemyHandle.setPos(Point3(0,10,0))
	#	self.numEnemies = 10
	#	self.testEnemy = []
	#	for i in range(2):
	#		self.enemyUID+=1
	#		self.testEnemy.append(Enemy(self.enemyUID, self.enemyHandle, "emenytb_t1", Point3(0,0,0)))
	#		self.enemyHandle.setScale(.25)
		
		self.enemyHandle = spawnCircle()		
			
		self.player = Player(self.wiimoteManager)
		
		self.musicController = MusicController()
		self.tunnel = Tunnel(self.musicController)
		
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
		
		#rotate stuff
		#self.enemyMove = LerpHprInterval(self.testEnemy[0].model,
		#					 duration = 107.385,
		#					 hpr=VBase3(360,360,360),
		#					 startHpr=VBase3(0,0,0)
		#					 )
		#self.enemyMove.loop()
		#self.enemyMove.start()
		
		#rotate stuff
		#self.enemyMove1 = LerpHprInterval(self.testEnemy[1].model,
		#					 duration = 107.385,
		#					 hpr=VBase3(360,360,360),
		#					 startHpr=VBase3(0,0,0)
		#					 )
		#self.enemyMove.loop()
		#self.enemyMove1.start()
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

	
