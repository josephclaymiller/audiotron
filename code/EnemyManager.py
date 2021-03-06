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
from EnemyData import enemyData, levelData


class EnemyManager (DirectObject):

	def __init__(self, musicController, HUD, player):
		self.musicController = musicController
		self.HUD=HUD
		self.player=player
		
		self.musicPlaying = {}
		self.setupLights()
		
		self.level = 0
		self.sublevels = [0]
		
		self.enemies = []
		self.deadEnemies = {}
		self.deadHandle = NodePath(PandaNode("DeadEnemies"))
		self.deadHandle.setTag("enemyChildren", str(0))
		self.deadHandle.hide()
		
		uid = 0
		for type, data in enemyData.iteritems():
			deadguys = []
			for i in range(50):
				deadguys.append(Enemy(uid, type, self.deadHandle))
				uid += 1
			self.deadEnemies[type] = deadguys
		
		self.handles = []
		self.unusedHandles = {}
		
		uid = 0
		for type, data in enemyData.iteritems():
			handles = []
			
			for i in range(20):
				handle = NodePath(PandaNode("EnemyHandle"+str(uid)))
				handle.reparentTo(render)
				handle.setTag("enemyChildren", str(0))
				handle.setTag("type", type)
				handles.append(handle)
				
				for lightName in data['lighting']:
					handle.setLight(self.lights[lightName])
				
				if len(data['beatsPulse']) > 0:
					self.musicController.addPulsingElement(handle, data['beatsPulse'])
				
				if len(data['beatsLight']) > 0:
					self.musicController.addLitElement(self.pulseLight[data['light']], data['beatsLight'])
					
				uid += 1
				
			self.unusedHandles[type] = handles
		
		taskMgr.add(self.cleanupEnemies, "EnemyCleanup")
		self.accept("EnemiesComboed", self.processCombo)
	
	def processCombo(self, combo):
		if (self.level < len(levelData)):
			for type, count in combo.iteritems():
				#if count > levelData[self.level][0][1]:
				#	self.player.combo=True
				for sublevel in self.sublevels:
				
					(sublevelType, sublevelCount) = levelData[self.level][sublevel]
					
					if (type == sublevelType and count >= sublevelCount):
						self.playMusic(enemyData[type]['music'], type)
						print "Unlock music ", enemyData[type]['music']
						
						#light enemy in HUD
						for lightName in enemyData[type]['lighting']:
							self.HUD.enemies[enemyData[type]['hud']].setLight(self.lights[lightName])
							self.HUD.billboard[enemyData[type]['hud']].hide()
						self.sublevels.remove(sublevel)
						
			if (len(self.sublevels) == 0):
				self.level += 1
				self.HUD.updateLevel(self.level)
				if (self.level < len(levelData)):
					self.sublevels = range(len(levelData[self.level]))
				else:
					self.player.alive=False
					self.HUD.endGame('you win!')
					self.sublevels = []
	
	def playMusic(self, musicFile, type):
		if musicFile in self.musicPlaying:
			self.musicPlaying[musicFile]['count'] += 1
		else:
			self.musicController.showNote('new track unlocked!')
			index = self.musicController.addSound(enemyData[type]['hud'])
			self.musicPlaying[musicFile] = {'count': 1, 'index': index}
	
	def getUnlockedEnemyTypes(self):
		unlockedTypes = []
		for level in range(self.level):
			for (enemy, combo) in levelData[level]:
				unlockedTypes.append(enemy)
		return unlockedTypes
				
	def getCurrentEnemyTypes(self):
		currentTypes = []
		for sublevel in self.sublevels:
			currentTypes.append(levelData[self.level][sublevel][0])
		return currentTypes
		
	def spawnEnemy(self, type, handle, startPos=Point3(0,0,0), startHpr=Point3(0,0,0)):
		if len(self.deadEnemies[type]) > 0:
			enemy = self.deadEnemies[type][0]
			self.enemies.append(enemy)
			self.deadEnemies[type].remove(enemy)
			enemy.spawn(handle, startPos, startHpr)
	
	def createHandle(self, enemyType, startPos = Point3(0,20,0)):
		if (len(self.unusedHandles[enemyType]) > 0):
			handle = self.unusedHandles[enemyType][0]
			self.handles.append(handle)
			self.unusedHandles[enemyType].remove(handle)
			handle.setPos(startPos)
			return handle
	
	def cleanupEnemies(self, task):
		for enemy in self.enemies:
			if (enemy.finishedDying()):
				enemy.cleanup(self.deadHandle)
				self.deadEnemies[enemy.type].append(enemy)
				self.enemies.remove(enemy)
			
		for handle in self.handles:
			if (int(handle.getTag("enemyChildren")) == 0):
				self.handles.remove(handle)
				type = handle.getTag("type")
				self.unusedHandles[type].append(handle)
				
		return Task.cont
		
	def setupLights(self):
		#red ambient light
		self.lights = {}
		
		self.ALred = AmbientLight('ALred')
		self.ALred.setColor(VBase4(1,0,0,1))
		self.ALredNP = render.attachNewNode(self.ALred)
		self.lights['ALred'] = self.ALredNP
		
		#yellow ambient light
		self.ALyellow = AmbientLight('ALyellow')
		self.ALyellow.setColor(VBase4(1,1,0,1))
		self.ALyellowNP = render.attachNewNode(self.ALyellow)
		self.lights['ALyellow'] = self.ALyellowNP
		
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
		
		#yellow right directional Light
		self.DLRyellow = DirectionalLight('DLRyellow')
		self.DLRyellow.setColor(VBase4(1, 1, 0, 1))
		self.DLRyellowNP = render.attachNewNode(self.DLRyellow)
		self.DLRyellowNP.setHpr(45, -45, 0)
		self.lights['DLRyellow'] = self.DLRyellowNP
		
		#blue right directional Light
		self.DLRblue = DirectionalLight('DLRblue')
		self.DLRblue.setColor(VBase4(0, 0, 1, 1))
		self.DLRblueNP = render.attachNewNode(self.DLRblue)
		self.DLRblueNP.setHpr(45, -45, 0)
		self.lights['DLRblue'] = self.DLRblueNP
		
		#white right directional Light
		self.DLRwhite = DirectionalLight('DLRwhite')
		self.DLRwhite.setColor(VBase4(1, 1, 1, .5))
		self.DLRwhiteNP = render.attachNewNode(self.DLRwhite)
		self.DLRwhiteNP.setHpr(45, -110, 0)
		self.lights['DLRwhite'] = self.DLRwhiteNP
		
		#red left directional Light
		self.DLLred = DirectionalLight('DLLred')
		self.DLLred.setColor(VBase4(1, 0, 0, 1))
		self.DLLredNP = render.attachNewNode(self.DLLred)
		self.DLLredNP.setHpr(-45, -45, 0)
		self.lights['DLLred'] = self.DLLredNP
		
		#yellow left directional Light
		self.DLLyellow = DirectionalLight('DLLyellow')
		self.DLLyellow.setColor(VBase4(1, 1, 0, 1))
		self.DLLyellowNP = render.attachNewNode(self.DLLyellow)
		self.DLLyellowNP.setHpr(-45, -45, 0)
		self.lights['DLLyellow'] = self.DLLyellowNP
		
		#blue left directional Light
		self.DLLblue = DirectionalLight('DLLblue')
		self.DLLblue.setColor(VBase4(0, 0, 1, 1))
		self.DLLblueNP = render.attachNewNode(self.DLLblue)
		self.DLLblueNP.setHpr(-45, -45, 0)
		self.lights['DLLblue'] = self.DLLblueNP
		
		#white left directional Light
		self.DLLwhite = DirectionalLight('DLLwhite')
		self.DLLwhite.setColor(VBase4(1, 1, 1, .5))
		self.DLLwhiteNP = render.attachNewNode(self.DLLwhite)
		self.DLLwhiteNP.setHpr(-45, -110, 0)
		self.lights['DLLwhite'] = self.DLLwhiteNP
		
		#white bottom directional light
		self.DLBwhite = DirectionalLight('DLBwhite')
		self.DLBwhite.setColor(VBase4(1, 1, 1, 1))
		self.DLBwhiteNP = render.attachNewNode(self.DLBwhite)
		self.DLBwhiteNP.setHpr(0, 60, 0)
		self.lights['DLBwhite'] = self.DLBwhiteNP
		
		self.pulseLight = []
		self.pulseLightNP = []
		for x in range(0,8):
			#white bottom directional light
			self.pulseLight.append(DirectionalLight('pulseLight'+str(x)))
			self.pulseLight[x].setColor(VBase4(1, 1, 1, 1))
			self.pulseLightNP.append(render.attachNewNode(self.pulseLight[x]))
			self.pulseLightNP[x].setHpr(0, 20, 0)
			self.lights['pulseLight'+str(x)] = self.pulseLightNP[x]
		
		
	
	
	def spawnCircle(self, type = "testEnemy", num = 5, r = 2.0, startPos = Point3(0,20,0)):
		handle = self.createHandle(type, startPos)
		
		r = min(5.0, max(r, 0.5 * num / math.pi))
		t = 0
		step = (2 * math.pi) / num
		
		for i in range(num):
			x = math.cos(t) * r
			z = math.sin(t) * r
			self.spawnEnemy(type, handle, Point3(x,0,z))
			t += step
		
		return handle
		

	def spawnRect(self, type = "testEnemy", rows = 3, cols = 2, spacing = 1.0, startPos = Point3(0,20,0)):
		handle = self.createHandle(type, startPos)
		
		right = cols * spacing / 2
		top = rows * spacing / 2
		
		for i in range(rows):
			for j in range(cols):
				x = right - spacing * j
				z = top - spacing * i
				self.spawnEnemy(type, handle, Point3(x,0,z))
		
		return handle
		
		
	def spawnSpiral(self, type = "testEnemy", num = 5, r = 2, direction = 1, depth = 50, startPos = Point3(0,0,0)):
		handle = self.createHandle(type, startPos)
		
		r = min(5.0, max(r, 0.5 * num / math.pi))
		t = 0
		step = (2 * math.pi) / num
		depth /= num
		
		for i in range(num):
			x = math.cos(t) * r * direction
			z = math.sin(t) * r * direction
			self.spawnEnemy(type, handle, Point3(x, -depth * i, z))
			t += step
		
		return handle
		
	def moveForward(self, handle, len=50, steps=6, endPos=Point3(0,-100,0)):
		interval=LerpPosInterval(handle,
							 duration = steps*1.846,
							 pos = endPos, 
							 startPos = VBase3(handle.getPos().getX(), steps * len + endPos.getY(), handle.getPos().getZ())
							 )
		interval.start()
		
	def moveSpiral(self, handle, direction=1, depth=50, len=50, steps=6, endPos=Point3(0,-100,0)):
		interval = LerpPosHprInterval(handle,
							 duration = steps * 1.846,
							 pos = VBase3(endPos.getX(), endPos.getY() - depth, endPos.getZ()), #change .5 to .305
							 hpr = VBase3(0, 0, steps * 180),
							 startPos = VBase3(handle.getPos().getX(), steps * len + endPos.getY(), handle.getPos().getZ()),
							 startHpr = VBase3(0,0,0)
							 )
		interval.start()
