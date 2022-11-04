from tkinter import *
from tkinter import messagebox
from pyautogui import *
import pyautogui
import time
from simple_mode import SimpleMode

# **************** .MAIN / TITLE & DIMENSIONS ****************
root = Tk()
root.title('The Defensive Siege Battle AI: Waaagh!')
root.resizable(width=False, height=False)

root_width = 800
root_height = 450

global screen_width, screen_height

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

xroot = (screen_width / 2) - (root_width / 2)
yroot = (screen_height / 2) - (root_height / 2)

root.geometry(f'{root_width}x{root_height}+{int( xroot )}+{int( yroot )}')

# ********************** GUI ICON ************************
icon = PhotoImage(file = "Ork_Symbols.png")
root.iconphoto(False, icon)
# ***************** BACKGROUND IMAGE *****************
bgImage = PhotoImage(file="TWWII_Battle_Skaven.png")
bgLabel = Label(root, image=bgImage)

messagebox.showwarning("WARNING! PLEASE READ IMPORTANT INSTRUCTIONS!","DISCLAIMER: This program (The Defensive Siege Battle AI: Waaagh!) is in no way associated with Creative Assembly or Games Workshop. This software was created solely for educational reasons, with no intention of exploiting the game in any manner. \n\nBy clicking Okay, you agree that the software may change and/or manage your game selections, as well as manipulate your mouse and keyboard operations to some extent. \n\nTo end the program, move the mouse to the upper left corner of the screen and keep it there for a few seconds. \n\nP.S: PLEASE REFRAIN from entering commands during the execution phase so that the program runs smoothly and without errors (e.g. moving the mouse, inputting keyboard keys, etc.) \n\nTo allow the program to operate smoothly, we recommend running the game in 1600x900 resolution in windowed mode. ")
# ***************** GLOBAL VARS. **************************

    # DEFAULT PARAMS:
    # monsterup = 0                 missileup = 1               infantryup = 9
    # monsterdown = 3               missiledown = 0             infantrydown = 0
    # monstersideways = 2           missilesideways = 4         infantrysideways = 6
    # monsterrotation = 0           missilerotation = 2         infantryrotation = 0

# USER INPUT VARIABLE LISTS:
# cmdr trait = monsval_data, misval_data, infval_data
# tracker trait = trkslidery
# battle master trait = bop_adjust_valx, bop_adjust_valy)

global monsval_data
global misval_data
global infval_data
global bop_adjust_valx
global bop_adjust_valy
global trk_get
global confidence_get
global gamePointx , gamePointy
gamePointx = 0
gamePointy = 0
monsval_data = 0, 3, 2, 0
misval_data = 1, 0 ,4 , 2
infval_data = 9, 0, 6, 0
bop_adjust_valx = 0
bop_adjust_valy = 0
trk_get = 5
confidence_get = 147, 15, 0

# ********************* GAME SELECTOR ************************

def GameSelect():
    time.sleep(0.05)

    gameLocator = pyautogui.locateOnScreen('GameLocator.png', confidence=0.9, grayscale=True)
    while gameLocator is None:
        gameLocator = pyautogui.locateOnScreen('GameLocator.png', confidence=0.9, grayscale=True)
    gamePointx, gamePointy = pyautogui.center(gameLocator)
    pyautogui.click(gamePointx, gamePointy, button="left", clicks=1)


# ***************** MAIN MENU FUNCTIONS **********************

