import math #for spawining circles and such

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
	
		self.model = Actor("../assets/models/" + str(modelName) + ".egg")
		self.model.reparentTo(self.handle)
		self.model.setScale(0.1, 0.1, 0.1)
		self.model.setPos(startPos)
		self.model.setHpr(startHpr)
		#self.model.reparentTo(self.handle)
		
		#self.tex = loader.loadTexture('../assets/images/target.PNG')
		#self.model.find('**/enemypom').setTexture(self.tex)
		#self.model.setTexture(self.tex)

		cs = CollisionSphere(0, 0, 0, 5)
		cNodePath = self.model.attachNewNode(CollisionNode('cEnemy' + str(self.uid)))
		cNodePath.node().addSolid(cs)
		cNodePath.node().setFromCollideMask(BitMask32.allOff())
		cNodePath.node().setIntoCollideMask(BitMask32.allOn())
		cNodePath.node().setCollideMask(BitMask32(42))
		cNodePath.show()
		base.cTrav.addCollider(cNodePath, base.cHandler)
		self.accept('cPlayerShootRay-into-cEnemy' + str(self.uid), self.shotByPlayer)
		
		#rotate stuff
		self.enemyMove = LerpHprInterval(self.model,
							 duration = 31.384,
							 hpr=VBase3(360,360,360),
							 startHpr=VBase3(0,0,0)
							 )
		self.enemyMove.loop()
		
		taskMgr.add(self.update, "EnemyUpdate")
	
	def update(self, task):
		return Task.cont

	def shotByPlayer(self):
		print "Enemy", self.uid, " shot by player!"

#returns a handle
def spawnCircle(num=5, r=2, modelName="emenytb_t1", startPos=Point3(0,20,0), uid=0):
	handle = NodePath(PandaNode("handle"+str(uid)))
	handle.reparentTo(render)
	handle.setPos(startPos)
	
	t=0
	step=(2*math.pi)/num
	
	enemies = []
	for i in range(num):
		x=math.cos(t)*r
		z=math.sin(t)*r
		if i == 0:
			enemies.append(Enemy(uid, handle, modelName, Point3(x,0,z)))
		else:
			enemies.append(Enemy(uid, handle, modelName, Point3(x,0,z)))
		t+=step
		uid+=1
		#print "made enemy at x:" + str(x) + " z:" + str(z)
		
	return handle
	
	#returns a handle
def spawnSpiral(num=5, r=2, direction=1, depth=50, modelName="emenytb_t1", startPos=Point3(0,20,0), uid=0):
	handle = NodePath(PandaNode("handle"+str(uid)))
	handle.reparentTo(render)
	handle.setPos(startPos)
	
	t=0
	step=(2*math.pi)/num
	depth/=num
	
	enemies = []
	for i in range(num):
		x=math.cos(t)*r*direction
		z=math.sin(t)*r*direction
		if i == 0:
			enemies.append(Enemy(uid, handle, modelName, Point3(x,0,z)))
		else:
			enemies.append(Enemy(uid, handle, modelName, Point3(x,depth*i,z)))
		t+=step
		uid+=1
		#print "made enemy at x:" + str(x) + " z:" + str(z)
	
	return handle
		