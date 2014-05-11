# Spawning ------------------------------------------------------------------- #

import ent

class SpawnGroup:
    ''' Holds Enemy Type and Count to create. '''
    def __init__(self, enemType, amount ):
        ''' Creation. '''
        self.enemType = enemType
        self.amount = amount
    
class SpawnCycle:
    ''' Holds Groups of Enemies to Create. '''
    def __init__(self, groups, time):
        ''' Creation. '''
        self.groups = groups
        self.time = time
        self.timer = 0
        
    def spawn(self, entMgr):
        ''' Create Entities in each Group. '''
        for group in self.groups:
            for i in range(group.amount):
                entMgr.createEnemy( group.enemType )
        self.timer = 0
                
    def tick(self, dt):
        ''' Update Countdown. '''
        self.timer += dt
        if self.timer > self.time:
            return True
        else:
            return False
            
# Spawning ------------------------------------------------------------------- #