def confidence_click():
    confmenu = Toplevel ()
    confmenu.title ( 'Conf. Slider' )

    conf_width = 300
    conf_height = 300

    xconf = (screen_width / 2) - (conf_width / 2)
    yconf = (screen_height / 2) - (conf_height / 2)

    confmenu.geometry ( f'{conf_width}x{conf_height}+{int ( xconf )}+{int ( yconf )}' )

    conficon = PhotoImage ( file="Ork_Symbols.png" )
    confmenu.iconphoto ( False, conficon )
    confmenu.resizable ( False, False )

    def conf_getVal():
        global confidence_get

        r_get = rslider.get()
        g_get = gslider.get()
        b_get = bslider.get()

        confidence_get = int(r_get), int(g_get), int(b_get)


    conflbl = Label(confmenu, text="Adjust Confidence Values:").place(x=10, y=10)

    rlbl = Label ( confmenu, text="RED Value:" ).place( x=10, y=50 )
    rslider = Scale( confmenu, from_=147, to=242, length=150 ,orient=HORIZONTAL )
    rslider.set ( 0 )
    rslider.place (x= 100, y=32 )

    glbl = Label ( confmenu, text="GREEN Value:" ).place ( x=10, y=120 )
    gslider = Scale ( confmenu, from_=15, to=29, length=150, orient=HORIZONTAL )
    gslider.set ( 0 )
    gslider.place ( x=100, y=100 )

    blbl = Label ( confmenu, text="BLUE Value:" ).place ( x=10, y=190 )
    bslider = Scale ( confmenu, from_=0, to=5, length=150, orient=HORIZONTAL )
    bslider.set ( 0 )
    bslider.place ( x=100, y=170 )


    confirmbtn = Button(confmenu, text="Apply Changes", command=conf_getVal, bd=3).place(x=40, y=250)
    Button(confmenu, text="Exit Window", command=confmenu.destroy, bd=3).place(x=180, y=250)

