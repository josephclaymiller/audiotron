#import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

class WiimoteEmulator(DirectObject):
	def __init__(self, wiimoteManager):
		self.accept('mouse1', self.mouseDown)
		self.accept('mouse1-up', self.mouseUp)
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
		
		self.wm = wiimoteManager
		
		self.wm.trackerData.ir.valid = True
		self.wm.trackerData.ir.x = self.wm.SCREEN_WIDTH / 2
		self.wm.trackerData.ir.y = self.wm.SCREEN_HEIGHT / 2
		
		self.wm.pointerData.ir.valid = True
		self.wm.pointerData.ir.x = self.wm.SCREEN_WIDTH / 2
		self.wm.pointerData.ir.y = self.wm.SCREEN_HEIGHT / 2
	
	def update(self, task):
		self.wm.trackerLock.acquire()
		self.wm.pointerLock.acquire()
		if base.mouseWatcherNode.hasMouse():
			self.wm.pointerData.ir.x =  base.mouseWatcherNode.getMouseX() * self.wm.SCREEN_WIDTH  / 2 + self.wm.SCREEN_WIDTH  / 2
			self.wm.pointerData.ir.y = -base.mouseWatcherNode.getMouseY() * self.wm.SCREEN_HEIGHT / 2 + self.wm.SCREEN_HEIGHT / 2
		
		self.wm.trackerData.ir.x = min(self.wm.SCREEN_WIDTH,  max(0, self.wm.trackerData.ir.x + self.xMove))
		self.wm.trackerData.ir.y = min(self.wm.SCREEN_HEIGHT, max(0, self.wm.trackerData.ir.y - self.yMove))
		
		for wmdata in (self.wm.pointerData, self.wm.trackerData):
			wmdata.screen.valid = True
			wmdata.screen.x = (wmdata.ir.x - (self.wm.SCREEN_WIDTH/2.0)) / (self.wm.SCREEN_WIDTH/2.0)
			wmdata.screen.y = ((self.wm.SCREEN_HEIGHT/2.0) - wmdata.ir.y) / (self.wm.SCREEN_HEIGHT/2.0)
			
		self.wm.trackerLock.release()
		self.wm.pointerLock.release()
		return Task.cont
	
	def mouseDown(self):
		messenger.send("FireButtonDown")
		
	def mouseUp(self):
		messenger.send("FireButtonUp")
		
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

