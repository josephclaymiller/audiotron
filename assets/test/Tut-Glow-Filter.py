#Author: Kwasi Mensah (kmensah@andrew.cmu.edu)
#Date: 7/25/2005

import direct.directbase.DirectStart
from pandac.PandaModules import Filename,Buffer,Shader
from pandac.PandaModules import PandaNode,NodePath
from pandac.PandaModules import ColorBlendAttrib
from pandac.PandaModules import AmbientLight,DirectionalLight
from pandac.PandaModules import TextNode,Point3,Vec4
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import sys,os
from music import *

# Figure out what directory this program is in.
MYDIR=os.path.abspath(sys.path[0])
MYDIR=Filename.fromOsSpecific(MYDIR).getFullpath()

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
      pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                    pos=(1.28,-0.95), align=TextNode.ARight, scale = .07)

#This function is responsible for setting up the two blur filters.
#It just makes a temp Buffer, puts a screen aligned card, and then sets
#the appropiate shader to do all the work. Gaussian blurs are decomposable
#into a two-pass algorithm which is faster than the equivalent one-pass
#algorithm, so we do it in two passes. The full explanation (for math buffs)
#can be found in the article above

def makeFilterBuffer(srcbuffer, name, sort, prog):
    blurBuffer=base.win.makeTextureBuffer(name, 512, 512)
    blurBuffer.setSort(sort)
    blurBuffer.setClearColor(Vec4(1,0,0,1))
    blurCamera=base.makeCamera2d(blurBuffer)
    blurScene=NodePath("new Scene")
    blurCamera.node().setScene(blurScene)
    shader = Shader.load(prog)
    card = srcbuffer.getTextureCard()
    card.reparentTo(blurScene)
    card.setShader(shader)
    return blurBuffer

class GlowDemo(DirectObject):
    def __init__(self):
        base.disableMouse()
        base.setBackgroundColor(0,0,0)
        camera.setPos(0,-50,0)
        self.gameMusic=music()
    
        # Post the instructions
        self.title = addTitle("Panda3D: Tutorial - Glow Filter")
        self.inst1 = addInstructions(0.95,"ESC: Quit")
        self.inst2 = addInstructions(0.90,"Space: Toggle Glow Filter On/Off")
        self.inst3 = addInstructions(0.85,"Enter: Toggle Running/Spinning")
        self.inst4 = addInstructions(0.80,"V: View the render-to-texture results")


        #create the shader that will determime what parts of the scene will glow
        glowShader=Shader.load(MYDIR + "/glowShader.sha")

        # load our model
        self.handle = NodePath(PandaNode("Handle"))
        self.handle.reparentTo(render)
        self.tron=Actor()
        self.tron.loadModel("models/tron")
        self.tron.loadAnims({"running":"models/tron_anim"})
        self.tron.reparentTo(self.handle)
        self.interval = self.tron.hprInterval(60,Point3(360,0,0))
        self.interval.loop()
        self.isRunning=False
        
        #make tron a pulsing element
        fun = []
        for i in range(0, 272/8):
            fun.append(i*8)
        self.gameMusic.addPulsingElement(self.handle, fun)

        #put some lighting on the tron model
        dlight = DirectionalLight('dlight')
        alight = AmbientLight('alight')
        dlnp = render.attachNewNode(dlight.upcastToPandaNode()) 
        alnp = render.attachNewNode(alight.upcastToPandaNode())
        dlight.setColor(Vec4(1.0, 0.7, 0.2, 1))
        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        dlnp.setHpr(0, -60, 0) 
        render.setLight(dlnp)
        render.setLight(alnp)

        # create the glow buffer. This buffer renders like a normal scene,
        # except that only the glowing materials should show up nonblack.
        glowBuffer=base.win.makeTextureBuffer("Glow scene", 512, 512)
        glowBuffer.setSort(-3)
        glowBuffer.setClearColor(Vec4(0,0,0,1))

        # We have to attach a camera to the glow buffer. The glow camera
        # must have the same frustum as the main camera. As long as the aspect
        # ratios match, the rest will take care of itself.
        glowCamera=base.makeCamera(glowBuffer, aspectRatio=base.getAspectRatio())

        # Tell the glow camera to use the glow shader
        tempnode = NodePath(PandaNode("temp node"))
        tempnode.setShader(glowShader)
        glowCamera.node().setInitialState(tempnode.getState())

        # set up the pipeline: from glow scene to blur x to blur y to main window.
        blurXBuffer=makeFilterBuffer(glowBuffer,  "Blur X", -2, MYDIR+"/XBlurShader.sha")
        blurYBuffer=makeFilterBuffer(blurXBuffer, "Blur Y", -1, MYDIR+"/YBlurShader.sha")
        self.finalcard = blurYBuffer.getTextureCard()
        self.finalcard.reparentTo(render2d)
        self.finalcard.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        
        # Panda contains a built-in viewer that lets you view the results of
        # your render-to-texture operations.  This code configures the viewer.

        self.accept("v", base.bufferViewer.toggleEnable)
        self.accept("V", base.bufferViewer.toggleEnable)
        self.accept("a",  self.gameMusic.addSound, ["SFX//newSound.wav"])
        self.accept("q", self.gameMusic.queueSound, ["SFX//newSound.wav"])
        self.accept("k", self.gameMusic.killSound, [0])
        self.accept("r", self.gameMusic.removeSound, [0])
        self.accept("s", self.gameMusic.swapSound, [0, "SFX//trial.wav"])
        self.accept("e", self.gameMusic.replaceSound, [1, "SFX//trial.wav"])
        base.bufferViewer.setPosition("llcorner")
        base.bufferViewer.setLayout("hline")
        base.bufferViewer.setCardSize(0.652,0)

        # event handling
        self.accept("space", self.toggleGlow)
        self.accept("enter", self.toggleDisplay)
        self.accept("escape", sys.exit, [0])

        self.glowOn=True;

    def toggleGlow(self):
        if self.glowOn:
            self.finalcard.reparentTo(hidden)
        else:
            self.finalcard.reparentTo(render2d)
        self.glowOn= not(self.glowOn)

    def toggleDisplay(self):
        self.isRunning=not(self.isRunning)
        if not(self.isRunning):
            camera.setPos(0,-50,0)
            self.tron.stop("running")
            self.tron.pose("running", 0)
            self.interval.loop()
        else:
            camera.setPos(0,-170,3)
            self.interval.finish()
            self.tron.setHpr(0,0,0)
            self.tron.loop("running")

if (base.win.getGsg().getSupportsBasicShaders()):
    t=GlowDemo()
else:
    t=addTitle("Glow Demo: Video driver says shaders not supported.")

run()