def adj_click():
    adjmenu = Toplevel()
    adjmenu.title('Adjust Position')

    adj_width = 500
    adj_height = 400

    xadj = (screen_width / 2) - (adj_width / 2)
    yadj = (screen_height / 2) - (adj_height / 2)

    adjmenu.geometry ( f'{adj_width}x{adj_height}+{int ( xadj )}+{int ( yadj )}' )

    adjicon = PhotoImage(file="Ork_Symbols.png")
    adjmenu.iconphoto(False, adjicon)
    adjmenu.resizable ( False, False )

    # DEFAULT PARAMS:
    # monsterup = 0                 missileup = 1               infantryup = 9
    # monsterdown = 3               missiledown = 0             infantrydown = 0
    # monstersideways = 2           missilesideways = 4         infantrysideways = 6
    # monsterrotation = 0           missilerotation = 2         infantryrotation = 0

    def intChecker():
        try:
            int(up_entry.get())
            int(down_entry.get())
            int(side_entry.get())
            int(rotate_entry.get())
            missing_lbl = Label ( adjmenu, text="Please fill out all the fields with an eligible number" )
            missing_lbl.place ( x=115, y=285 )
            missing_lbl.after ( 2000, lambda: missing_lbl.place_forget () )
        except ValueError:
            error_lbl = Label ( adjmenu, text="Non-integer value detected! Please enter a valid number" )
            error_lbl.place ( x=95, y=285 )
            error_lbl.after ( 2000, lambda: error_lbl.place_forget () )


    global up_lbl, down_lbl, side_lbl, rotate_lbl
    global up_entry, down_entry, side_entry, rotate_entry

    up_lbl = Label ( adjmenu, text="Default UP position value :" )
    up_lbl.place ( x=40, y=120 )
    up_entry = Entry ( adjmenu, width=10 )
    up_entry.place ( x=50, y=150 )
    up_entry.insert( 0, "0" )

    down_lbl = Label ( adjmenu, text="Default DOWN position value :" )
    down_lbl.place ( x=40, y=220 )
    down_entry = Entry ( adjmenu, width=10 )
    down_entry.place ( x=50, y=250 )
    down_entry.insert ( 0, "0" )

    side_lbl = Label ( adjmenu, text="Default SIDE position value :" )
    side_lbl.place ( x=290, y=120 )
    side_entry = Entry ( adjmenu, width=10 )
    side_entry.place ( x=300, y=150 )
    side_entry.insert( 0, "0")

    rotate_lbl = Label ( adjmenu, text="Default ROTATE position value :" )
    rotate_lbl.place ( x=290, y=220 )
    rotate_entry = Entry ( adjmenu, width=10 )
    rotate_entry.place ( x=300, y=250 )
    rotate_entry.insert ( 0, "0" )

    def storeValue():
        global monsval_data
        global misval_data
        global infval_data

        type_state = utype.get()

        up_get = up_entry.get()
        down_get = down_entry.get()
        side_get = side_entry.get()
        rotate_get = rotate_entry.get()

        # USER INPUT VARIABLE LISTS:
        # monsval_data, misval_data, infval_data

        if (int(type_state) == 1):
            monsval_data = int(up_get),int(down_get), int(side_get), int(rotate_get)
        elif (int(type_state) == 2):
            misval_data = int(up_get),int(down_get), int(side_get), int(rotate_get)
        elif (int(type_state) == 3):
            infval_data = int(up_get),int(down_get), int(side_get), int(rotate_get)
        else:
            print("Did not Work")

    def adj_tcheck_click():
        adj_tcheck_win = Toplevel()
        adj_tcheck_win.title ( 'Type Selection' )

        adj_tcheck_win_width = 250
        adj_tcheck_win_height = 200

        xadj_tcheck_win = (screen_width / 2) - (adj_tcheck_win_width / 2)
        yadj_tcheck_win = (screen_height / 2) - (adj_tcheck_win_height / 2)

        adj_tcheck_win.geometry ( f'{adj_tcheck_win_width}x{adj_tcheck_win_height}+{int ( xadj_tcheck_win )}+{int ( yadj_tcheck_win )}' )

        adj_tcheck_icon = PhotoImage (file="Ork_Symbols.png")
        adj_tcheck_win.iconphoto (False, adj_tcheck_icon)
        adj_tcheck_win.resizable( False, False )

        def adj_tconfirm_click():
            if (utype.get() == 1):
                # -------------- UPDATE LABEL ---------------- #
                up_lbl.config( text="MONSTER UP position value :" )
                up_lbl.place( x=40, y=120 )

                down_lbl.config ( text="MONSTER DOWN position value :" )
                down_lbl.place( x=40, y=220 )

                side_lbl.config ( text="MONSTER SIDE position value :" )
                side_lbl.place( x=290, y=120 )

                rotate_lbl.config ( text="MONSTER ROTATE position value :" )
                rotate_lbl.place ( x=290, y=220 )

                # -------------- UPDATE ENTRY INDEX ---------- #
                up_entry.delete ( 0, 1 )
                up_entry.insert( 0, "0")

                down_entry.delete( 0, 1 )
                down_entry.insert ( 1, "3" )

                side_entry.delete( 0, 1)
                side_entry.insert ( 0, "2" )

                rotate_entry.delete( 0, 1 )
                rotate_entry.insert( 0, "0" )

            elif (utype.get() == 2):
                # -------------- UPDATE LABEL ---------------- #
                up_lbl.config( text="MISSILE UP position value :" )
                up_lbl.place( x=40, y=120 )

                down_lbl.config ( text="MISSILE DOWN position value :" )
                down_lbl.place( x=40, y=220 )

                side_lbl.config ( text="MISSILE SIDE position value :" )
                side_lbl.place( x=290, y=120 )

                rotate_lbl.config ( text="MISSILE ROTATE position value :" )
                rotate_lbl.place ( x=290, y=220 )

                # -------------- UPDATE ENTRY INDEX ---------- #
                up_entry.delete ( 0, 1 )
                up_entry.insert ( 0, "1" )

                down_entry.delete ( 0, 1 )
                down_entry.insert ( 1, "0" )

                side_entry.delete ( 0, 1 )
                side_entry.insert ( 0, "4" )

                rotate_entry.delete ( 0, 1 )
                rotate_entry.insert ( 0, "2" )


            elif (utype.get() == 3):
                # -------------- UPDATE LABEL ---------------- #
                up_lbl.config( text="INFANTRY UP position value :" )
                up_lbl.place( x=40, y=120 )

                down_lbl.config ( text="INFANTRY DOWN position value :" )
                down_lbl.place( x=40, y=220 )

                side_lbl.config ( text="INFANTRY SIDE position value :" )
                side_lbl.place( x=290, y=120 )

                rotate_lbl.config ( text="INFANTRY ROTATE position value :" )
                rotate_lbl.place ( x=290, y=220 )

                # -------------- UPDATE ENTRY INDEX ---------- #
                up_entry.delete ( 0, 1 )
                up_entry.insert ( 0, "9" )

                down_entry.delete ( 0, 1 )
                down_entry.insert ( 1, "0" )

                side_entry.delete ( 0, 1 )
                side_entry.insert ( 0, "6" )

                rotate_entry.delete ( 0, 1 )
                rotate_entry.insert ( 0, "0" )


        global utype
        utype = IntVar ()
        utype.set ( '0' )

        tcheck_rdbtn1 = Radiobutton ( adj_tcheck_win, text="Monsters", variable=utype, value=1 ).pack (pady=5)
        tcheck_rdbtn2 = Radiobutton ( adj_tcheck_win, text="Missle", variable=utype, value=2 ).pack (pady=5)
        tcheck_rdbtn3 = Radiobutton ( adj_tcheck_win, text="Infantry", variable=utype, value=3 ).pack (pady=5)

        tcheck_confirm_btn = Button( adj_tcheck_win, text= "Confirm Selection", command=adj_tconfirm_click, bd=3).pack(pady=10)
        tcheck_exit_btn = Button ( adj_tcheck_win, text="Exit", command= adj_tcheck_win.destroy, bd=3).pack(pady=8)


    adj_infolbl = Label ( adjmenu, text="Type your position values:" ).place ( x=10, y=10 )
    tcheck_btn = Button ( adjmenu, text="Select Unit Type", command=adj_tcheck_click, bd=3 ).place ( x=190, y=55 )
    checkPos_btn = Button ( adjmenu, text="Confirm pos. values", command=intChecker, bd=3 ).place(x=180 ,y=320)
    storeval_btn = Button ( adjmenu, text="Apply Changes", command=storeValue, bd=3).place ( x=140, y=360 )
    Button (adjmenu, text="Exit Window", command=adjmenu.destroy, bd=3 ).place(x=250, y=360)

