from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import Point3

import math


class HeadTracker(DirectObject):
	def __init__(self, wiimoteManager):
		self.wm = wiimoteManager
	
		self.basePos = Point3(0, 0, 0)
		self.headPos = Point3(self.basePos)
		self.lookPos = Point3(0, 100, 0)
		
		self.rangeX = 4.0
		self.rangeZ = 4.0
		
		self.cameraCenterX = self.wm.SCREEN_WIDTH / 2
		self.cameraCenterY = self.wm.SCREEN_HEIGHT / 2
		
		self.accept('space', self.callibrate)
	
	def callibrate(self):
		print "Callibrate"
		self.wm.trackerLock.acquire()
		if (self.wm.trackerData.ir.valid):
			self.cameraCenterY = self.wm.trackerData.ir.y
		self.wm.trackerLock.release()
	
	def update(self, task):
		self.wm.trackerLock.acquire()
		
		if (self.wm.trackerData.ir.valid):
			self.headPos.setX(self.basePos.getX() + (self.wm.trackerData.ir.x - self.cameraCenterX) * self.rangeX / self.wm.SCREEN_WIDTH)
			self.headPos.setZ(self.basePos.getZ() + (self.wm.trackerData.ir.y - self.cameraCenterY) * self.rangeZ / self.wm.SCREEN_HEIGHT)
			#print "IR positions\t", trackerData.ir.x, "\t", trackerData.ir.y, "\tSetting camaera pos\t", self.headPos.getX(), "\t", self.headPos.getY(), "\t", self.headPos.getZ()
		
		self.wm.trackerLock.release()
		
		base.camera.setPos(self.headPos)
		base.camera.lookAt(self.lookPos)
		
		return Task.cont
		
	