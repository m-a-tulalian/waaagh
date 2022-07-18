from PIL import Image, ImageTk
from pyautogui import *
import pyautogui
import time
import keyboard
import pyscreeze
import random
import sys
import win32api, win32con
import pyKey
from pyKey import pressKey, releaseKey, press, sendSequence, showKeys

global finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX, mapCenterY, mapCenterX, capturePointX, capturePointY, total_units, units, ranged_array, monster_array, infantry_array, lord_card_position_x, lord_card_position_y
# ************************ MAIN ALGO ************************ #
class SimpleMode:
    def __init__(self):
        pass

    def mainTacticianTrait(self, game_Pointx, game_Pointy):
        global finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX, mapCenterY, mapCenterX, capturePointX, capturePointY, total_units, units, lord_card_position_x, lord_card_position_y
        self.mapDrag ()
        self.toggleuniticon ()
        finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX, mapCenterY, mapCenterX = self.get_MapSize ()
        capturePointX, capturePointY = self.get_CapturePointData ( finalMapSizeX, finalMapSizeY, mapCornerX )
        total_units, units = self.unit_Counter ( game_Pointx, game_Pointy, finalMapSizeY, finalMapSizeX, mapCornerX )
        lord_card_position_x, lord_card_position_y = self.get_lord_data ( finalMapSizeY, finalMapSizeX, mapCornerX )

    def mainCommanderTrait(self,mon_values, m_values, i_values):
        global ranged_array, monster_array, infantry_array
        self.place_AllUnitsCapPoint ( capturePointX, capturePointY, total_units, finalMapSizeY, finalMapSizeX,
                                      mapCornerX )
        ranged_array, monster_array, infantry_array = self.commander_placement ( units, mon_values, m_values, i_values,
                                                                                 total_units, finalMapSizeY,
                                                                                 finalMapSizeX,
                                                                                 mapCornerX )
        monster_array.append ( 4 )
        monster_array.append ( 13 )
        self.toggle_GuardMode ( 1 )

    def mainTrackerTrait(self, defense_line, confidence):
        halt = 0
        counter = 0
        halt_counter = 0
        back_unit = 0
        back_unit_far = 0
        enemy_close = self.find_enemy_horizontal_map (
            defense_line, finalMapSizeX, mapCornerY, mapCornerX )
        while enemy_close is False:
            while halt == 0:
                self.enemy_tracker ( finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX )
                enemy_close = self.find_enemy_horizontal_map (
                    defense_line, finalMapSizeX, mapCornerY, mapCornerX )
                if enemy_close is True:
                    if back_unit == 1:
                        press ( key='ENTER', sec=.03 )
                        time.sleep ( .1 )
                        pressKey ( key='CTRL' )
                        for mpos in monster_array:
                            self.click_assigned_unit ( lord_card_position_x, lord_card_position_y, mpos, total_units )
                            time.sleep ( .1 )
                        time.sleep ( .3 )
                        releaseKey ( key='CTRL' )
                        time.sleep ( .5 )
                        self.attack_first_center_area_small ( confidence, finalMapSizeY, finalMapSizeX, mapCornerX )
                        press ( key='ENTER', sec=.03 )
                        time.sleep ( .1 )
                        self.toggle_skills ( lord_card_position_x, lord_card_position_y )
                        time.sleep ( .1 )
                    if back_unit == 6:
                        self.bring_unit_back ( mapCenterX, mapCenterY - 130 )
                    if back_unit == 13:
                        back_unit = 0
                        back_unit_far = 0
                    counter += 1
                    if back_unit_far == 20:
                        self.bring_unit_back ( mapCenterX, mapCenterY - 130 )
                        back_unit_far = 0
                    back_unit += 1
                    back_unit_far += 1
                    if counter == 30:
                        self.toggle_all_fireatwill ()
                    if counter > 160:
                        self.toggle_GuardMode ( 0 )
                        self.attackAll ( confidence, finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX )
                        halt = 1
                halt_counter += 1
                if halt_counter > 250:
                    self.attackAll ( confidence, finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX )
                    halt = 1

    def mainBattleMasterTrait(self, battle_master_bop_adjust_x, battle_master_bop_adjust_y, confidence):
        battle_end = self.battle_master_bop_player ( battle_master_bop_adjust_x, battle_master_bop_adjust_y,
                                                     finalMapSizeX, mapCornerX )
        while battle_end <= 60:
            captured_point = pyautogui.locateOnScreen ( 'RedCapturePoint.png', confidence=0.9, )
            if captured_point is None:
                self.select_AllUnits ()
                self.enemy_tracker ( finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX )
                self.attackAll ( confidence, finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX )
                press ( key='ENTER', sec=.03 )
                time.sleep ( .1 )
                self.toggle_skills ( lord_card_position_x, lord_card_position_y )
                time.sleep ( .1 )
                time.sleep ( 20 )
                battle_end = self.battle_master_bop_player ( battle_master_bop_adjust_x, battle_master_bop_adjust_y,
                                                             finalMapSizeX, mapCornerX )
            if captured_point is not None:
                self.select_AllUnits ()
                self.bring_unit_back ( mapCenterX, mapCenterY - 130 )
                press ( key='ENTER', sec=.03 )
                time.sleep ( .1 )
                self.toggle_skills ( lord_card_position_x, lord_card_position_y )
                time.sleep ( .1 )
                time.sleep ( 20 )

    # SM MAIN #
    def smActive(self, mon_values, m_values, i_values, battle_master_bop_adjust_x, battle_master_bop_adjust_y, defense_line, confidence, game_Pointx , game_Pointy):
        # ** code test order ** #
        # ** INITIALIZATION ** #
        self.mainTacticianTrait(game_Pointx, game_Pointy)
        # ** PREP PHASE ** #
        self.mainCommanderTrait(mon_values, m_values, i_values)
        self.startBattle ()
        # ** BATTLE PHASE ** #
        self.mainTrackerTrait(defense_line, confidence)
        self.mainBattleMasterTrait(battle_master_bop_adjust_x, battle_master_bop_adjust_y, confidence)
        # ** END ** #




    def attackAll(self, confidence, finalMapSizey, finalMapSizex, mapCornery, mapCornerx): #  Selects All Units Then Attacks The First Enemy From The Bottom Of The Screen
        self.select_AllUnits ()
        self.move_to_first_enemy (confidence,finalMapSizey, finalMapSizex, mapCornery, mapCornerx)
        time.sleep(.5)
        self.face_CamDown ( finalMapSizey, finalMapSizex, mapCornerx )
        time.sleep(.5)
        self.attack_first_center_area (finalMapSizey, finalMapSizex, mapCornerx)


    def startBattle(self): # Find And Click The Start Battle Button
        sblocate = pyautogui.locateCenterOnScreen ( 'SB_blue.png', confidence=0.9 )
        time.sleep ( 1 )
        pyautogui.click ( sblocate, clicks=2, interval=0.50 )
        time.sleep ( 1 )


    # CAMERA RELATED METHODS #
    def move_CursorToCenter(self, finalMapSizey, finalMapSizex, mapCornerx): # moves the cursor to the center of the game
        pyautogui.moveTo ( finalMapSizey * 1.5 + (mapCornerx - finalMapSizex), finalMapSizey )


    def mapDrag(self): # Drags Minimap To Maximum Size
        initialMapSize = pyautogui.center (
            pyautogui.locateOnScreen ( 'MapAdjust.png', confidence=0.7, grayscale=True ) )
        while initialMapSize is None:
            initialMapSize = pyautogui.center (
                pyautogui.locateOnScreen ( 'MapAdjust.png', confidence=0.7, grayscale=True ) )
        initialMapSizex, initialMapSizey = initialMapSize
        print ( initialMapSize )
        pyautogui.moveTo ( x=initialMapSizex, y=initialMapSizey)
        pyautogui.dragRel ( -300, 300, duration=1, button='left' )


    def get_MapSize(self): # Get Specific Map Location Values
        finalMapSizeX, finalMapSizeY = pyautogui.center (
            pyautogui.locateOnScreen ( 'MapAdjust.png', confidence=0.7, grayscale=True ) )
        while finalMapSizeX is None and finalMapSizeY is None:
            pyautogui.center (
                pyautogui.locateOnScreen ( 'MapAdjust.png', confidence=0.7, grayscale=True ) )
        mapCornerX, mapCornerY = pyautogui.center (
            pyautogui.locateOnScreen ( 'TacMapButton.png', confidence=0.7, grayscale=True ) )
        while mapCornerX is None and mapCornerY is None:
            mapCornerX, mapCornerY = pyautogui.center (
                pyautogui.locateOnScreen ( 'TacMapButton.png', confidence=0.7, grayscale=True ) )
        mapCenterX = (finalMapSizeX + mapCornerX) / 2
        mapCenterY = (finalMapSizeY + mapCornerY) / 2
        return finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX, mapCenterY, mapCenterX


    def move_To_MapCenter(self, mapCenterx, mapCentery): # Moves Camera To The Center Of The Map
        pyautogui.moveTo ( mapCenterx, mapCentery )
        pyautogui.click ( x=mapCenterx, y=mapCentery, button="left", clicks=2 )


    def rotate_MapTop(self, mapCenterx, mapCentery): # Moves Camera Facing South
        self.move_To_MapCenter ( mapCenterx, mapCentery )
        exitLoop = 0
        camerafailsafe = 0
        while exitLoop != 1:
            im = pyautogui.screenshot ( region=(mapCenterx, mapCentery - 100, 4, 30) )
            for x in range ( 0, 4, 2 ):
                for y in range ( 0, 30, 5 ):
                    r, g, b = im.getpixel ( (x, y) )
                    if r in range ( 30, 50 ) and g in range ( 160, 250 ):
                        exitLoop = 1
                        break
            if exitLoop != 1:
                press ( key='e', sec=.03 )
                time.sleep ( .06 )
                camerafailsafe = camerafailsafe + 1
                if camerafailsafe == 60 or camerafailsafe == 40:
                    self.move_To_MapCenter ( mapCenterx, mapCentery )
            if keyboard.is_pressed ( 'w' ) or keyboard.is_pressed ( 's' ) or keyboard.is_pressed (
                    'a' ) or keyboard.is_pressed (
                    'd' ) or keyboard.is_pressed ( 'q' ) or keyboard.is_pressed ( 'e' ):
                self.move_To_MapCenter ( mapCenterx, mapCentery )
            if camerafailsafe == 50:
                self.options_CameraChange ()


    def rotate_MapBottom(self, mapCenterx, mapCentery): # Moves Camera Facing North
        self.move_To_MapCenter ( mapCenterx, mapCentery )
        exitLoop = 0
        camerafailsafe = 0
        while exitLoop != 1:
            im = pyautogui.screenshot ( region=(mapCenterx, mapCentery + 80, 4, 30) )
            for x in range ( 0, 4, 2 ):
                for y in range ( 0, 30, 5 ):
                    r, g, b = im.getpixel ( (x, y) )
                    if r in range ( 30, 50 ) and g in range ( 160, 250 ):
                        exitLoop = 1
                        break
            if exitLoop != 1:
                press ( key='e', sec=.03 )
                time.sleep ( .06 )
                camerafailsafe = camerafailsafe + 1
                if camerafailsafe == 60 or camerafailsafe == 40:
                    self.move_To_MapCenter ( mapCenterx, mapCentery )
            if keyboard.is_pressed ( 'w' ) or keyboard.is_pressed ( 's' ) or keyboard.is_pressed (
                    'a' ) or keyboard.is_pressed (
                'd' ) or keyboard.is_pressed ( 'q' ) or keyboard.is_pressed ( 'e' ):
                self.move_To_MapCenter ( mapCenterx, mapCentery )
            if camerafailsafe == 50:
                self.options_CameraChange ()


    def options_CameraChange(self): # Goes To Settings And Adjusts Map Option
        press ( key='ESC', sec=.03 )
        time.sleep ( .5 )
        optionsButtonX, optionsButtonY = pyautogui.center (
            pyautogui.locateOnScreen ( 'GameOptionButton.png', confidence=0.7, grayscale=True ) )
        pyautogui.moveTo ( optionsButtonX, optionsButtonY )
        pyautogui.click ( x=optionsButtonX, y=optionsButtonY, button="left", clicks=1 )
        time.sleep ( .5 )
        controlsButtonX, controlsButtonY = pyautogui.center (
            pyautogui.locateOnScreen ( 'GameOptionControlsButton.png', confidence=0.7, grayscale=True ) )
        pyautogui.moveTo ( controlsButtonX, controlsButtonY )
        pyautogui.click ( x=controlsButtonX, y=controlsButtonY, button="left", clicks=1 )
        time.sleep ( .5 )
        standardCameraX, standardCameraY = pyautogui.center (
            pyautogui.locateOnScreen ( 'GameOptionStandardCamera.png', confidence=0.7, grayscale=True ) )
        pyautogui.moveTo ( standardCameraX, standardCameraY )
        pyautogui.click ( x=standardCameraX, y=standardCameraY, button="left", clicks=1 )
        time.sleep ( .5 )
        confirmOptionsX, confirmOptionsY = pyautogui.center (
            pyautogui.locateOnScreen ( 'GameOptionsConfirm.png', confidence=0.7, grayscale=True ) )
        pyautogui.moveTo ( confirmOptionsX, confirmOptionsY )
        pyautogui.click ( x=confirmOptionsX, y=confirmOptionsY, button="left", clicks=1 )
        time.sleep ( .5 )
        press ( key='ESC', sec=.03 )
        time.sleep ( .5 )
        press ( key='ESC', sec=.03 )
        time.sleep ( .5 )
        press ( key='V', sec=.5 )


    def rotate_MapLeft(self, mapCenterx, mapCentery): # Moves Camera Facing West
        exitLoop = 0
        camerafailsafe = 0
        while exitLoop != 1:
            im = pyautogui.screenshot ( region=(mapCenterx - 100, mapCentery, 30, 4) )
            for x in range ( 0, 30, 2 ):
                for y in range ( 0, 4, 5 ):
                    r, g, b = im.getpixel ( (x, y) )
                    if r in range ( 30, 50 ) and g in range ( 160, 250 ):
                        exitLoop = 1
                        break
            if exitLoop != 1:
                press ( key='e', sec=.03 )
                time.sleep ( .06 )
                camerafailsafe = camerafailsafe + 1
                if camerafailsafe == 60 or camerafailsafe == 40:
                    self.move_To_MapCenter ( mapCenterx, mapCentery )
            if keyboard.is_pressed ( 'w' ) or keyboard.is_pressed ( 's' ) or keyboard.is_pressed (
                    'a' ) or keyboard.is_pressed (
                    'd' ) or keyboard.is_pressed ( 'q' ) or keyboard.is_pressed ( 'e' ):
                self.move_To_MapCenter ( mapCenterx, mapCentery )
            if camerafailsafe == 50:
                self.options_CameraChange ()


    def rotate_MapRight(self, mapCenterx, mapCentery):# Moves Camera Facing East
        exitLoop = 0
        camerafailsafe = 0
        while exitLoop != 1:
            im = pyautogui.screenshot ( region=(mapCenterx + 80, mapCentery, 30, 4) )
            for x in range ( 0, 30, 2 ):
                for y in range ( 0, 4, 5 ):
                    r, g, b = im.getpixel ( (x, y) )
                    if r in range ( 30, 50 ) and g in range ( 160, 250 ):
                        exitLoop = 1
                        break
            if exitLoop != 1:
                press ( key='e', sec=.03 )
                time.sleep ( .06 )
                camerafailsafe = camerafailsafe + 1
                if camerafailsafe == 60 or camerafailsafe == 40:
                    self.move_To_MapCenter ( mapCenterx, mapCentery )
            if keyboard.is_pressed ( 'w' ) or keyboard.is_pressed ( 's' ) or keyboard.is_pressed (
                    'a' ) or keyboard.is_pressed (
                    'd' ) or keyboard.is_pressed ( 'q' ) or keyboard.is_pressed ( 'e' ):
                self.move_To_MapCenter ( mapCenterx, mapCentery )
            if camerafailsafe == 50:
                self.options_CameraChange ()


    def face_CamDown(self, finalMapSizey, finalMapSizex, mapCornerx): # Faces Camera Down
        center_x, center_y = self.get_center_point (finalMapSizey, finalMapSizex, mapCornerx)
        pyautogui.moveTo ( center_x, center_y )
        pyautogui.dragRel ( 0, +70, duration=.3, button='middle' )


    def get_CapturePointData(self, finalMapSizex, finalMapSizey, mapCornerx): # Gathers Capture Point Location Value
        press ( key='TAB', sec=.03 )
        time.sleep ( .5 )
        pyautogui.moveTo ( finalMapSizex, finalMapSizey )
        time.sleep ( .3 )
        pyautogui.dragRel ( -300, -300, duration=.2, button='middle' )
        time.sleep ( .3 )
        capturePointX, capturePointY = pyautogui.center (
            pyautogui.locateOnScreen ( 'MapCapturePoint.png', confidence=0.6, grayscale=True,
                                       region=(
                                           mapCornerx - finalMapSizex, finalMapSizey,
                                           finalMapSizex,
                                           (finalMapSizey + finalMapSizey)) ) )
        press ( key='TAB', sec=.03 )
        return capturePointX, capturePointY


    def get_center_point(self, finalMapSizey, finalMapSizex, mapCornerx): # Calculate The Center Point
        center_x = finalMapSizey * 1.1 + (mapCornerx - finalMapSizex)
        center_y = finalMapSizey
        return center_x, center_y


    def get_LordIconData(self,finalMapSizey, finalMapSizex, mapCornerx): # Gets Lord Icon Location Value
        lordIcon = pyautogui.locateOnScreen ( 'LordIcon.png', confidence=0.9, region=(
            mapCornerx - finalMapSizex, finalMapSizey, finalMapSizex, finalMapSizey + 100) )
        while lordIcon is None:
            lordIcon = pyautogui.locateOnScreen ( 'LordIcon.png', confidence=0.9, region=(
                mapCornerx - finalMapSizex, finalMapSizey, finalMapSizex, finalMapSizey + 100) )
        lordIconX, lordIconY = pyautogui.center ( lordIcon )
        return lordIconX, lordIconY


    def battle_master_bop(self, battle_master_bop_adjust_x, battle_master_bop_adjust_y, finalMapSizex,  mapCornerx): # Calculates If The Player Is Winning Or Losing
        spell_browserx, spell_browsery = pyautogui.center (
            pyautogui.locateOnScreen ( 'SpellBrowser.png', confidence=.8, grayscale=True ) )
        balace_of_power = (mapCornerx - ((mapCornerx - finalMapSizex) * 3)) + ((mapCornerx - finalMapSizex) / 2.3)
        playerBOP, enemyBOP = 0, 0
        area = (mapCornerx - finalMapSizex) / 2.5
        im = pyautogui.screenshot ( region=(
            int ( balace_of_power ) + battle_master_bop_adjust_x, spell_browsery + battle_master_bop_adjust_y,
            int ( area ),
            1) )
        for x in range ( int ( area ) ):
            for y in range ( 1 ):
                r, g, b = im.getpixel ( (x, y) )
                if r in range ( 121, 230 ) and g in range ( 89, 160 ) and b in range ( 15, 30 ):
                    playerBOP += 1
                    if playerBOP == 1:
                        pyautogui.moveTo ( int ( balace_of_power ) + battle_master_bop_adjust_x + x,
                                           spell_browsery + battle_master_bop_adjust_y + y )
                elif r in range ( 123, 230 ) and g in range ( 38, 60 ) and b in range ( 20, 30 ):
                    enemyBOP += 1
        if playerBOP >= enemyBOP:
            return True
        else:
            return False


    def battle_master_bop_player(self, battle_master_bop_adjust_x, battle_master_bop_adjust_y, finalMapSizex, mapCornerx): # Calculates how much the player is winning by

        spell_browserx, spell_browsery = pyautogui.center (
            pyautogui.locateOnScreen ( 'SpellBrowser.png', confidence=.8, grayscale=True ) )
        balace_of_power = (mapCornerx - ((mapCornerx - finalMapSizex) * 3)) + ((mapCornerx - finalMapSizex) / 2.3)
        playerBOP = 0
        area = (mapCornerx - finalMapSizex) / 2.5
        im = pyautogui.screenshot ( region=(
            int ( balace_of_power ) + battle_master_bop_adjust_x, spell_browsery + battle_master_bop_adjust_y,
            int ( area ),
            1) )
        for x in range ( int ( area ) ):
            for y in range ( 1 ):
                r, g, b = im.getpixel ( (x, y) )
                if r in range ( 121, 230 ) and g in range ( 89, 160 ) and b in range ( 15, 30 ):
                    playerBOP += 1
        return playerBOP


    def get_center_area(self, finalMapSizey, finalMapSizex, mapCornerx): # Gets Specific Calculation Values
        normalsize = (mapCornerx - finalMapSizex)
        halfsize = (normalsize / 2)
        quartersize = (halfsize / 2)
        attackstartx = finalMapSizex - (normalsize + (halfsize * 3) + quartersize)
        attacksizex = ((normalsize * 2) + (quartersize * 3)) - 30
        attacksizey = ((halfsize + quartersize) * 2.5)
        attackstarty = finalMapSizey - halfsize - 190
        return attackstartx, attackstarty, attacksizex, attacksizey


    def get_center_area_small(self,finalMapSizey, finalMapSizex, mapCornerx): # Gets Specific Calculation Values
        normalsize = (mapCornerx - finalMapSizex)
        halfsize = (normalsize / 2)
        quartersize = (halfsize / 2)
        attackstartx = finalMapSizex - (normalsize + (halfsize * 3) + quartersize)
        attacksizex = ((normalsize * 2) + (quartersize * 3)) - 30
        attacksizey = quartersize + 30
        attackstarty = finalMapSizey + halfsize + quartersize - 60
        return attackstartx, attackstarty, attacksizex, attacksizey


    def attack_first_center_area(self, finalMapSizey, finalMapSizex, mapCornerx): # Attacks First Enemy On The Screen Starting From Bottom
        middle_x, middle_y, area_x, area_y = self.get_center_area (finalMapSizey, finalMapSizex, mapCornerx)
        one_pass = 0
        im = pyautogui.screenshot ( region=(middle_x, middle_y, area_x, area_y) )
        for y in reversed ( range ( 0, int ( area_y ), 2 ) ):
            for x in range ( int ( area_x ) ):
                r, g, b = im.getpixel ( (x, y) )
                if one_pass == 0:
                    if r in range ( 135, 242 ) and g in range ( 15, 29 ) and b in range ( 2, 8 ):
                        pyautogui.moveTo ( middle_x + x, middle_y + y )
                        time.sleep ( .1 )
                        pyautogui.click ( button='right' )
                        one_pass = 1


    def attack_first_center_area_small(self, confidence, finalMapSizey, finalMapSizex, mapCornerx): # Attacks First Enemy On The Screen Starting From Bottom But In A Smaller Radius So That Player Units Does Not Go Too Far From The Defensive Line
        r_conf, g_conf, b_conf = confidence
        middle_x, middle_y, area_x, area_y = self.get_center_area_small (finalMapSizey, finalMapSizex, mapCornerx)
        one_pass = 0
        im = pyautogui.screenshot ( region=(middle_x, middle_y, area_x, area_y) )
        for y in reversed ( range ( int ( area_y ) ) ):
            for x in range ( int ( area_x ) ):
                r, g, b = im.getpixel ( (x, y) )
                if one_pass == 0:
                    if r in range ( r_conf, 242 ) and g in range ( g_conf, 29 ) and b in range ( b_conf, 5 ):
                        pyautogui.moveTo ( middle_x + x, middle_y + y )
                        time.sleep ( .1 )
                        pyautogui.click ( button='right' )
                        one_pass = 1


    def find_all_enemy_map(self, finalMapSizey, finalMapSizex, mapCornery, mapCornerx): # Searches For All Enemy Units On The Map
        area_x = mapCornerx - finalMapSizex
        area_y = finalMapSizey - mapCornery
        enemy_location = []
        im = pyautogui.screenshot ( region=(finalMapSizex, mapCornery, area_x, area_y) )
        for y in range ( 0, int ( area_y ), 4 ):
            for x in range ( 0, int ( area_x ), 2 ):
                r, g, b = im.getpixel ( (x, y) )
                if r in range ( 147, 184 ) and g in range ( 15, 20 ) and b in range ( 0, 5 ):
                    enemy_location.append ( [finalMapSizex + x, mapCornery + y] )
        return enemy_location


    def find_first_enemy_map(self, confidence, finalMapSizey, finalMapSizex, mapCornery, mapCornerx): # Searches For The First Enemy Unit On The Map Starting From Top
        r_conf, g_conf, b_conf = confidence
        area_x = mapCornerx - finalMapSizex
        area_y = finalMapSizey - mapCornery
        first_enemy = None
        im = pyautogui.screenshot ( region=(finalMapSizex, mapCornery, area_x, area_y) )
        for y in range ( 0, int ( area_y ), 4 ):
            for x in range ( 0, int ( area_x ), 2 ):
                r, g, b = im.getpixel ( (x, y) )
                if r in range ( r_conf, 242 ) and g in range ( g_conf, 29 ) and b in range ( b_conf, 5 ):
                    if first_enemy is None:
                        first_enemy = [finalMapSizex + x, mapCornery + y]
                    if first_enemy is not None:
                        continue
        return first_enemy


    def move_to_first_enemy(self, confidence , finalMapSizey, finalMapSizex, mapCornery, mapCornerx): # Moves To The First Enemy Found On The Map
        first_enemy_found = self.find_first_enemy_map (confidence ,finalMapSizey, finalMapSizex, mapCornery, mapCornerx)
        pyautogui.moveTo ( first_enemy_found )
        time.sleep ( .2 )
        pyautogui.click ( button='left', clicks=2 )


    def find_enemy_horizontal_map(self, defense_line=0, finalMapSizex=None, mapCornery=None, mapCornerx=None): # Searches Horizontally For The First Enemy Unit On The Map Near Capture Point
        area_x = mapCornerx - finalMapSizex
        adjusted_y = defense_line + mapCornery + 50
        one_pass = 0
        im = pyautogui.screenshot ( region=(finalMapSizex, adjusted_y, area_x, 30) )
        for y in range ( 0, 30, 1 ):
            for x in range ( 0, int ( area_x ), 2 ):
                r, g, b = im.getpixel ( (x, y) )
                if one_pass == 0:
                    if r in range ( 147, 184 ) and g in range ( 15, 20 ) and b in range ( 0, 5 ):
                        pyautogui.moveTo ( finalMapSizex + x, adjusted_y + y )
                        time.sleep ( .2 )
                        pyautogui.click ( button='left', clicks=2 )
                        one_pass = 1
                        return True
        if one_pass == 0:
            return False


    def enemy_tracker(self, finalMapSizey, finalMapSizex, mapCornery, mapCornerx): # Searches For All Enemy Units On The Map
        enemies = self.find_all_enemy_map ( finalMapSizey, finalMapSizex, mapCornery, mapCornerx)
        for enemy in enemies:
            pyautogui.moveTo ( enemy )


    # UNIT SELECTION METHODS #
    def lord_Selected(self, finalMapSizey, finalMapSizex, mapCornerx): # Checks If The Lord Is Selected
        lordIconX, lordIconY = self.get_LordIconData (finalMapSizey, finalMapSizex, mapCornerx)
        im = pyautogui.screenshot ( region=(lordIconX, lordIconY, 26, 2) )
        r, g, b = im.getpixel ( (25, 1) )
        if r in range ( 39, 47 ) and g in range ( 220, 234 ) and b in range ( 215, 225 ):
            return 2
        else:
            return 1


    def toggleuniticon(self): # Checks And Toggles Unit Icons
        pressKey ( 'SPACEBAR' )
        time.sleep ( 1 )
        showIconsX, showIconsY = pyautogui.center (
            pyautogui.locateOnScreen ( 'ToggleUnitIcons.png', confidence=0.7, grayscale=True ) )
        unitIconsX, unitIconsY = pyautogui.center (
            pyautogui.locateOnScreen ( 'UnitIcons.png', confidence=0.9, grayscale=True ) )
        if showIconsX and unitIconsY is not None:
            im = pyautogui.screenshot ( region=(showIconsX, unitIconsY, 1, 1) )
            r, g, b = im.getpixel ( (0, 0) )
            # unactivated color 31 , 28 ,25
            if r in range ( 30, 32 ) and g in range ( 27, 29 ) and b in range ( 24, 26 ):
                pyautogui.moveTo ( showIconsX, unitIconsY )
                pyautogui.click ( x=showIconsX, y=unitIconsY, button="left", clicks=1 )
        releaseKey ( 'SPACEBAR' )


    def select_AllUnits(self): # Selects All Units
        pressKey ( 'CTRL' )
        pressKey ( 'A' )
        time.sleep ( .3 )
        releaseKey ( 'CTRL' )
        releaseKey ( 'A' )


    def rotate_UnitLeft(self): # Rotates Selected Unit To The Counter Clockwise
        pressKey ( 'CTRL' )
        press ( key='LEFT', sec=.03 )
        releaseKey ( 'CTRL' )
        time.sleep ( 0.5 )


    def rotate_UnitRight(self): # Rotates Selected Unit To The Clockwise
        pressKey ( 'CTRL' )
        press ( key='RIGHT', sec=.03 )
        releaseKey ( 'CTRL' )
        time.sleep ( 0.5 )


    def add_UnitWidth(self): # Makes The Unit Formation Wider
        pressKey ( 'CTRL' )
        press ( key='UP', sec=.03 )
        releaseKey ( 'CTRL' )
        time.sleep ( 0.5 )


    def minus_UnitWidth(self): # Makes The Unit Formation Less Wide
        pressKey ( 'CTRL' )
        press ( key='DOWN', sec=.03 )
        releaseKey ( 'CTRL' )
        time.sleep ( 0.5 )


    def move_UnitLeft(self): # Moves The Unit One Movement Value To The Left
        press ( key='LEFT', sec=.03 )


    def move_UnitRight(self): # Moves The Unit One Movement Value To The Right
        press ( key='RIGHT', sec=.03 )


    def move_UnitUp(self): # Moves The Unit One Movement Value To The Up
        press ( key='UP', sec=.03 )


    def move_UnitDown(self): # Moves The Unit One Movement Value To The Down
        press ( key='DOWN', sec=.03 )


    def unitPositionUp(self, up): # Moves The Unit To The Up Depending On Values
        for moveup in range ( up ):
            self.move_UnitUp ()
            time.sleep ( .1 )


    def unitPositionDown(self, down): # Moves The Unit To The Down Depending On Values
        for movedown in range ( down ):
            self.move_UnitDown ()
            time.sleep ( .1 )


    def unitPositionRight(self, sideways): # Moves The Unit To The Right Depending On Values
        for moveright in range ( sideways ):
            self.move_UnitRight ()
            time.sleep ( .1 )


    def unitPositionLeft(self, sideways): # Moves The Unit To The Left Depending On Values
        for moveleft in range ( sideways ):
            self.move_UnitLeft ()
            time.sleep ( .1 )


    def unitRotation(self, rotation): # Rotates The Unit Depending On Values
        if rotation >= 0:
            for rotate in range ( rotation ):
                self.rotate_UnitRight ()
                time.sleep ( .1 )
        else:
            for rotate in range ( rotation ):
                self.rotate_UnitLeft ()
                time.sleep ( .1 )


    def unit_Counter(self, menuButtonX,menuButtonY, finalMapSizey, finalMapSizex, mapCornerx): # Assigns Values To The Units
        menuButtonX = menuButtonX - 30
        total_Units = 0
        units = []
        lord = 0
        time.sleep ( .2 )
        press(key='ENTER', sec=.03)
        pyautogui.moveTo ( finalMapSizex , finalMapSizey )
        time.sleep ( .2 )
        while lord != 2:
            press ( key=',', sec=.03 )
            time.sleep ( .1 )
            total_Units = total_Units + 1
            if pyautogui.locateOnScreen ( 'MonsterUnit.png', confidence=0.7,
                                          region=(menuButtonX, menuButtonY, 600, 600) ):
                units.append ( "Monster" )
            elif pyautogui.locateOnScreen ( 'MissileUnit.png', confidence=0.7,
                                            region=(menuButtonX, menuButtonY, 600, 600) ):
                units.append ( "Missile" )
            else:
                time.sleep(.1)
                if pyautogui.locateOnScreen ( 'MonsterUnit.png', confidence=0.7,
                                              region=(menuButtonX, menuButtonY, 600, 600) ):
                    units.append ( "Monster" )
                elif pyautogui.locateOnScreen ( 'MissileUnit.png', confidence=0.7,
                                                region=(menuButtonX, menuButtonY, 600, 600) ):
                    units.append ( "Missile" )
                else:
                    time.sleep ( .1 )
                    if pyautogui.locateOnScreen ( 'MonsterUnit.png', confidence=0.7,
                                                  region=(menuButtonX, menuButtonY, 600, 600) ):
                        units.append ( "Monster" )
                    elif pyautogui.locateOnScreen ( 'MissileUnit.png', confidence=0.7,
                                                    region=(menuButtonX, menuButtonY, 600, 600) ):
                        units.append ( "Missile" )
                    else:
                        time.sleep ( .1 )
                        if pyautogui.locateOnScreen ( 'MonsterUnit.png', confidence=0.7,
                                                      region=(menuButtonX, menuButtonY, 600, 600) ):
                            units.append ( "Monster" )
                        elif pyautogui.locateOnScreen ( 'MissileUnit.png', confidence=0.7,
                                                        region=(menuButtonX, menuButtonY, 600, 600) ):
                            units.append ( "Missile" )
                        else:
                            time.sleep ( .1 )
                            if pyautogui.locateOnScreen ( 'MonsterUnit.png', confidence=0.7,
                                                          region=(menuButtonX, menuButtonY, 600, 600) ):
                                units.append ( "Monster" )
                            elif pyautogui.locateOnScreen ( 'MissileUnit.png', confidence=0.7,
                                                            region=(menuButtonX, menuButtonY, 600, 600) ):
                                units.append ( "Missile" )
                            else:
                                units.append ( "Melee" )
            lord = self.lord_Selected (finalMapSizey, finalMapSizex, mapCornerx)
        return total_Units, units


    def place_AllUnitsCenter(self, finalMapSizey, finalMapSizex, mapCornerx): # Places All Units To The Center Of The Map
        self.select_AllUnits ()
        time.sleep ( .5 )
        center_x, center_y = self.get_center_point (finalMapSizey, finalMapSizex, mapCornerx)
        press ( key='TAB', sec=.03 )
        time.sleep ( .7 )
        pyautogui.dragRel ( -300, -300, duration=.2, button='middle' )
        time.sleep ( .3 )
        pyautogui.moveTo ( center_x, center_y )
        pressKey ( key='ALT' )
        pyautogui.dragRel ( 0, -150, duration=.2, button='right' )
        releaseKey ( key='ALT' )
        press ( key='TAB', sec=.03 )
        time.sleep ( .7 )
        pyautogui.click ( button='left' )
        time.sleep ( .5 )


    def place_AllUnitsCapPoint(self, capturePointX, capturePointY, total_units, mapY, mapX, mapCornerx): # Places All Units To The Capture Point
        time.sleep ( .5 )
        x = 1
        time.sleep ( .5 )
        self.place_AllUnitsCenter (mapY, mapX, mapCornerx)
        time.sleep ( 1 )
        press ( key='TAB', sec=.03 )
        time.sleep ( .7 )
        pyautogui.dragRel ( -150, -150, duration=.2, button='middle' )
        time.sleep ( .3 )
        pyautogui.dragRel ( -150, -150, duration=.2, button='middle' )
        time.sleep ( .3 )
        while (x != (total_units + 1)):
            press ( key=',', sec=.03 )
            time.sleep ( .2 )
            pyautogui.moveTo ( capturePointX, capturePointY - 30 )
            time.sleep ( .2 )
            pyautogui.click ( button="right" )
            x = x + 1
        self.select_AllUnits ()
        for y in range ( 10 ):
            self.add_UnitWidth ()
        time.sleep ( .2 )
        press ( key='TAB', sec=.03 )
        time.sleep ( 1 )
        press ( key='ENTER', sec=.3 )

    def toggle_GuardMode(self, skirmish): # Toggles Guard Mode And Skirmish Mode
        self.select_AllUnits ()
        guardModeX, guardModeY = pyautogui.center (
            pyautogui.locateOnScreen ( 'GuardMode.png', confidence=0.7, grayscale=True ) )
        pyautogui.moveTo ( guardModeX, guardModeY )
        time.sleep(.2)
        pyautogui.click ( button="left", clicks=1 )
        time.sleep(.3)
        if skirmish == 1:
            pyautogui.moveTo ( guardModeX + 120, guardModeY )
            time.sleep ( .2 )
            pyautogui.click ( button="left", clicks=1 )
            time.sleep ( .3 )
        press ( key='ENTER', sec=.3 )

    def toggle_skills(self, lord_x, lord_y): # Toggles Lord Skills
        pyautogui.moveTo ( lord_x, lord_y )
        time.sleep ( .2 )
        pyautogui.click ( button="left", clicks=1 )
        time.sleep ( .3 )
        skill_one_x = 90
        skill_one_y = 213
        skill_two_x = 165
        skill_two_y = 187
        skill_three_x = 195
        skill_three_y = 112
        toggle_unit_camera = pyautogui.center (
            pyautogui.locateOnScreen ( 'ToggleUnitCamera.png', confidence=0.7, grayscale=True ) )
        while toggle_unit_camera is None:
            toggle_unit_camera = pyautogui.center (
                pyautogui.locateOnScreen ( 'ToggleUnitCamera.png', confidence=0.7, grayscale=True ) )
        toggle_unit_camera_x, toggle_unit_camera_y = toggle_unit_camera
        pyautogui.moveTo ( toggle_unit_camera_x + skill_one_x, toggle_unit_camera_y - skill_one_y )
        time.sleep ( .1 )
        pyautogui.click ( button="left", clicks=1 )
        time.sleep ( .1 )
        pyautogui.moveTo ( toggle_unit_camera_x + skill_two_x, toggle_unit_camera_y - skill_two_y )
        time.sleep ( .1 )
        pyautogui.click ( button="left", clicks=1 )
        time.sleep ( .1 )
        pyautogui.moveTo ( toggle_unit_camera_x + skill_three_x, toggle_unit_camera_y - skill_three_y )
        time.sleep ( .1 )
        pyautogui.click ( button="left", clicks=1 )
        time.sleep ( .1 )


    def toggle_all_fireatwill(self): # Toggles Fire At Will For All Units
        self.select_AllUnits ()
        guardModeX, guardModeY = pyautogui.center (
            pyautogui.locateOnScreen ( 'GuardMode.png', confidence=0.7, grayscale=True ) )
        pyautogui.moveTo ( guardModeX + 60, guardModeY )
        time.sleep ( .2 )
        pyautogui.click ( button="left", clicks=1 )
        time.sleep ( .3 )
        press(key='ENTER', sec=.03)


    def commander_position_monster(self, placement, mon_up, mon_down, mon_side, mon_rotate): # Positions Monster Units
        self.unitPositionUp ( mon_up )
        self.unitPositionDown ( mon_down )
        if placement == 1:
            self.unitPositionRight ( mon_side )
            placement = 2
        elif placement == 2:
            self.unitPositionLeft ( mon_side )
            placement = 1
        self.unitRotation ( mon_rotate )
        return placement


    def commander_position_missile(self, placement, m_up, m_down, m_side, m_rotate): # Positions Missile Units
        self.unitPositionUp ( m_up )
        self.unitPositionDown ( m_down )
        if placement == 1:
            self.unitPositionRight ( m_side )
            placement = 2
        elif placement == 2:
            self.unitPositionLeft ( m_side )
            placement = 1
        self.unitRotationLine(m_rotate, placement)
        return placement


    def unitRotationLine(self, rotation, line_placement): # Unit Rotations
        if line_placement == 1:
            print ( "went into line 1" )
            if rotation >= 0:
                print ( "rotated right" + str ( rotation ) )
                for rotate in range ( rotation ):
                    self.rotate_UnitRight ()
                    time.sleep ( .2 )
            else:
                rotation = rotation * -1
                for rotate in range ( rotation ):
                    print ( "rotated left" + str ( rotation ) )
                    self.rotate_UnitLeft ()
                    time.sleep ( .2 )
        if line_placement == 2:
            print ( "went into line 2" )
            rotation = rotation * -1
            print ( str ( rotation ) )
            if rotation >= 0:
                for rotate in range ( rotation ):
                    print ( "rotated right" + str ( rotation ) )
                    self.rotate_UnitRight ()
                    time.sleep ( .2 )
            else:
                rotation = rotation * -1
                for rotate in range ( rotation ):
                    print ( "rotated left" + str ( rotation ) )
                    self.rotate_UnitLeft ()
                    time.sleep ( .2 )


    def commander_position_infantry(self, placement, i_up, i_down, i_side, i_rotate): # Positions Infantry Units
        self.unitPositionUp ( i_up )
        self.unitPositionDown ( i_down )
        if placement == 1:
            self.unitPositionRight ( i_side )
            placement = 2
        elif placement == 2:
            self.unitPositionLeft ( i_side )
            placement = 1
        self.unitRotation ( i_rotate )
        return placement


    def commander_placement(self, unit_array, mon_values, m_values, i_values, total_units, finalMapSizey, finalMapSizex, mapCornerx): # Places Units Depending On Assignment
        mon_line = 1
        ranged_array = []
        monster_array = []
        infantry_array = []
        m_line = 1
        i_line = 1
        missile_counter = 0
        monsterup, monsterdown, monstersideways, monsterrotation = mon_values
        missileup, missiledown, missilesideways, missilerotation = m_values
        infantryup, infantrydown, infantrysideways, infantryrotation = i_values
        for x in range ( len ( unit_array ) ):
            unit_Selected = unit_array[x]
            press ( key=',', sec=.03 )
            if 'Monster' in unit_Selected:
                mon_line = self.commander_position_monster ( mon_line, monsterup, monsterdown, monstersideways,
                                                             monsterrotation )
                monster_array.append ( x + 1 )
            elif 'Missile' in unit_Selected:
                m_line = self.commander_position_missile ( m_line, missileup, missiledown, missilesideways,
                                                           missilerotation )
                missile_counter += 1
                ranged_array.append ( x + 1 )
                if missile_counter == 2:
                    missiledown += 3
                    missile_counter = 0
            else:
                i_line = self.commander_position_infantry ( i_line, infantryup, infantrydown, infantrysideways,
                                                            infantryrotation )
                infantry_array.append ( x + 1 )
        time.sleep ( .5 )
        self.battle_efficiency_autofire(ranged_array, total_units, finalMapSizey, finalMapSizex, mapCornerx)
        return ranged_array, monster_array, infantry_array


    def click_assigned_unit(self, x, y, pos, units): # Clicks Assigned Unit
        unit_total = units * 60
        pos_adjusted = unit_total - (pos * 60)
        pyautogui.moveTo ( x + pos_adjusted, y )
        pyautogui.click ( button="left", clicks=1 )


    def toggle_fireatwill(self): # Toggles Fire At Will
        autofire_x, autofire_y = pyautogui.center (
            pyautogui.locateOnScreen ( 'Autofire.png', confidence=0.5, grayscale=True ) )
        while autofire_x is None:
            autofire_x, autofire_y = pyautogui.center (
                pyautogui.locateOnScreen ( 'Autofire.png', confidence=0.5, grayscale=True ) )
        pyautogui.moveTo ( autofire_x, autofire_y )
        time.sleep ( .1 )
        pyautogui.click ( button="left", clicks=1 )
        time.sleep ( .1 )
        press(key='ENTER', sec=.03)


    def bring_unit_back(self, mapx, mapy): # Brings Unit Back To Capture Point
        pyautogui.moveTo ( mapx, mapy )
        time.sleep ( .2 )
        pyautogui.click ( button="right", clicks=1 )


    def battle_efficiency_autofire(self, r_array, units_total,finalMapSizey, finalMapSizex, mapCornerx): # Selects Specific Units To Toggle Fire At Will
        lord_x, lord_y = self.get_LordIconData (finalMapSizey, finalMapSizex, mapCornerx)
        autocounter = 1
        time.sleep ( .05 )
        for x in r_array:
            if autocounter == 3 or autocounter == 4:
                pressKey ( key='CTRL' )
                self.click_assigned_unit ( lord_x, lord_y, x, units_total)
            autocounter += 1
        time.sleep ( .05 )
        releaseKey ( key='CTRL' )
        self.toggle_fireatwill ()


    def get_lord_data(self, finalMapSizey, finalMapSizex, mapCornerx): # Gets Lord Position Data
        lord_x, lord_y = self.get_LordIconData (finalMapSizey, finalMapSizex, mapCornerx)
        return  lord_x,lord_y


        # self.mapDrag()
        # finalMapSizeY, finalMapSizeX, mapCornerY, mapCornerX, mapCenterY, mapCenterX = self.get_MapSize ()
        # self.toggleuniticon ()
        # capturePointX, capturePointY = self.get_CapturePointData ( finalMapSizeX, finalMapSizeY, mapCornerX )
        # total_units, units = self.unit_Counter (game_Pointx, game_Pointy, finalMapSizeY, finalMapSizeX, mapCornerX)