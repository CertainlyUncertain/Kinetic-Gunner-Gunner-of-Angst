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

# Graphics Manager ----------------------------------------------------------- #

from vector import Vector3
import ogre.renderer.OGRE as ogre
#import ogre.renderer.ogreterrain as ogreterrain

# Manages graphics. Creates graphics, scene, scene nodes, renders scene
class GfxMgr:
    ''' Manages ogre SceneManager, its affiliates, and SceneNodes. '''

    def __init__(self, engine):
        ''' Creation. '''
        self.engine = engine
        self.freeNodes = []
        self.usedNodes = []
        self.totalNodes = 0
        print "Ggraphics Manager Created."

    def init(self):
        ''' Initialization. '''
        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.createScene()
        self.laserTimer = 0
        self.laserDuration = 0.20
        self.rayDuration = 0.25
        print "Graphics Manager Initialized."

    def crosslink(self):
        ''' Links to other Managers. '''
        self.setupCamera()
        
    def tick(self, dtime):
        ''' Update Function. '''
        if self.laser and self.laserTimer > 0:
            self.laserTimer -= dtime
            if self.laserTimer <= 0:
                self.laser.setVisible(False)
                self.ray.setVisible(False)
        self.root.renderOneFrame()
        
    def stop(self):
        ''' Shut Down. '''
        del self.root
        print "Graphics Manager Stopped."

