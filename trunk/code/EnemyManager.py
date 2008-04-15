import math

from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import NodePath
from pandac.PandaModules import PandaNode
from pandac.PandaModules import Point3

from pandac.PandaModules import AmbientLight, DirectionalLight #needed to setup lighting
from pandac.PandaModules import VBase4, VBase3

from direct.interval.LerpInterval import LerpPosInterval, LerpPosHprInterval #needed for movement

from Enemy import Enemy
from EnemyData import enemyData, enemyLevels, comboLevels


class EnemyManager (DirectObject):

	def __init__(self, musicController):
		self.musicController = musicController
		
		self.level = 0
		
		self.enemies = []
		self.enemiesSpawned = 0
		
		self.handles = []
		self.handlesCreated = 0
		
		self.musicPlaying = {}
		
		self.setupLights()
		
		taskMgr.add(self.cleanupEnemies, "EnemyCleanup")
		self.accept("EnemiesComboed", self.processCombo)
	
	def processCombo(self, combo):
		if (self.level < len(enemyLevels)):
			levelType = enemyLevels[self.level]
			for type, count in combo.iteritems():
				if (type == levelType and count >= comboLevels[self.level]):
					self.level += 1
					self.playMusic(enemyData[type]['music'])
					print "Unlock music ", enemyData[type]['music']
	
	def playMusic(self, musicFile):
		if musicFile in self.musicPlaying:
			self.musicPlaying[musicFile]['count'] += 1
		else:
			index = self.musicController.queueSound("..//assets//audio//" + musicFile)
			self.musicPlaying[musicFile] = {'count': 1, 'index': index}
		
	def spawnEnemy(self, type, handle, startPos=Point3(0,0,0), startHpr=Point3(0,0,0)):
		enemy = Enemy(self.enemiesSpawned, type, handle, startPos, startHpr)
		self.enemies.append(enemy)
		self.enemiesSpawned += 1
		self.playMusic(enemyData[type]['music'])
	
	def createHandle(self, enemyType, startPos = Point3(0,20,0)):
		handle = NodePath(PandaNode("EnemyHandle"+str(self.handlesCreated)))
		handle.reparentTo(render)
		handle.setPos(startPos)
		handle.setTag("enemyChildren", str(0))
		self.handlesCreated += 1
		self.handles.append(handle)
		
		for lightName in enemyData[enemyType]['lighting']:
			handle.setLight(self.lights[lightName])
		
		if len(enemyData[enemyType]['beatsPulse']) > 0:
			self.musicController.addPulsingElement(handle, enemyData[enemyType]['beatsPulse'])
		
		if len(enemyData[enemyType]['beatsLight']) > 0:
			self.musicController.addLitElement(handle, enemyData[enemyType]['beatsLight'])
		
		return handle
		
	
	def cleanupEnemies(self, task):
		for enemy in self.enemies:
			if (enemy.deleteMe):
				self.enemies.remove(enemy)
				
				musicFile = enemyData[enemy.type]['music']
				self.musicPlaying[musicFile]['count'] -= 1
				if (self.musicPlaying[musicFile]['count'] == 0):
					self.musicController.fadeOutSound(self.musicPlaying[musicFile]['index'])
					del self.musicPlaying[musicFile]
			
		for handle in self.handles:
			if (int(handle.getTag("enemyChildren")) == 0):
				print "Removing ", handle.getName()
				self.musicController.removePulsingElement(handle)
				self.handles.remove(handle)
				handle.removeNode()
				
				
		return Task.cont
		
	def setupLights(self):
		#red ambient light
		self.lights = {}
		
		self.ALred = AmbientLight('ALred')
		self.ALred.setColor(VBase4(1,0,0,1))
		self.ALredNP = render.attachNewNode(self.ALred)
		self.lights['ALred'] = self.ALredNP
		
		#green ambient light
		self.ALgreen = AmbientLight('ALgreen')
		self.ALgreen.setColor(VBase4(0,1,0,1))
		self.ALgreenNP = render.attachNewNode(self.ALgreen)
		self.lights['ALgreen'] = self.ALgreenNP
		
		#blue ambient light
		self.ALblue = AmbientLight('ALblue')
		self.ALblue.setColor(VBase4(0,0,1,1))
		self.ALblueNP = render.attachNewNode(self.ALblue)
		self.lights['ALblue'] = self.ALblueNP
		
		#red right directional Light
		self.DLRred = DirectionalLight('DLRred')
		self.DLRred.setColor(VBase4(1, 0, 0, 1))
		self.DLRredNP = render.attachNewNode(self.DLRred)
		self.DLRredNP.setHpr(45, -45, 0)
		self.lights['DLRred'] = self.DLRredNP
		
		#green right directional Light
		self.DLRgreen = DirectionalLight('DLRgreen')
		self.DLRgreen.setColor(VBase4(0, 1, 0, 1))
		self.DLRgreenNP = render.attachNewNode(self.DLRgreen)
		self.DLRgreenNP.setHpr(45, -45, 0)
		self.lights['DLRgreen'] = self.DLRgreenNP
		
		#blue right directional Light
		self.DLRblue = DirectionalLight('DLRblue')
		self.DLRblue.setColor(VBase4(0, 0, 1, 1))
		self.DLRblueNP = render.attachNewNode(self.DLRblue)
		self.DLRblueNP.setHpr(45, -45, 0)
		self.lights['DLRblue'] = self.DLRblueNP
		
		#red left directional Light
		self.DLLred = DirectionalLight('DLLred')
		self.DLLred.setColor(VBase4(1, 0, 0, 1))
		self.DLLredNP = render.attachNewNode(self.DLLred)
		self.DLLredNP.setHpr(-45, -45, 0)
		self.lights['DLLred'] = self.DLLredNP
		
		#green left directional Light
		self.DLLgreen = DirectionalLight('DLLgreen')
		self.DLLgreen.setColor(VBase4(0, 1, 0, 1))
		self.DLLgreenNP = render.attachNewNode(self.DLLgreen)
		self.DLLgreenNP.setHpr(-45, -45, 0)
		self.lights['DLLgreen'] = self.DLLgreenNP
		
		#blue left directional Light
		self.DLLblue = DirectionalLight('DLLblue')
		self.DLLblue.setColor(VBase4(0, 0, 1, 1))
		self.DLLblueNP = render.attachNewNode(self.DLLblue)
		self.DLLblueNP.setHpr(-45, -45, 0)
		self.lights['DLLblue'] = self.DLLblueNP
		
		#white bottom directional light
		self.DLBwhite = DirectionalLight('DLBwhite')
		self.DLBwhite.setColor(VBase4(1, 1, 1, 1))
		self.DLBwhiteNP = render.attachNewNode(self.DLBwhite)
		self.DLBwhiteNP.setHpr(0, 60, 0)
		self.lights['DLBwhite'] = self.DLBwhiteNP
	
	
	def spawnCircle(self, type = "testEnemy", num = 5, r = 2, startPos = Point3(0,20,0)):
		handle = self.createHandle(type, startPos)
		
		t = 0
		step = (2 * math.pi) / num
		
		for i in range(num):
			x = math.cos(t) * r
			z = math.sin(t) * r
			self.spawnEnemy(type, handle, Point3(x,0,z))
			t += step
		
		return handle
		
		
	#returns a handle
	def spawnSpiral(self, type = "testEnemy", num = 5, r = 2, direction = 1, depth = 50, startPos = Point3(0,0,0)):
		handle = self.createHandle(type, startPos)
		
		t = 0
		step = (2 * math.pi) / num
		depth /= num
		
		for i in range(num):
			x = math.cos(t) * r * direction
			z = math.sin(t) * r * direction
			self.spawnEnemy(type, handle, Point3(x, depth * i, z))
			t += step
		
		return handle
		
	def moveForward(self, handle, len=50, steps=4, endPos=Point3(0,0,0)):
		interval=LerpPosInterval(handle,
							 duration = steps*1.846,
							 pos=endPos, 
							 startPos=VBase3(0,steps*len+endPos.getY(),0)
							 )
		interval.start()
		
	def moveSpiral(self, handle, direction=1, depth=50, len=50, steps=4, endPos=Point3(0,0,0)):
		interval=LerpPosHprInterval(handle,
							 duration = steps*1.846,
							 pos=VBase3(endPos.getX(), endPos.getY()-depth, endPos.getZ()), #change .5 to .305
							 hpr=VBase3(0,0,steps*180),
							 startPos=VBase3(0,steps*len+endPos.getY(),0),
							 startHpr=VBase3(0,0,0)
							 )
		interval.start()
