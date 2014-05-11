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

# Entity Manager ------------------------------------------------------------- #

import ogre.renderer.OGRE as ogre
from vector import Vector3
import utils

class CamMgr:
    def __init__(self, engine):
        ''' Creation. '''
        self.engine = engine
        self.camYaw = 180.0
        self.yawSpeed = -0.1
        self.camPitch = 0.0
        self.pitchSpeed = -0.1
        self.pitchMax = 75.0
        self.pitchMin = -15.0
        self.debugCam = False
        self.transVector = Vector3(0,0,0)
        self.yawRot = 0.0
        self.pitchRot = 0.0
        self.rollRot = 0.0
        print "Camera Manager Created."

    def init(self):
        ''' Initialization. '''
        self.camYawNode = None
        self.camPitchNode = None
        print "Camera Manager Initialized."
        pass        

    def crosslink(self):
        ''' Links Camera Nodes from Graphics Manager '''
        self.camera = self.engine.gfxMgr.camera
        self.camYawNode = self.engine.gfxMgr.camYawNode
        self.camPitchNode = self.engine.gfxMgr.camPitchNode
        self.camYawNode.yaw(ogre.Degree(self.camYaw).valueRadians())
        self.camPitchNode.pitch(ogre.Degree(self.camPitch).valueRadians())
        print "Camera Manager Linked."

    def tick(self, dt):
        ''' Update Camera, Yaw, Pitch, and Roll '''
        if self.camYawNode:
            self.camYawNode.translate(self.camYawNode.orientation * self.transVector * dt)
            self.transVector = Vector3(0,0,0)
            self.Yaw(self.yawRot)
            self.yawRot = 0.0
        if self.camPitchNode:
            self.Pitch(self.pitchRot)
            self.pitchRot = 0.0
            self.camPitchNode.roll(ogre.Degree(self.rollRot))
            self.rollRot = 0.0
        
    def stop(self):
        self.camera = None
        self.camYawNode = None
        self.camPitchNode = None
        pass
        
# Entity Manager ------------------------------------------------------------- #

    def Yaw(self, amount):
        ''' Yaws the Camera Yaw Node clamped by Min and Max '''
        self.camYaw = utils.fixAngle( self.camYaw + self.yawSpeed * amount )
        self.camYawNode.resetOrientation()
        self.camYawNode.yaw(ogre.Degree(self.camYaw).valueRadians())

    def Pitch(self, amount):
        ''' Pitches the Camera Pitch Node clamped by Min and Max '''
        self.camPitch = utils.fixAngle( self.camPitch + self.pitchSpeed * amount )
        self.camPitch = utils.clamp( self.camPitch, self.pitchMin, self.pitchMax )
        self.camPitchNode.resetOrientation()
        self.camPitchNode.pitch(ogre.Degree(self.camPitch).valueRadians())

    def swap(self):
        ''' Swaps between 1st person and 3rd person (debug) cameras '''
        self.debugCam = not self.debugCam
        if( self.debugCam ):
            self.camYawNode = self.engine.gfxMgr.debugYawNode
            self.camPitchNode = self.engine.gfxMgr.debugPitchNode
            self.pitchMin = -90.0
        else:
            self.camYawNode = self.engine.gfxMgr.camYawNode
            self.camPitchNode = self.engine.gfxMgr.camPitchNode
            self.pitchMin = 0.0
        self.camera.parentSceneNode.detachObject(self.camera)
        self.camPitchNode.attachObject(self.camera)
    
    def clear(self):
        ''' Clears Node References and Resets Yaw and Pitch. '''
        self.camYawNode = None
        self.camPitchNode = None
        self.camYaw = 180.0
        self.camPitch = 0.0

# Entity Manager ------------------------------------------------------------- #