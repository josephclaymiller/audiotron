import direct.directbase.DirectStart 
from pandac.PandaModules import Fog
from direct.showbase.DirectObject import DirectObject
from direct.interval.MetaInterval import Sequence #needed to continuously move the tunnel
from pandac.PandaModules import VBase3, VBase4
from direct.interval.LerpInterval import LerpPosHprInterval #needed to move and rotate tunnel
from direct.interval.FunctionInterval import Func #needed to continuously move the tunnel
from pandac.PandaModules import NodePath, PandaNode #used to make a tunnel Node Path which controlls tunnel specific lights
from pandac.PandaModules import DirectionalLight, AmbientLight #needed to setup lighting
import sys #used to exit
from music import MusicController #needed for playing game music and pulsing lights
from tunnel import Tunnel #needed for the tunnel! :P
from Enemy import Enemy
from pandac.PandaModules import CollisionHandlerEvent, CollisionTraverser
from direct.actor.Actor import Actor

class World(DirectObject):
	def __init__(self):
		###Standard initialization stuff
		#Cammera settings
		base.disableMouse() #disable mouse control so that we can place the camera
		camera.setPos(0,0,0)
		camera.lookAt(0,0,-100)
		base.setBackgroundColor(0,0,0) #set the background color to black
		
		#load music controller
		self.GMC=MusicController()
		
		#Load the tunel and start the tunnel
		self.tunnel=Tunnel(self.GMC)
		
		#setup collisions and load an enemy
		self.setupCollision()
		self.enemyTest()
		
		 #Define the keyboard input
		#Escape closes the demo
		self.accept('escape', sys.exit)
		#Handle pausing the tunnel
		self.accept('p', self.tunnel.handlePause)
		#Handle turning the fog on and off
		self.accept('t', ToggleFog, [self.tunnel.NP, self.tunnel.fog])
	
	def enemyTest(self):
		#create node path
		self.enemyNP = NodePath(PandaNode("enemyNP"))
		self.enemyNP.reparentTo(render)
		self.enemyNP.setPos(0,0,-20)
		
		#load actor
		self.enemy1=Enemy(self.enemyNP)
		#self.model = Actor("../assets/models/ememydtb.egg")
		#self.model.reparentTo(self.enemyNP)
		self.enemy1.model.setPos(0,0,-20)
		self.enemy1.model.setScale(.25)
		#self.model.reparentTo(self.enemyNP)
		
		#create lighting
		alight = AmbientLight('alight')
		alight.setColor(VBase4(.5, 0, 0, 1))
		alnp = self.enemyNP.attachNewNode(alight)
		self.enemyNP.setLight(alnp)
		
		dlight = DirectionalLight('dlight')
		dlight.setColor(VBase4(0, 0, .75, 1))
		dlnp = self.enemyNP.attachNewNode(dlight)
		dlnp.setHpr(0, -60, 0)
		self.enemyNP.setLight(dlnp)
		
		dlight = DirectionalLight('dlight')
		dlight.setColor(VBase4(1, 1, 1, 1))
		dlnp = self.enemyNP.attachNewNode(dlight)
		dlnp.setHpr(0, 60, 0)
		self.enemyNP.setLight(dlnp)
		
		#create pulse
		pulse = [x*4 for x in range(self.GMC.numSixteenths/4)]
		self.GMC.addPulsingElement(self.enemyNP, pulse)
	
	def setupCollision(self):
		self.cHandler = CollisionHandlerEvent()
		self.cHandler.setInPattern("%fn-into-%in")
		base.cHandler = self.cHandler

		self.cTrav = CollisionTraverser()
		base.cTrav = self.cTrav

#This function will toggle fog on a node
def ToggleFog(node, fog):
	#If the fog attached to the node is equal to the one we passed in, then
	#fog is on and we should clear it
	if node.getFog() == fog: node.clearFog()
	#Otherwise fog is not set so we should set it
	else: node.setFog(fog)
	
w = World()
run()