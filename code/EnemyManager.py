import math

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Point3

from Enemy import Enemy


class EnemyManager (DirectObject):

	def __init__(self):
		self.enemies = []
		self.enemiesSpawned = 0
		
		self.handles = []
		self.handlesCreated = 0
		
		taskMgr.add(self.cleanupEnemies, "EnemyCleanup")
	
	def spawnEnemy(self, handle, modelName, startPos=Point3(0,0,0), startHpr=Point3(0,0,0)):
		enemy = Enemy(self.enemiesSpawned, handle, modelName, startPos, startHpr)
		self.enemies.append(enemy)
		self.enemiesSpawned += 1
	
	def createHandle(self, startPos = Point3(0,20,0)):
		handle = NodePath(PandaNode("EnemyHandle"+str(self.handlesCreated)))
		handle.reparentTo(render)
		handle.setPos(startPos)
		handle.setTag("enemyChildren", str(0))
		self.handlesCreated += 1
		self.handles.append(handle)
		return handle
		
	
	def cleanupEnemies(self, task):
		for enemy in self.enemies:
			if (enemy.deleteMe):
				self.enemies.remove(enemy)
			
		for handle in self.handles:
			if (int(handle.getTag("enemyChildren")) == 0):
				print "Removing ", handle.getName()
				#messenger.send('removeEnemyHandle', [handle])
				self.handles.remove(handle)
				#handle.removeNode()
				
				
		return Task.cont
	
	
	def spawnCircle(self, num = 5, r = 2, modelName = "emenytb_t1", startPos = Point3(0,20,0)):
		handle = self.createHandle(startPos)
		t = 0
		step = (2 * math.pi) / num
		
		for i in range(num):
			x = math.cos(t) * r
			z = math.sin(t) * r
			self.spawnEnemy(handle, modelName, Point3(x,0,z))
			t += step
		
		return handle
		
	#returns a handle
	def spawnSpiral(self, num = 5, r = 2, direction = 1, depth = 50, modelName = "emenytb_t1", startPos = Point3(0,20,0)):
		handle = self.createHandle(startPos)
		
		t = 0
		step = (2 * math.pi) / num
		depth /= num
		
		for i in range(num):
			x = math.cos(t) * r * direction
			z = math.sin(t) * r * direction
			self.spawnEnemy(handle, modelName, Point3(x, depth * i, z))
			t += step
		
		return handle
			
