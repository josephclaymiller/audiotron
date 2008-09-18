import PyWiiUse as wiiuse
import threading
import sys
import config
import math


class IRPoint:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		self.valid = False
		self.dist = 0
	
	def __cmp__(self, other):
		return cmp(self.dist, other.dist)

class WMData:
	def __init__(self):
		self.screen = IRPoint()
		self.ir = IRPoint()
		self.ir1 = IRPoint()
		self.ir2 = IRPoint()
		self.samples = []
		self.maxSamples = 100

	def update (self, vis, x, y):
		if (vis):
			self.samples.append(IRPoint(x, y))
			
		numSamples = len(self.samples)
		if (numSamples > self.maxSamples):
			self.samples.pop(0)
			numSamples -= 1
		
		if (numSamples <= 0):
			self.ir.valid = False
			self.screen.valid = False
		else:
			average = IRPoint()
			for point in self.samples:
				average.x += point.x
				average.y += point.y
			
			average.x /= numSamples
			average.y /= numSamples
			
			#for point in self.samples:
			#	point.dist = (point.x - average.x) * (point.x - average.x) + (point.y - average.y) * (point.y - average.y)
			
			#samplesSorted = self.samples[:]
			#samplesSorted.sort()
			
			#median = samplesSorted[int(math.floor(numSamples / 2))]
			#if (numSamples
			#if (numSamples % 2 == 1):
			#	median = samplesSorted[math.floor(numSamples / 2)]
			#else:
			#	meds = samplesSorted[numSamples / 2 - 1 : numSamples / 2]
			#	median = IRPoint((meds[0].x + meds[1].x) / 2, (meds[0].y + meds[1].y) / 2)
			
			self.ir = average #median
			self.ir.valid = True
			
			self.screen.x = (self.ir.x - (800/2.0)) / (800/2.0)
			self.screen.y = ((600/2.0) - self.ir.y) / (600/2.0)
			self.screen.valid = True
		

class WiimoteManager(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

		self.WM_ID_TRACKER = 0
		self.WM_ID_POINTER = 1

		self.trackerData = WMData()
		self.pointerData = WMData()

		self.trackerLock = threading.Lock()
		self.pointerLock = threading.Lock()

		self.CAMERA_WIDTH = 1024
		self.CAMERA_HEIGHT = 768

		self.SCREEN_WIDTH = 800
		self.SCREEN_HEIGHT = 600
	
		self.nmotes = 2
		
		
	def run(self):
		while(True):
			self.wiimotes = wiiuse.init(self.nmotes, [self.WM_ID_TRACKER, self.WM_ID_POINTER], self.handle_event, self.handle_status, self.handle_disconnect)

			found = wiiuse.find(self.wiimotes, self.nmotes, 5)
			if not found:
				print 'No wiimotes found'
				sys.exit(1)

			connected = wiiuse.connect(self.wiimotes, self.nmotes)
			if connected:
				print 'Connected to %i wiimotes (of %i found).' % (connected, found)
			else:
				print 'failed to connect to any wiimote.'
				sys.exit(1)

			for i in range(self.nmotes):
				wm = self.wiimotes[i]
				wiiuse.set_leds(wm, wiiuse.LED[i])
				wiiuse.set_ir(wm, 1)
				wiiuse.motion_sensing(wm, 1)
				wiiuse.set_aspect_ratio(wm, wiiuse.ASPECT_4_3)
				wiiuse.set_ir_vres(wm, 800, 600)
				#wiiuse.set_ir_sensitivity(wm, 5)
				if (wm.contents.unid == self.WM_ID_POINTER):
					wiiuse.set_ir_position(wm, wiiuse.IR_BELOW)
				else:
					wiiuse.set_ir_position(wm, wiiuse.IR_ABOVE)

			reconnectFlag = False
			while (not reconnectFlag):
				try:
					wiiuse.poll(self.wiimotes, 2)
				except:
					print "Poll failed, reconnecting wiimotes!"
					wiiuse.disconnect(self.wiimotes[0])
					wiiuse.disconnect(self.wiimotes[1])
					reconnectFlag = True


	def handle_status(self, wmp, attachment, speaker, ir, led, battery_level):
		print "wiimote status change"
		
	def handle_disconnect(self, wmp):
		print "wiimote disconnected\n"

	def handle_event(self, wmp):
		wm = wmp.contents
		#print "self:\t", self
		#print "wmp:\t", wmp
		#print "wm:\t", wm
		
		if (wm.unid == self.WM_ID_TRACKER):
			self.trackerLock.acquire()
			wmdata = self.trackerData
		else:
			self.pointerLock.acquire()
			wmdata = self.pointerData

		if (config.TOGGLE_RUMBLE_TEST and wiiuse.is_just_pressed(wm, wiiuse.button['A'])):
			wiiuse.toggle_rumble(wmp)
		
		if (wm.unid == self.WM_ID_POINTER):
			if (wiiuse.is_just_pressed(wm, wiiuse.button['B'])):
				messenger.send("FireButtonDown")
			elif (wiiuse.is_released(wm, wiiuse.button['B'])):
				messenger.send("FireButtonUp")

		if (wiiuse.using_ir(wm)):
			wmdata.update(wm.ir.num_dots >= 2, wm.ir.x, wm.ir.y)
			'''if (wm.ir.dot[0].visible):
				wmdata.ir1.valid = True
				wmdata.ir1.x = wm.ir.dot[0].rx
				wmdata.ir1.y = wm.ir.dot[0].ry
			else:
				wmdata.ir1.valid = False
			
			if (wm.ir.dot[1].visible):
				wmdata.ir2.valid = True
				wmdata.ir2.x = wm.ir.dot[1].rx
				wmdata.ir2.y = wm.ir.dot[1].ry
			else:
				wmdata.ir2.valid = False
			
			if (wm.ir.num_dots >= 1):
				wmdata.update(wm.ir.
				wmdata.screen.valid = True
				wmdata.screen.x = (wmdata.ir.x - (self.SCREEN_WIDTH/2.0)) / (self.SCREEN_WIDTH/2.0)
				wmdata.screen.y = ((self.SCREEN_HEIGHT/2.0) - wmdata.ir.y) / (self.SCREEN_HEIGHT/2.0)
			else:
				wmdata.ir.valid = False'''
		
		if (wm.unid == self.WM_ID_TRACKER):
			self.trackerLock.release()
		else:
			self.pointerLock.release()


