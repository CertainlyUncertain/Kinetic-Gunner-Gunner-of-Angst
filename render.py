# Renderer ------------------------------------------------------------------- #

from vector import Vector3
import utils
import math
import ogre.renderer.OGRE as ogre

class Renderer:
    def __init__(self, ent):
        self.ent = ent
        print "Rendering setting up for: ", str(self.ent)
        self.oEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + "_ogreEnt", self.ent.mesh)
        self.oNode =  self.ent.engine.gfxMgr.getNode()
        self.oNode.attachObject(self.oEnt)
        self.oNode.setPosition(self.ent.pos)
        #self.yawNode =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'yNode', ent.pos)
        #self.pitchNode = self.yawNode.createChildSceneNode(self.ent.uiname + 'pNode')
        #self.rollNode = self.pitchNode.createChildSceneNode(self.ent.uiname + 'rNode')
        #self.pitchNode.yaw( ogre.Degree(90) )
        #self.rollNode.attachObject(self.oEnt)

        # Create Smoke and Explosion Particles
        self.smoke = self.ent.engine.gfxMgr.sceneManager.createParticleSystem("Smoke" + self.ent.uiname, "Angst/Smoke")
        ##sunNode = self.camYawNode.createChildSceneNode("SunNode", (0,-50,0))
        ##self.oNode.setInheritOrientation(False)
        self.oNode.attachObject(self.smoke)
        self.smoke.setEmitting(False)

        self.explosion = self.ent.engine.gfxMgr.sceneManager.createParticleSystem("Explosion" + self.ent.uiname, "Angst/Explosion")
        ##sunNode = self.camYawNode.createChildSceneNode("SunNode", (0,-50,0))
        ##sunNode.setInheritOrientation(False)
        self.oNode.attachObject(self.explosion)
        self.explosion.setEmitting(False)
        
    def tick(self, dtime):
        #---------- Update Scene Node Position and Orientation ----------------
        # self.yawNode.setPosition(self.ent.pos)
        #self.yawNode.resetOrientation()
        # self.yawNode.yaw( ogre.Degree(self.ent.deltaYaw) )
        #self.pitchNode.resetOrientation()
        # self.pitchNode.pitch( ogre.Degree(-self.ent.deltaPitch) )
        #self.rollNode.resetOrientation()
        # self.rollNode.roll( ogre.Degree(self.ent.deltaRoll) )

        # Particles
        if self.ent.flag == "Dead":
            self.smoke.setEmitting(False)
            self.explosion.setEmitting(True)
            self.oEnt.setVisible(False)
            pass
        elif self.ent.flag == "Damaged":
            self.smoke.setEmitting(True)
            pass

        self.oNode.setPosition(self.ent.pos)
        self.oNode.resetOrientation()
        self.oNode.yaw( ogre.Degree(self.ent.yaw) )
        self.oNode.pitch( ogre.Degree(-self.ent.pitch) )
        self.oNode.roll( ogre.Degree(self.ent.roll) )
        
    def delete(self):
        self.oNode.detachObject(self.oEnt)
        self.smoke.setEmitting(False)
        self.explosion.setEmitting(False)
        self.oNode.detachObject(self.smoke)
        self.oNode.detachObject(self.explosion)
        #self.oEnt.detachFromParent()
        self.oEnt = None
        node = self.oNode
        self.oNode = None
        self.ent = None
        return node
        
# Renderer ------------------------------------------------------------------- #
