from vector import Vector3

import utils
import math
import ogre.renderer.OGRE as ogre

class Renderer:
    def __init__(self, ent):
        self.ent = ent
        print "Rendering setting up for: ", str(self.ent)
        self.oEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + "_ogreEnt", self.ent.mesh)
        self.yawNode =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'yNode', ent.pos)
        self.pitchNode = self.yawNode.createChildSceneNode(self.ent.uiname + 'pNode')
        self.rollNode = self.pitchNode.createChildSceneNode(self.ent.uiname + 'rNode')
        self.pitchNode.yaw( ogre.Degree(90) )
        self.rollNode.attachObject(self.oEnt)
        
    def tick(self, dtime):
        #---------- Update Scene Node Position and Orientation ----------------
        self.yawNode.setPosition(self.ent.pos)
        #self.yawNode.resetOrientation()
        self.yawNode.yaw( ogre.Degree(self.ent.deltaYaw) )
        #self.pitchNode.resetOrientation()
        self.pitchNode.pitch( ogre.Degree(-self.ent.deltaPitch) )
        #self.rollNode.resetOrientation()
        self.rollNode.roll( ogre.Degree(self.ent.deltaRoll) )

# --------------------------------------------------------------------------- #