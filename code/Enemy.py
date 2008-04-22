from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task import Task
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import BitMask32
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Point3
from pandac.PandaModules import BillboardEffect
from direct.interval.LerpInterval import LerpHprInterval #needed to move and rotate enemies
from pandac.PandaModules import VBase3, VBase4

from EnemyData import enemyData
import CollisionBitMasks


class Enemy (DirectObject):

	def __init__(self, uid, type, handle, startPos=Point3(0,0,0), startHpr=Point3(0,0,0)):
		self.uid = uid
		self.type = type
		self.data = enemyData[type]
		self.handle = handle
		self.targetted = False
		self.destroyed = False
		self.deleteMe = False
		
		handle.setTag("enemyChildren", str(int(handle.getTag("enemyChildren")) + 1))
		
		taskMgr.add(self.update, "EnemyUpdate" + str(self.uid))
		
		self.model = Actor("..//assets//models//enemies//Enemies fin//" + str(self.data['anim']) + ".egg")
		self.model.loadAnims({"die":"..//assets//models//enemies//Enemies fin//" + str(self.data['anim']) + ".egg"})
		self.model.reparentTo(self.handle)
		self.model.setScale(self.data['scale'])
		self.model.setPos(startPos)
		self.model.setHpr(startHpr)
		self.model.reparentTo(self.handle)
		
		self.billboard = loader.loadModelCopy('..//assets//models//plane.egg.pz')
		self.billboard.reparentTo(self.model)
		self.billboard.setPos(0, 0, 0)
		self.billboard.setScale(1 / self.data['scale'])
		self.billboard.setTexture(loader.loadTexture("..//assets//images//targetCursor.png"))
		self.billboard.setTransparency(True)
		self.billboard.setBillboardPointEye()
		self.billboard.hide()

		cs = CollisionSphere(0, 0, 0, self.data['cScale']) #used to be (0,0,0,5)
		cNodePath = self.model.attachNewNode(CollisionNode('cEnemy' + str(self.uid)))
		cNodePath.node().addSolid(cs)
		cNodePath.node().setFromCollideMask(CollisionBitMasks.enemyMask)
		cNodePath.node().setIntoCollideMask(CollisionBitMasks.shootRayMask)
		#cNodePath.show()
		base.cTrav.addCollider(cNodePath, base.cHandler)
		self.cNodePath = cNodePath
		
		self.accept('EnemyTargetted', self.shotByPlayer)
		self.accept('cEnemy' + str(self.uid) + '-into-cEnemyKillPlane', self.hitKillPlane)
		self.accept('cEnemy' + str(self.uid) + '-into-cPlayerSphere', self.hitPlayer)
		
		#rotate stuff
		self.enemyMove = LerpHprInterval(self.model,
							duration = 31.384,
							hpr=VBase3(360,360,360),
							startHpr=VBase3(0,0,0)
							)
		self.enemyMove.loop()
		
	def hitKillPlane(self, event):
		self.destroy()
	
	def hitPlayer(self, event):
		messenger.send("EnemyHitPlayer")

	def shotByPlayer(self, id, player):
		if (id == self.uid and not self.targetted):
			self.billboard.show()
			print "Enemy", self.uid, " shot by player!"
			player.targettedEnemies.append(self)
			self.targetted = True

		
	def destroy(self):
		if not self.destroyed:
			self.model.play('die')
			if (self.model.getCurrentAnim() == 'die'):
				self.model.getAnimControl('die').setPlayRate(self.data['playRate'])
			base.cTrav.removeCollider(self.cNodePath)
			self.cNodePath.remove()
			self.destroyed = True
	
	def cleanup(self):
		self.model.cleanup()
		self.model.remove()
		self.handle.setTag("enemyChildren", str(int(self.handle.getTag("enemyChildren")) - 1))
		taskMgr.remove("EnemyUpdate" + str(self.uid))
		self.ignoreAll()
		self.deleteMe = True
	
	def update(self, task):
		if (self.destroyed and (self.model.getCurrentAnim() != 'die' or not self.model.getAnimControl('die').isPlaying())):
			self.cleanup()
		return Task.cont