# Entities ------------------------------------------------------------------- #

from vector        import Vector3
from physics       import Physics
from render        import Renderer
from unitAI        import UnitAI
from pathing       import Pathing
from particles     import Particles
import command
import utils

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Entity:
    ''' Base Entity Class. '''
    
    aspectTypes = []
    
    def __init__(self, engine, id, pos = Vector3(0,0,0), mesh = 'robot.mesh', vel = Vector3(0, 0, 0), yaw = 0):
        ''' Creation. '''
        self.engine = engine
        # General
        self.eid = id
        self.uiname = "Robot" + str(id)
        self.mesh = mesh
        self.aspects = []
        self.flag = "Healthy"
        # Combat
        self.health = 1
        self.points = 0
        # Position and Movement
        self.pos = pos
        self.vel = vel
        self.deltaYaw   = 0.0
        self.deltaPitch = 0.0
        self.deltaRoll = 0.0
        self.speed = 0.0
        self.yaw = 0.0

    def init(self):
        ''' Creates and Initializes Aspects. '''
        for aspType in self.aspectTypes:
            self.aspects.append(aspType(self))
        
    def tick(self, dtime):
        ''' Updates Aspects. '''
        for aspect in self.aspects:
            aspect.tick(dtime)
        #print "Delta: yaw:%f, pitch:%f, roll:%f\n" % (self.deltaYaw, self.deltaPitch, self.deltaRoll)
        
    def delete(self):
        ''' Destroys Aspects. '''
        self.particles.delete()
        node = self.renderer.delete()
        self.aspects = []
        return node
        
    def damage(self, amount):
        ''' Updates Health, Status, and Command, and plays Sounds. '''
        self.health -= amount
        print self.uiname + " Health: " + str(self.health) + '/' + str(self.maxHealth)
        if self.health <= -(self.maxHealth/2):
            self.engine.sndMgr.playSound(self.engine.sndMgr.hit) #, self.pos )
            self.unitai.setCommand( command.Explode(self) )
            self.flag = "Dead"
            return self.points
        elif self.health <= 0:
            self.flag = "Crashing"
            self.engine.sndMgr.playSound(self.engine.sndMgr.jetExplode) #, self.pos )
            self.unitai.setCommand( command.Crash(self) )
            #self.unitai.addCommand( command.Explode(self) )
            return self.points
        else:
            self.flag = "Damaged"
            self.engine.sndMgr.playSound(self.engine.sndMgr.hit) #, self.pos )
            return 0
        
    def getBoundingBox(self):
        ''' Returns Axis-Aligned Bounding Box. '''
        return self.renderer.oEnt.getWorldBoundingBox()
        
    def __str__(self):
        ''' Converts to String. '''
        x = "---\nEntity: %s \nPos: %s, Vel: %s,  mesh = %s\nSpeed: %f, Heading: %f" % (self.uiname, str(self.pos), str(self.vel), self.mesh, self.speed, self.yaw)
        return x

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class PlayerJet(Entity):
    ''' Player Jet Entity Class. '''
    
    def __init__(self, engine, id, pos = Vector3(0,0,0), orientation = 0, speed = 500):
        ''' Creation. '''
        Entity.__init__(self, engine, id, pos = pos, vel = Vector3(0, 0, 0))
        # General ----------------------
        self.aspectTypes = [ Pathing, Physics, Renderer, Particles ]
        self.mesh = 'player.mesh'
        self.uiname = 'PlayerJet' + str(id)
        self.flag = "Player"
        # Combat -----------------------
        self.maxHealth = 100
        self.health = 100
        self.points = 0
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
        self.rollRate  = 75
        
    @property
    def pathing(self):
        return self.aspects[0]
    @property
    def physics(self):
        return self.aspects[1]
    @property
    def renderer(self):
        return self.aspects[2]
    @property
    def particles(self):
        return self.aspects[3]
        
    def damage(self, amount):
        self.health -= amount
        self.engine.sndMgr.playSound(self.engine.sndMgr.hit) #, self.pos )
        print self.uiname + " Health: " + str(self.health) + '/' + str(self.maxHealth)
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class EnemyJet(Entity):
    ''' Enemy Jet Entity Class. '''
    
    def __init__(self, engine, id, pos = Vector3(0,0,0), orientation = 0, speed = 525):
        ''' Creation. '''
        Entity.__init__(self, engine, id, pos = pos, vel = Vector3(0, 0, 0) )
        # General ----------------------
        self.aspectTypes = [ UnitAI, Physics, Renderer, Particles ] #Combat
        self.mesh = 'enemy.mesh' #jet.mesh / RZR-002.mesh
        self.uiname = 'EnemyJet' + str(id)
        self.flag = "Enemy"
        # Combat -----------------------
        self.maxHealth = 50
        self.health = 50
        self.points = 25
        self.fireCooldown = 5
        self.distance = 10000
        self.difference = -1
        self.explodeDmg = 50
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
    @property
    def particles(self):
        return self.aspects[3]
        
    def fire(self):
        ''' Creates an Enemy Missile Entity. '''
        self.engine.entityMgr.createMissile(Missile, self)
        self.fireCooldown = 10
        
    def tick(self, dtime):
        ''' Updates Firing Cooldown. '''
        Entity.tick(self, dtime)
        if 100 < self.distance < 3000 and self.difference > 0:
            if self.fireCooldown < 0 < self.health:
                self.fire()
            else:
                self.fireCooldown -= dtime
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Missile(Entity):
    ''' Enemy Missile Entity Class. '''
    
    def __init__(self, engine, id, source):
        ''' Creation. '''
        Entity.__init__(self, engine, id, pos = source.pos, vel = Vector3(0, 0, 0) )
        # General ----------------------
        self.aspectTypes = [ UnitAI, Physics, Renderer, Particles ]
        self.mesh = 'missile.mesh' #missile3.mesh / missile.mesh
        self.uiname = 'Missile' + str(id)
        self.flag = "Missile"
        # Combat -----------------------
        self.maxHealth = 10
        self.health = 10
        self.points = 5
        self.duration = 10
        self.distance = 10000
        self.explodeDmg = 25
        # Speed ------------------------
        self.acceleration = 50
        self.maxSpeed = 1000
        self.speed = source.speed
        self.desiredSpeed = self.maxSpeed
        # Yaw --------------------------
        self.desiredYaw = source.yaw
        self.yaw = source.yaw
        self.yawRate  = 100
        # Pitch ------------------------
        self.desiredPitch = source.pitch
        self.pitch = source.pitch
        self.pitchRate  = 100
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
    @property
    def particles(self):
        return self.aspects[3]
            
    def tick(self, dtime):
        ''' Updates Remaining Duration. '''
        Entity.tick(self, dtime)
        if self.duration < 0:
            self.unitai.setCommand( command.Crash(self) )
            self.duration = 10
        else:
            self.duration -= dtime
  
def damage(self, amount):
        ''' Updates Health and Command and plays Sounds. '''
        self.health -= amount
        print self.uiname + " Health: " + str(self.health) + '/' + str(self.maxHealth)
        if self.health <= 0:
            self.engine.sndMgr.playSound(self.engine.sndMgr.missileExplode) #, self.pos )
            self.unitai.setCommand( command.Explode(self) )
            self.flag = "Dead"
            return self.points
          
# Entities ------------------------------------------------------------------- #
