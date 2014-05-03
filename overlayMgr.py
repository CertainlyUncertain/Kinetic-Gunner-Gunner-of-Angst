import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class OverlayMgr():
	def __init__(self, engine):
		self.engine = engine

	def init(self):
		self.trackpercent = 0
		
		overlayManager = ogre.OverlayManager.getSingleton()
		self.overlayManager = overlayManager
		#create panels


		self.trackheight = 550
		self.trackwidth = 800
		self.trackofset = 590

		


		self.targetPanel = overlayManager.createOverlayElement('Panel', 'TargetPanel')
		self.targetPanel.metricsMode = ogre.GMM_PIXELS
		self.targetPanel.setPosition(self.trackofset+self.trackwidth/2, self.trackheight-10)
		self.targetPanel.setDimensions(4, 40)
		self.targetPanel.materialName="Examples/Crosshair"

		self.targetPanel2 = overlayManager.createOverlayElement('Panel', 'TargetPanel2')
		self.targetPanel2.metricsMode = ogre.GMM_PIXELS
		self.targetPanel2.setPosition(self.trackofset+self.trackwidth/2-19, self.trackheight+10)
		self.targetPanel2.setDimensions(40, 4)
		self.targetPanel2.materialName="Examples/Crosshair"

		





		
		self.overlay = overlayManager.create('MessageOverlay')



		self.overlay.add2D(self.targetPanel)
		self.overlay.add2D(self.targetPanel2)

		self.overlay.show()
	
		
	def tick(self, hp, now,score,combo):
		pass


		





	
