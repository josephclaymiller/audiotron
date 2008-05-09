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
from pandac.PandaModules import VBase4

from EnemyData import levelData

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
		
		self.alive=True
		
		self.mult=1
		
		self.shotTimer=OnscreenImage(image='..//assets//HUD//blinker.png', pos=Vec3(0,0,0), scale=Vec3(1.43,0,1.1))
		self.shotTimer.setTransparency(TransparencyAttrib.MAlpha)
		
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
		
		self.lives=7
		self.health=2
		self.score=0

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
		self.cSphereNode.node().addSolid(CollisionSphere(0, 1.35, 0, 0.25))
		#self.cSphereNode.show()
		
		self.cHandler = CollisionHandlerQueue()
		self.cRayTrav = CollisionTraverser('ShootingRayTraverser')
		self.cRayTrav.addCollider(cNodePath, self.cHandler)
		
		self.accept("FireButtonDown", self.fireButtonDown)
		self.accept("FireButtonUp", self.fireButtonUp)
		self.accept("EnemyHitPlayer", self.hitByEnemy)
		taskMgr.add(self.update, "PlayerUpdate")
	
	def fireButtonDown(self):
		if self.alive:
			time = globalClock.getRealTime()
			self.HUD.killCombo()
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
		#self.HUD.killCombo()
		
		if self.HUD.maxCombo >= levelData[self.HUD.level][0][1]:
			if self.mult < self.HUD.level+2:
				self.mult+=1
		else:
			self.mult=1
		
		self.HUD.updateScore(self.score, self.mult)
		
		#playing drum tracks based on score or time
		if self.score > 6000:
			if self.musicController.music[10].status()==1:
				self.musicController.addSound(10)
				self.musicController.showNote('6000 points!\ndrums unlocked!')
				for x in range(8,10):
					if self.musicController.music[x].status()==2:
						self.musicController.fadeOutSound(x)
		elif self.score > 2000:
			if self.musicController.music[9].status()==1:
				self.musicController.addSound(9)
				self.musicController.showNote('2000 points!\ndrums unlocked!')
				if self.musicController.music[8].status()==2:
					self.musicController.fadeOutSound(8)
					
		if self.HUD.maxCombo >= 20:
			if self.musicController.music[12].status()==1:
				self.musicController.addSound(12)
				self.musicController.showNote('20+ combo!\nmelody unlocked!')
				if self.musicController.music[11].status()==2:
					self.musicController.fadeOutSound(11)
		elif self.HUD.maxCombo >= 10:
			if self.musicController.music[11].status()==1:
				self.musicController.addSound(11)
				self.musicController.showNote('10+ combo!\nmelody unlocked!')
				if self.musicController.music[12].status()==2:
					self.musicController.fadeOutSound(12)
		
		messenger.send("EnemiesComboed", [combo])
	
	def hitByEnemy(self):
		if self.alive and not config.INVULNERABILITY:
			self.musicController.hitSFX.play()
			self.HUD.flashColor=VBase4(1,0,0,1)
			self.HUD.flash.show()
			self.HUD.flashTime=globalClock.getRealTime()
			taskMgr.add(self.HUD.flasher, 'flasher' + str(self.HUD.flashTime))
			print "play!!"
			self.health-=1
			if self.health<1:
				self.health=2
				self.lives-=1
				if self.lives<0:
					self.HUD.endGame('you lose')
					for x in range(0,13):
						if self.musicController.music[x].status()==2:
							self.musicController.fadeOutSound(x)
					for x in range(13,15):
						if self.musicController.music[x].status()==1:
							self.musicController.addSound(x)
					self.alive=False
					print "you loose"
			
			if self.lives<1 and self.musicController.music[14].status()==1:
				self.musicController.addSound(14)
				self.musicController.showNote('very low health!\ntrack unlocked!')
			elif self.lives<2 and self.musicController.music[13].status()==1:
				self.musicController.addSound(13)
				self.musicController.showNote('low health!\ntrack unlocked!')
			
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

