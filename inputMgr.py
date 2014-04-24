# Input manager. Initialize and manage keyboard and mouse. Buffered and unbuffered input
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS


from vector import Vector3
import os
from command import *
import time

class InputMgr(OIS.KeyListener, OIS.MouseListener, OIS.JoyStickListener):
    def __init__(self, engine):
        self.engine = engine
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.JoyStickListener.__init__(self)
        self.move = 500
        self.rotate = 0.01
        self.toggle = 0.1
        self.selectionRadius = 100
        pass


    def init(self):
        windowHandle = 0
        renderWindow = self.engine.gfxMgr.root.getAutoCreatedWindow()
        windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        paramList = [("WINDOW", str(windowHandle))]

        if os.name == "nt":
            t = [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_NONEXCLUSIVE")]
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
 
        import random
        self.randomizer = random
        self.randomizer.seed(None)
        print "Initialized Input Manager"

    def crosslink(self):
        pass

    def stop(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
        
    def tick(self, dtime):
        self.keyboard.capture()
        self.mouse.capture()
        self.keyPressed(dtime)
        self.handleModifiers(dtime)
        pass

    def handleModifiers(self, dtime):
        self.leftShiftDown = self.keyboard.isKeyDown(OIS.KC_LSHIFT)
        self.leftCtrlDown = self.keyboard.isKeyDown(OIS.KC_LCONTROL)
        pass
        
    def handleCamera(self, dtime):
        pass
        
    def keyPressed(self, evt):
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
        if self.keyboard.isKeyDown(OIS.KC_PGUP):
            self.engine.camMgr.transVector.y += self.move
        # Down
        if self.keyboard.isKeyDown(OIS.KC_PGDOWN):
            self.engine.camMgr.transVector.y -= self.move          
        # Yaw
        if self.keyboard.isKeyDown(OIS.KC_Q):
            self.engine.camMgr.yawRot = self.rotate
        # Yaw
        if self.keyboard.isKeyDown(OIS.KC_E):
            self.engine.camMgr.yawRot = -self.rotate
        # Pitch
        if self.keyboard.isKeyDown(OIS.KC_Z):
            self.engine.camMgr.pitchRot = self.rotate
        # Pitch
        if self.keyboard.isKeyDown(OIS.KC_X):
            self.engine.camMgr.pitchRot = -self.rotate
        # Roll
        if self.keyboard.isKeyDown(OIS.KC_R):
            self.engine.camMgr.rollRot = self.rotate
        # Roll
        if self.keyboard.isKeyDown(OIS.KC_V):
            self.engine.camMgr.rollRot = -self.rotate
        # Swap Cameras (Between First-Person and Debug Views)
        if self.keyboard.isKeyDown(OIS.KC_G):
            self.engine.camMgr.Swap()
        # Pause
        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            time.sleep(10)
        # Quit
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.stop()

        return True

    def keyReleased(self, evt):
        return True
    
    # MouseListener
    def mouseMoved(self, evt):
        currMouse = self.mouse.getMouseState()
        self.engine.camMgr.Yaw(currMouse.X.rel)
        self.engine.camMgr.Pitch(currMouse.Y.rel)
        return True

    def mousePressed(self, evt, id):
        #if id == OIS.MB_Left:
            #self.handleMouseSelection(evt)

        #elif id == OIS.MB_Right:
            #self.handleMouseOrders(evt)
        return True

    def handleMouseSelection(self, evt):
        self.mouse.capture()
        self.ms = self.mouse.getMouseState()
        print str(self.ms)

        self.ms.width = self.engine.gfxMgr.viewPort.actualWidth 
        self.ms.height = self.engine.gfxMgr.viewPort.actualHeight
        self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(*self.mousePos)
        result  =  mouseRay.intersects(self.engine.gfxMgr.groundPlane)

        if result.first:
            pos =  mouseRay.getPoint(result.second)
            self.mousePosWorld = pos

            closest = None
            closestDistance = self.selectionRadius * self.selectionRadius
            for ent in self.engine.entityMgr.ents.values():
                distSquared =  ent.pos.squaredDistance(pos)
                if distSquared < closestDistance:
                    closest = ent
                    closestDistance = distSquared

            if closest: # One level deep
                if self.leftShiftDown:
                    self.engine.selectionMgr.addSelectedEnt(closest)
                else:
                    self.engine.selectionMgr.selectEnt(closest)
            else:
                self.engine.selectionMgr.killSelection()

    def handleMouseOrders(self, evt):
        self.mouse.capture()
        self.ms = self.mouse.getMouseState()
        print str(self.ms)
        selection = self.engine.selectionMgr.getSelected()

        self.ms.width = self.engine.gfxMgr.viewPort.actualWidth 
        self.ms.height = self.engine.gfxMgr.viewPort.actualHeight
        self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(*self.mousePos)
        result  =  mouseRay.intersects(self.engine.gfxMgr.groundPlane)

        if result.first:
            pos =  mouseRay.getPoint(result.second)
            self.mousePosWorld = pos

            closest = None
            closestDistance = self.selectionRadius * self.selectionRadius
            for ent in self.engine.entityMgr.ents.values():
                distSquared =  ent.pos.squaredDistance(pos)
                if distSquared < closestDistance:
                    closest = ent
                    closestDistance = distSquared

            for ent in selection:
                if closest:
                    if self.leftCtrlDown:
                        if self.leftShiftDown:
                            ent.aspects[2].addCommand( Intercept(ent,closest) )
                        else:
                            ent.aspects[2].setCommand( Intercept(ent,closest) )
                    else:
                        if self.leftShiftDown:
                            ent.aspects[2].addCommand( Follow(ent,closest) )
                        else:
                            ent.aspects[2].setCommand( Follow(ent,closest) )
                else:
                    if self.leftShiftDown:
                            ent.aspects[2].addCommand( Move(ent,self.mousePosWorld) )
                    else:
                        ent.aspects[2].setCommand( Move(ent,self.mousePosWorld) )
                
    def mouseReleased(self, evt, id):
        return True
    
    # JoystickListener
    def buttonPressed(self, evt, button):
        return True
    def buttonReleased(self, evt, button):
        return True
    def axisMoved(self, evt, axis):
        return True

#---------------------------------------------------------------------------------------------------
