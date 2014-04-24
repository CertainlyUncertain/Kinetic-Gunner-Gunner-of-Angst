from vector import Vector3

class EntityMgr:
    def __init__(self, engine):
        import time
        print "starting ent mgr"
        self.engine = engine
                
    def init(self):
        self.ents = {}
        self.nEnts = 0
        import ent
        self.entTypes = [ent.PlayerJet, ent.EnemyJet]


    def createEnt(self, entType, pos = Vector3(0,100,0), yaw = 0, speed = 500):
        ent = entType(self.engine, self.nEnts, pos, yaw, speed)
        ent.init()
        self.ents[self.nEnts] = ent;
        self.nEnts = self.nEnts + 1
        return ent


    def tick(self, dt):
        for eid, ent in self.ents.iteritems():
            ent.tick(dt)
        

