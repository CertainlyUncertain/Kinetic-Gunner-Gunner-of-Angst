from vector import Vector3
import command

class EntityMgr:
    def __init__(self, engine):
        import time
        print "starting ent mgr"
        self.engine = engine
                
    def init(self):
        self.player = None
        self.enemies = {}
        self.nEnems = 0
        self.projectiles = {}
        self.nProjs = 0
        import random
        self.randomizer = random
        self.randomizer.seed(None)
        import ent
        self.entTypes = [ent.PlayerJet, ent.EnemyJet]

    def createPlayer(self, playerType, pos, yaw, speed):
        self.player = playerType(self.engine, 0, pos, yaw, speed)
        self.player.init()
        return self.player
    
    def createEnemy(self, enemyType, pos = None, speed = None):
        if pos == None:
            x = self.randomizer.randint(-5000, 5000)
            y = self.randomizer.randint(-500, 2500)
            z = self.randomizer.randint(-5000, 5000)
            pos = self.player.pos + Vector3(x,y,z)
        if speed == None:
            speed = self.player.speed + 10
            
        ent = enemyType(self.engine, self.nEnems, pos, 0, speed)
        ent.init()
        ent.unitai.addCommand( command.Follow( ent, self.player, self.createRandomOffset() ) )
        self.enemies[self.nEnems] = ent;
        self.nEnems = self.nEnems + 1
        return ent
        
    def createProjectile(self, projType, source, target):
        ent = projType(self.engine, self.nProjs, source.pos, source.yaw, source.speed)
        ent.init()
        self.projectiles[self.nProjs] = ent;
        self.nProjs = self.nProjs + 1
        return ent
        
    def createRandomOffset(self):
        x = self.randomizer.randint(125, 175)
        y = self.randomizer.randint(50,100)
        i = self.randomizer.randint(1,2)
        z = self.randomizer.randint(125, 175) * (-1)**i
        return Vector3(x,y,z)

    def tick(self, dt):
        # for eid, ent in self.ents.iteritems():
            # ent.tick(dt)
        self.player.tick(dt)
        for eid, ent in self.enemies.iteritems():
            ent.tick(dt)
        for eid, ent in self.projectiles.iteritems():
            ent.tick(dt)