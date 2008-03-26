import sys
import math
import threading

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
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
from Player import Player
from tunnel import Tunnel
from music import MusicController


class World (DirectObject):

	def __init__(self):
		if config.EMULATE_WIIMOTE:
			self.wiimoteEmulator = WiimoteEmulator()
		else:
			self.wiimoteManager = WiimoteManager()
			self.wiimoteManager.setDaemon(True)
		
		self.accept('escape', sys.exit)
		
	def start(self):
		
		base.setBackgroundColor(0,0,0) #set the background color to black
		
		self.setupCollision()
		
		self.enemyHandle = NodePath(PandaNode("EnemyHandle"))
		self.enemyHandle.reparentTo(render)
		self.numEnemies = 10
		for i in range(4):
			self.testEnemy = Enemy(i, self.enemyHandle, "enemysxx", Point3((i - 2) * 5, 10, 5))
			
		self.player = Player(self.wiimoteManager)
		
		self.musicController = MusicController()
		self.tunnel = Tunnel(self.musicController)
		
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

	
