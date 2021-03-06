from direct.showbase.DirectObject import DirectObject #needed
from direct.task import Task #for the task manager & stuff
#from pandac.PandaModules import ClockObject #for the global clock
from direct.showbase.Loader import Loader #for loading & unloading SFX
#import direct.directbase.DirectStart #for loading SFX old(not sure if this is needed)
from pandac.PandaModules import AudioSound #for setTime()
import colorsys #so I can change RGB to HSB
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode
from pandac.PandaModules import Vec4, Vec3
from pandac.PandaModules import VBase4
#import math

class MusicController(DirectObject):
	
	def __init__(self, wii):
		self.bpm=130
		self.numMeasures=17
		self.numSixteenths=self.numMeasures*16
		self.maxSounds=1000
		self.secondsPerLoop=float(self.numMeasures*240)/self.bpm #=(#measures per loop * beats per measure) * (seconds per beat) = (17*4)*(60/bpm)
		self.loopStartTime=globalClock.getRealTime()
		self.loopEndTime=0 #initialized at 0 to start loop at game start! ***NOTE: should be set to self.loopStartTime+self.secondsPerLoop :NOTE***
		self.music = [] #needs to be filled with sounds loaded like "self.music.append(loader.loadSfx("SoundFile.wav"))"
		self.isPlaying = []
		self.tempMusic = [] #a temp array for playing music...gets cleared every new loop
		
		self.HUDfont = loader.loadFont('..//assets//HUD//ElectricBoots.TTF')
		self.dieSFX = loader.loadSfx("..//assets//audio//FX_135.wav")
		self.hitSFX = loader.loadSfx("..//assets//audio//sfx//hit.wav")
		self.hitSFX.setVolume(.75)
		self.enterSFX = loader.loadSfx("..//assets//audio//sfx//enter.wav")
		self.enterSFX.setPlayRate(.75)
		
		
		#enemy music
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Tom Hon Solo.wav"))			#0
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Shane Rhythm Guitar.wav"))		#1
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Shane upbeat Vidaurri.wav"))	#2
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Kevin hachacha.wav"))			#3
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Kevin Backup Guitar.wav"))		#4
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Brian Backup Trumpet.wav"))	#5
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Brian Backup Vocals Hi.wav"))	#6
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Brian Backup Vocals.wav"))		#7
		
		for x in range(0,8):
			self.music[x].stop()
		
		#drums
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Shane Drums Least.wav"))		#8
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Shane Drums Mid.wav"))			#9
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Shane Drums Full.wav"))		#10
		
		#melody
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Brian Melody Trumpet.wav"))	#11
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Shane Melody Guitar.wav"))		#12
		
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Violin Death.wav"))		#13
		self.music.append(loader.loadSfx("..//assets//audio//Game2Stereo_Violin Death 2.wav"))		#14
		
		for x in range(9, 15):
			self.music[x].stop()
			
		for x in range(0,15):
			self.isPlaying.append(False)
		self.isPlaying[8]=True
		
		
		self.blinker=OnscreenImage(image='..//assets//HUD//blinker.png', pos=Vec3(0,0,0), scale=Vec3(1.33,0,1))
		self.blinker.setColor(1,1,0,1)
		self.blinkFade=1
		self.blinker.setTransparency(TransparencyAttrib.MAlpha)
		
		self.sixteenth=0
		self.secondsPerSixteenth=self.secondsPerLoop/self.numSixteenths
		self.timingWindow=self.secondsPerSixteenth/2
		self.pulseQueue = [] #a list of every pulse (divided into 16th notes)
		self.pulseElements = [] # a list of every pulsing element
		self.lightQueue = []
		self.litElements = []
		self.destructionQueue = []
		self.lastPulseTime=globalClock.getRealTime()
		
		#start at Pos(0,0), clear the text and go to pos(0,.4) once the game actually starts!
		if not wii:
			self.noteTXT = OnscreenText(text = 'press the trigger (b button) to start the game', pos = (0,0), scale = 0.1, fg=(1,1,0,1), align=TextNode.ACenter, font=self.HUDfont, mayChange=True)
		else:
			self.noteTXT = OnscreenText(text = 'press the left mouse button to start the game', pos = (0,0), scale = 0.1, fg=(1,1,0,1), align=TextNode.ACenter, font=self.HUDfont, mayChange=True)
		self.note = False
		self.noteCount = 0
				
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
			
			#play sound clips
			for i in range(len(self.music)):
				if self.isPlaying[i]:
					self.music[i].setTime(globalClock.getRealTime()-time)
					self.music[i].play()
					#print i
		
		#print str(len(self.music))
		return Task.cont
	
	def addSound(self, typeNum):
		#self.unlockSFX.play()
		self.music[typeNum].setTime(globalClock.getRealTime()-self.loopStartTime)
		self.music[typeNum].setVolume(0)
		self.music[typeNum].play()
		self.isPlaying[typeNum]=True
		taskMgr.add(self.fadeInSound, "fadeInSound"+str(typeNum), extraArgs=[typeNum, globalClock.getRealTime(), self.music])
	
	def fadeInSound(task, x, time, music):
		realTime=globalClock.getRealTime()
		if (realTime-time) < 1.846:
			music[x].setVolume(((realTime-time)*(realTime-time)/3.408))
			return Task.cont
		
		music[x].setVolume(1)
		return Task.done
		
	def fadeOutSound(self, x):
		if x<len(self.music):
			self.isPlaying[x]=False
			taskMgr.add(self.fader, "fader"+str(x), extraArgs=[x, globalClock.getRealTime(), self.music])
			return x
		return -1
	
	def fader(task, x, time, music):
		realTime=globalClock.getRealTime()
		if (realTime-time) < .923:
			music[x].setVolume(1-((realTime-time)/.923))
			return Task.cont
		
		music[x].stop()
		return Task.done
		
	def pulseManager(self, task):
		time=globalClock.getRealTime()

		deflate=(time-self.lastPulseTime)*(.25/(self.secondsPerLoop/self.numMeasures))
		fade=(time-self.lastPulseTime)*(-2.0/(self.secondsPerLoop/self.numMeasures))
		self.blinkFade-=(time-self.lastPulseTime)/.6
		#print str(fade)
		
		#self.beatBarR.setScale(Vec3(.015,0,self.beatBarR.getSz()-bar))
		#self.beatBarL.setScale(Vec3(.015,0,self.beatBarR.getSz()-bar))
		
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
			
			if self.sixteenth%4==0:
				self.blinkFade=1
			#	self.beatBarR.setScale(Vec3(.015,0,.6))
			#	self.beatBarL.setScale(Vec3(.015,0,.6))
			
			if self.note:
				self.noteCount+=1
				if self.noteCount>=16:
					self.note=False
					self.noteTXT.setText('')
				
			#increment sixteenth and check if a new loop has started
			#print self.sixteenth, " ", time-self.loopStartTime
			self.sixteenth+=1
		
		self.blinker.setColor(self.blinkFade,self.blinkFade,0,1)
		if self.note:
			self.noteTXT.setFg((1,1,1-self.blinkFade,1))
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
	
	def removeLitElement(self, element):
		if (self.litElements.count(element)):
			self.litElements.remove(element)
			
		for sixteenth in self.lightQueue:
			if (sixteenth.count(element)):
				sixteenth.remove(element)
	
	def isOnBeatNow(self, time):
		thirtysecond=(time-self.loopStartTime)/(self.secondsPerSixteenth/2)
		beat = int(thirtysecond)%8
		
		#print "sixteenth" + str(self.sixteenth)
		#print "time: " + str(time-self.loopStartTime)
		#print "shot time: " + str(thirtysecond)
		#print "shot beat: " + str(beat)
		
		if beat == 0 or beat == 7:
			#print "true"
			return True
		
		#print "false"
		return False
	
	def showNote(self, note):
		self.noteTXT.setText(note)
		self.note=True
		self.noteCount=0
	
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
