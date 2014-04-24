from vector import Vector3
from expression import Expression
import ent
import command
import random

class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        print "starting Game mgr"
        pass

    def init(self):
        random.seed()
        self.loadLevel()


    def loadLevel(self):
        self.game1()
        

    def game1(self):
        # Create Terrain
        # Create Player
        player = self.engine.entityMgr.createEnt(ent.PlayerJet, Vector3(1000,750,1000), 0, 500)
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 3 ), Expression( 270, 7 ), Expression( 0, 3 ), Expression( -270, 7 ) ]
        pitch = [ ]#Expression( 0, 5 ), Expression( -15, 3 ), Expression( 15, 3 ) ]
        player.aspects[0].addMultiple( speed, yaw, pitch )

        # Create Enemy Spawns
        for i in range(0,21):
            x = random.randrange(-750, 750)
            y = random.randrange(-150,150)
            z = random.randrange(-750, 750)
            created = self.engine.entityMgr.createEnt(ent.EnemyJet, player.pos - Vector3(x,y,z), 0, 525)
            created.follow( player )

        import time
        #time.sleep(20)
        # Set UI Elements


    def tick(self, dt):
        # Check for level complete?
        # Update Enemy Spawn List?
        pass

    def stop(self):
        pass

