import sys
import threading

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib

from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import BitMask32
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Vec3

import config
import CollisionBitMasks

if config.HEADTRACK_3D:
	from HeadTracker3D import *
else:
	from HeadTracker2D import *
	

class Player (DirectObject):

	def __init__(self, handle, wiimoteManager, musicController, HUD):
	
		self.wm = wiimoteManager
		self.handle = handle
		self.headTracker = HeadTracker(self.wm, self.handle)
		self.musicController = musicController
		self.HUD = HUD
		
		self.handle.reparentTo(render)
		base.camera.reparentTo(self.handle)

		if not config.MANUAL_CAMERA_CONTROL:
			taskMgr.add(self.headTracker.update, "HeadTrackerUpdate")
			base.disableMouse()
		
		self.targettedEnemies = []
		self.comboSize = 0
		self.targetting = False
		self.targetTime = 0
		self.onBeat=False
		
		self.lives=3
		self.health=4

		self.targetImage = OnscreenImage(image = "..//assets//images//targetCursor.png", pos = (0, 0, 0), scale = (32.0/self.wm.SCREEN_WIDTH, 0, 32.0/self.wm.SCREEN_HEIGHT), parent = render2d)
		self.targetImage.setTransparency(TransparencyAttrib.MAlpha)
		
		self.cShootNode = CollisionNode('cPlayerShootRay')
		self.cShootNode.setFromCollideMask(CollisionBitMasks.shootRayMask)
		self.cShootNode.setIntoCollideMask(BitMask32.allOff())
		self.shootRay = CollisionRay()
		self.cShootNode.addSolid(self.shootRay)
		cNodePath = base.camera.attachNewNode(self.cShootNode)
		
		self.cSphereNode = self.handle.attachNewNode(CollisionNode('cPlayerSphere'))
		self.cSphereNode.node().setFromCollideMask(BitMask32.allOff())
		self.cSphereNode.node().setIntoCollideMask(CollisionBitMasks.enemyMask)
		self.cSphereNode.node().addSolid(CollisionSphere(0, 1.35, 0, 0.35))
		#self.cSphereNode.show()
		
		self.cHandler = CollisionHandlerQueue()
		self.cRayTrav = CollisionTraverser('ShootingRayTraverser')
		self.cRayTrav.addCollider(cNodePath, self.cHandler)
		
		self.accept("FireButtonDown", self.fireButtonDown)
		self.accept("FireButtonUp", self.fireButtonUp)
		self.accept("EnemyHitPlayer", self.hitByEnemy)
		taskMgr.add(self.update, "PlayerUpdate")
	
	def fireButtonDown(self):
		time = globalClock.getRealTime()
		self.targetting = True
		
		#finding fireButtonUp time
		targetSixteenth = int((time - self.musicController.loopStartTime) / self.musicController.secondsPerSixteenth)
		beat = targetSixteenth % 4
		#making targetSixteenth always be on beat!
		targetSixteenth += (4 - beat)
		
		#print str(beat)
		
		if (self.musicController.isOnBeatNow(time)):
			print "nice job"
			self.maxCombo = 800
			targetSixteenth += 28
			if beat == 3:
				targetSixteenth += 4
			self.targetImage.setColor(1,1,0,1)
			self.onBeat=True
		else:
			self.maxCombo = 400
			targetSixteenth += 12
			self.onBeat=False
		
		self.targetTime = self.musicController.loopStartTime + targetSixteenth * self.musicController.secondsPerSixteenth
		taskMgr.add(self.fireTimer, "fireTimer")
	
	def fireTimer(self, task):
		time = globalClock.getRealTime()
		fade = 1
		if self.onBeat:
			fade=1-(self.targetTime-time)/3.7
			self.targetImage.setColor(1,1,fade,1)
		else:
			fade=1-(self.targetTime-time)/1.85
			self.targetImage.setColor(1,fade,fade,1)
		if globalClock.getRealTime() >= self.targetTime:
			if len(self.musicController.destructionQueue) > 0:
				element = self.musicController.destructionQueue.pop(0)
				self.musicController.dieSFX.play()
				element.destroy()
			self.fireButtonUp()
			return Task.done
		
		#print str(globalClock.getRealTime()-self.musicController.loopStartTime)
		#print str(self.targetTime-self.musicController.loopStartTime)
		return Task.cont
	
	def fireButtonUp(self):
		self.targetting = False
		self.onBeat=False
		self.targetImage.setColor(1,1,1,1)
		taskMgr.remove("fireTimer")
		combo = {}
		for enemy in self.targettedEnemies:
			if (enemy.type in combo):
				combo[enemy.type] += 1
			else:
				combo[enemy.type] = 1
		
		self.musicController.addDestructionElements(self.targettedEnemies)
		self.targettedEnemies = []
		messenger.send("EnemiesComboed", [combo])
	
	def hitByEnemy(self):
		self.health-=1
		if self.health<1:
			self.health=4
			self.lives-=1
			if self.lives<0:
				print "you loose"
		
		self.HUD.hit(self.lives, self.health)
		print "Player hit by enemy!"
	
	def update(self, task):
		self.wm.pointerLock.acquire()
		if (self.wm.pointerData.screen.valid):
			self.targetImage.setPos(self.wm.pointerData.screen.x, 0, self.wm.pointerData.screen.y)
			
			if (self.targetting and self.maxCombo > len(self.targettedEnemies)):
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
			#print "Fire ", self.wm.pointerData.screen.x, " ", self.wm.pointerData.screen.y
			self.cRayTrav.traverse(render)
			
			if (self.cHandler.getNumEntries() > 0):
				self.cHandler.sortEntries()
				shotNode = self.cHandler.getEntry(0).getIntoNodePath()
				messenger.send('cPlayerShootRay-into-cEnemy', [int(shotNode.getName().strip('cEnemy'))])
				
		
		self.wm.pointerLock.release()

