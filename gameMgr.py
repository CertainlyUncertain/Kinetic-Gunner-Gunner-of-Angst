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
        player = self.engine.entityMgr.createEnt(ent.PlayerJet, Vector3(1000,1000,1000), 0, 750)
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 3 ), Expression( 270, 5 ), Expression( 0, 3 ), Expression( -270, 5 ) ]
        pitch = [ Expression( 0, 5 ), Expression( 30, 3 ), Expression( -60, 6 ), Expression( 30, 3 ) ]
        player.aspects[0].addMultiple( speed, yaw, pitch )

        # Create Enemy Spawns
        for i in range(0,10):
            x = random.randrange(-5000, 5000)
            y = random.randrange(-500,2500)
            z = random.randrange(-5000, 5000)
            created = self.engine.entityMgr.createEnt(ent.EnemyJet, player.pos + Vector3(x,y,z), 0, 755)
            i = random.randint(1,2)
            x = random.randint(125, 175) * (-1)**i
            y = random.randrange(50,100)
            i = random.randint(1,2)
            z = random.randrange(125, 175) * (-1)**i
            created.follow( player, Vector3(x,y,z) )

        import time

        # Set UI Elements


    def tick(self, dt):
        # Check for level complete?
        # Update Enemy Spawn List?
        pass

    def stop(self):
        pass

