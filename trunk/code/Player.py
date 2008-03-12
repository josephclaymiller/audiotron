import sys

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage

from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import GeomNode
from pandac.PandaModules import BitMask32

from WiimoteManager import *
import config

if config.HEADTRACK_3D:
	from HeadTracker3D import *
else:
	from HeadTracker2D import *
	

class Player (DirectObject):

	def __init__(self):
	
		self.headTracker = HeadTracker()

		if not config.MANUAL_CAMERA_CONTROL:
			taskMgr.add(self.headTracker.update, "HeadTrackerUpdate")
			base.disableMouse()

		self.targetImage = OnscreenImage(image = '../assets/images/target.PNG', pos = (0, 0, 0), scale = (32.0/SCREEN_WIDTH, 0, 32.0/SCREEN_HEIGHT), parent = render2d)
	
		self.cShootNode = CollisionNode('cPlayerShootRay')
		self.cShootNode.setFromCollideMask(BitMask32(42))
		self.cShootNode.setIntoCollideMask(BitMask32.allOff())
		self.shootRay = CollisionRay()
		self.cShootNode.addSolid(self.shootRay)
		cNodePath = base.camera.attachNewNode(self.cShootNode)
		cNodePath.show()
		
		self.cRayTrav = CollisionTraverser('ShootingRayTraverser')
		self.cRayTrav.addCollider(cNodePath, base.cHandler)
		
		self.accept('cPlayerShootRay-into-cEnemy', self.collisionRayEnemy)
		self.accept("FireButton", self.fire)
		taskMgr.add(self.update, "PlayerUpdate")
	
	def update(self, task):
		pointerLock.acquire()
		if (pointerData.screen.valid):
			self.shootRay.setFromLens(base.camNode, pointerData.screen.x, pointerData.screen.y)
			self.targetImage.setPos(pointerData.screen.x, 0, pointerData.screen.y)
		
		pointerLock.release()
		return Task.cont

	def fire(self):
		pointerLock.acquire()
		if (pointerData.ir.valid):
			print "Fire ", pointerData.screen.x, " ", pointerData.screen.y
			self.cRayTrav.traverse(render)
		
		pointerLock.release()

	def collisionRayEnemy(self, event):
		print "Collision!"
