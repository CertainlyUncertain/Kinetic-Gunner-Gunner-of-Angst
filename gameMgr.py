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

# Game Manager --------------------------------------------------------------- #

from vector import Vector3
from spawning import *
from expression import Expression
import ent

class GameMgr:
    ''' Class that manages Game Related Variables and Actions. '''
    
    def __init__(self, engine):
        ''' Creation. '''
        self.engine = engine
        # Game Variables
        self.playing = False
        self.mouseWasDown = False
        self.score = 0
        self.levelTimer = 100
        self.levelDuration = 100
        self.levels = []
        self.currentLevel = 1
        self.lastLevel = 2
        self.spawns = []
        self.spawnIndex = 0
        # Weapon Variables
        self.primaryWeapon = self.weapon1
        self.secondaryWeapon = self.weapon2
        self.weaponCooldown = 0.0
        self.weaponHeat = 0
        self.weaponMaxHeat = 100
        self.weaponCoolingSpeed = 20
        print "Game Manager Created."
        
    def init(self):
        ''' Initialization. '''
        self.levels = [ self.level1, self.level2, self.level3 ]
        print "Game Manager Initialized."
        
    def crosslink(self):
        ''' Links to other Managers. '''
        self.loadLevel()
        print "Game Manager Linked."

    def tick(self, dt):
        ''' Update Function. '''
        if self.playing:
            if self.engine.entityMgr.player.health <= 0:
                self.levelEnd(False)
            else:
                # Check for level complete
                if self.levelTimer < 0:
                    self.levelEnd( True )
                else:
                    self.levelTimer -= dt
                    # Overheating
                    self.weaponHeat -= self.weaponCoolingSpeed * dt
                    if self.weaponHeat < 0:
                        self.weaponHeat = 0
                    # Firing Cooldown
                    if self.weaponCooldown > 0:
                        self.weaponCooldown -= dt
                    else:
                        if self.engine.inputMgr.MB_Left_Down:
                            self.primaryWeapon()
                        elif self.engine.inputMgr.MB_Right_Down:
                            self.secondaryWeapon()
                    # Update Enemy Spawn List
                    if self.spawns[self.spawnIndex].tick(dt):
                        self.spawns[self.spawnIndex].spawn(self.engine.entityMgr)
                        self.spawnIndex = (self.spawnIndex + 1) % len(self.spawns)
        else:
            if self.engine.inputMgr.MB_Left_Down and not self.mouseWasDown:
                # Do stuff
                self.loadLevel()
        # Save Previous Mouse State
        self.mouseWasDown = self.engine.inputMgr.MB_Left_Down

    def stop(self):
        ''' Shut Down. '''
        print "Game Manager Stopped."
        pass
        
