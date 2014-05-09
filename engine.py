# Gunner of Angst Main Engine ------------------------------------------------ #

class Engine(object):
    ''' The root of the global manager tree '''

    def __init__(self):
        pass

    def init(self):
        import time
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
        self.camMgr.stop()
        self.gameMgr.stop()
        self.inputMgr.stop()
        self.gfxMgr.stop()

    def run(self):
        import time
        import ogre.renderer.OGRE as ogre
        weu = ogre.WindowEventUtilities() # Needed for linux/mac
        weu.messagePump()                 # Needed for linux/mac

	    # Show Splash Screen
        self.overlayMgr.showSplash()
        self.gfxMgr.root.renderOneFrame()
        time.sleep( 3 )
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
            print "entTick"
            self.entityMgr.tick(dtime)
            print "gfxTick"
            self.gfxMgr.tick(dtime)
            print "netTick"
            self.netMgr.tick(dtime)
            print "camTick"
            self.camMgr.tick(dtime)
            print "gameTick"
            self.gameMgr.tick(dtime)
            print "sndTick"
            self.sndMgr.tick(dtime)
            print "ovrTick"
            self.overlayMgr.tick(dtime)
            print "inputTick"
            self.inputMgr.tick(dtime)
            
            self.runTime += dtime
        
            weu.messagePump()             # Needed for linux/mac
            time.sleep(0.001)

        self.stop()
        print "381 Engine exiting..."
        
    
