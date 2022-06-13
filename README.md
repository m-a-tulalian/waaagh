# waaagh
USER MANUAL

DISCLAIMER!!	
  This program (The Defensive Siege Battle AI: Waaagh!) is in no way associated with Creative Assembly or Games Workshop. This software was created solely for educational reasons, with no intention of exploiting the game in any manner. By clicking Okay, you agree that the software may change and/or manage your game selections, as well as manipulate your mouse and keyboard operations to some extent.
  
What is “The Defensive Siege AI: Waaagh!”?
  The Defensive Siege AI: Waaagh! or Waaagh! is a bot that aims to emulate a player by controlling the user's soldiers in a defensive siege fight using keyboard and mouse inputs. The AI's goal is to alleviate the player's stress and win the defensive siege battle. The researchers built the project on the Python language (Python 3.9 as of June 2022) with elements of the tkinter module for the user interface and pyautogui for image recognition and gathering visual data.

Features
- Game Detector
    - this module is responsible for detecting the pre-requisite game Total War: Warhammer II.
- Uniform Settings Failsafe Module
		- is a module that checks and modifies settings so that the program uses fewer resources to find more values. 
-	Tactician Trait Module
		- is a module that checks each of the player's units to assign specific roles that the commander trait uses.
- 	Commander Trait Module
		- is a module that positions units in strategic points depending on the roles given by the tactician trait module.
-	Tracker Trait Module
		- is a module that registers the positions of enemy units to use for attacking and defending.
-	Battle Master Trait Module
		- is a module that constantly checks the battle to know whether or not the player is losing or winning so that it sends new instructions to the players units

Instructions (How to use)
-	For the program to detect the game, press the Scan button.
-	Keep pressing the Scan button until the text says that the game has been detected. Once the game is detected the Execute button will become available.
-	To start the program simply press the Execute and wait for the program to finish running (i.e., finishing the battle, whether by defeat or victory).

Important Notes
- Start the game at 1600 x 900 resolution in windowed mode before running the program.
- For an even playing field, disable the offensive spells of both heroes and lords during the battle setup. Defensive spells are the only types of spells allowed.
- Before executing the program, make sure that the unit card details are on. (Is toggled on by pressing the 'I’ hotkey).
-	Start the AI during the deployment phase.
-	Refrain from inputting commands while the AI is running. The AI will do most of the work for you.
-	To stop the program, drag the mouse to the upper left corner of the screen until the program stops moving your mouse.

Error Correction
- In the event the program stops midway, simply exit the program, restart it, and repeat the steps as mentioned in the “how to use” section.
-	If the user chooses to change the values in the behavior menu, please keep in mind that the software is developed with specified default values to achieve optimal performance. Changing the values, for example, does not guarantee victory and is merely a possible solution. 

Program Requirements 
- The program can run on any level of hardware that supports the game.
- The game Total War: Warhammer II is needed for the program to run.
- Windows is the preferred OS for the program.

Credits / Inspirations
- The software is inspired by a similar program named Fate Grand Automata (FGA), a bot for the game Fate/Grand Order on Android and iOS.

