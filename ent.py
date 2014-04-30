from vector        import Vector3
from physics       import Physics
from render        import Renderer
from unitAI        import UnitAI
from pathing       import Pathing
from command       import *
import utils

#-----------------------------------------------------------------------------------------
class Entity:

    aspectTypes = []
    
    def __init__(self, engine, id, pos = Vector3(0,0,0), mesh = 'robot.mesh', vel = Vector3(0, 0, 0), yaw = 0):
        self.engine = engine
        self.uiname = "Robot" + str(id)
        self.eid = id
        self.pos = pos
        self.vel = vel
        self.mesh = mesh
        self.deltaYaw   = 0.0
        self.deltaPitch = 0.0
        self.deltaRoll = 0.0
        self.speed = 0.0
        self.heading = 0.0
        self.aspects = []
        self.isSelected = False

    def init(self):
        self.initAspects()

    def initAspects(self):
        for aspType in self.aspectTypes:
            self.aspects.append(aspType(self))
        
    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.tick(dtime)
        
    def stop(self):
        self.desiredSpeed = 0
        self.desiredHeading = self.heading
        
    def die(self):
        pass
        
    def __str__(self):
        x = "---\nEntity: %s \nPos: %s, Vel: %s,  mesh = %s\nSpeed: %f, Heading: %f, desiredSpeed: %f, desiredHeading: %f" % (self.uiname, str(self.pos), str(self.vel), self.mesh, self.speed, self.yaw, self.desiredSpeed, self.desiredYaw)
        return x

#---------------------------------------------------------------------------------------------------

class PlayerJet(Entity):
    def __init__(self, engine, id, pos = Vector3(0,0,0), orientation = 0, speed = 500):
        Entity.__init__(self, engine, id, pos = pos )
        # General
        self.aspectTypes = [ Pathing, Physics, Renderer ]
        self.mesh = 'razor.mesh'
        self.uiname = 'PlayerJet' + str(id)
        self.health = 100
        # Speed ------------------------
        self.acceleration = 100
        self.maxSpeed = speed
        self.speed = speed
        self.desiredSpeed = speed
        # Yaw --------------------------
        self.desiredYaw = orientation
        self.yaw = orientation
        self.yawRate  = 50
        # Pitch ------------------------
        self.desiredPitch = 0
        self.pitch = 0
        self.pitchRate  = 50
        # Roll -------------------------
        self.desiredRoll = orientation
        self.roll = orientation
        self.rollRate  = 90
        
    @property
    def pathing(self):
        return self.aspects[0]
    @property
    def physics(self):
        return self.aspects[1]
    @property
    def renderer(self):
        return self.aspects[2]
            
#---------------------------------------------------------------------------------------------------

class EnemyJet(Entity):
    def __init__(self, engine, id, pos = Vector3(0,0,0), orientation = 0, speed = 525):
        Entity.__init__(self, engine, id, pos = pos )
        # General
        self.aspectTypes = [ UnitAI, Physics, Renderer ]
        self.mesh = 'RZR-002.mesh'
        self.uiname = 'EnemyJet' + str(id)
        self.health = 50
        # Speed ------------------------
        self.acceleration = 100
        self.maxSpeed = speed
        self.speed = speed
        self.desiredSpeed = speed
        # Yaw --------------------------
        self.desiredYaw = orientation
        self.yaw = orientation
        self.yawRate  = 75
        # Pitch ------------------------
        self.desiredPitch = orientation
        self.pitch = orientation
        self.pitchRate  = 60
        # Roll -------------------------
        self.desiredRoll = orientation
        self.roll = orientation
        self.rollRate  = 90
        
    @property
    def unitai(self):
        return self.aspects[0]
    @property
    def physics(self):
        return self.aspects[1]
    @property
    def renderer(self):
        return self.aspects[2]
        
#---------------------------------------------------------------------------------------------------

class Missile(Entity):
    def __init__(self, engine, id, source):
        Entity.__init__(self, engine, id, pos = source.pos )
        # General
        self.aspectTypes = [ UnitAI, Physics, Renderer ]
        self.mesh = 'missile.mesh'
        self.uiname = 'Missile' + str(id)
        # Speed ------------------------
        self.acceleration = 100
        self.maxSpeed = 750
        self.speed = source.speed
        self.desiredSpeed = self.maxSpeed
        # Yaw --------------------------
        self.desiredYaw = source.yaw
        self.yaw = source.yaw
        self.yawRate  = 30
        # Pitch ------------------------
        self.desiredPitch = source.pitch
        self.pitch = source.pitch
        self.pitchRate  = 30
        # Roll -------------------------
        self.desiredRoll = source.roll
        self.roll = source.roll
        self.rollRate  = 90
        
    @property
    def unitai(self):
        return self.aspects[0]
    @property
    def physics(self):
        return self.aspects[1]
    @property
    def renderer(self):
        return self.aspects[2]
        
#---------------------------------------------------------------------------------------------------