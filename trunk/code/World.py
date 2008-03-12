from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import CollisionHandlerEvent

import sys
import math
import threading

import config
from WiimoteManager import *
from WiimoteEmulator import *
from Enemy import *
from Player import *


class World (DirectObject):

	def __init__(self):
		if config.EMULATE_WIIMOTE:
			self.wiimoteEmulator = WiimoteEmulator()
			taskMgr.add(self.wiimoteEmulator.update, "updateEmulator")
		else:
			self.wiimoteManager = WiimoteManager()
			self.wiimoteManager.setDaemon(True)
			self.wiimoteManager.start()
		
	def start(self):
		
		self.setupCollision()
		
		self.testEnemy = Enemy()
		self.player = Player()

		#Load the first environment model
		self.environ = loader.loadModel("models/environment")
		self.environ.reparentTo(render)
		self.environ.setScale(0.25,0.25,0.25)
		self.environ.setPos(-8,42,0)

		#Load the panda actor, and loop its animation
		pandaActor = Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
		pandaActor.setScale(0.005,0.005,0.005)
		pandaActor.reparentTo(render)
		pandaActor.loop("walk")

		#Create the four lerp intervals needed to walk back and forth
		pandaPosInterval1 = pandaActor.posInterval(13, Point3(0,-10,0), startPos = Point3(0,10,0))
		pandaPosInterval2 = pandaActor.posInterval(13, Point3(0,10,0), startPos = Point3(0,-10,0))
		pandaHprInterval1 = pandaActor.hprInterval(3, Point3(180,0,0), startHpr = Point3(0,0,0))
		pandaHprInterval2 = pandaActor.hprInterval(3, Point3(0,0,0), startHpr = Point3(180,0,0))

		#Create and play the sequence that coordinates the intervals
		self.pandaPace = Sequence(pandaPosInterval1, pandaHprInterval1, pandaPosInterval2, pandaHprInterval2, name = "pandaPace")
		self.pandaPace.loop()
	
	def setupCollision(self):
		self.cHandler = CollisionHandlerEvent()
		self.cHandler.setInPattern("%fn-into-%in")
		base.cHandler = self.cHandler

		self.cTrav = CollisionTraverser()
		base.cTrav = self.cTrav

	
