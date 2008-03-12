import direct.directbase.DirectStart
from pandac.PandaModules import *

from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
import math

from pandac.PandaModules import WindowProperties
from direct.gui.OnscreenImage import OnscreenImage

import pywiiuse as wiiuse


targetImage = OnscreenImage(image = 'target.PNG', pos = (0, 0, 0), scale = (32.0/800, 0, 32.0/600), parent = render2d)
targetImage1 = OnscreenImage(image = 'target.PNG', pos = (1, 0, 1), scale = (32.0/800, 0, 32.0/600), parent = render2d)
targetImage2 = OnscreenImage(image = 'target.PNG', pos = (1, 0, -1), scale = (32.0/800, 0, 32.0/600), parent = render2d)
targetImage3 = OnscreenImage(image = 'target.PNG', pos = (-1, 0, 1), scale = (32.0/800, 0, 32.0/600), parent = render2d)
targetImage4 = OnscreenImage(image = 'target.PNG', pos = (-1, 0, -1), scale = (32.0/800, 0, 32.0/600), parent = render2d)



def my_handle_event(wiimote_p):
	""" handle_event gets called when a generic event occurs (button press, motion sensing, etc) """
	global exitflag
	wm = wiimote_p.contents

	if (IS_PRESSED(wm, WIIMOTE_BUTTON_A)):
		wiiuse_toggle_rumble(wm)


	if (WIIUSE_USING_IR(wm) and wm.ir.num_dots >= 2):
		(x, y) = (0, 0)
		for i in range(4):
			if (wm.ir.dot[i].visible):
				x += wm.ir.dot[i].rx
				y += wm.ir.dot[i].ry
		x /= wm.ir.num_dots
		y /= wm.ir.num_dots
		
		#print "IR pos: ", wm.ir.x, ",", wm.ir.y, "\t\tAdjusted: ", (wm.ir.x - 400) / 400.0, ",", (300 - wm.ir.y) / 300.0, "\n"
		targetImage.setPos((wm.ir.x - 400) / 400.0, 0, (300 - wm.ir.y) / 300.0)
		
		#print "Averaged ir pos: ", x, ",", y
		#targetImage.setPos((x - 512) / 512.0, 0, (384 - y) / 384.0)


winProperties = WindowProperties(base.win.getProperties())
winProperties.clearFixedSize()
winProperties.setFullscreen(True)

#Load the first environment model
environ = loader.loadModel("models/environment")
environ.reparentTo(render)
environ.setScale(0.25,0.25,0.25)
environ.setPos(-8,42,0)

wiimotes, connected = wiiuse.init(1, [1], my_handle_event)

wm1 = 0
wm2 = 0

if connected > 0:
	wm1 = wiimotes[0].contents
	wiiuse_set_ir(wm1, 1)
	wiiuse_motion_sensing(wm1, 1)
	wiiuse_set_aspect_ratio(wm1, WIIUSE_ASPECT_4_3)
	wiiuse_set_ir_position(wm1, WIIUSE_IR_BELOW)
	wiiuse_set_ir_vres(wm1, 800, 600)
	
if connected > 1:
	wm2 = wiimotes[1].contents
	wiiuse_set_ir(wm2, 1)
	wiiuse_motion_sensing(wm2, 1)
	wiiuse_set_aspect_ratio(wm2, WIIUSE_ASPECT_4_3)
	wiiuse_set_ir_position(wm2, WIIUSE_IR_BELOW)
	wiiuse_set_ir_vres(wm2, 800, 600)


#Task to move the camera
def SpinCameraTask(task):
	angledegrees = task.time * 6.0
	angleradians = angledegrees * (math.pi / 180.0)
	base.camera.setPos(20*math.sin(angleradians),-20.0*math.cos(angleradians),3)
	base.camera.setHpr(angledegrees, 0, 0)
	return Task.cont


def PollWiimoteTask(task):
	try:
		wiiuse_poll(wiimotes, connected)
	except:
		wiiuse_disconnect(wiimotes[0])

	return Task.cont

taskMgr.add(SpinCameraTask, "SpinCameraTask")
taskMgr.add(PollWiimoteTask, "PollWiimoteTask")

#Load the panda actor, and loop its animation
pandaActor = Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor.setScale(0.005,0.005,0.005)
pandaActor.reparentTo(render)
pandaActor.loop("walk")

#Create the four lerp intervals needed to walk back and forth
pandaPosInterval1= pandaActor.posInterval(13,Point3(0,-10,0), startPos=Point3(0,10,0))
pandaPosInterval2= pandaActor.posInterval(13,Point3(0,10,0), startPos=Point3(0,-10,0))
pandaHprInterval1= pandaActor.hprInterval(3,Point3(180,0,0), startHpr=Point3(0,0,0))
pandaHprInterval2= pandaActor.hprInterval(3,Point3(0,0,0), startHpr=Point3(180,0,0))

#Create and play the sequence that coordinates the intervals
pandaPace = Sequence(pandaPosInterval1, pandaHprInterval1, pandaPosInterval2, pandaHprInterval2, name = "pandaPace")
pandaPace.loop()

run()