# Graphics Manager ----------------------------------------------------------- #

    def createRoot(self):
        ''' Root Constructor. '''
        self.root = ogre.Root()
 
    def defineResources(self):
        ''' Reads resources from resources.cfg. '''
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
 
    def setupRenderSystem(self):
        ''' Create and Configure the Rendering System. '''
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog -> Application.setupRenderSystem()")
 
    def createRenderWindow(self):
        ''' Creates the Render Window. '''
        self.root.initialise(True, "(CS 381 Spring 2014 Final Project)")
 
    def initializeResourceGroups(self):
        ''' Initialize Resources from defineResources(). '''
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
        self.materialManager = ogre.MaterialManager.getSingleton()
        self.materialManager.setDefaultTextureFiltering(ogre.TFO_ANISOTROPIC)
        self.materialManager.setDefaultAnisotropy(7)
 
    def createScene(self):
        ''' Creates Scene Elements. (SceneManager, Camera, Viewport, etc.) '''
        self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, "Default SceneManager")
        #self.sceneManager.shadowTechnique = ogre.SHADOWTYPE_STENCIL_MODULATIVE
        self.sceneManager.setShadowFarDistance( 10000 )
        self.meshManager = ogre.MeshManager.getSingleton ()

        self.camera = self.sceneManager.createCamera("Camera")
        self.camera.nearClipDistance = 1

        self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)
        self.particleManager = ogre.ParticleSystemManager.getSingleton()

    def setupCamera(self):
        ''' Set up the Camera Nodes and attach the Camera. '''
        self.debugYawNode = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNodeD',(12500, 10000, 12500))
        self.debugPitchNode = self.debugYawNode.createChildSceneNode('PitchNodeD')
        
        self.camYawNode = self.engine.entityMgr.player.renderer.oNode.createChildSceneNode('CamNode1',(0, 30, 0))
        self.camPitchNode = self.camYawNode.createChildSceneNode('PitchNode1')
        self.camPitchNode.attachObject(self.camera)
        
        self.laser = self.sceneManager.createParticleSystem( "Laser", "Angst/Laser" )
        self.laserNode = self.camPitchNode.createChildSceneNode('LaserNode', (0,-6,0))
        self.laserNode.attachObject(self.laser)
        self.laser.setVisible(False)

        self.ray = self.sceneManager.createParticleSystem( "Ray", "Angst/Ray" )
        self.rayNode = self.camPitchNode.createChildSceneNode('RayNode', (0,-6,0))
        self.rayNode.attachObject(self.ray)
        self.ray.setVisible(False)

        self.turret = self.sceneManager.createEntity("LAZER", "laser.mesh")
        self.turretNode = self.camPitchNode.createChildSceneNode('turretNode', (0,-10,-5))
        #self.turretNode.setInheritOrientation(False)
        self.turretNode.yaw(ogre.Degree(90))
        self.turretNode.roll(ogre.Degree(10))
        self.turretNode.attachObject(self.turret)
        
        ##Currently Debug Trail
        # sunParticle = self.sceneManager.createParticleSystem("Sun", "Angst/Sun")
        # sunNode = self.camYawNode.createChildSceneNode("SunNode", (0,-50,0))
        # sunNode.setInheritOrientation(False)
        # sunNode.attachObject(sunParticle)
        
        self.engine.camMgr.crosslink()
        
    def showLaser(self, main = True):
        ''' Show the laser weapon beam. '''
        if main:
            self.laserTimer = self.laserDuration
            self.laser.setVisible(True)
        else:
            self.laserTimer = self.rayDuration
            self.ray.setVisible(True)
        
    def setupScene1(self):
        ''' Sets up the Scene for the first Level. '''
        self.sceneManager.ambientLight = 0.1, 0.1, 0.05
        self.light = self.sceneManager.createLight ('Sun')
        self.light.type = ogre.Light.LT_DIRECTIONAL
        self.light.direction = Vector3(0, -1, 1).normalisedCopy()
        self.light.diffuseColour = (0.8, 0.8, 0.6)
        self.light.specularColour = (0.8, 0.8, 0.6)
 
        # sunParticle = self.sceneManager.createParticleSystem("Sun", "Angst/Sun")
        # sunNode = self.camPitchNode.createChildSceneNode("Particle", (0,5,5))
        # sunNode.attachObject(sunParticle)
 
        # Setup a ground plane
        worldSize = 25000
        height = 160
        self.sceneManager.setWorldGeometry("terrain.cfg")
        self.groundPlane = ogre.Plane ((0, 1, 0), height)
        self.meshManager.createPlane ('Ground', 'General', self.groundPlane,
                                    worldSize, worldSize, 20, 20, True, 1, 5, 5, (0, 0, 1))
        ent = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode('Water', (worldSize/2,0,worldSize/2)).attachObject(ent)
        ent.setMaterialName ('Angst/Ocean2_Cg')
        ent.castShadows = False
        # Sky Box/Plane --------------------------------------------------------
        self.sceneManager.setSkyDome (True, "Angst/Sky1", 10, 6)
        #plane = ogre.Plane ((0, -1, 0), -10)
        #self.sceneManager.setSkyPlane (True, plane, "Examples/SpaceSkyPlane", 100, 45, True, 0.5, 150, 150)
        # Fog ------------------------------------------------------------------
        #fadeColour = (0.1, 0.1, 0.1)
        #self.viewPort.backgroundColour = fadeColour
        #self.sceneManager.setFog (ogre.FOG_LINEAR, fadeColour, 0.0, 3000, 7500)
        
        #ent = self.sceneManager.createEntity('MountainEnt', 'Mountain.mesh')
        #node = self.sceneManager.getRootSceneNode().createChildSceneNode('Mountain', (0,325,0))
        #node.attachObject(ent)
        #node.setScale(500,1500,1000)
        
        self.setupCamera()

    def setupScene2(self):
        ''' Sets up the Scene for the second Level. '''
        self.sceneManager.ambientLight = 0.05, 0.05, 0.075
        self.light = self.sceneManager.createLight ('Moon')
        self.light.type = ogre.Light.LT_DIRECTIONAL
        self.light.direction = Vector3(1, -1, 1).normalisedCopy()
        self.light.diffuseColour = (0.4, 0.4, 0.6)
        self.light.specularColour = (0.4, 0.4, 0.6)
 
        # Setup a ground plane.
        worldSize = 25000
        height = 160
        self.sceneManager.setWorldGeometry("terrain2.cfg")
        self.groundPlane = ogre.Plane ((0, 1, 0), height)
        #meshManager = ogre.MeshManager.getSingleton ()
        self.meshManager.createPlane ('Ground', 'General', self.groundPlane,
                                    35000, 35000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        water = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode('Water', (worldSize/2,0,worldSize/2)).attachObject(water)
        water.setMaterialName ('OceanCg')
        water.castShadows = False
        # Sky Box/Plane --------------------------------------------------------
        self.sceneManager.setSkyDome (True, "Angst/Nebula2", 10, 4)
        #plane = ogre.Plane ((0, -1, 0), -10)
        #self.sceneManager.setSkyPlane (True, plane, "Examples/SpaceSkyPlane", 100, 45, True, 0.5, 150, 150)
        # Fog ------------------------------------------------------------------
        #fadeColour = (0.1, 0.1, 0.1)
        #self.viewPort.backgroundColour = fadeColour
        #self.sceneManager.setFog (ogre.FOG_LINEAR, fadeColour, 0.0, 3000, 7500)
        self.setupCamera()

    def clearScene(self):
        self.camera.parentSceneNode.detachObject(self.camera)
        self.laser.parentSceneNode.detachObject(self.laser)
        self.laser = None
        self.freeNodes = []
        self.usedNodes = []
        self.totalNodes = 0
        self.sceneManager.clearScene()

    def getNode(self):
        ''' Retreives/Creates and returns an ogre Scene Node. '''
        if len(self.freeNodes) > 0:
            node = self.freeNodes.pop()#len(self.freeNodes) )
            # Show?
        else:
            node = self.sceneManager.getRootSceneNode().createChildSceneNode(str(self.totalNodes))
            self.totalNodes += 1
        self.usedNodes.append( node )
        return node
        
    def recycleNode(self, node):
        ''' Moves am ogre Scene Node into the recycle list. '''
        i = self.usedNodes.index(node)
        self.usedNodes.pop(i)
        # hide?
        self.freeNodes.append(node)
        return node
        
# Graphics Manager ----------------------------------------------------------- #
