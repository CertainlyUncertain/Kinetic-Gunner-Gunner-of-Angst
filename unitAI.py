# UnitAI --------------------------------------------------------------------- #

import command

class UnitAI:

    def __init__(self, ent):
        ''' Creation. '''
        self.ent = ent
        self.commands = []
        
    def tick(self, dtime):
        if self.commands != []:
            if self.commands[0].tick(dtime):
                self.commands.pop(0)
                    
    def addCommand(self, newCommand):
        ''' Adds to end of Command List. '''
        self.commands.append( newCommand )

    def clearCommands(self):
        ''' Empties Command List. '''
        self.commands = []

    def setCommand(self, newCommand):
        ''' Replaces Command List. '''
        self.clearCommands()
        self.addCommand( newCommand )

# UnitAI --------------------------------------------------------------------- #