def trkr_click():
    trkmenu = Toplevel ()
    trkmenu.title ( 'Detection Slider' )

    trk_width = 400
    trk_height = 200

    xtrk = (screen_width / 2) - (trk_width / 2)
    ytrk = (screen_height / 2) - (trk_height / 2)

    trkmenu.geometry ( f'{trk_width}x{trk_height}+{int ( xtrk )}+{int ( ytrk )}' )

    trkicon = PhotoImage ( file="Ork_Symbols.png" )
    trkmenu.iconphoto ( False, trkicon )
    trkmenu.resizable ( False, False )

    def trk_getVal():
        global trk_get

        trk_getInput = trkslidery.get()
        trk_get = int(trk_getInput)


    trklbl = Label ( trkmenu, text="Adjustment Slider of Enemy Detection: " ).place ( x=10, y=10 )
    trkbtn = Button ( trkmenu, text="Apply Changes", command=trk_getVal, bd=3 ).place ( x=100, y=60 )
    Button ( trkmenu, text="Exit Window", command=trkmenu.destroy, bd=3 ).place ( x=220, y=60 )

    trklbly = Label ( trkmenu, text="Y Value : " ).place ( x=30, y=120 )
    trkslidery = Scale ( trkmenu, from_=0, to=100, length=200, orient=HORIZONTAL )
    trkslidery.place ( x=100, y=100 )


