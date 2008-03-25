from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import GeomNode
from pandac.PandaModules import BitMask32
from direct.actor.Actor import Actor

class Enemy (DirectObject):

	def __init__(self, NP):
		self.NP=NP
		self.model = Actor("../assets/models/ememydtb.egg")
		self.model.reparentTo(self.NP)
		self.model.setScale(0.25, 0.25, 0.25)
		#self.model.reparentTo(self.NP)
		self.model.setPos(0, 10, 5)
		
		self.tex = loader.loadTexture('../assets/images/target.PNG')
		#self.model.find('**/ememypom').setTexture(self.tex)
		self.model.setTexture(self.tex)

		cs = CollisionSphere(0, 0, 0, 5)
		cNodePath = self.model.attachNewNode(CollisionNode('cEnemy'))
		cNodePath.node().addSolid(cs)
		cNodePath.node().setFromCollideMask(BitMask32.allOff())
		cNodePath.node().setIntoCollideMask(BitMask32.allOn())
		cNodePath.node().setCollideMask(BitMask32(42))
		cNodePath.show()
		base.cTrav.addCollider(cNodePath, base.cHandler)

		taskMgr.add(self.update, "EnemyUpdate")
	
	def update(self, task):
		return Task.cont
