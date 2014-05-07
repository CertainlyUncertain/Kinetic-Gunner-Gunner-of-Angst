import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class OverlayMgr():
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.overlayManager = ogre.OverlayManager.getSingleton()
        self.fontManager = ogre.FontManager.getSingleton()
        self.font = self.fontManager.create( "BlueHighway", "General" )
        self.font.setType(ogre.FT_TRUETYPE)
        self.font.setSource("fonts/bluehigh.ttf")
        self.fontManager.load( "BlueHighway", "General" )

        self.maxAngst = 510
        fontSize = 42
        self.score = 0
        
        # Splash Screen
        self.splashScreen = self.overlayManager.createOverlayElement('Panel', 'SplashScreenPanel')
        self.splashScreen.metricsMode = ogre.GMM_PIXELS
        self.splashScreen.setPosition( 0, 0 )
        self.splashScreen.setDimensions( self.engine.gfxMgr.viewPort.actualWidth, self.engine.gfxMgr.viewPort.actualHeight )
        self.splashScreen.materialName = "Angst/SplashScreen"

        # Crosshairs
        self.targetPanel = self.overlayManager.createOverlayElement('Panel', 'TargetPanel')
        self.targetPanel.metricsMode = ogre.GMM_PIXELS
        self.targetPanel.setPosition(self.engine.gfxMgr.viewPort.actualWidth/2-64, self.engine.gfxMgr.viewPort.actualHeight/2-64)
        self.targetPanel.setDimensions(128, 128)
        self.targetPanel.materialName="Angst/Crosshair"

        # Score
        self.scoreText = self.overlayManager.createOverlayElement("TextArea", "ScoreTextArea")
        self.scoreText.setMetricsMode(ogre.GMM_PIXELS)
        self.scoreText.setCaption("Score: " + str(self.score))
        self.scoreText.setPosition(5, 5)
        self.scoreText.setFontName("BlueHighway")
        self.scoreText.setCharHeight(fontSize)
        self.scoreText.setColour( (1.0,1.0,0.7) ) #color of angst: (0.54,0.4,0.97)

        self.scorePanel = self.overlayManager.createOverlayElement("Panel", "ScorePanel")
        self.scorePanel.metricsMode = ogre.GMM_PIXELS
        self.scorePanel.setPosition(0, self.engine.gfxMgr.viewPort.actualHeight-fontSize)
        self.scorePanel.setDimensions(150, 42)
        self.scorePanel.materialName = "Angst/BarBG"
        self.scorePanel.addChild( self.scoreText )
        
        # Angst Meter Background
        self.angstMeter = self.overlayManager.createOverlayElement('Panel', 'AngstPanel')
        self.angstMeter.metricsMode = ogre.GMM_PIXELS
        self.angstMeter.setPosition(self.engine.gfxMgr.viewPort.actualWidth-512, self.engine.gfxMgr.viewPort.actualHeight-25)
        self.angstMeter.setDimensions(self.maxAngst, 24)
        self.angstMeter.materialName="Angst/BarBG"
        # Angst Meter
        self.angstBar = self.overlayManager.createOverlayElement('Panel', 'AngstBarPanel')
        self.angstBar.metricsMode = ogre.GMM_PIXELS
        self.angstBar.setPosition(self.engine.gfxMgr.viewPort.actualWidth-511, self.engine.gfxMgr.viewPort.actualHeight-24)
        self.angstBar.setDimensions(0, 22)
        self.angstBar.materialName="Angst/Bar"

        # Add Panels to Overlay
        self.overlay = self.overlayManager.create('UIOverlay')
        self.overlay.add2D(self.targetPanel)
        self.overlay.add2D(self.scorePanel)
        self.overlay.add2D(self.angstMeter)
        self.overlay.add2D(self.angstBar)
        self.overlay.add2D(self.splashScreen) # this has to be last to render over everything else
        self.overlay.show()

    def ShowSplash(self):
        self.splashScreen.materialName = "Angst/SplashScreen"
        self.splashScreen.show()
        pass

    def ShowVictorySplash(self):
        self.splashScreen.materialName = "Angst/Victory"
        self.splashScreen.show()
        pass

    def ShowDefeatSplash(self):
        self.splashScreen.materialName = "Angst/Defeat"
        self.splashScreen.show()
        pass
    
    def HideSplash(self):
        self.splashScreen.hide()

    def destroy(self, name):
        self.overlayManager.destroyOverlayElement( name )

    def tick(self, dt):
        angstRatio = 1.0 - (float(self.engine.entityMgr.player.health) / float(self.engine.entityMgr.player.maxHealth))
        self.angstBar.setDimensions(angstRatio * self.maxAngst, 22)

        # update score
        self.score = self.engine.gameMgr.score
        self.scoreText.setCaption("Score: " + str(self.score))
        self.scorePanel.setDimensions(136 + (len(str(self.score))*18), 42)
        
    def stop(self):
        self.overlayManager.destroyAll()

