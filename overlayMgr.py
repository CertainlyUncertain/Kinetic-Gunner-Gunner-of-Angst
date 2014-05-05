import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class OverlayMgr():
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.overlayManager = ogre.OverlayManager.getSingleton()
        self.font = ogre.FontManager.getSingleton().create( "BlueHighway", "General" )
        self.font.setType(ogre.FT_TRUETYPE)
        self.font.setSource("fonts/bluehigh.ttf")
        self.font.load()

        self.maxAngst = 510

        # splash screen
        self.splashScreen = self.overlayManager.createOverlayElement('Panel', 'SplashScreenPanel')
        self.splashScreen.metricsMode = ogre.GMM_PIXELS
        self.splashScreen.setPosition( 0, 0 )
        self.splashScreen.setDimensions( self.engine.gfxMgr.viewPort.actualWidth, self.engine.gfxMgr.viewPort.actualHeight )
        self.splashScreen.materialName = "Angst/SplashScreen"

        # crosshairs
        self.targetPanel = self.overlayManager.createOverlayElement('Panel', 'TargetPanel')
        self.targetPanel.metricsMode = ogre.GMM_PIXELS
        self.targetPanel.setPosition(self.engine.gfxMgr.viewPort.actualWidth/2-64, self.engine.gfxMgr.viewPort.actualHeight/2-64)
        self.targetPanel.setDimensions(128, 128)
        self.targetPanel.materialName="Angst/Crosshair"

        # score
        self.textArea = self.overlayManager.createOverlayElement("TextArea", "ScoreTextArea")
        self.textArea.setMetricsMode(ogre.GMM_PIXELS)
        self.textArea.setCaption("hello world")
        self.textArea.setPosition(10, 10)
        self.textArea.setDimensions(100, 13)
        self.textArea.setFontName("BlueHighway")
        self.textArea.setCharHeight(13)
        self.textArea.setColour( (1.0, 1.0, 0.7) )

        # angst meter
        self.angstMeter = self.overlayManager.createOverlayElement('Panel', 'AngstPanel')
        self.angstMeter.metricsMode = ogre.GMM_PIXELS
        self.angstMeter.setPosition(self.engine.gfxMgr.viewPort.actualWidth-512, self.engine.gfxMgr.viewPort.actualHeight-24)
        self.angstMeter.setDimensions(self.maxAngst, 24)
        self.angstMeter.materialName="Angst/BarBG"

        self.angstBar = self.overlayManager.createOverlayElement('Panel', 'AngstBarPanel')
        self.angstBar.metricsMode = ogre.GMM_PIXELS
        self.angstBar.setPosition(self.engine.gfxMgr.viewPort.actualWidth-511, self.engine.gfxMgr.viewPort.actualHeight-23)
        self.angstBar.setDimensions(0, 22)
        self.angstBar.materialName="Angst/Bar"

        # add display panels
        self.overlay = self.overlayManager.create('UIOverlay')
        self.overlay.add2D(self.targetPanel)
        self.overlay.add2D(self.angstMeter)
        self.overlay.add2D(self.angstBar)
        self.overlay.add2D(self.splashScreen) # this has to be last to render over everything else
        self.overlay.show()

        self.textArea.show()

    def destroy(self, name):
        self.overlayManager.destroyOverlayElement( name )

    def tick(self, dt):
        angstRatio =  1.0 - (float(self.engine.entityMgr.player.health) / float(self.engine.entityMgr.player.maxHealth))
        self.angstBar.setDimensions(angstRatio * self.maxAngst, 22)

