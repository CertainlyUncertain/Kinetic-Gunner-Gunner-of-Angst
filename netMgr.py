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

# Networking Manager --------------------------------------------------------- #

class NetMgr:
    ''' Create networking threads, find clients/servers, sync entities. '''
    
    def __init__(self, engine):
        ''' Creation. '''
        self.engine = engine
        print "Network Manager Created."
        pass

    def init(self):
        ''' Initialization. '''
        print "Network Manager Initialized."
        pass

    def crosslink(self):
        ''' Link to other Managers. '''
        print "Network Manager Linked."
        pass
        
    def tick(self, dt):
        ''' Update. '''
        pass

    def stop(self):
        ''' Shut Down. '''
        print "Network Manager Stopped."
        pass

# Networking Manager --------------------------------------------------------- #