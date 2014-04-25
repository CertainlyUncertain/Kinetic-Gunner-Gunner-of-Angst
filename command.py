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
    def __init__(self, ent, targ, offset = Vector3(0,0,0)):
        Command.__init__(self, ent)
        self.target = targ
        self.offset = math.sqrt((offset.x)**2 + (offset.z)**2)
        self.angle = math.degrees(math.atan2(-offset.z, offset.x))
        self.height = offset.y

    def tick(self, dtime):
        # Set Target Point
        point = Vector3(0, self.target.pos.y + self.height, 0)
        angleRad = math.radians(utils.diffAngle(self.target.yaw, -self.angle))
        point.x = self.target.pos.x + self.offset * math.cos(angleRad)
        point.z = self.target.pos.z + self.offset * -math.sin(angleRad)
        # Check Planar Distance
        distance = math.sqrt((point.x - self.ent.pos.x)**2 + (point.z - self.ent.pos.z)**2)
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(point)
        # Check Distance
        if distance < 100:
            if math.fabs(utils.diffAngle(self.ent.yaw, self.ent.desiredYaw)) < 90:
                self.ent.desiredSpeed = self.target.speed
            else:
                self.ent.desiredSpeed = self.ent.maxSpeed - math.fabs(self.ent.speed - self.ent.maxSpeed)
                self.ent.desiredYaw = self.target.yaw
        else:
            self.ent.desiredSpeed = self.ent.maxSpeed
        # Height Difference (Pitch)
        difference = point.y - self.ent.pos.y
        self.ent.desiredPitch = math.degrees(math.atan2(difference, distance))
        # if math.fabs(difference) > 33:
            # self.ent.desiredPitch = math.degrees(math.atan2(difference, distance))
        # else:
            # self.ent.desiredPitch = self.target.pitch
#---------------------------------------------------------------------------------------------------