def bop_click():
    bopmenu = Toplevel()
    bopmenu.title('Balance of Power Slider')

    bop_width = 400
    bop_height = 300

    xbop = (screen_width / 2) - (bop_width / 2)
    ybop = (screen_height / 2) - (bop_height / 2)

    bopmenu.geometry (f'{bop_width}x{bop_height}+{int( xbop )}+{int( ybop )}')

    bopicon = PhotoImage ( file="Ork_Symbols.png" )
    bopmenu.iconphoto ( False, bopicon )
    bopmenu.resizable(False, False)

    def bop_getVal():
        global bop_adjust_valx
        global bop_adjust_valy

        bop_adjust_valxinput = bopsliderx.get()
        bop_adjust_valx = int(bop_adjust_valxinput)
        bop_adjust_valyinput = bopslidery.get()
        bop_adjust_valy = int(bop_adjust_valyinput)



    boplbl = Label( bopmenu, text="Balance of Power Height Adjustment: " ).place( x=10, y=10 )

    boplblx = Label( bopmenu, text="X Value : ").place( x=30, y=120 )
    bopsliderx = Scale( bopmenu, from_=-2, to=2, length=200,orient=HORIZONTAL )
    bopsliderx.place ( x=100, y=100 )

    boplbly = Label ( bopmenu, text="Y Value : " ).place ( x=30, y=220 )
    bopslidery = Scale ( bopmenu, from_=-2, to=2, length=200, orient=HORIZONTAL )
    bopslidery.place(x=100, y=200)

    bopbtn = Button ( bopmenu, text="Apply Changes", command=bop_getVal, bd=3 ).place( x=100, y=50 )
    Button ( bopmenu, text="Exit Window", command=bopmenu.destroy, bd=3 ).place ( x=220, y=50 )



def abt_click():
    abtmenu = Toplevel()
    abtmenu.title('About the Program')

    abt_width = 600
    abt_height = 660

    xabt = (screen_width / 2) - (abt_width / 2)
    yabt = (screen_height / 2) - (abt_height / 2)

    abtmenu.geometry ( f'{abt_width}x{abt_height}+{int ( xabt )}+{int ( yabt )}' )

    abticon = PhotoImage ( file="Ork_Symbols.png" )
    abtmenu.iconphoto ( False, abticon )
    abtmenu.resizable ( False, False )

    abtframe = LabelFrame ( abtmenu ,text= "The Defensive Siege Battle AI: Waaagh!", labelanchor=N)
    abtframe.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
    abtmenu.grid_columnconfigure(0, weight=1)

    descframe = LabelFrame ( abtframe, text="What is Waaagh! ?", labelanchor= N)
    descframe.grid(row=1, column=0, sticky='nesw', padx=10, pady=10)
    desc = Message( descframe, text="Waaagh! is a bot that operates as a proxy for a human-controlled player in a defensive siege battle in the Real Time Strategy Game Total War: Warhammer II.", aspect=100, justify=LEFT, width=530 )
    desc.pack (padx=10, pady=10 )

    funcframe = LabelFrame ( abtframe, text="What does Waaagh! do?", labelanchor= N)
    funcframe.grid ( row=2, column=0, sticky='nesw', padx=10, pady=10 )
    func = Message ( funcframe,text="Waaagh! will command the player's soldiers in a defensive siege warfare against the opposing AI and win the battle. \n\nIts goal is to give instructions to troops in the game automatically without the player's involvement and, over time, develop and apply the most efficient and effective strategy for defeating the opposing AI.", aspect=100, justify=LEFT, width=530 )
    func.pack ( padx=10, pady=10 )

    submodframe = LabelFrame ( abtframe, text="The Traits / Attributes of Waaagh! (Sub-modules)", labelanchor= N)
    submodframe.grid ( row=3, column=0, sticky='nesw', padx=10, pady=10 )
    submod = Message ( submodframe,text="Tactician Trait – a module where the AI detects and identifies information on each unit on the field to know the units required for the scenario.\n\nCommander Trait – a module that uses a predetermined series of keyboard and mouse inputs to shift units depending on the scenario.\n\nTracker Trait - A module that tracks and sends data about the movements of the enemy units on the mini-map.\n\nBattle Master Trait – a module where it monitors certain fields such as entity count and balance of power.",aspect=100, justify=LEFT, width=530 )
    submod.pack ( padx=10, pady=10 )

    objframe = LabelFrame ( abtframe, text="The Objective of Waaagh!", labelanchor= N)
    objframe.grid ( row=4, column=0, sticky='nesw', padx=10, pady=10 )
    obj = Message ( objframe,text="The objective of this program is to differentiate the enemy units from the players units and use the players units in the field to defeat the enemy units and win the defensive siege battle.", aspect=200, justify=LEFT, width=530)
    obj.pack ( padx=10, pady=10 )

    Button(abtframe, text="Back to Main", command=abtmenu.destroy).grid(row=5, column=0, pady=10)


