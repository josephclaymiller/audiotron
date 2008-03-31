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
		
		self.handlesCreated = 0
		
		taskMgr.add(self.cleanupEnemies, "EnemyCleanup")
	
	def spawnEnemy(self, handle, modelName, startPos=Point3(0,0,0), startHpr=Point3(0,0,0)):
		enemy = Enemy(self.enemiesSpawned, handle, modelName, startPos, startHpr)
		self.enemies.append(enemy)
		self.enemiesSpawned += 1
	
	def cleanupEnemies(self, task):
		for enemy in self.enemies:
			if (enemy.deleteMe):
				del enemy
		return Task.cont
	
	
	def spawnCircle(self, num = 5, r = 2, modelName = "emenytb_t1", startPos = Point3(0,20,0)):
		handle = NodePath(PandaNode("handle"+str(self.handlesCreated)))
		handle.reparentTo(render)
		handle.setPos(startPos)
		
		t = 0
		step = (2 * math.pi) / num
		
		for i in range(num):
			x = math.cos(t) * r
			z = math.sin(t) * r
			self.spawnEnemy(handle, modelName, Point3(x,0,z))
			t += step
		
		self.handlesCreated += 1
		return handle
		
	#returns a handle
	def spawnSpiral(self, num = 5, r = 2, direction = 1, depth = 50, modelName = "emenytb_t1", startPos = Point3(0,20,0)):
		handle = NodePath(PandaNode("handle"+str(self.handlesCreated)))
		handle.reparentTo(render)
		handle.setPos(startPos)
		
		t = 0
		step = (2 * math.pi) / num
		depth /= num
		
		for i in range(num):
			x = math.cos(t) * r * direction
			z = math.sin(t) * r * direction
			self.spawnEnemy(handle, modelName, Point3(x, depth * i, z))
			t += step
		
		self.handlesCreated += 1
		return handle
			
