from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import Point3

import math

from WiimoteManager import *

class HeadTracker(DirectObject):
	def __init__(self):
		self.basePos = Point3(0, -10, 7)
		self.headPos = Point3(self.basePos)
		self.lookPos = Point3(0, 50, 5)
		
		#These are the settings I am using in my tunnel demo (I would have coded directly into the game, but I cannot install it) -Brian
		#self.basePose = Point3(0, 0, 0)
		#self.headPos = Point3(self.basePos)
		#self.lookPos = Point3(0, 0, -100) #I'm not sure this needs to be -100 as opposed to -50 or -500
		
		self.rangeX = 20.0
		self.rangeZ = 10.0
		
		self.cameraCenterX = SCREEN_WIDTH / 2
		self.cameraCenterY = SCREEN_HEIGHT / 2
		
		self.accept('space', self.callibrate)
	
	def callibrate(self):
		print "Callibrate"
		trackerLock.acquire()
		if (trackerData.ir.valid):
			self.cameraCenterY = trackerData.ir.y
		trackerLock.release()
	
	def update(self, task):
		trackerLock.acquire()
		
		if (trackerData.ir.valid):
			self.headPos.setX(self.basePos.getX() + (trackerData.ir.x - self.cameraCenterX) * self.rangeX / SCREEN_WIDTH)
			self.headPos.setZ(self.basePos.getZ() + (trackerData.ir.y - self.cameraCenterY) * self.rangeZ / SCREEN_HEIGHT)
			#print "IR positions\t", trackerData.ir.x, "\t", trackerData.ir.y, "\tSetting camaera pos\t", self.headPos.getX(), "\t", self.headPos.getY(), "\t", self.headPos.getZ()
		
		trackerLock.release()
		
		base.camera.setPos(self.headPos)
		base.camera.lookAt(self.lookPos)
		
		return Task.cont
		
	