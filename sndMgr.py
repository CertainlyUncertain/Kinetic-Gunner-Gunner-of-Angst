# Sound Manager -------------------------------------------------------------- #

import math
import ogre.renderer.OGRE as ogre
#import ogre.io.OIS as OIS
import ogre.sound.OgreAL as OgreAL


class SndMgr:

    def __init__(self, engine):
        self.engine = engine
        self.manager = OgreAL.SoundManager()
        self.soundCount = 0
        self.bgm = None
        self.explode = "explosion.wav"
        self.laser = "laser.wav"
        print "Sound Manager Constructed "
        
    def init(self):
        print "Initializing Sound manager"
        pass

    def playSound(self, snd):
        sound = self.manager.createSound("Snd" + str(self.soundCount), snd)
        self.soundCount += 1
        sound.setGain(0.25)
        sound.play()

    def playMusic(self, msc):
        if self.bgm:
            self.manager.destroySound( self.bgm )
        self.bgm = self.manager.createSound("bgm", msc, True)
        self.bgm.setGain(0.1)
        self.bgm.play()
        
    def stop(self):
        self.manager._releaseSource(self.bgm)
        self.manager.destroyAllSounds()
        
    def tick(self, dtime):
        pass

# Sound Manager -------------------------------------------------------------- #
