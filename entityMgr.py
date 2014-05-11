# ========================== Start Copyright Notice ========================== #
#                                                                              #
#   Copyright 2014 F.D.I.S.                                                    #
#   This file is part of Kinetic Gunner: Gunner of Angst                       #
#                                                                              #
#   For the latest version, please visit:                                      #
#   https://github.com/CertainlyUncertain/Kinetic-Gunner-Gunner-of-Angst       #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public License          #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                              #
# =========================== End Copyright Notice =========================== #

# Entity Manager ------------------------------------------------------------- #

from vector import Vector3
import command

class EntityMgr:
    ''' Creates, manages, and destroys Entities. '''
    
    def __init__(self, engine):
        ''' Creation. '''
        self.engine = engine
        print "Entity Manager Created."
                
    def init(self):
        ''' Initialization. '''
        # Player --------
        self.player = None
        ##self.projectiles = {}
        ##self.nProjs = 0
        # Hostiles ------
        self.enemies = {}
        self.nEnems = 0
        self.missiles = {}
        self.nMissiles = 0
        # Other ---------
        self.dead = []
        import random ##--##
        self.randomizer = random
        self.randomizer.seed(None)
        import ent ##--##
        self.entTypes = [ent.PlayerJet, ent.EnemyJet]
        print "Entity Manager Initialized."

    def crosslink(self):
        ''' Links to other Managers. '''
        print "Entity Manager Linked."
        pass
        
    def tick(self, dt):
        ''' Update Function. '''
        if self.player:
            self.player.tick(dt)
        for eid, ent in self.enemies.iteritems():
            ent.tick(dt)
        for eid, ent in self.missiles.iteritems():
            ent.tick(dt)
        self.cleanup()
        
    def stop(self):
        ''' Shut Down. '''
        print "Entity Manager Stopped."
        pass
        
# Entity Manager ------------------------------------------------------------- #

    def createPlayer(self, playerType, pos, yaw, speed):
        ''' Create the Player's Entity. '''
        self.player = playerType(self.engine, 0, pos, yaw, speed)
        self.player.init()
        self.player.renderer.oEnt.setMaterialName ('Angst/Player')
        return self.player
    
    def createEnemy(self, enemyType, pos = None, speed = None):
        ''' Creates an Enemy Jet Entity. '''
        if pos == None:
            x = self.randomizer.randint(-5000, 5000)
            y = self.randomizer.randint(-500, 2500)
            z = self.randomizer.randint(-5000, 5000)
            pos = self.player.pos + Vector3(x,y,z)
        if speed == None:
            speed = self.player.speed + 10
            
        ent = enemyType(self.engine, self.nEnems, pos, 0, speed)
        ent.init()
        ent.unitai.addCommand( command.OffsetFollow(ent, self.player, self.createRandomOffset()) )
        self.enemies[ent.uiname] = ent;
        self.nEnems = self.nEnems + 1
        ent.renderer.oEnt.setMaterialName ('Angst/Enemy')
        return ent
        
    def createMissile(self, missileType, source):
        ''' Creates an Enemy Missile Entity. '''
        ent = missileType(self.engine, self.nMissiles, source)
        ent.init()
        ent.unitai.addCommand( command.Ram(ent, self.player) )
        self.missiles[ent.uiname] = ent;
        self.nMissiles = self.nMissiles + 1
        ent.renderer.oEnt.setMaterialName ('Angst/Missile')
        return ent
        
    def cleanup(self):
        ''' Deletes Dead Entities. '''
        for ent in self.dead:
            # Get ID
            index = ent.uiname
            # Remove from List
            if index in self.enemies:
                self.enemies.pop(index)
            elif index in self.missiles:
                self.missiles.pop(index)
            # Delete Ent and ogre ent
            node = ent.delete()
            # Recycle Node
            self.engine.gfxMgr.recycleNode(node)
            print 'Enemy Count: ' + str(len(self.enemies))
            print 'Missile Count: ' + str(len(self.missiles))
        # Clear List
        self.dead = []
        
    def clear(self):
        ''' Clears All Entity References. '''
        # Player --------
        self.player = None
        ##self.projectiles = {}
        ##self.nProjs = 0
        # Hostiles ------
        self.enemies = {}
        self.nEnems = 0
        self.missiles = {}
        self.nMissiles = 0
        # Other ---------
        self.dead = []

    def createRandomOffset(self):
        ''' Creates a random 3D offset. '''
        x = self.randomizer.randint(-350, -275)
        y = self.randomizer.randint(75,125)
        i = self.randomizer.randint(1,2)
        z = self.randomizer.randint(275, 350) * (-1)**i
        return Vector3(x,y,z)
        
# Entity Manager ------------------------------------------------------------- #
