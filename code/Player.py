import sys
import threading

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib

from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import BitMask32

import config
import CollisionBitMasks

if config.HEADTRACK_3D:
	from HeadTracker3D import *
else:
	from HeadTracker2D import *
	

class Player (DirectObject):

	def __init__(self, wiimoteManager):
	
		self.wm = wiimoteManager
		self.headTracker = HeadTracker(wiimoteManager)

		if not config.MANUAL_CAMERA_CONTROL:
			taskMgr.add(self.headTracker.update, "HeadTrackerUpdate")
			base.disableMouse()
		
		self.targettedEnemies = []
		self.targetting = False

		self.targetImage = OnscreenImage(image = "..//assets//images//targetCursor.png", pos = (0, 0, 0), scale = (32.0/self.wm.SCREEN_WIDTH, 0, 32.0/self.wm.SCREEN_HEIGHT), parent = render2d)
		self.targetImage.setTransparency(TransparencyAttrib.MAlpha)
		
		self.cShootNode = CollisionNode('cPlayerShootRay')
		self.cShootNode.setFromCollideMask(CollisionBitMasks.shootRayMask)
		self.cShootNode.setIntoCollideMask(BitMask32.allOff())
		self.shootRay = CollisionRay()
		self.cShootNode.addSolid(self.shootRay)
		cNodePath = base.camera.attachNewNode(self.cShootNode)
		cNodePath.show()
		
		self.cHandler = CollisionHandlerQueue()
		self.cRayTrav = CollisionTraverser('ShootingRayTraverser')
		self.cRayTrav.addCollider(cNodePath, self.cHandler)
		
		self.accept("FireButtonDown", self.fireButtonDown)
		self.accept("FireButtonUp", self.fireButtonUp)
		taskMgr.add(self.update, "PlayerUpdate")
	
	def fireButtonDown(self):
		self.targetting = True
		
	def fireButtonUp(self):
		self.targetting = False
		for enemy in self.targettedEnemies:
			enemy.destroy()
	
	def update(self, task):
		self.wm.pointerLock.acquire()
		if (self.wm.pointerData.screen.valid):
			self.targetImage.setPos(self.wm.pointerData.screen.x, 0, self.wm.pointerData.screen.y)
			
			if (self.targetting):
				self.shootRay.setFromLens(base.camNode, self.wm.pointerData.screen.x, self.wm.pointerData.screen.y)
				self.cRayTrav.traverse(render)
				
				if (self.cHandler.getNumEntries() > 0):
					self.cHandler.sortEntries()
					shotNode = self.cHandler.getEntry(0).getIntoNodePath()
					messenger.send('EnemyTargetted', [int(shotNode.getName().strip('cEnemy')), self])
		
		self.wm.pointerLock.release()
		return Task.cont

	def fire(self):
		self.wm.pointerLock.acquire()
		if (self.wm.pointerData.ir.valid):
			print "Fire ", self.wm.pointerData.screen.x, " ", self.wm.pointerData.screen.y
			self.cRayTrav.traverse(render)
			
			if (self.cHandler.getNumEntries() > 0):
				self.cHandler.sortEntries()
				shotNode = self.cHandler.getEntry(0).getIntoNodePath()
				messenger.send('cPlayerShootRay-into-cEnemy', [int(shotNode.getName().strip('cEnemy'))])
				
		
		self.wm.pointerLock.release()

	def collisionRayEnemy(self, event):
		print "Player shot enemy!"
