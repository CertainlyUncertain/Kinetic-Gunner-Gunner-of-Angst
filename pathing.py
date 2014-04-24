from expression import Expression
import math

class Pathing:
    paths = {}
    indices = {}
    
    def __init__(self, ent, speed = [], yaw = [], pitch = []):
        self.ent = ent
        # Speed
        self.paths['speed'] = speed
        self.indices['speed'] = 0
        # Yaw
        self.paths['yaw'] = yaw
        self.indices['yaw'] = 0
        # Pitch
        self.paths['pitch'] = pitch
        self.indices['pitch'] = 0

    def tick(self, dt):
        # Yaw ---------------------------------------------
        if len(self.paths['yaw']) > 0:
            self.ent.desiredYaw, self.ent.yawRate = self.paths['yaw'][self.indices['yaw']].tick(dt)
            #self.ent.desiredYaw += math.copysign(self.ent.yawRate * dt, self.ent.desiredYaw)
            if self.paths['yaw'][self.indices['yaw']].complete():
                self.indices['yaw'] = (self.indices['yaw'] + 1) % len(self.paths['yaw'])
        # Pitch -------------------------------------------
        if len(self.paths['pitch']) > 0:
            self.ent.desiredPitch, self.ent.pitchRate = self.paths['pitch'][self.indices['pitch']].tick(dt)
            #self.ent.desiredPitch += math.copysign(self.ent.pitchRate * dt, self.ent.desiredPitch)
            if self.paths['pitch'][self.indices['pitch']].complete():
                self.indices['pitch'] = (self.indices['pitch'] + 1) % len(self.paths['pitch'])
        # Speed -------------------------------------------
        if len(self.paths['speed']) > 0:
            self.ent.desiredSpeed, self.ent.acceleration = self.paths['speed'][self.indices['speed']].tick(dt)
            #self.ent.desiredSpeed += math.copysign(self.ent.acceleration * dt, self.ent.desiredSpeed)
            if self.paths['speed'][self.indices['speed']].complete():
                self.indices['speed'] = (self.indices['speed'] + 1) % len(self.paths['speed'])


    def addSingle(self, key, adding):
        self.paths[key].append( adding )

    def addMultiple(self, speed = [], yaw = [], pitch = []):
        self.paths['speed'].extend( speed )
        self.paths['yaw'].extend( yaw )
        self.paths['pitch'].extend( pitch )
#---------------------------------------------------------------------------------------------------
