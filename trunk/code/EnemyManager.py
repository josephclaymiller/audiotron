import math

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Point3

from pandac.PandaModules import AmbientLight, DirectionalLight #needed to setup lighting
from pandac.PandaModules import VBase4

from Enemy import Enemy


class EnemyManager (DirectObject):

	def __init__(self, musicController):
		self.musicController = musicController
		
		self.enemies = []
		self.enemiesSpawned = 0
		
		self.handles = []
		self.handlesCreated = 0
		
		self.setupLights()
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
				messenger.send('removeEnemyHandle', [handle])
				self.handles.remove(handle)
				handle.removeNode()
				
				
		return Task.cont
		
	def setupLights(self):
		#red ambient light
		self.ALred = AmbientLight('ALred')
		self.ALred.setColor(VBase4(1,0,0,1))
		self.ALredNP = render.attachNewNode(self.ALred)
		
		#green ambient light
		self.ALgreen = AmbientLight('ALgreen')
		self.ALgreen.setColor(VBase4(0,1,0,1))
		self.ALgreenNP = render.attachNewNode(self.ALgreen)
		
		#blue ambient light
		self.ALblue = AmbientLight('ALblue')
		self.ALblue.setColor(VBase4(0,0,1,1))
		self.ALblueNP = render.attachNewNode(self.ALblue)
		
		#blue right directional Light
		self.DLRblue = DirectionalLight('self.DLRblue')
		self.DLRblue.setColor(VBase4(0, 0, 1, 1))
		self.DLRblueNP = render.attachNewNode(self.DLRblue)
		self.DLRblueNP.setHpr(45, -45, 0)
		
		#white bottom directional light
		self.DLBwhite = DirectionalLight('self.DLBwhite')
		self.DLBwhite.setColor(VBase4(1, 1, 1, 1))
		self.DLBwhiteNP = render.attachNewNode(self.DLBwhite)
		self.DLBwhiteNP.setHpr(0, 60, 0)
	
	
	def spawnCircle(self, num = 5, r = 2, modelName = "emenytb_t1", startPos = Point3(0,20,0)):
		handle = self.createHandle(startPos)
		t = 0
		step = (2 * math.pi) / num
		
		for i in range(num):
			x = math.cos(t) * r
			z = math.sin(t) * r
			self.spawnEnemy(handle, modelName, Point3(x,0,z))
			t += step
		
		
		#TRIAL ADD LIGHTS AND PULSE
		handle.setLight(self.ALredNP)
		handle.setLight(self.DLRblueNP)
		handle.setLight(self.DLBwhiteNP)
		
		
		pulse = [x*4 for x in range(self.musicController.numSixteenths/4)]
		self.musicController.addPulsingElement(handle, pulse)
		
		#END TRIAL ADD LIGHTS AND PULSE
		return handle
		
	#returns a handle
	def spawnSpiral(self, num = 5, r = 2, direction = 1, depth = 50, modelName = "emenytb_t1", startPos = Point3(0,0,0)):
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
			
