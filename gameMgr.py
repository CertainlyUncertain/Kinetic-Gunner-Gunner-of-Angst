from vector import Vector3
from spawning import *
from expression import Expression
import ent
import command

class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        # Game Variables
        self.primaryWeapon = self.weapon1
        self.secondaryWeapon = self.weapon2
        self.weaponCooldown = 0.0
        self.score = 0
        print "starting Game mgr"
        pass

    def init(self):
        import random
        self.randomizer = random
        self.randomizer.seed(None)
        self.spawns = []
        self.spawnIndex = 0
        self.loadLevel()

    def weapon1(self):
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(0.5, 0.5)
        targ = None
        for eid, ent in self.engine.entityMgr.enemies.iteritems():
            result  =  mouseRay.intersects(ent.renderer.oEnt.getWorldBoundingBox())
            if result.first:
                if not targ:
                    targ = ent
                    min = result.second
                else:
                    if result.second < min:
                        targ = ent
                        min = result.second
        if targ:
            print "Direct Hit! on " + targ.uiname
            targ.damage( 25 )
        self.weaponCooldown = 0.5

    def weapon2(self):
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(0.5, 0.5)
        for eid, ent in self.engine.entityMgr.enemies.iteritems():
            result  =  mouseRay.intersects(ent.renderer.oEnt.getWorldBoundingBox())
            if result.first:
                print "Direct Hit! on " + ent.uiname
                ent.unitai.setCommand( command.Crash(ent) )
                ent.unitai.addCommand( command.Follow(ent, self.engine.entityMgr.player, self.createRandomOffset()) )
        self.weaponCooldown = 1.0
                
    def weapon3(self):
        raySceneQuery = self.engine.gfxMgr.sceneManager.createRayQuery(ogre.Ray())
        raySceneQuery.setSortByDistance( True )
        raySceneQuery.setRay(targetRay)

        result = raySceneQuery.execute()
        if len(result) > 0:
            for item in result:
                if item.movable:
                    print item.movable.getName()
        self.engine.gfxMgr.sceneManager.destroyQuery(raySceneQuery)
        self.weaponCooldown = 0.333

    # def firePrimary(self):
        # if self.weaponCooldown < 0:
            # self.primaryWeapon()
        # pass
       
    # def fireSecondary(self):
        # if self.weaponCooldown < 0:
            # self.secondaryWeapon()
        # pass

    def switchWeapon(self, num):
        if num == 3:
            self.currentWeapon = self.weapon3
        elif num == 2:
            self.currentWeapon = self.weapon2
        else:
            self.currentWeapon = self.weapon1
        
    def loadLevel(self):
        self.level1()
        #self.levels[self.currentLevel]

    def levelComplete(self, victory = True ):
        # Clear Scene
        # if Victory:
            # Display Victory Score Screen
        # else: Defeat
            # Display Defeat Score Screen
        pass
        
    def level1(self):
        # Create Terrain
        # Create Player
        player = self.engine.entityMgr.createPlayer(ent.PlayerJet, Vector3(1000,900,1000), 0, 750)
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 3 ), Expression( 270, 5 ), Expression( 0, 3 ), Expression( -270, 5 ) ]
        pitch = [ Expression( 0, 5 ), Expression( 30, 3 ), Expression( -60, 6 ), Expression( 30, 3 ) ]
        player.pathing.addMultiple( speed, yaw, pitch )
            
        self.spawns.append( SpawnCycle( [SpawnGroup(ent.EnemyJet, 1)], 30) )

        # Set UI Elements

    def createRandomOffset(self):
        x = self.randomizer.randint(125, 175)
        y = self.randomizer.randint(50,100)
        i = self.randomizer.randint(1,2)
        z = self.randomizer.randint(125, 175) * (-1)**i
        return Vector3(x,y,z)

    def tick(self, dt):
        # Firing Cooldown
        if self.weaponCooldown > 0:
            self.weaponCooldown -= dt
        else:
            if self.engine.inputMgr.MB_Left_Down:
                self.primaryWeapon()
            elif self.engine.inputMgr.MB_Right_Down:
                self.secondaryWeapon()
        # Check for level complete?
        # Update Enemy Spawn List
        if self.spawns[self.spawnIndex].tick(dt):
            self.spawns[self.spawnIndex].spawn(self.engine.entityMgr)
            self.spawnIndex = (self.spawnIndex + 1) % len(self.spawns)
        pass

    def stop(self):
        pass

