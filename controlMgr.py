# Simple Keyboard arrows based manual Control Aspect for 38Engine
# Sushil Louis

#from vector import Vector3
import utils
import math
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class ControlMgr:
    toggleMax = 0.01
    def __init__(self, engine):
        self.engine = engine
        print "Control Manager Constructed "
        
    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.toggle = self.toggleMax
        pass

    def stop(self):
        pass
        
    def tick(self, dtime):
        #----------make player ent respond to keyboard controls-----------------------------------
        if self.toggle >= 0:
            self.toggle = self.toggle - dtime

        if  self.toggle < 0:
            self.keyboard.capture()
            self.player = self.engine.entityMgr.ents[0]
            # Movement
            if self.keyboard.isKeyDown(OIS.KC_P):
                self.toggle = self.toggleMax
                self.player.desiredSpeed = utils.clamp(self.player.desiredSpeed + self.player.deltaSpeed, 0, self.player.maxSpeed)
            if  self.keyboard.isKeyDown(OIS.KC_L):
                self.toggle = self.toggleMax
                self.player.desiredSpeed = utils.clamp(self.player.desiredSpeed - self.player.deltaSpeed, 0, self.player.maxSpeed)

            # Yaw
            if  self.keyboard.isKeyDown(OIS.KC_J):
                self.toggle = self.toggleMax
                self.player.aspects[1].node.yaw(self.player.turningRate*dtime)
            if  self.keyboard.isKeyDown(OIS.KC_K):
                self.toggle = self.toggleMax
                self.player.aspects[1].node.yaw(-self.player.turningRate*dtime)
            # Pitch
            if  self.keyboard.isKeyDown(OIS.KC_U):
                self.toggle = self.toggleMax
                self.player.aspects[1].node.pitch(self.player.turningRate*dtime)
            if  self.keyboard.isKeyDown(OIS.KC_I):
                self.toggle = self.toggleMax
                self.player.aspects[1].node.pitch(-self.player.turningRate*dtime)
            # Roll
            if  self.keyboard.isKeyDown(OIS.KC_N):
                self.toggle = self.toggleMax
                self.player.aspects[1].node.roll(self.player.turningRate*dtime)
            if  self.keyboard.isKeyDown(OIS.KC_M):
                self.toggle = self.toggleMax
                self.player.aspects[1].node.roll(-self.player.turningRate*dtime)
#-----------------------------------------------------------------------------------------
