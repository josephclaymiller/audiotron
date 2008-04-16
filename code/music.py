from direct.showbase.DirectObject import DirectObject #needed
from direct.task import Task #for the task manager & stuff
#from pandac.PandaModules import ClockObject #for the global clock
from direct.showbase.Loader import Loader #for loading & unloading SFX
#import direct.directbase.DirectStart #for loading SFX old(not sure if this is needed)
from pandac.PandaModules import AudioSound #for setTime()
import colorsys #so I can change RGB to HSB
from pandac.PandaModules import Vec4 #for Vec4
#import math

class MusicController(DirectObject):
	
	def __init__(self):
		self.bpm=130
		self.numMeasures=17
		self.numSixteenths=self.numMeasures*16
		self.maxSounds=1000
		self.secondsPerLoop=float(self.numMeasures*240)/self.bpm #=(#measures per loop * beats per measure) * (seconds per beat) = (17*4)*(60/bpm)
		self.loopStartTime=globalClock.getRealTime()
		self.loopEndTime=0 #initialized at 0 to start loop at game start! ***NOTE: should be set to self.loopStartTime+self.secondsPerLoop :NOTE***
		self.music = [] #needs to be filled with sounds loaded like "self.music.append(loader.loadSfx("SoundFile.wav"))"
		self.tempMusic = [] #a temp array for playing music...gets cleared every new loop
		
		self.dieSFX = loader.loadSfx("..//assets//audio//FX_135.wav")
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Shane Drums Least.wav")) #always load drum track
		
		self.sixteenth=0
		self.secondsPerSixteenth=self.secondsPerLoop/self.numSixteenths
		self.timingWindow=self.secondsPerSixteenth/2
		self.pulseQueue = [] #a list of every pulse (divided into 16th notes)
		self.pulseElements = [] # a list of every pulsing element
		self.lightQueue = []
		self.litElements = []
		self.destructionQueue = []
		self.lastPulseTime=globalClock.getRealTime()
		
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
		time=globalClock.getRealTime()
		
		if time>=self.loopEndTime:
			self.loopStartTime=time
			self.loopEndTime=time+self.secondsPerLoop
			self.sixteenth=0
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
				self.music[i].setTime(globalClock.getRealTime()-time)
				self.music[i].play()
				#print i
		
		#print str(len(self.music))
		return Task.cont
	
	def addSound(self, name):
		i=len(self.music)
		#print i
		if (i+len(self.tempMusic))<self.maxSounds:
			self.music.append(loader.loadSfx(name))
			self.music[i].setTime(globalClock.getRealTime()-self.loopStartTime)
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
		
	def fadeOutSound(self, x):
		if x<len(self.music):
			taskMgr.add(self.fader, "fader"+str(x), extraArgs=[x, globalClock.getRealTime(), self.music])
			return x
		return -1
	
	def fader(task, x, time, music):
		realTime=globalClock.getRealTime()
		if (realTime-time) < .923:
			music[x].setVolume(1-((realTime-time)/.923))
			return Task.cont
		
		music[x].stop()
		loader.unloadSfx(music[x])
		del music[x]
		return Task.done
		
	
	def removeSound(self, x):
		i=len(self.tempMusic)
		if x<len(self.music):
			#print len(self.music)
			self.music[x].stop()
			self.tempMusic.append(self.music.pop(x))
			self.tempMusic[i].setTime(globalClock.getRealTime()-self.loopStartTime)
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
			self.music[x].setTime(globalClock.getRealTime()-self.loopStartTime)
			self.music[x].play()
			return x
		return -1
	
	def pulseManager(self, task):
		time=globalClock.getRealTime()

		deflate=(time-self.lastPulseTime)*(.25/(self.secondsPerLoop/self.numMeasures))
		fade=(time-self.lastPulseTime)*(-1.0/(self.secondsPerLoop/self.numMeasures))
		#print str(fade)
		
		#decrease scale of all pulsing elements
		for element in self.pulseElements:
			element.setScale(element.getSx() - deflate)
			
		#decrease lumens of all lit elements
		for element in self.litElements:
			addBrightness(element, fade)
		
		if (self.loopStartTime + (self.sixteenth * self.secondsPerSixteenth)) < time:
			#pulse elements by scale
			for element in self.pulseQueue[self.sixteenth]:
				element.setScale(1)
			#pulse elements by light
			for element in self.lightQueue[self.sixteenth]:
				addBrightness(element, 200)#I can add whatever I want because the max lumens is restricted by restrain
				#print "Pulse! " + str(self.sixteenth)
			
			if (len(self.destructionQueue) > 0) and self.sixteenth%2 == 0:
				element = self.destructionQueue.pop(0)
				self.dieSFX.play()
				element.destroy()
				
			#increment sixteenth and check if a new loop has started
			self.sixteenth+=1
		
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
	
	def addDestructionElements(self, elements):
		self.destructionQueue.extend(elements)
	
	def removePulsingElement(self, element):
		if (self.pulseElements.count(element)):
			self.pulseElements.remove(element)
			
		for sixteenth in self.pulseQueue:
			if (sixteenth.count(element)):
				sixteenth.remove(element)
	
	#-------------------------------
	# CHANGE ME!!!!!!!!!!!
	#-------------------------------
	def isOnBeatNow(self, time):
		thirtysecond=(time-self.loopStartTime)/(self.secondsPerSixteenth/2)
		beat = int(thirtysecond)%8
		
		print "time: " + str(time-self.loopStartTime)
		print "shot time: " + str(thirtysecond)
		print "shot beat: " + str(beat)
		
		if beat == 0 or beat == 7:
			print "true"
			return True
		
		print "false"
		return False
	
	def debugPrint(self):
		print "\n****************"
		print "Pulse elements: ", len(self.pulseElements)
		print "Lit elements: ", len(self.litElements)
		print "\n*** Pulse queue:"
		for i in range(len(self.pulseQueue)):
			print i, "/16:\t", len(self.pulseQueue[i])
		print "\n*** Light queue:"
		for i in range(len(self.lightQueue)):
			print i, "/16:\t", len(self.lightQueue[i])
		print "****************\n"

#Simple function to keep a value in a given range (by default .5 and 1)
def restrain(i, mn = .5, mx = 1): return min(max(i, mn), mx)

#Simple function to change the brightness of a light without changing the Hue or Saturation
def addBrightness(light, amount):
	color = light.getColor()
	h, s, b = colorsys.rgb_to_hsv( color[0], color[1], color[2] )
	brightness = restrain(b + amount)
	r, g, b = colorsys.hsv_to_rgb( h, s, brightness )
	light.setColor( Vec4( r, g, b, 1 ) )