# Game Manager --------------------------------------------------------------- #

    def weapon1(self):
        ''' Single Target Laser. '''
        if (self.weaponHeat + 15) < self.weaponMaxHeat:
            mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(0.5, 0.5)
            targ = None
            for eid, ent in self.engine.entityMgr.enemies.iteritems():
                result  =  mouseRay.intersects(ent.renderer.oEnt.getWorldBoundingBox()) #ent.getBoundingBox()
                if result.first:
                    if not targ:
                        targ = ent
                        min = result.second
                    else:
                        if result.second < min:
                            targ = ent
                            min = result.second

            for eid, ent in self.engine.entityMgr.missiles.iteritems():
                result  =  mouseRay.intersects(ent.renderer.oEnt.getWorldBoundingBox()) #ent.getBoundingBox()
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
                self.score += targ.damage( 25 )
            self.engine.sndMgr.playSound(self.engine.sndMgr.laser)
            self.weaponHeat += 15
            self.weaponCooldown = 0.5
            self.engine.gfxMgr.showLaser(True)

    def weapon2(self):
        ''' Piercing Laser. '''
        if (self.weaponHeat + 35) < self.weaponMaxHeat:
            mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(0.5, 0.5)
            for eid, ent in self.engine.entityMgr.enemies.iteritems():
                result  =  mouseRay.intersects(ent.renderer.oEnt.getWorldBoundingBox()) #ent.getBoundingBox()
                if result.first:
                    print "Direct Hit! on " + ent.uiname
                    self.score += ent.damage( 25 )
            for eid, ent in self.engine.entityMgr.missiles.iteritems():
                result  =  mouseRay.intersects(ent.renderer.oEnt.getWorldBoundingBox()) #ent.getBoundingBox()
                if result.first:
                    print "Direct Hit! on " + ent.uiname
                    self.score += ent.damage( 25 )
            self.engine.sndMgr.playSound(self.engine.sndMgr.laser)
            self.weaponHeat += 35
            self.weaponCooldown = 1.0
            self.engine.gfxMgr.showLaser(False)
                
    def weapon3(self):
        ''' Pinpoint Laser. '''
        raySceneQuery = self.engine.gfxMgr.sceneManager.createRayQuery(ogre.Ray())
        raySceneQuery.setSortByDistance( True )
        raySceneQuery.setRay(targetRay)

        result = raySceneQuery.execute()
        if len(result) > 0:
            for item in result:
                if item.movable:
                    print item.movable.getName()
        self.engine.gfxMgr.sceneManager.destroyQuery(raySceneQuery)
        self.engine.sndMgr.playSound(self.engine.sndMgr.laser)
        self.weaponHeat += 15
        self.weaponCooldown = 0.333

    def switchWeapon(self, num, primary = True):
        ''' Weapon Selection. '''
        if num == 3:
            if primary:
                self.primaryWeapon = self.weapon3
            else:
                self.secondaryWeapon = self.weapon3
        elif num == 2:
            if primary:
                self.primaryWeapon = self.weapon2
            else:
                self.secondaryWeapon = self.weapon2
        else:
            if primary:
                self.primaryWeapon = self.weapon1
            else:
                self.secondaryWeapon = self.weapon1
        
    def loadLevel(self):
        ''' Load Current Level. '''
        self.levels[self.currentLevel-1]()
        self.playing = True
        self.engine.overlayMgr.hideSplash()

    def levelEnd(self, victory = False ):
        ''' End of Level. (Victory/Defeat) '''
        self.playing = False
        # if Victory:
        if victory:
            # Display Victory Score Screen
            self.engine.overlayMgr.showVictorySplash()
            #self.engine.sndMgr.playMusic( "bg1.wav" )
            self.currentLevel += 1
            # Check for last level?
            if self.currentLevel > self.lastLevel:
                self.currentLevel = 1
        # else: Defeat
        else:
            # Display Defeat Score Screen
            self.engine.overlayMgr.showDefeatSplash()
            self.engine.sndMgr.playMusic( "bg1.wav" )
        # Clear Scene & Entity Manager
        self.engine.camMgr.clear()
        self.engine.entityMgr.clear()
        self.engine.gfxMgr.clearScene()
        
    def level1(self):
        ''' First Level Loading Function. '''
        # Create Player
        player = self.engine.entityMgr.createPlayer(ent.PlayerJet, Vector3(12500,900,12500), 0, 750)
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 5 ), Expression( -90, 3 ), Expression( 0, 3 ), Expression( -180, 5 ), Expression( -270, 6 ), Expression( 0, 2 ),
                Expression( -90, 3 ), Expression( 0, 2 ), Expression( 90, 3 ), Expression( 270, 5 ), Expression( 0, 2 ), Expression( -90, 3 ) ]
        pitch = [ Expression( 0, 5 ), Expression( 30, 3 ), Expression( -60, 6 ), Expression( 30, 3 ),
                    Expression( 0, 5 ), Expression( -15, 2 ), Expression( 30, 4 ), Expression( -15, 2 ) ]
        player.pathing.setMultiple( speed, yaw, pitch )
            
        self.spawns = [ SpawnCycle( [SpawnGroup(ent.EnemyJet, 1)], 10), SpawnCycle( [SpawnGroup(ent.EnemyJet, 2)], 15),
                        SpawnCycle( [SpawnGroup(ent.EnemyJet, 1)], 5), SpawnCycle( [SpawnGroup(ent.EnemyJet, 1)], 5)]
        self.levelDuration = 120
        self.levelTimer = self.levelDuration
        # Create Terrain
        self.engine.gfxMgr.setupScene1()
        # Set BGM
        self.engine.sndMgr.playMusic( "bg2.wav" )

    def level2(self):
        ''' Second Level Loading Function. '''
        # Create Player
        player = self.engine.entityMgr.createPlayer(ent.PlayerJet, Vector3(12500,1250,12500), 0, 750)
        # Add Commands
        speed = []
        yaw = [ Expression( 0, 5 ), Expression( 90, 3 ), Expression( 0, 3 ), Expression( 180, 5 ), Expression( 270, 6 ), Expression( 0, 2 ),
                Expression( 90, 3 ), Expression( 0, 2 ), Expression( -90, 3 ), Expression( -270, 5 ), Expression( 0, 2 ), Expression( 90, 3 ) ]
        pitch = [ Expression( 0, 5 ), Expression( 25, 4 ), Expression( -50, 8 ), Expression( 25, 4 ),
                    Expression( 0, 5 ), Expression( -15, 3 ), Expression( 30, 6 ), Expression( -15, 3 ) ]
        player.pathing.setMultiple( speed, yaw, pitch )
            
        self.spawns = [ SpawnCycle( [SpawnGroup(ent.EnemyJet, 2)], 10), SpawnCycle( [SpawnGroup(ent.EnemyJet, 3)], 15),
                        SpawnCycle( [SpawnGroup(ent.EnemyJet, 4)], 20), SpawnCycle( [SpawnGroup(ent.EnemyJet, 1)], 10) ]
        self.levelDuration = 150
        self.levelTimer = self.levelDuration
        # Create Terrain
        self.engine.gfxMgr.setupScene2()
        # Set BGM
        self.engine.sndMgr.playMusic( "bg2.wav" )

    def level3(self):
        ''' Third Level Loading Function. '''
        pass

# Game Manager --------------------------------------------------------------- #
