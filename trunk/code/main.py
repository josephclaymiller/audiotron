import direct.directbase.DirectStart
from pandac.PandaModules import WindowProperties

import config
from World import World


props = WindowProperties(base.win.getProperties())
props.setCursorHidden(True)
base.win.requestProperties(props)
if config.FULLSCREEN:
	props.setFullscreen(True)
	base.openMainWindow(props=props, gsg=base.win.getGsg())


world = World()
world.start()
run()
