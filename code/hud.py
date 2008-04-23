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
		for x in range(0,4):
			y=((x%2)*-2)+1
			z=x/2
			self.life.append(OnscreenImage(image='..\\assets\\HUD\\heart4.png', pos=Vec3(.055*y+y*z*.11,0,-.9), scale=Vec3(.045,0,.045)))
			self.life[x].setTransparency(TransparencyAttrib.MAlpha)
			
		self.enemies = []
		self.billboard =[]
		self.idleModel = []
		self.enemyTypes = []
		self.combo = {}
		self.comboTag = {}
		
		for x in range(0, len(levelData)):
			for y in range(0, len(levelData[x])):
				self.enemyTypes.append(levelData[x][y][0])
		
		for x in range(0, len(self.enemyTypes)):
			data=enemyData[self.enemyTypes[x]]
			
			self.combo[self.enemyTypes[x]] = 0
			self.comboTag[self.enemyTypes[x]] = OnscreenText(text = str(x), pos = (-.85+x*.225,.75), scale = 0.075, fg=(1,1,1,1), align=TextNode.ACenter, font=self.HUDfont, mayChange=True)
			
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
	
	def hit(self, lives, health):
		if health < 4:
			self.life[lives].setImage('..\\assets\\HUD\\heart'+str(health)+'.png')
			self.life[lives].setTransparency(TransparencyAttrib.MAlpha)
		else:
			self.life[lives+1].hide()
	
	def updateShoot(self, beat):
		if beat<4:
			self.shoot[beat].setImage('..\\assets\\HUD\\shoot2.png')
			self.shoot[beat].setTransparency(TransparencyAttrib.MAlpha)
		else:
			beat=beat%4
			self.shoot[beat].setImage('..\\assets\\HUD\\shoot3.png')
			self.shoot[beat].setTransparency(TransparencyAttrib.MAlpha)
			if beat >= 3:
				for x in range(0,4):
					self.shoot[x].setImage('..\\assets\\HUD\\shoot1.png')
					self.shoot[x].setTransparency(TransparencyAttrib.MAlpha)
		