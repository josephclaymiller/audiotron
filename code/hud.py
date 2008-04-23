from direct.showbase.DirectObject import DirectObject #needed
from direct.task import Task #for the task manager & stuff

from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib

from direct.showbase.Loader import Loader #for loading & unloading SFX
#import direct.directbase.DirectStart #for loading SFX old(not sure if this is needed)
from pandac.PandaModules import AudioSound #for setTime()
import colorsys #so I can change RGB to HSB
from pandac.PandaModules import Vec3 #for Vec4
#import math

class HUD(DirectObject):

	def __init__(self):
		self.HUDfont = loader.loadFont('..\\HUD\\ARCADE.TTF')
		
		self.life = []
		for x in range(0,4):
			y=((x%2)*-2)+1
			z=x/2
			self.life.append(OnscreenImage(image='..\\assets\\HUD\\heart4.png', pos=Vec3(.055*y+y*z*.11,0,-.9), scale=Vec3(.045,0,.045)))
			self.life[x].setTransparency(TransparencyAttrib.MAlpha)
		
		self.beatBarL = OnscreenImage(image='..\\assets\\HUD\\beatBar.png', pos=Vec3(-1.25,0,0), scale=Vec3(.015,0,.6))
		self.beatBarL.setTransparency(TransparencyAttrib.MAlpha)
		
		self.beatBarR = OnscreenImage(image='..\\assets\\HUD\\beatBar.png', pos=Vec3(1.25,0,0), scale=Vec3(.015,0,.6))
		self.beatBarR.setTransparency(TransparencyAttrib.MAlpha)
			
		#self.shoot = []
		#for x in range(0,4):
		#	self.shoot.append(OnscreenImage(image='..\\assets\\HUD\\shoot1.png', pos=Vec3(1.235-x*.18,0,-.9), scale=Vec3(.0375,0,.0375)))
		#	self.shoot[x].setTransparency(TransparencyAttrib.MAlpha)
	
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
		