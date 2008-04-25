import direct.directbase.DirectStart
from pandac.PandaModules import WindowProperties
from direct.actor.Actor import Actor

import config
from World import World
from EnemyData import enemyData

props = WindowProperties(base.win.getProperties())
props.setCursorHidden(True)
base.win.requestProperties(props)
if config.FULLSCREEN:
	props.setFullscreen(True)
	base.openMainWindow(props=props, gsg=base.win.getGsg())

for type, data in enemyData.iteritems():
	loader.loadModelCopy("..//assets//models//enemies//" + str(data['model']) + ".egg")
	actor = Actor("..//assets//models//enemies//" + str(data['anim']) + ".egg")
	actor.loadAnims({"die":"..//assets//models//enemies//" + str(data['anim']) + ".egg"})

loader.loadModelCopy('..//assets//models//tunnels//tunneltrapazoid.egg')
loader.loadModelCopy('..//assets//models//plane.egg.pz')
loader.loadTexture("..//assets//images//targetCursor.png")
loader.loadTexture("..//assets//HUD//blinker.png")
loader.loadTexture("..//assets//HUD//heart1.PNG")
loader.loadTexture("..//assets//HUD//heart.PNG")
loader.loadFont('..//assets//HUD//ElectricBoots.TTF')
loader.loadSfx("..//assets//audio//Game2Stereo_Shane Drums Least.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Shane Rhythm Guitar.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Tom Hon Solo.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Shane Rhythm Guitar.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Shane upbeat Vidaurri.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Kevin hachacha.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Kevin Backup Guitar.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Brian Backup Trumpet.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Brian Backup Vocals Hi.wav")
loader.loadSfx("..//assets//audio//Game2Stereo_Brian Backup Vocals.wav")
loader.loadSfx("..//assets//audio//FX_135.wav")

world = World()
world.start()
run()

print "Got here!?"