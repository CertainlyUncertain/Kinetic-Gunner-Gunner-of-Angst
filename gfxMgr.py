# Graphics manager
import ogre.renderer.OGRE as ogre

# Manages graphics. Creates graphics, scene, scene nodes, renders scene
class GfxMgr:
    def __init__(self, engine):
        self.engine = engine
        self.freeNodes = []
        self.usedNodes = []
        self.totalNodes = 0

    def init(self):
        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.setupScene()

    def tick(self, dtime):
        self.root.renderOneFrame()

    # The Root constructor for the ogre
    def createRoot(self):
        self.root = ogre.Root()
 
    # Here the resources are read from the resources.cfg
    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load("resources.cfg")
 
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            secName = seci.peekNextKey()
            settings = seci.getNext()
 
            for item in settings:
                typeName = item.key
                archName = item.value
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
 
    # Create and configure the rendering system (either DirectX or OpenGL) here
    def setupRenderSystem(self):
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog -> Application.setupRenderSystem()")
 
    # Create the render window
    def createRenderWindow(self):
        self.root.initialise(True, "(CS 381 Spring 2014 Final Project)")
 
    # Initialize the resources here (which were read from resources.cfg in defineResources()
    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
 
    # Now, create a scene here. Three things that MUST BE done are sceneManager, camera and
    # viewport initializations
    def setupScene(self):
        self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, "Default SceneManager")

        self.camera = self.sceneManager.createCamera("Camera")
        self.camera.nearClipDistance = 5

        self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)
        self.sceneManager.ambientLight = 0.9, 0.8, 0.6
 
        # Setup a ground plane.
        self.sceneManager.setWorldGeometry("terrain.cfg")
        self.groundPlane = ogre.Plane ((0, 1, 0), 350)
        meshManager = ogre.MeshManager.getSingleton ()
        meshManager.createPlane ('Ground', 'General', self.groundPlane,
                                    30000, 30000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        ent = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode('Water').attachObject(ent)
        ent.setMaterialName ('Ocean2_Cg')
        ent.castShadows = False
        # Sky Box/Plane --------------------------------------------------------
        self.sceneManager.setSkyDome (True, "Examples/CloudySky", 5, 8)
        #plane = ogre.Plane ((0, -1, 0), -10)
        #self.sceneManager.setSkyPlane (True, plane, "Examples/SpaceSkyPlane", 100, 45, True, 0.5, 150, 150)
        # Fog ------------------------------------------------------------------
        #fadeColour = (0.1, 0.1, 0.1)
        #self.viewPort.backgroundColour = fadeColour
        #self.sceneManager.setFog (ogre.FOG_LINEAR, fadeColour, 0.0, 3000, 7500)

    def crosslink(self):
        self.debugYawNode = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNodeD',(0, 4000, 0))
        self.debugPitchNode = self.debugYawNode.createChildSceneNode('PitchNodeD')
        
        self.camYawNode = self.engine.entityMgr.player.renderer.oNode.createChildSceneNode('CamNode1',(-6, 30, -5))
        self.camPitchNode = self.camYawNode.createChildSceneNode('PitchNode1')
        self.camPitchNode.attachObject(self.camera)
 
    # In the end, clean everything up (delete)
    def stop(self):
        del self.root

    def getNode(self):
        if len(self.freeNodes) > 0:
            node = self.freeNodes.pop()#len(self.freeNodes) )
            # Show?
        else:
            node = self.sceneManager.getRootSceneNode().createChildSceneNode(str(self.totalNodes))
            self.totalNodes += 1
        self.usedNodes.append( node )
        return node
        
    def recycleNode(self, node):
        i = self.usedNodes.index(node)
        self.usedNodes.pop(i)
        # hide?
        self.freeNodes.append(node)
        return node
        
# ---------------------------------------------------------------------------- #