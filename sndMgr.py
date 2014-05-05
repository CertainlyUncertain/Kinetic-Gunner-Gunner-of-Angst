# Simple Keyboard arrows based manual Control Aspect for 38Engine
# Sushil Louis

#from vector import Vector3
import utils
import math
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ogre.sound.OgreAL as OgreAL


class SndMgr:

    def __init__(self, engine):
        self.engine = engine
        #self.engine.gfxMgr.root.loadPlugin("OgreOggSound")
        self.manager = OgreAL.SoundManager()
        print "Sound Manager Constructed "

        self.sndExplosion = "explosion.wav"
        self.sndShoot = "shoot.wav"
        
        
    def init(self):
        print "Initializing Sound manager"
        #self.sndMgr = OgreAL.SoundManager()
        self.bgm = self.manager.createSound("background", "bg2.wav", True) #"bg2.wav"
        self.bgm.setGain(0.1)
        self.bgm.play()

    def playSound(self, snd):
        sound = self.manager.createSound("background", snd)
        sound.setGain(0.1)
        sound.play()

    def stop(self):
        self.manager._releaseSource(self.bgm)
        self.manager.destroyAllSounds()
        
    def tick(self, dtime):
        pass

    def loadLevel(self, dtime):
        pass
