from vector import Vector3
from spawning import *
from expression import Expression
import ent
import command

class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        # Game Variables
        self.score = 0
        self.levelTimer = 100
        self.levels = []
        self.currentLevel = 1
        self.lastLevel = 3
        self.spawns = []
        self.spawnIndex = 0
        # Weapon Variables
        self.primaryWeapon = self.weapon1
        self.secondaryWeapon = self.weapon2
        self.weaponCooldown = 0.0
        self.weaponHeat = 0
        self.weaponMaxHeat = 100
        self.weaponCoolingSpeed = 20
        print "Game Manager Created"

    def init(self):
        import random
        self.randomizer = random
        self.randomizer.seed(None)
        self.levels = [ self.level1, self.level2, self.level3 ]
        print "Game Manager Initializing"

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

        for eid, ent in self.engine.entityMgr.missiles.iteritems():
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
            self.score += targ.damage( 25 )
        self.engine.sndMgr.playSound(self.engine.sndMgr.laser)
        self.weaponHeat += 15
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
        self.levels[self.currentLevel-1]()

    def levelEnd(self, victory = False ):

        # if Victory:
        if victory:
            # Display Victory Score Screen
            self.engine.overlayMgr.ShowVictorySplash()
            self.currentLevel += 1
            # Check for last level?
            if self.currentLevel > self.maxLevel:
                self.currentLevel = 1
        # else: Defeat
        else:
            # Display Defeat Score Screen
            self.engine.overlayMgr.ShowDefeatSplash()
        # Clear Scene & Entity Manager
        self.engityMgr.clear()
        self.engine.clearScene()
        # Wait for input
        while not self.engine.imputMgr.MB_Left_Down:
            pass
        # Do stuff
        
        
    def level1(self):
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 5 ), Expression( -90, 3 ), Expression( 0, 3 ), Expression( -180, 5 ), Expression( -270, 6 ), Expression( 0, 2 ),
                Expression( -90, 3 ), Expression( 0, 2 ), Expression( 90, 3 ), Expression( 270, 5 ), Expression( 0, 2 ), Expression( -90, 3 ) ]
        pitch = [ Expression( 0, 5 ), Expression( 30, 3 ), Expression( -60, 6 ), Expression( 30, 3 ),
                    Expression( 0, 5 ), Expression( -15, 2 ), Expression( 30, 4 ), Expression( -15, 2 ) ]
        player.pathing.addMultiple( speed, yaw, pitch )
            
        self.spawns = [ SpawnCycle( [SpawnGroup(ent.EnemyJet, 2)], 15), SpawnCycle( [SpawnGroup(ent.EnemyJet, 3)], 20) ]
        self.levelTimer = 270
        # Create Terrain
        self.engine.gfxMgr.setupScene1()
        # Set BGM
        self.engine.sndMgr.playMusic( "bg2.wav" )

    def level2(self):
        # Create Player
        player = self.engine.entityMgr.createPlayer(ent.PlayerJet, Vector3(1000,900,1000), 0, 750)
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 5 ), Expression( 90, 3 ), Expression( 0, 3 ), Expression( 180, 5 ), Expression( 270, 6 ), Expression( 0, 2 ),
                Expression( 90, 3 ), Expression( 0, 2 ), Expression( -90, 3 ), Expression( -270, 5 ), Expression( 0, 2 ), Expression( 90, 3 ) ]
        pitch = [ Expression( 0, 5 ), Expression( 25, 4 ), Expression( -50, 8 ), Expression( 25, 4 ),
                    Expression( 0, 5 ), Expression( -15, 3 ), Expression( 30, 6 ), Expression( -15, 3 ) ]
        player.pathing.addMultiple( speed, yaw, pitch )
            
        self.spawns = [ SpawnCycle( [SpawnGroup(ent.EnemyJet, 2)], 15), SpawnCycle( [SpawnGroup(ent.EnemyJet, 3)], 10), SpawnCycle( [SpawnGroup(ent.EnemyJet, 2)], 20) ]
        self.levelTimer = 300
        # Create Terrain
        self.engine.gfxMgr.setupScene2()
        # Set BGM
        self.engine.sndMgr.playMusic( "bg1.wav" )

    def level3(self):
        pass
        
    def createRandomOffset(self):
        x = self.randomizer.randint(-175, -125)
        y = self.randomizer.randint(50,100)
        i = self.randomizer.randint(1,2)
        z = self.randomizer.randint(125, 175) * (-1)**i
        return Vector3(x,y,z)

    def tick(self, dt):
        if self.engine.entityMgr.player.health <= 0:
            self.levelEnd(False)
        else:
            # Overheating
            self.weaponHeat -= self.weaponCoolingSpeed * dt
            if self.weaponHeat < 0:
                self.weaponHeat = 0
            # Firing Cooldown
            if self.weaponCooldown > 0:
                self.weaponCooldown -= dt
            else:
                if self.engine.inputMgr.MB_Left_Down:
                    self.primaryWeapon()
                elif self.engine.inputMgr.MB_Right_Down:
                    self.secondaryWeapon()
            # Check for level complete?
            if self.levelTimer < 0:
                self.levelEnd( True )
            else:
                self.levelTimer -= dt
            # Update Enemy Spawn List
            if self.spawns[self.spawnIndex].tick(dt):
                self.spawns[self.spawnIndex].spawn(self.engine.entityMgr)
                self.spawnIndex = (self.spawnIndex + 1) % len(self.spawns)

    def crosslink(self):
        self.loadLevel()

    def stop(self):
        pass

