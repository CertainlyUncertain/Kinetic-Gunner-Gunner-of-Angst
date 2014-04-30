from vector import Vector3

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
        # self.ents = {}
        import ent
        self.entTypes = [ent.PlayerJet, ent.EnemyJet]

    def createPlayer(self, playerType, pos, yaw, speed):
        self.player = playerType(self.engine, 0, pos, yaw, speed)
        self.player.init()
        return self.player
    
    def createEnemy(self, enemyType, pos = Vector3(0,100,0), yaw = 0, speed = 500):
        ent = enemyType(self.engine, self.nEnems, pos, yaw, speed)
        ent.init()
        self.enemies[self.nEnems] = ent;
        self.nEnems = self.nEnems + 1
        return ent
        
    def createProjectile(self, projType, source, target):
        ent = projType(self.engine, self.nProjs, pos, yaw, speed)
        ent.init()
        self.projectiles[self.nProjs] = ent;
        self.nProjs = self.nProjs + 1
        return ent
        
    # def createEnt(self, entType, pos = Vector3(0,100,0), yaw = 0, speed = 500):
        # ent = entType(self.engine, self.nEnts, pos, yaw, speed)
        # ent.init()
        # self.ents[self.nEnts] = ent;
        # self.nEnts = self.nEnts + 1
        # return ent

    def tick(self, dt):
        # for eid, ent in self.ents.iteritems():
            # ent.tick(dt)
        self.player.tick(dt)
        for eid, ent in self.enemies.iteritems():
            ent.tick(dt)
        for eid, ent in self.projectiles.iteritems():
            ent.tick(dt)