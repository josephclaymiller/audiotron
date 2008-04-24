from direct.showbase.DirectObject import DirectObject #needed
from direct.task import Task #for the task manager & stuff

from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib

from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode

from direct.showbase.Loader import Loader #for loading & unloading SFX
#import direct.directbase.DirectStart #for loading SFX old(not sure if this is needed)
from pandac.PandaModules import AudioSound #for setTime()
import colorsys #so I can change RGB to HSB
from pandac.PandaModules import Vec3 #for Vec4
#import math
from EnemyData import enemyData, levelData
from pandac.PandaModules import Point3
from pandac.PandaModules import NodePath, PandaNode
from direct.interval.LerpInterval import LerpHprInterval
from pandac.PandaModules import VBase4, VBase3
import random

class HUD(DirectObject):

	def __init__(self, handle):
		self.HUDfont = loader.loadFont('..//assets//HUD//ElectricBoots.TTF')
		self.handle = handle
		
		self.life = []
		for x in range(0,8):
			self.life.append(OnscreenImage(image='..\\assets\\HUD\\heart.PNG', pos=Vec3(-1.235+x*.11,0,-.9), scale=Vec3(.04625,0,.04625)))
			self.life[x].setTransparency(TransparencyAttrib.MAlpha)
		
		self.level=0
		self.enemies = []
		self.billboard =[]
		self.idleModel = []
		self.enemyTypes = []
		self.maxCombo=0
		self.combo = {}
		self.comboTag = {}
		
		self.score=0
		self.newScore=0
		
		self.comboTXT = OnscreenText(text = 'combo\n0/4', pos = (1.1,.9), scale = 0.075, fg=(1,0,0,1), align=TextNode.ACenter, font=self.HUDfont, mayChange=True)
		self.multTXT = OnscreenText(text = 'mult\nx2', pos = (-1.1,.9), scale = 0.075, fg=(1,1,0,1), align=TextNode.ACenter, font=self.HUDfont, mayChange=True)
		self.scoreTXT = OnscreenText(text = 'score\n0', pos = (1.275,-.85), scale = 0.075, fg=(1,1,1,1), align=TextNode.ARight, font=self.HUDfont, mayChange=True)
		
		for x in range(0, len(levelData)):
			for y in range(0, len(levelData[x])):
				self.enemyTypes.append(levelData[x][y][0])
		
		for x in range(0, len(self.enemyTypes)):
			data=enemyData[self.enemyTypes[x]]
			
			self.combo[self.enemyTypes[x]] = 0
			self.comboTag[self.enemyTypes[x]] = OnscreenText(text="0", pos = (-.85+x*.225,.75), scale = 0.075, fg=(1,1,1,1), align=TextNode.ACenter, font=self.HUDfont, mayChange=True)
			
			self.enemies.append(NodePath(PandaNode("Enemy"+str(self.enemyTypes[x]))))
			self.enemies[x].reparentTo(self.handle)
			self.enemies[x].setScale(data['scale']*.08)
			self.enemies[x].setPos(Point3(-.45+x*.12,2,.48))
			#self.enemies[x].setHpr(startHpr)
			
			self.idleModel.append(loader.loadModelCopy("..//assets//models//enemies//" + str(data['model']) + ".egg"))
			self.idleModel[x].reparentTo(self.enemies[x])
			
			self.billboard.append(loader.loadModelCopy('..//assets//models//plane.egg.pz'))
			self.billboard[x].reparentTo(self.enemies[x])
			self.billboard[x].setPos(0, 0, 0)
			self.billboard[x].setScale(1 / data['scale'])
			self.billboard[x].setTexture(loader.loadTexture("..//assets//images//targetCursor.png"))
			self.billboard[x].setTransparency(True)
			self.billboard[x].setBillboardPointEye()
			self.billboard[x].hide()
			
			#rotate stuff
			self.enemyMove = LerpHprInterval(self.enemies[x],
								duration = random.randint(25,35),
								hpr=VBase3(360,360,360),
								startHpr=VBase3(0,0,0)
								)
			self.enemyMove.loop()
		
		self.billboard[0].show()
		taskMgr.add(self.incScore, "incScore")
	
	def hit(self, lives, health):
		if health < 2:
			self.life[lives].setImage('..\\assets\\HUD\\heart'+str(health)+'.PNG')
			self.life[lives].setTransparency(TransparencyAttrib.MAlpha)
		else:
			self.life[lives+1].hide()
	
	def updateCombo(self, type):
		self.combo[type]+=1
		self.comboTag[type].setText(str(self.combo[type]))
		if self.combo[type] >= levelData[self.level][0][1]:
			self.comboTag[type].setFg((1,1,0,1))
		
		if self.combo[type]>self.maxCombo:
			self.maxCombo=self.combo[type]
			self.comboTXT.setText('combo\n' + str(self.maxCombo) + '/' + str(levelData[self.level][0][1]))
			if self.maxCombo>=levelData[self.level][0][1]:
				self.comboTXT.setFg((1,1,0,1))
		
	def killCombo(self):
		for x in range(0,len(self.enemyTypes)):
			self.combo[self.enemyTypes[x]]=0
			self.comboTag[self.enemyTypes[x]].setText("")
			self.comboTag[self.enemyTypes[x]].setFg((1,0,0,1))
			self.maxCombo=0
			self.comboTXT.setText('combo\n0/'+str(levelData[self.level][0][1]))
			self.comboTXT.setFg((1,0,0,1))
		
	def updateLevel(self, level):
		for x in range(0, len(levelData[self.level])):
			self.billboard[enemyData[levelData[self.level][x][0]]['hud']].hide()
		self.level=level
		if self.level>4:
			self.level=4
		else:
			for x in range(0, len(levelData[self.level])):
				self.billboard[enemyData[levelData[self.level][x][0]]['hud']].show()
	
	def updateScore(self, score):
		self.newScore=score
		#taskMgr.add(self.incScore, "incScore"+str(score))
	
	def incScore(self, task):
		if self.score < self.newScore:
			self.score+=int((self.newScore-self.score)/100)+1
			self.scoreTXT.setText('score\n'+str(self.score))
		return Task.cont