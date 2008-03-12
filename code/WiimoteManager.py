import PyWiiUse as wiiuse
import threading
import sys

class IRPoint:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.valid = False

class WMData:
	def __init__(self):
		self.screen = IRPoint()
		self.ir = IRPoint()
		self.ir1 = IRPoint()
		self.ir2 = IRPoint()


WM_ID_TRACKER = 0
WM_ID_POINTER = 1

trackerData = WMData()
pointerData = WMData()

trackerLock = threading.Lock()
pointerLock = threading.Lock()

CAMERA_WIDTH = 1024
CAMERA_HEIGHT = 768

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
	

class WiimoteManager(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
	
		nmotes = 2
		self.wiimotes = wiiuse.init(nmotes, [WM_ID_TRACKER, WM_ID_POINTER], self.handle_event, self.handle_status, self.handle_disconnect)

		found = wiiuse.find(self.wiimotes, nmotes, 5)
		if not found:
			print 'No wiimotes found'
			sys.exit(1)

		connected = wiiuse.connect(self.wiimotes, nmotes)
		if connected:
			print 'Connected to %i wiimotes (of %i found).' % (connected, found)
		else:
			print 'failed to connect to any wiimote.'
			sys.exit(1)

		for i in range(nmotes):
			wm = self.wiimotes[i]
			wiiuse.set_leds(wm, wiiuse.LED[i])
			wiiuse.set_ir(wm, 1)
			wiiuse.motion_sensing(wm, 1)
			wiiuse.set_aspect_ratio(wm, wiiuse.ASPECT_4_3)
			wiiuse.set_ir_position(wm, wiiuse.IR_BELOW)
			wiiuse.set_ir_vres(wm, 800, 600)


	def run(self):
		while (True):
			wiiuse.poll(self.wiimotes, 2)


	def handle_status(self, wmp, attachment, speaker, ir, led, battery_level):
		print "wiimote status change"
		
	def handle_disconnect(self, wmp):
		print "wiimote disconnected\n"

	def handle_event(self, wmp):
		wm = wmp.contents
		
		if (wm.unid == WM_ID_TRACKER):
			trackerLock.acquire()
			wmdata = trackerData
		else:
			pointerLock.acquire()
			wmdata = pointerData

		if (wiiuse.is_just_pressed(wm, wiiuse.button['A'])):
			wiiuse.toggle_rumble(wmp)
		
		
		if (wiiuse.is_just_pressed(wm, wiiuse.button['B'])):
			messenger.send("FireButton")

		if (wiiuse.using_ir(wm)):
			if (wm.ir.dot[0].visible):
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
				wmdata.ir.valid = True
				wmdata.ir.x = wm.ir.x
				wmdata.ir.y = wm.ir.y
				wmdata.screen.valid = True
				wmdata.screen.x = (wmdata.ir.x - (SCREEN_WIDTH/2.0)) / (SCREEN_WIDTH/2.0)
				wmdata.screen.y = ((SCREEN_HEIGHT/2.0) - wmdata.ir.y) / (SCREEN_HEIGHT/2.0)
			else:
				wmdata.ir.valid = False
		
		if (wm.unid == WM_ID_TRACKER):
			trackerLock.release()
		else:
			pointerLock.release()


