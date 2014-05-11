# ========================== Start Copyright Notice ========================== #
#                                                                              #
#   Copyright 2014 F.D.I.S.                                                    #
#   This file is part of Kinetic Gunner: Gunner of Angst                       #
#                                                                              #
#   For the latest version, please visit:                                      #
#   https://github.com/CertainlyUncertain/Kinetic-Gunner-Gunner-of-Angst       #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public License          #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                              #
# =========================== End Copyright Notice =========================== #

# Sound Manager -------------------------------------------------------------- #

import math
from vector import Vector3
#import ogre.renderer.OGRE as ogre
import ogre.sound.OgreAL as OgreAL

class SndMgr:
    ''' Manages Sounds and Music. '''
    
    def __init__(self, engine):
        ''' Set Manager and Sounds. '''
        self.engine = engine
        self.manager = OgreAL.SoundManager()
        self.sounds = []
        self.done = []
        self.soundCount = 0
        self.bgm = None
        self.missileExplode = "Grenade.wav" #("Grenade.wav", 0.25) [file,gain]
        self.laser = "laser.wav"
        self.hit = "Hit.wav"
        self.jetExplode = "Bomb.wav"
        print "Sound Manager Created."
        
    def init(self):
        ''' Initialize. '''
        print "Sound Manager Initialized."
        pass

    def crosslink(self):
        ''' Links to other Managers. '''
        print "Sound Manager Linked."
        pass

    def tick(self, dtime):
        ''' Update. '''
        i = 0
        for snd in self.sounds:
            if not snd.isPlaying():
                self.done.append( self.sounds.pop(i) )
            i += 1
        for snd in self.done:
            self.manager.destroy(snd)
        pass
        
    def stop(self):
        ''' Shut Down. '''
        for i in range(5):
            print self.manager.hasSound( "Snd" + str(i) )
        self.manager.destroyAllSounds()
        print "Sound Manager Stopped."
        
# Sound Manager -------------------------------------------------------------- #

    def playSound(self, snd, pos = None):
        ''' Play a sound. '''
        sound = self.manager.createSound("Snd" + str(self.soundCount), snd) #snd[0]
        self.soundCount += 1
        if pos:
            sound.setPosition( pos )
        sound.setGain(0.25) #snd[1]
        sound.play()

    def playMusic(self, msc):
        ''' Play Background Music. '''
        if self.bgm:
            self.bgm.pause()
            self.manager.destroySound( self.bgm )
        self.bgm = self.manager.createSound("bgm", msc) #, True) #Looping Causes Crashes
        self.bgm.setGain(0.1)
        self.bgm.play()

# Sound Manager -------------------------------------------------------------- #
