from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task import Task
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import GeomNode
from pandac.PandaModules import BitMask32
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode

numEnemies = 0

class Enemy (DirectObject):

	def __init__(self, uid, handle, modelname, startpos):
	
		self.uid = uid		
		self.handle = handle
	
		self.model = Actor("../assets/models/" + modelname + ".egg")
		self.model.setScale(0.25, 0.25, 0.25)
		self.model.setPos(startpos)
		self.model.reparentTo(self.handle)
		
		self.tex = loader.loadTexture('../assets/images/target.PNG')
		#self.model.find('**/enemypom').setTexture(self.tex)
		self.model.setTexture(self.tex)

		cs = CollisionSphere(0, 0, 0, 5)
		cNodePath = self.model.attachNewNode(CollisionNode('cEnemy' + str(self.uid)))
		cNodePath.node().addSolid(cs)
		cNodePath.node().setFromCollideMask(BitMask32.allOff())
		cNodePath.node().setIntoCollideMask(BitMask32.allOn())
		cNodePath.node().setCollideMask(BitMask32(42))
		#cNodePath.show()
		base.cTrav.addCollider(cNodePath, base.cHandler)
		self.accept('cPlayerShootRay-into-cEnemy' + str(self.uid), self.shotByPlayer)

		taskMgr.add(self.update, "EnemyUpdate")
	
	def update(self, task):
		return Task.cont

	def shotByPlayer(self):
		print "Enemy", self.uid, " shot by player!"
		