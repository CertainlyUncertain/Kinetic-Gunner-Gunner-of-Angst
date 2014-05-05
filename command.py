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
        
class Crash( Command ):
    def __init__(self, ent):
        Command.__init__(self, ent)
        self.ent.desiredPitch = -45
        self.ent.desiredSpeed = self.ent.speed
        self.ent.desiredYaw = self.ent.yaw
        self.ent.desiredRoll = self.ent.roll
        self.timer = 5.0
        
    def tick(self, dt):
        ## Check for Ground
            ## Raytrace forward
            ## Check Distance to closest
            ## If Ent and not terrain
                ## Kill it as well
                ## Die
            ## If Ground
                ## Die
                
        # raySceneQuery = self.engine.gfxMgr.sceneManager.createRayQuery(ogre.Ray( self.ent.pos, self.ent.vel ))
        # raySceneQuery.setSortByDistance( True )

        # result = raySceneQuery.execute()
        # if len(result) > 0:
            # if result[0].first < 50:
                # if item.movable:
                    # print item.movable.getName()
                # elif item.worldFragment:
                    # print item.worldFragment
                # #self.ent.die()
        # self.engine.gfxMgr.sceneManager.destroyQuery(raySceneQuery)
        
        ## vs Height
            ## if < ground
                ## Die
                ## Return True
            ## else:
                ## Return False
                
        ## vs Timer
        ## Update Timer
        self.timer -= dt
            ## Check for Done
        if self.timer < 0:
            ## Return True/False
            return True
            ## Die
        return False

class Explode( Command ):
    def __init__(self, ent):
        Command.__init__(self, ent)
        #self.ent.desiredPitch = self.ent.pitch
        #self.ent.desiredSpeed = self.ent.speed
        #self.ent.desiredYaw = self.ent.yaw
        #self.ent.desiredRoll = self.ent.roll
        #self.ent.desiredSpeed = 0
        self.timer = 2.0
        
    def tick(self, dt):
        self.timer -= dt
        if self.timer < 0:
            self.ent.engine.entityMgr.dead.append(self.ent)
            return True
        return False  
        
class Follow( Command ):
    def __init__(self, ent, targ):
        Command.__init__(self, ent)
        self.target = targ

    def tick(self, dtime):
        # Check Planar Distance
        distance = math.sqrt((self.target.pos.x - self.ent.pos.x)**2 + (self.target.pos.z - self.ent.pos.z)**2)
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(self.target.pos)
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
        difference = self.target.pos.y - self.ent.pos.y
        self.ent.desiredPitch = math.degrees(math.atan2(difference, distance))
            
class OffsetFollow( Command ):
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
            
class Intercept( Command ):
    def __init__(self, ent, targ):
        Command.__init__(self, ent)
        self.target = targ
        self.angle = math.degrees(math.atan2(-offset.z, offset.x))
        self.height = offset.y

    def tick(self, dtime):
        # Check Planar Distance
        distance = math.sqrt((self.target.pos.x - self.ent.pos.x)**2 + (self.target.pos.z - self.ent.pos.z)**2)
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(self.target.pos)
        # Check Distance
        if distance < 50:
            # Explode
            ##self.ent.unitai.addCommand( Explode(self.ent) )
            if math.fabs(utils.diffAngle(self.ent.yaw, self.ent.desiredYaw)) < 90:
                self.ent.desiredSpeed = self.target.speed
            else:
                self.ent.desiredSpeed = self.ent.maxSpeed - math.fabs(self.ent.speed - self.ent.maxSpeed)
                self.ent.desiredYaw = self.target.yaw
        else:
            # Set Course
            #self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(self.target.pos)
            self.ent.desiredSpeed = self.ent.maxSpeed
        # Height Difference (Pitch)
        difference = self.target.pos.y - self.ent.pos.y
        self.ent.desiredPitch = math.degrees(math.atan2(difference, distance))

    # def __init__(self, ent, targetEnt):
        # Command.__init__(self, ent, targetEnt)
        # self.targetEntity = targetEnt
        # self.entity.desiredHeading = self.getDesiredHeadingToTargetPosition(self.targetEntity.pos, self.entity.pos)
        # self.entity.desiredSpeed = self.entity.maxSpeed
        # self.done = False
        # self.isEntityTarget = True
        # print "Intercepting: ", str(self.targetEntity)

    # def tick(self, dt):
        # if not self.done:
            # if self.entity.pos.squaredDistance(self.targetEntity.pos) < 100:
                # self.done = True
                # self.entity.desiredSpeed = 0
            # else:
                # self.entity.desiredHeading = self.getDesiredHeadingToTargetPosition(self.targetEntity.pos, self.entity.pos)
                
    # def tick(self, dtime):
        # # Set Speed
        # self.ent.desiredSpeed = self.ent.maxSpeed

        # # Calculate Intercept Point
        # distance = math.sqrt((self.target.pos.x - self.ent.pos.x)**2 + (self.target.pos.z - self.ent.pos.z)**2)
        # speed = self.ent.speed
        # if( speed < 0.01 ):
            # time = 0
        # else:
            # time = distance / speed
        # print time
        # point = self.target.pos + self.target.vel * time
        
        # # Set Heading
        # self.ent.desiredHeading = math.atan2( -( point.z - self.ent.pos.z ),
                                                  # point.x - self.ent.pos.x )
        # self.ent.desiredHeading = utils.fixAngle(self.ent.desiredHeading)
        
#---------------------------------------------------------------------------------------------------
