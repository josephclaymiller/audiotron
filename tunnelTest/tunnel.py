# Code base on a tutorial by: Shao Zhang and Phil Saltzman
# Last Updated: 4/18/2005

from pandac.PandaModules import Fog
from direct.showbase.DirectObject import DirectObject
from direct.interval.MetaInterval import Sequence #needed to continuously move the tunnel
from pandac.PandaModules import VBase3, VBase4
from direct.interval.LerpInterval import LerpPosHprInterval #needed to move and rotate tunnel
from direct.interval.FunctionInterval import Func #needed to continuously move the tunnel
from pandac.PandaModules import NodePath, PandaNode #used to make a tunnel Node Path which controlls tunnel specific lights
from pandac.PandaModules import DirectionalLight #needed to setup lighting
from music import MusicController #needed for playing game music and pulsing lights

#Global variables for the tunnel dimensions and speed of travel
TUNNEL_SEGMENT_LENGTH = 40					 
TUNNEL_TIME = 1.846	 #Amount of time for one segment to travel the
					 #distance of TUNNEL_SEGMENT_LENGTH

class Tunnel(DirectObject):
	#Code to initialize the tunnel
	def __init__(self, GMC):
		#instantiating music controller
		self.GMC=GMC
		
		#Creates the list [None, None, None, None]
		self.tunnel = [None for i in range(5)]
		
		#creates a NodePath handle for doing stuff to the entire tunnel
		self.NP = NodePath(PandaNode("tunnelNP"))
		self.NP.reparentTo(render)
		
		#adding tunnel lights
		dlight = DirectionalLight('dlight')
		dlight.setColor(VBase4(1, 1, 1, 1))
		dlnp = self.NP.attachNewNode(dlight)
		dlnp.setHpr(0, -60, 0)
		self.NP.setLight(dlnp)
		
		#pulsing dlight
		pulse = [x*8 for x in range(self.GMC.numSixteenths/8)]
		print str(len(pulse))
		self.GMC.addLitElement(dlight, pulse)
		
		for x in range(5):
			#Load a copy of the tunnel
			self.tunnel[x] = loader.loadModelCopy('..//assets//models//tunneltrapazoid.egg')
			#The front segment needs to be attached to render
			if x == 0:
				self.tunnel[x].reparentTo(self.NP)
			#The rest of the segments parent to the previous one, so that by moving
			#the front segement, the entire tunnel is moved
			else: self.tunnel[x].reparentTo(self.tunnel[x-1])
			#We have to offset each segment by its length so that they stack onto
			#each other. Otherwise, they would all occupy the same space.
			self.tunnel[x].setPos(0, 0, -TUNNEL_SEGMENT_LENGTH)
			#Now we have a tunnel consisting of 4 repeating segments with a
			#hierarchy like this:
			#render<-tunnel[0]<-tunnel[1]<-tunnel[2]<-tunnel[3]<-tunnel[4]
		
		#Create an instance of fog called 'distanceFog'.
		#'distanceFog' is just a name for our fog, not a specific type of fog.
		self.fog = Fog('distanceFog')
		#Set the initial color of our fog to black.
		self.fog.setColor(0, 0, 0)
		#Set the density/falloff of the fog.	The range is 0-1.
		#The higher the numer, the "bigger" the fog effect.
		self.fog.setExpDensity(.03)
		#Set fog to only affect the Tunnel...set to render if you want fog to affect everything
		self.NP.setFog(self.fog)
		
		self.contTunnel()
			
	#This function is called to snap the front of the tunnel to the back
	#to simulate traveling through it
	def contTunnel(self):
		#This line uses slices to take the front of the list and put it on the
		#back. For more information on slices check the Python manual
		self.tunnel = self.tunnel[1:]+ self.tunnel[0:1]
		#Set the front segment (which was at TUNNEL_SEGMENT_LENGTH) to 0, which
		#is where the previous segment started
		self.tunnel[0].setZ(0)
		#Reparent the front to render to preserve the hierarchy outlined above
		self.tunnel[0].reparentTo(self.NP)
		#Set the scale to be apropriate (since attributes like scale are
		#inherited, the rest of the segments have a scale of 1)
		self.tunnel[0].setScale(.155, .155, .5) #old (.155, .155, .305)
		#Set the new back to the values that the rest of teh segments have
		self.tunnel[4].reparentTo(self.tunnel[3])
		self.tunnel[4].setZ(-TUNNEL_SEGMENT_LENGTH)
		self.tunnel[4].setScale(1)
		
		#Set up the tunnel to move one segment and then call contTunnel again
		#to make the tunnel move infinitely
		self.tunnelMove = Sequence(
			LerpPosHprInterval(self.tunnel[0],
							 duration = TUNNEL_TIME,
							 pos=VBase3(0,0,(TUNNEL_SEGMENT_LENGTH*.5)), #change .5 to .305
							 hpr=VBase3(36,0,0),
							 startPos=VBase3(0,0,0),
							 startHpr=VBase3(0,0,0)
							 ),
			Func(self.contTunnel)
			)
		self.tunnelMove.start()


		#This function calls toggle interval to pause or unpause the tunnel.
	#Like addFogDensity, ToggleInterval could not be passed directly in the
	#accept command since the value of self.tunnelMove changes whenever
	#self.contTunnel is called
	def handlePause(self):
		ToggleInterval(self.tunnelMove)
#End Class World

#This function will toggle any interval passed to it between playing and paused
def ToggleInterval(interval):
	if interval.isPlaying(): interval.pause()
	else: interval.resume()

