from vector import Vector3
from expression import Expression
import ent
import command
import random

class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        # Game Variables
        self.currentWeapon = self.weapon1
        self.weaponCooldown = 0.0
        self.weaponCooldownMax = 0.5
        self.score = 0
        print "starting Game mgr"
        pass

    def init(self):
        random.seed()
        self.loadLevel()

    def weapon1(self):
        targ = None
        for eid, ent in self.engine.entityMgr.enemiess.iteritems():
            result  =  mouseRay.intersects(ent.renderer.oEnt.getWorlBoundingBox())
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
            targ.unitai.setCommand( command.Crash(targ) )
            targ.unitai.addCommand( command.Follow(targ, self.engine.entityMgr.player, Vector3(10,20,30)) )

    def weapon2(self):
        for eid, ent in self.engine.entityMgr.enemiess.iteritems():
            result  =  mouseRay.intersects(ent.renderer.oEnt.getWorlBoundingBox())
            if result.first:
                print "Direct Hit! on " + ent.uiname
                result.first.unitai.setCommand( command.Crash(targ) )
                result.first.unitai.addCommand( command.Follow(targ, self.engine.entityMgr.player, Vector3(10,20,30)) )
                
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

    def fire(self, ray):
        if self.weaponCooldown < 0:
            self.currentWeapon()
            self.weaponCooldown = self.weaponCooldownMax
        pass
       
    def switchWeapon(self, num):
        if num == 3:
            self.currentWeapon = self.weapon3
        elif num == 2:
            self.currentWeapon = self.weapon2
        else:
            self.currentWeapon = self.weapon1
        
    def loadLevel(self):
        self.level1()

    def level1(self):
        # Create Terrain
        # Create Player
        player = self.engine.entityMgr.createPlayer(ent.PlayerJet, Vector3(1000,1000,1000), 0, 750)
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 3 ), Expression( 270, 5 ), Expression( 0, 3 ), Expression( -270, 5 ) ]
        pitch = [ Expression( 0, 5 ), Expression( 30, 3 ), Expression( -60, 6 ), Expression( 30, 3 ) ]
        player.pathing.addMultiple( speed, yaw, pitch )

        # Create Enemy Spawns
        for i in range(0,10):
            x = random.randrange(-5000, 5000)
            y = random.randrange(-500,2500)
            z = random.randrange(-5000, 5000)
            created = self.engine.entityMgr.createEnemy(ent.EnemyJet, player.pos + Vector3(x,y,z), 0, 755)
            x = random.randint(125, 175)
            y = random.randint(50,100)
            i = random.randint(1,2)
            z = random.randint(125, 175) * (-1)**i
            created.unitai.addCommand( command.Follow( created, player, Vector3(x,y,z) ) )

        # Set UI Elements


    def tick(self, dt):
        # Firing Cooldown
        self.weaponCooldown -= dt
        # Check for level complete?
        # Update Enemy Spawn List?
        pass

    def stop(self):
        pass

