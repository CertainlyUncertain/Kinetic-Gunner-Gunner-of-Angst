from vector        import Vector3
import utils
import math
import ent

class Command:
    def __init__(self, ent):
        self.ent = ent
        pass

    def getDesiredHeadingToTargetPosition(self, targetPos):
        diff = targetPos - self.ent.pos
        return math.degrees(math.atan2(-diff.z, diff.x))
    
    def tick(self, dtime):
        pass


class Move( Command ):
    def __init__(self, ent, targ):
        Command.__init__(self, ent)
        self.target = targ
        
    def tick(self, dt):
        return True

class Follow( Command ):
    def __init__(self, ent, targ, offset = 100):
        Command.__init__(self, ent)
        self.target = targ
        self.offset = offset

    def tick(self, dtime):
        # Set Target Point
        point = Vector3(0, self.target.pos.y, 0)
        point.x = self.target.pos.x + self.offset * math.cos(math.radians(self.target.yaw))
        point.z = self.target.pos.z + self.offset * -math.sin(math.radians(self.target.yaw))
        # Check Planar Distance
        distance = math.sqrt((point.x - self.ent.pos.x)**2 + (point.z - self.ent.pos.z)**2)
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(point)
        # Check Distance
        if distance < 300:
            self.ent.desiredSpeed = self.target.speed
            self.ent.desiredYaw = self.target.yaw
        else:
            self.ent.desiredSpeed = self.ent.maxSpeed
        # Height Difference (Pitch)
        difference = point.y - self.ent.pos.y
        if math.fabs(difference) > 100:
            self.ent.desiredPitch = math.degrees(math.atan2(difference, distance))
        else:
            self.ent.desiredPitch = self.target.pitch
#---------------------------------------------------------------------------------------------------
