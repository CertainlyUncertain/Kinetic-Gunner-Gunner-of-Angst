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

# Gunner of Angst Main Engine ------------------------------------------------ #

import time

class Engine(object):
    ''' The Root of the global Manager tree. '''

    def __init__(self):
        ''' Creation. '''
        pass

    def init(self):
        ''' Create, Initialize, and Crosslink Each Manager. '''
        import entityMgr
        self.entityMgr = entityMgr.EntityMgr(self)
        self.entityMgr.init()
        self.keepRunning = True;

        import gfxMgr
        self.gfxMgr = gfxMgr.GfxMgr(self)
        self.gfxMgr.init()

        import sndMgr
        self.sndMgr = sndMgr.SndMgr(self)
        self.sndMgr.init()

        import netMgr
        self.netMgr = netMgr.NetMgr(self)
        self.netMgr.init()

        import inputMgr
        self.inputMgr = inputMgr.InputMgr(self)
        self.inputMgr.init()

        import gameMgr
        self.gameMgr = gameMgr.GameMgr(self)
        self.gameMgr.init()

        import cameraMgr
        self.camMgr = cameraMgr.CamMgr(self)
        self.camMgr.init()

        import overlayMgr
        self.overlayMgr = overlayMgr.OverlayMgr(self)
        self.overlayMgr.init()

        self.gameMgr.crosslink()
        #self.gfxMgr.crosslink()
        self.inputMgr.crosslink()
        #self.camMgr.crosslink()

    def stop(self):
        ''' Stops each Manager. '''
        self.netMgr.stop()
        self.overlayMgr.stop()
        self.camMgr.stop()
        self.gameMgr.stop()
        self.entityMgr.stop()
        self.sndMgr.stop()
        self.inputMgr.stop()
        self.gfxMgr.stop()
        print "Engine Stopped."

    def pause(self):
        ''' Pauses the game by "pausing" certain Managers. '''
        pass

    def run(self):
        ''' Runs the program, ticking each Manager in a loop, until quit. '''
        import ogre.renderer.OGRE as ogre
        weu = ogre.WindowEventUtilities() # Needed for linux/mac
        weu.messagePump()                 # Needed for linux/mac

	    # Show Splash Screen
        self.overlayMgr.showSplash()
        self.gfxMgr.root.renderOneFrame()
        time.sleep(4)
        self.overlayMgr.hideSplash()

        # Run the Game
        self.oldTime = time.time()
        self.runTime = 0
        while (self.keepRunning):
            now = time.time() # Change to time.clock() for Direct3D (Windows)
            dtime = now - self.oldTime
            if( dtime > 0.25 ):
                dtime = 0.25
            self.oldTime = now
            self.entityMgr.tick(dtime)
            self.gfxMgr.tick(dtime)
            self.netMgr.tick(dtime)
            self.camMgr.tick(dtime)
            self.gameMgr.tick(dtime)
            self.sndMgr.tick(dtime)
            self.overlayMgr.tick(dtime)
            self.inputMgr.tick(dtime)

            self.runTime += dtime

            weu.messagePump()             # Needed for linux/mac
            time.sleep(0.001)

        self.stop()

    def quit(self):
        self.keepRunning = False

# Gunner of Angst Main Engine ------------------------------------------------ #