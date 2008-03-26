from direct.showbase.DirectObject import DirectObject #needed
from direct.task import Task #for the task manager & stuff
#from pandac.PandaModules import ClockObject #for the global clock
from direct.showbase.Loader import Loader #for loading & unloading SFX
#import direct.directbase.DirectStart #for loading SFX old(not sure if this is needed)
from pandac.PandaModules import AudioSound #for setTime()
import colorsys #so I can change RGB to HSB
from pandac.PandaModules import Vec4 #for Vec4

class MusicController(DirectObject):
	
	def __init__(self):
		self.GLOBAL_CLOCK_TEMP=0 #tempararily replacing any instances of "globalClock.getRealTime()"
		self.bpm=130
		self.numMeasures=17
		self.numSixteenths=self.numMeasures*16
		self.maxSounds=1000
		self.secondsPerLoop=float(self.numMeasures*240)/self.bpm #=(#measures per loop * beats per measure) * (seconds per beat) = (17*4)*(60/bpm)
		self.loopStartTime=self.GLOBAL_CLOCK_TEMP
		self.loopEndTime=0 #initialized at 0 to start loop at game start! ***NOTE: should be set to self.loopStartTime+self.secondsPerLoop :NOTE***
		self.music = [] #needs to be filled with sounds loaded like "self.music.append(loader.loadSfx("SoundFile.wav"))"
		self.tempMusic = [] #a temp array for playing music...gets cleared every new loop
		
		#TRIAL
		#self.music.append(loader.loadSfx("SFX//NeverHome.mp3"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Shane Drums Full.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Shane Rhythm Guitar.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Tom Hon Solo.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Kevin hachacha.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Shane Melody Guitar.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Brian Backup Trumpet.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Brian Backup Vocals.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Brian Backup Vocals Hi.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Kevin Backup Guitar.wav"))
		#self.music.append(loader.loadSfx("..//assets//audio//Game2_Shane upbeat Vidaurri.wav"))#TRIAL DELETE
		
		
		self.sixteenth=0
		self.secondsPerSixteenth=self.secondsPerLoop/self.numSixteenths
		self.pulseQueue = [] #a list of every pulse (divided into 16th notes)
		self.pulseElements = [] # a list of every pulsing element
		self.lightQueue = []
		self.litElements = []
		self.lastPulseTime=self.GLOBAL_CLOCK_TEMP
		
		#initialize pulse queue
		for i in range(0,self.numSixteenths):
			self.pulseQueue.append([])
			self.lightQueue.append([])
		#print "pulse queue len: " +str(len(self.pulseQueue))
		#print "light queue len: " +str(len(self.lightQueue))
		

		taskMgr.add(self.playMusic, "playMusic")
		taskMgr.add(self.pulseManager, "pulseManager")
	
	def getPos(self):
		return float((gobalClock.getRealTime-self.loopStartTime)/self.secondsPerLoop)
	
	def playMusic(self, task):
		time=self.GLOBAL_CLOCK_TEMP
		
		if time>=self.loopEndTime:
			self.loopStartTime=time
			self.loopEndTime=time+self.secondsPerLoop
			#self.sixteenth=0 #used to need this when sixteenth wasn't reset in the pulseManager (now this is unnecisary)
			#TRIAL
			#self.loopEndTime=time+self.music[0].length() #TRIAL DELETE
			
			#delete temp sound clips
			for i in range(len(self.tempMusic)):
				#print "delete"
				self.tempMusic[0].stop()
				loader.unloadSfx(self.tempMusic[0])
				del self.tempMusic[0]
			
			#play sound clips
			for i in range(len(self.music)):
				self.music[i].setTime(self.GLOBAL_CLOCK_TEMP-time)
				self.music[i].play()
				#print i
				
		return Task.cont
	
	def addSound(self, name):
		i=len(self.music)
		#print i
		if (i+len(self.tempMusic))<self.maxSounds:
			self.music.append(loader.loadSfx(name))
			self.music[i].setTime(self.GLOBAL_CLOCK_TEMP-self.loopStartTime)
			self.music[i].play()
			return i
		#print len(self.music)
		return -1
	
	def queueSound(self, name):
		i=len(self.music)
		#print i
		if (i+len(self.tempMusic))<self.maxSounds:
			self.music.append(loader.loadSfx(name))
			return i
		#print len(self.music)
		return -1
	
	def removeSound(self, x):
		i=len(self.tempMusic)
		if x<len(self.music):
			#print len(self.music)
			self.music[x].stop()
			self.tempMusic.append(self.music.pop(x))
			self.tempMusic[i].setTime(self.GLOBAL_CLOCK_TEMP-self.loopStartTime)
			self.tempMusic[i].play()
			#print len(self.music)
			return i
		return -1
	
	def killSound(self, x):
		if x<len(self.music):
			#print len(self.music)
			self.music[x].stop()
			loader.unloadSfx(self.music[x])
			del self.music[x]
			#print len(self.music)
			return x
		return -1
	
	#put one sound, "x", in the TEMP LOOP and QUEUE a new sound, "name"
	def swapSound(self, x, name):
		i=self.queueSound(name)
		if i<0:
			self.killSound(x)
			#print "hi"
			return self.queueSound(name)
		#print "remove"
		self.removeSound(x)
		return i
	
	def replaceSound(self, x, name):
		if x<len(self.music):
			self.music[x].stop()
			loader.unloadSfx(self.music[x])
			self.music[x]=loader.loadSfx(name)
			self.music[x].setTime(self.GLOBAL_CLOCK_TEMP-self.loopStartTime)
			self.music[x].play()
			return x
		return -1
	
	def pulseManager(self, task):
		time=self.GLOBAL_CLOCK_TEMP

		deflate=(time-self.lastPulseTime)*(.25/(self.secondsPerLoop/self.numMeasures))
		fade=(time-self.lastPulseTime)*(-1.0/(self.secondsPerLoop/self.numMeasures))
		##print str(fade)
		
		#decrease scale of all pulsing elements
		for i in range(len(self.pulseElements)):
			self.pulseElements[i].setScale(self.pulseElements[i].getSx()-deflate)
			
		#decrease lumens of all lit elements
		for i in range(len(self.litElements)):
			addBrightness(self.litElements[i],fade)
		
		if (self.loopStartTime+(self.sixteenth*self.secondsPerSixteenth)) < time:
			#pulse elements by scale
			for i in range(len(self.pulseQueue[self.sixteenth])):
				self.pulseQueue[self.sixteenth][i].setScale(1)
			#pulse elements by light
			for i in range(len(self.lightQueue[self.sixteenth])):
				addBrightness(self.lightQueue[self.sixteenth][i],200)#I can add whatever I want because the max lumens is restricted by restrain
				#print "Pulse! " + str(self.sixteenth)
				
			#increment sixteenth and check if a new loop has started
			self.sixteenth+=1
			if self.sixteenth>=self.numSixteenths:
				self.sixteenth=0
		
		self.lastPulseTime=time
		return Task.cont
	
	def addPulsingElement(self, element, beats):
		self.pulseElements.append(element)
		for i in range(len(beats)):
			self.pulseQueue[beats[i]].append(element)
			#print "added pulse"
			
	def addLitElement(self, light, beats):
		self.litElements.append(light)
		for i in range(len(beats)):
			self.lightQueue[beats[i]].append(light)
			#print "added light pulse to" + str(beats[i])

#Simple function to keep a value in a given range (by default .5 and 1)
def restrain(i, mn = .5, mx = 1): return min(max(i, mn), mx)

#Simple function to change the brightness of a light without changing the Hue or Saturation
def addBrightness(light, amount):
	color = light.getColor()
	h, s, b = colorsys.rgb_to_hsv( color[0], color[1], color[2] )
	brightness = restrain(b + amount)
	r, g, b = colorsys.hsv_to_rgb( h, s, brightness )
	light.setColor( Vec4( r, g, b, 1 ) )