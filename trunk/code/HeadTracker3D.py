from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import Point3
from direct.gui.OnscreenImage import OnscreenImage

import math

import config


if config.SHOW_HEADTRACK_POINTS:
	trackdot1 = OnscreenImage(image = '../assets/images/target.PNG', pos = (0, 0, 0), scale = (32.0/800/4, 0, 32.0/600/4), parent = render2d)
	trackdot2 = OnscreenImage(image = '../assets/images/target.PNG', pos = (0, 0, 0), scale = (32.0/800/4, 0, 32.0/600/4), parent = render2d)

	def headtrackerPoints(task):
		wm.trackerLock.acquire()
		if (wm.trackerData.ir1.valid):
			trackdot1.setPos((trackerData.ir1.x - 512) / 512.0, 0, (384 - trackerData.ir1.y) / 384.0)
		if (wm.trackerData.ir2.valid):
			trackdot2.setPos((trackerData.ir2.x - 512) / 512.0, 0, (384 - trackerData.ir2.y) / 384.0)
		wm.trackerLock.release()
		return Task.cont

	taskMgr.add(headtrackerPoints, "headtrackerPoints")


class HeadTracker(DirectObject):
	def __init__(self):
		self.headX = 0
		self.headY = 0
		self.headDist = 2
		self.lookPos = Point3(0, 10, 5)
		self.cameraIsAboveScreen = False
		self.cameraVerticaleAngle = 0  #begins assuming the camera is point straight forward
		self.relativeVerticalAngle = 0  #current head position view angle
		self.dotDistanceInMM = 8.5 * 25.4  #width of the wii sensor bar
		self.screenHeightInMM = 220
		self.radiansPerPixel = math.pi / 4 / 1024.0  #45 degree field of view with a 1024x768 camera
		self.movementScaling = 5.0
		self.accept('space', self.callibrate)
	
	def callibrate(self):
		print "Callibrate"
		angle = math.acos(.5 / self.headDist) - math.pi / 2  #angle of head to screen
		if (self.cameraIsAboveScreen):
			angle  = -angle;
		self.cameraVerticaleAngle = angle - self.relativeVerticalAngle  #absolute camera angle
	
	def update(self, task):
		trackerLock.acquire()
		if (trackerData.ir1.valid and trackerData.ir2.valid):
			dx = trackerData.ir1.x - trackerData.ir2.x
			dy = trackerData.ir1.y - trackerData.ir2.y
			pointDist = math.sqrt(dx * dx + dy * dy)

			angle = self.radiansPerPixel * pointDist / 2
			
			#in units of screen hieght since the box is a unit cube and box hieght is 1
			self.headDist = self.movementScaling * self.dotDistanceInMM / 2 / math.tan(angle) / self.screenHeightInMM

			avgX = (trackerData.ir1.x + trackerData.ir2.x) / 2.0
			avgY = (trackerData.ir1.y + trackerData.ir2.y) / 2.0

			self.headX = self.movementScaling *  math.sin(self.radiansPerPixel * (avgX - 512)) * self.headDist

			self.relativeVerticalAngle = (avgY - 384) * self.radiansPerPixel  #relative angle to camera axis

			self.headY = self.movementScaling * math.sin(self.relativeVerticalAngle + self.cameraVerticaleAngle) * self.headDist
			if(self.cameraIsAboveScreen):
				self.headY += .5
			else:
				self.headY -= .5
		
		trackerLock.release()
		
		base.camera.setPos(self.headX, -self.headDist - 10, self.headY + 5)
		base.camera.lookAt(self.lookPos)
		#print "Setting camaera pos\t", self.headX, "\t", self.headY, "\t", self.headDist
		
		return Task.cont
		
	