menubar = Menu(root)
root.config(menu=menubar)

MainMenu = Menu(menubar, tearoff=0)
bhv_submenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label='Main Menu', menu=MainMenu)

MainMenu.add_cascade(label='Behaviors', menu=bhv_submenu)
bhv_submenu.add_command(label='Tactician Trait', command=confidence_click)
bhv_submenu.add_command(label='Commander Trait', command=adj_click)
bhv_submenu.add_command(label='Tracker Trait', command=trkr_click)
bhv_submenu.add_command(label='Battle Master Trait', command=bop_click)

MainMenu.add_command(label='About', command=abt_click)
MainMenu.add_separator()

MainMenu.add_command(label='Exit Program', command=root.destroy)

# ***************** SCAN / EXECUTE **************************

def ScanPrompt():
    successlbl_1 = Label(root, text="Total War Warhammer II is running.")
    successlbl_2 = Label(root, text="Total War Warhammer II is running. Game detected.")
    failurelbl = Label(root, text="Total War Warhammer II is not running. Game not detected.")
    if pyautogui.locateOnScreen('titleimage.png', confidence=0.7, grayscale=True) is not None:
        global gamePointx, gamePointy
        gamePointx, gamePointy = pyautogui.center(pyautogui.locateOnScreen('titleimage.png', confidence=0.7, grayscale=True))

        # *************************** FAILSAFE SOMEWHAT **************************************
        if pyautogui.locateOnScreen('SB_blue.png', confidence=0.9, grayscale=True) is not None:
            Executebtn.config(state=NORMAL)
            print ( successlbl_2 )
            successlbl_2.place ( x=255, y=210 )
            successlbl_2.after ( 2000, lambda: successlbl_2.place_forget () )
        else:
            pass
        print( successlbl_1 )
        successlbl_1.place( x=300, y=210 )
        successlbl_2.after( 2000, lambda: successlbl_1.place_forget() )
    else:
        Executebtn.config(state=DISABLED)
        print(failurelbl)
        failurelbl.place(x=235, y=210)
        failurelbl.after(2000, lambda: failurelbl.place_forget())


def ExecutePrompt():
    Executebtn.config(state=DISABLED)

    smBot = SimpleMode()
    GameSelect()
    smBot.smActive(sent_mon_values= monsval_data, sent_m_values= misval_data, sent_i_values= infval_data, sent_battle_master_bop_adjust_x= bop_adjust_valx,
                   sent_battle_master_bop_adjust_y= bop_adjust_valy, sent_defense_line=trk_get, sent_confidence=confidence_get, sent_game_Pointx=gamePointx,
                   sent_game_Pointy=gamePointy)

#******** CANVAS ***********
bgcanvas = Canvas(root, width=800, height=450)
bgcanvas.pack(fill="both", expand=True)
bgcanvas.create_image(0, 0, image=bgImage, anchor=NW)
bgcanvas.create_text(400, 160, text="WAAAGH! THE DEFENSIVE SIEGE BATTLE AI", font=("BlackwoodCastle", 25), fill='black')
bgcanvas.create_text(403, 162, text="WAAAGH! THE DEFENSIVE SIEGE BATTLE AI", font=("BlackwoodCastle", 25), fill='darkorange')

Scanbtn = Button(root, text="Scan", font=("BlackwoodCastle", 20), activebackground="darkred", command=ScanPrompt)
Executebtn = Button(root, state=DISABLED, text="Execute", font=("BlackwoodCastle", 20), activebackground="darkgreen", command=ExecutePrompt)
Scanwdw = bgcanvas.create_window(250, 260, anchor='nw', window=Scanbtn)
Executewdw = bgcanvas.create_window(450, 260, anchor='nw', window=Executebtn)

root.mainloop()


