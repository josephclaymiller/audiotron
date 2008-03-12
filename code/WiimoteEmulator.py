#import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from WiimoteManager import *

class WiimoteEmulator(DirectObject):
	def __init__(self):
		self.accept('mouse1', self.mouseClick)
		self.accept('w', self.startMoveUp)
		self.accept('s', self.startMoveDown)
		self.accept('a', self.startMoveLeft)
		self.accept('d', self.startMoveRight)
		self.accept('w-up', self.stopMoveUp)
		self.accept('s-up', self.stopMoveDown)
		self.accept('a-up', self.stopMoveLeft)
		self.accept('d-up', self.stopMoveRight)
		
		self.xMove = 0
		self.yMove = 0
		self.xSpeed = 12
		self.ySpeed = 12
		
		trackerData.ir.valid = True
		trackerData.ir.x = SCREEN_WIDTH / 2
		trackerData.ir.y = SCREEN_HEIGHT / 2
		
		pointerData.ir.valid = True
		pointerData.ir.x = SCREEN_WIDTH / 2
		pointerData.ir.y = SCREEN_HEIGHT / 2
	
	def update(self, task):
		trackerLock.acquire()
		pointerLock.acquire()
		if base.mouseWatcherNode.hasMouse():
			pointerData.ir.x =  base.mouseWatcherNode.getMouseX() * SCREEN_WIDTH  / 2 + SCREEN_WIDTH  / 2
			pointerData.ir.y = -base.mouseWatcherNode.getMouseY() * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 2
		
		trackerData.ir.x = min(SCREEN_WIDTH,  max(0, trackerData.ir.x + self.xMove))
		trackerData.ir.y = min(SCREEN_HEIGHT, max(0, trackerData.ir.y - self.yMove))
		
		for wmdata in (pointerData, trackerData):
			wmdata.screen.valid = True
			wmdata.screen.x = (wmdata.ir.x - (SCREEN_WIDTH/2.0)) / (SCREEN_WIDTH/2.0)
			wmdata.screen.y = ((SCREEN_HEIGHT/2.0) - wmdata.ir.y) / (SCREEN_HEIGHT/2.0)
			
		trackerLock.release()
		pointerLock.release()
		return Task.cont
	
	def mouseClick(self):
		messenger.send("FireButton")
		
	def startMoveUp(self):
		self.yMove -= self.ySpeed
	
	def startMoveDown(self):
		self.yMove += self.ySpeed
		
	def startMoveLeft(self):
		self.xMove -= self.xSpeed
		
	def startMoveRight(self):
		self.xMove += self.xSpeed

	def stopMoveUp(self):
		self.yMove += self.ySpeed
	
	def stopMoveDown(self):
		self.yMove -= self.ySpeed
		
	def stopMoveLeft(self):
		self.xMove += self.xSpeed
		
	def stopMoveRight(self):
		self.xMove -= self.xSpeed

