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

# Input Manager -------------------------------------------------------------- #

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
from vector import Vector3
import os
import time

class InputMgr(OIS.KeyListener, OIS.MouseListener, OIS.JoyStickListener):
    ''' Manages keyboard and mouse, with buffered and unbuffered input. '''
    
    def __init__(self, engine):
        ''' Creates Input Listeners and Initializes Variables. '''
        self.engine = engine
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.JoyStickListener.__init__(self)
        self.move = 1000
        self.rotate = 25
        self.selectionRadius = 100
        self.MB_Left_Down = False
        self.MB_Right_Down = False
        print "Input Manager Created."

    def init(self):
        ''' Sets the Window and Creates Input System and Objects. '''
        windowHandle = 0
        renderWindow = self.engine.gfxMgr.root.getAutoCreatedWindow()
        windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        paramList = [("WINDOW", str(windowHandle))]

        if os.name == "nt":
            #t = [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_NONEXCLUSIVE")]
            t = [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_EXCLUSIVE")]
        else:
            t = [("x11_mouse_grab", "true"), ("x11_mouse_hide", "true")]
            #t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "true")]

        paramList.extend(t)

        self.inputManager = OIS.createPythonInputSystem(paramList)
 
        # Now InputManager is initialized for use. Keyboard and Mouse objects
        # must still be initialized separately
        self.keyboard = None
        self.mouse    = None
        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
            self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
            #Joystick
        except Exception, e:
            print "No Keyboard or mouse!!!!"
            raise e
        if self.keyboard:
            self.keyboard.setEventCallback(self)
        if self.mouse:
            self.mouse.setEventCallback(self)
            self.windowResized( renderWindow )
 
        print "Input Manager Initialized."

    def crosslink(self):
        ''' Links to other Managers. '''
        pass

    def tick(self, dtime):
        ''' Update keyboard and mouse. '''
        self.keyboard.capture()
        self.mouse.capture()
        self.handleCamera(dtime)
        self.handleModifiers(dtime)
        # Quit
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.keepRunning = False
        pass
        
    def stop(self):
        ''' Destory Input Objects and System. '''
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
        print "Input Manager Stopped."
        
    # Keyboard Listener ----------------------------------------------------- #
    def keyPressed(self, evt):
        '''Handles Toggleable Key Presses'''
        # Swap Cameras (Between First-Person and Debug Views)
        if self.keyboard.isKeyDown(OIS.KC_G):
            self.engine.camMgr.swap()
        # Pause ------------------------DEBUG-----------------------------------
        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            time.sleep(10)
        return True

    def keyReleased(self, evt):
        return True
    
    def handleModifiers(self, dtime):
        self.leftShiftDown = self.keyboard.isKeyDown(OIS.KC_LSHIFT)
        self.leftCtrlDown = self.keyboard.isKeyDown(OIS.KC_LCONTROL)
        pass
        
    def handleCamera(self, dtime):
        '''Move the camera using keyboard input.'''
        # Forward
        if self.keyboard.isKeyDown(OIS.KC_W):
            self.engine.camMgr.transVector.z -= self.move
        # Backward
        if self.keyboard.isKeyDown(OIS.KC_S):
            self.engine.camMgr.transVector.z += self.move
        # Left
        if self.keyboard.isKeyDown(OIS.KC_A):
            self.engine.camMgr.transVector.x -= self.move
        # Right
        if  self.keyboard.isKeyDown(OIS.KC_D):
            self.engine.camMgr.transVector.x += self.move
        # Up     
        if self.keyboard.isKeyDown(OIS.KC_3):
            self.engine.camMgr.transVector.y += self.move
        # Down
        if self.keyboard.isKeyDown(OIS.KC_4):
            self.engine.camMgr.transVector.y -= self.move          
        # Yaw
        if self.keyboard.isKeyDown(OIS.KC_Q):
            self.engine.camMgr.yawRot = -self.rotate
        # Yaw
        if self.keyboard.isKeyDown(OIS.KC_E):
            self.engine.camMgr.yawRot = self.rotate
        # Pitch
        if self.keyboard.isKeyDown(OIS.KC_Z):
            self.engine.camMgr.pitchRot = -self.rotate
        # Pitch
        if self.keyboard.isKeyDown(OIS.KC_X):
            self.engine.camMgr.pitchRot = self.rotate
        # Roll
        if self.keyboard.isKeyDown(OIS.KC_R):
            self.engine.camMgr.rollRot = self.rotate
        # Roll
        if self.keyboard.isKeyDown(OIS.KC_V):
            self.engine.camMgr.rollRot = -self.rotate
        pass
        
    # MouseListener --------------------------------------------------------- #
    def mouseMoved(self, evt):
        currMouse = self.mouse.getMouseState()
        self.engine.camMgr.yawRot += currMouse.X.rel
        self.engine.camMgr.pitchRot += currMouse.Y.rel
        return True

    def mousePressed(self, evt, id):
        #self.mouse.capture()
        #self.ms = self.mouse.getMouseState()

        #self.ms.width = self.engine.gfxMgr.viewPort.actualWidth 
        #self.ms.height = self.engine.gfxMgr.viewPort.actualHeight
        #self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        
        if id == OIS.MB_Left:
            self.MB_Left_Down = True

        elif id == OIS.MB_Right:
            self.MB_Right_Down = True
        return True
                
    def mouseReleased(self, evt, id):
        if id == OIS.MB_Left:
            self.MB_Left_Down = False

        elif id == OIS.MB_Right:
            self.MB_Right_Down = False
        return True
    
    # JoystickListener ------------------------------------------------------ #
    def buttonPressed(self, evt, button):
        return True
    def buttonReleased(self, evt, button):
        return True
    def axisMoved(self, evt, axis):
        return True

    def windowResized (self, rw):
        temp = 0
        width, height, depth, left, top= rw.getMetrics(temp,temp,temp, temp, temp)  # Note the wrapped function as default needs unsigned int's
        ms = self.mouse.getMouseState()
        ms.width = width
        ms.height = height
         
# Input Manager -------------------------------------------------------------- #
