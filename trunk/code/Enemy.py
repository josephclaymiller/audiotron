from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task import Task
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import GeomNode
from pandac.PandaModules import BitMask32
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Point3
from direct.interval.LerpInterval import LerpHprInterval #needed to move and rotate enemies
from pandac.PandaModules import VBase3, VBase4


class Enemy (DirectObject):

	def __init__(self, uid, handle, modelName, startPos=Point3(0,0,0), startHpr=Point3(0,0,0)):
		self.uid = uid
		self.handle = handle
		self.deleteMe = False
		
		handle.setTag("enemyChildren", str(int(handle.getTag("enemyChildren")) + 1))
		
		taskMgr.add(self.update, "EnemyUpdate" + str(self.uid))
		
		self.model = Actor("../assets/models/" + str(modelName) + ".egg")
		self.model.reparentTo(self.handle)
		self.model.setScale(0.1, 0.1, 0.1)
		self.model.setPos(startPos)
		self.model.setHpr(startHpr)
		self.model.reparentTo(self.handle)

		cs = CollisionSphere(0, 0, 0, 5)
		cNodePath = self.model.attachNewNode(CollisionNode('cEnemy' + str(self.uid)))
		cNodePath.node().addSolid(cs)
		cNodePath.node().setFromCollideMask(BitMask32.allOff())
		cNodePath.node().setIntoCollideMask(BitMask32.allOn())
		cNodePath.node().setCollideMask(BitMask32(42))
		cNodePath.show()
		base.cTrav.addCollider(cNodePath, base.cHandler)
		self.cNodePath = cNodePath
		self.accept('cPlayerShootRay-into-cEnemy', self.shotByPlayer)
		
		#rotate stuff
		self.enemyMove = LerpHprInterval(self.model,
							 duration = 31.384,
							 hpr=VBase3(360,360,360),
							 startHpr=VBase3(0,0,0)
							 )
		self.enemyMove.loop()
		
		
		
	
	def destroy(self):
		if not self.deleteMe:
			base.cTrav.removeCollider(self.cNodePath)
			self.model.cleanup()
			self.model.remove()
			self.cNodePath.remove()
			self.handle.setTag("enemyChildren", str(int(self.handle.getTag("enemyChildren")) - 1))
			taskMgr.remove("EnemyUpdate" + str(self.uid))
			self.ignoreAll()
			self.deleteMe = True
	
	def update(self, task):
		return Task.cont

	def shotByPlayer(self, id):
		#print "Enemy", self.uid, " shot by player!"
		if (id == self.uid):
			self.destroy()
