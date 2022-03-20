########## Imports ##########

import pickle # Save data
import time
from time import sleep # Imports the sleep command
from threading import Timer # Timers
from ctypes import windll
from functools import partial # Used for passing arguments to a function when binding tkinter objects
from tkinter import *  # Tkinter is used to make UI design stuff

from pynput import mouse as positionMouse
from pynput.mouse import Button as MouseButton, Controller
mouse = Controller()
from pynput import keyboard as listenerKeyboard
from pynput.keyboard import Key, Controller as KeyboardController
keyboard = KeyboardController()

########## Save Data Loading/Saving ##########

CommandsChosen = [ # Default values for the commands
    True, # Beg
    True, # Fish
    True, # Hunt
    True, # Dig
    True, # Post Meme
    False, # Landmine
    False, # Padlock
]

PowerupsChosen = [ # Default values for powerups
    False,
    False,
    False,
    False,
]

powerupAmounts = [ # Default powerup amounts
    1,
    1,
    1,
    1,
]

PositionValues = [ # Default position values
    [0, 0],
    [0, 0],
]

UserPatreon = False # Default patreon value

def SaveStorage(): # Saves everything
    pickle.dump(SaveData, open("SaveData", "wb"))

try: # Loads the save data
    SaveData = pickle.load(open("SaveData", "rb")) 
except: # If the save data hasn't been made yet it'll create it
    SaveData = [ # Save data variable where everything is stored
        CommandsChosen,
        PowerupsChosen,
        powerupAmounts,
        PositionValues,
        UserPatreon,
    ]
    SaveStorage()

# Grabbing values from SaveData
CommandsChosen = SaveData[0]
PowerupsChosen = SaveData[1]
powerupAmounts = SaveData[2]
PositionValues = SaveData[3]
UserPatreon = SaveData[4]

########## Color Variables ##########

# Gray colors
gray40 = "#404040"
gray25 = "#252525" # Main background color
gray20 = "#202020" # Button background color
gray15 = "#151515" # Button hover color
gray10 = "#101010" # Button active color

# Green colors
greenColor = "#00FF00"
greenHoverColor = "#00BB00"
greenActiveColor = "#007500"

# Red colors
redColor = "#FF0000"
redHoverColor = "#BB0000"
redActiveColor = "#750000"

# Save and exit button colors
saveButtonColor = "#00DD00"
exitButtonColor = "#DD0000"

########## Window Editing ##########

# Window
root=Tk()
root.overrideredirect(True)

tk_title = "Dank Memer Auto Farm Software" # The window title
root.title(tk_title)

##### Geometry #####

# Width & Height
rootWidth = 450
rootHeight = 425

# X Position
rootXPosition = root.winfo_screenwidth() * .5 - rootWidth / 2
rootXPosition = round(rootXPosition)

# Y Position
rootYPosition = root.winfo_screenheight() * .5 - rootHeight / 2
rootYPosition = round(rootYPosition)

root.geometry(str(rootWidth)+"x"+str(rootHeight)+"+"+str(rootXPosition)+"+"+str(rootYPosition))

##### Changing the default title bar ######

root.minimized = False
root.maximized = False

title_bar = Frame(root, bg=gray15, relief='raised', bd=0, highlightthickness=0) # Title bar

def set_appwindow(mainWindow): # Shows the program in the task bar and at the bottom of the screen
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())

def minimize_me(): # Hides window
    root.attributes("-alpha",0)
    root.minimized = True       

def deminimize(event):
    root.focus() 
    root.attributes("-alpha",1) # Shows window
    if root.minimized == True:
        root.minimized = False                              


# Title bar buttons
close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=gray15,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', bg=gray15,padx=2,pady=2,bd=0,fg="#757575",font=("calibri", 13),highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=gray15,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=gray15,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)

# Main program window
window = Frame(root, bg=gray25,highlightthickness=0)

# Title bar button packing
title_bar.pack(fill=X)
close_button.pack(side=RIGHT,ipadx=7,ipady=1)
expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
title_bar_title.pack(side=LEFT, padx=10)
window.pack(expand=1, fill=BOTH)

# Title bar motion binding
def changex_on_hovering(event):
    global close_button
    close_button['bg']='red'
def returnx_to_normalstate(event):
    global close_button
    close_button['bg']=gray15

def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=gray40
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=gray15

def get_pos(event): # Executes when the title bar is clicked to move the window

    if root.maximized == False:
        
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event): # Runs when the window is dragged
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

        def release_window(event): # Runs when window is released
            root.config(cursor="arrow")
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)

title_bar.bind('<Button-1>', get_pos) # Allows you to drag the window from the title bar
title_bar_title.bind('<Button-1>', get_pos) # Allows you to drag the window from the title

# Title bar button hovering effected
close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)

root.bind("<FocusIn>",deminimize) # Lets you view the window by clicking the window icon on the taskbar
root.after(10, lambda: set_appwindow(root)) # Shows icon on the taskbar

########## Gui Design ##########

# Page toggle functions
def toggleMainPage(type): # Toggles main page visibility
    if (type == True):
        MainPageFrame.pack(expand=1, fill=BOTH)
    elif (type == False):
        MainPageFrame.pack_forget()

def toggleCommandsPage(type): # Toggles commands page visiblity
    if (type == True):
        CommandSettingsFrame.pack(expand=1, fill=BOTH)
    elif (type == False):
        CommandSettingsFrame.pack_forget()

def togglePowerupsPage(type): # Toggles powerups page visibility
    if (type == True):
        PowerupSettingsFrame.pack(expand=1, fill=BOTH)
    elif (type == False):
        PowerupSettingsFrame.pack_forget()

def togglePositionsPage(type): # Toggles positions page visiblity
    if (type == True):
        PositionsFrame.pack(expand=1, fill=BOTH)
    elif (type == False):  
        PositionsFrame.pack_forget()

def toggleRunPage(type): # Toggles the run page visibility
    if (type == True):
        RunPageFrame.pack(expand=1, fill=BOTH)
    elif (type == False):
        RunPageFrame.pack_forget()

# Button hover effect functions
def tkinterButton_enter(event, buttonHoverColor): # Hover enter function
    event.widget['background'] = buttonHoverColor

def tkinterButton_leave(event, buttonColor): # Hover leave function
    event.widget['background'] = buttonColor


def tkinterOptionButton_enter(event):
    eventBG = event.widget['background']
    if (eventBG == greenColor):
        event.widget['background'] = greenHoverColor
    elif (eventBG == redColor):
        event.widget['background'] = redHoverColor

def tkinterOptionButton_leave(event):
    eventBG = event.widget['background']
    if (eventBG == greenHoverColor):
        event.widget['background'] = greenColor
    elif (eventBG == redHoverColor):
        event.widget['background'] = redColor



##### Main Page #####

MainPageFrame = Frame(window, bg=gray25,highlightthickness=0) # Frame for everything on the main page
MainPageFrame.pack(expand=1, fill=BOTH)

MainPageTitleText = "Dank Memer Auto Farm" # Page title text
MainPageSubTitleText = "Customize your settings then click run to begin the automation" # Page sub title text

MainPageTitleLabel = Label(MainPageFrame, text=MainPageTitleText, font=("Arial", 25), bg=gray25, fg="white", wraplength=rootWidth - 25, justify="center") # Page title
MainPageTitleLabel.pack()

MainPageSubTitleLabel = Label(MainPageFrame, text=MainPageSubTitleText, font=("Arial", 12),bg=gray25, fg="white", wraplength=rootWidth - 25, justify = "center") # Page sub title
MainPageSubTitleLabel.pack()


MainSettingsLabel = Label(MainPageFrame, text="Settings", font=("Arial", 22), bg=gray25, fg="white", wraplength=rootWidth - 25) # Settings text
MainSettingsLabel.pack(anchor="nw", padx=20, pady=5)


def patreonButtonClicked():
    global CommandsChosen
    buttonBG = patreonButton.cget("bg")
    global UserPatreon
    if (buttonBG == greenColor or buttonBG == greenHoverColor):
        patreonButton.config(background=redColor, activebackground=redActiveColor)
        SaveData[4] = False
        SaveStorage()
    elif (buttonBG == redColor or buttonBG == redHoverColor):
        patreonButton.config(background=greenColor, activebackground=greenActiveColor)
        SaveData[4] = True
        SaveStorage()


MainSettingsFrame = Frame(MainPageFrame, bg = gray25) # Frame for all of the settings buttons
MainSettingsFrame.pack(side=LEFT, anchor = "nw", pady = 5)

patreonFrame = Frame(MainSettingsFrame, bg=gray25)
patreonFrame.grid(row=0, column=0, columnspan=3, sticky="W")

patreonButton = Button(patreonFrame, width = 3, height = 1)
patreonButton.config(command=patreonButtonClicked)
if (UserPatreon == True): # Checks save data
    patreonButton.config(bg=greenColor, activebackground=greenActiveColor)
else:
   patreonButton.config(bg=redColor, activebackground=redActiveColor)
patreonButton.grid(row=0, column=0, padx=(20, 5), pady=5)
patreonButton.bind("<Enter>", tkinterOptionButton_enter)
patreonButton.bind("<Leave>", tkinterOptionButton_leave)

# Text label for the button
CommandLabel = Label(patreonFrame, bg=gray25, text="Dank Memer Patreon", font=("Arial", 18), fg="white")
CommandLabel.grid(row=0, column=1, sticky="NW")

CommandSubLabel = Label(patreonFrame, bg=gray25, text="(Shortens Cooldowns)", font=("Arial", 12), fg="white")
CommandSubLabel.grid(row=0, column=2, sticky="W")

def settingsButtonClicked(buttonClicked):
    if (buttonClicked == settingsButtons[0]): # Commands button
        toggleMainPage(False)
        toggleCommandsPage(True)
    elif (buttonClicked == settingsButtons[1]): # Powerups button
        toggleMainPage(False)
        togglePowerupsPage(True)
    elif (buttonClicked == settingsButtons[2]): # Positions button
        toggleMainPage(False)
        togglePositionsPage(True)

settingsButtons = [] # Holds settings buttons
settingsLabels = [] # Holds settings labels

settingsButtonsText = [ # Text for the settings buttons
    "Commands",
    "Powerups",
    "Positions",
]
settingsLabelsText = [ # Text for the settings labels
    "Select which currency commands you want to run",
    "Select items/powerups to boost your grinding ability",
    "Edit screen positions to make sure the mouse works correctly"
]

for x in range(0, 3): # Creates 3 settings buttons
    # Button
    settingsButton = Button(MainSettingsFrame, width=10, text=settingsButtonsText[x], font=("Arial", 14, "bold"), bg=gray20, activebackground=gray10, fg="white", activeforeground="white", borderwidth=1)
    settingsButton.config(command=partial(settingsButtonClicked, settingsButton))
    settingsButton.grid(row=x+2, column=0, sticky="NW", padx=(20, 10), pady=7)
    settingsButton.bind("<Enter>", lambda event:tkinterButton_enter(event, gray15))
    settingsButton.bind("<Leave>", lambda event:tkinterButton_enter(event, gray20))

    # Label
    settingsLabel = Label(MainSettingsFrame, bg=gray25, text=settingsLabelsText[x], font=("Arial", 12), fg="white", wraplength=280, justify=LEFT)
    settingsLabel.grid(row=x+2, column=1, sticky="w", padx = 10)

    # Storing the button and label
    settingsButtons.append(settingsButton)
    settingsLabels.append(settingsLabel)


##### Commands Page #####

CommandSettingsFrame = Frame(window, bg=gray25,highlightthickness=0) # Frame for everything on the commands page

commandsTitleText = "Commands" # Title text
commandsTitleSubText = "Select which commands to run" # Title sub text

commandsLabel = Label(CommandSettingsFrame, text=commandsTitleText, font=("Arial", 25), bg=gray25, fg="#fff", wraplength=rootWidth - 25, justify="center") # Title Label
commandsLabel.pack()

commandsSubLabel = Label(CommandSettingsFrame, text=commandsTitleSubText, font=("Arial", 14),bg=gray25, fg="#fff", wraplength=rootWidth - 25, justify = "center") # Sub Title Label
commandsSubLabel.pack()
##### Buttons #####

buttonWidth = 3
buttonHeight = 1

buttonPaddingX = (15, 5)
buttonPaddingY = 5

# Frame to align everything
buttonsFrame = Frame(CommandSettingsFrame, bg=gray25)
buttonsFrame.pack(side="left", fill="both", expand=False)

def commandButtonClicked(commandButton, buttonId):
    global CommandsChosen
    buttonBG = commandButton.cget("bg")
    if (buttonBG == greenColor or buttonBG == greenHoverColor):
        commandButton.config(background=redColor, activebackground=redActiveColor)
        CommandsChosen[buttonId] = False
    elif (buttonBG == redColor or buttonBG == redHoverColor):
        commandButton.config(background=greenColor, activebackground=greenActiveColor)
        CommandsChosen[buttonId] = True

CommandButtons = [] # List that stores all of the command buttons
CommandButtonLabels = [] # List that stores all the labels for the commands
CommandButtonLabelText = [
    "beg",
    "fish",
    "hunt",
    "dig",
    "postmeme",
    "use landmine",
    "use padlock"
]
CommandRequirementText = [
    "(No Requirements)",
    "(Requires Fishing Rod",
    "(Requires Hunting Rifle)",
    "(Requires Shovel)",
    "(Rquires Laptops)",
    "(Safety Command)",
    "(Safety Command)"
]

for x in range(7): # Creates all the command buttons, text labels, and requirements
    # Button
    CommandButton = Button(buttonsFrame, width = buttonWidth, height = buttonHeight)
    CommandButton.config(command=partial(commandButtonClicked, CommandButton, x))
    if (CommandsChosen[x] == True): # Checks save data
        CommandButton.config(bg=greenColor, activebackground=greenActiveColor)
    else:
        CommandButton.config(bg=redColor, activebackground=redActiveColor)
    CommandButton.grid(row=x, column=0, padx=buttonPaddingX, pady=buttonPaddingY)
    CommandButton.bind("<Enter>", tkinterOptionButton_enter)
    CommandButton.bind("<Leave>", tkinterOptionButton_leave)

    CommandButtons.append(CommandButton) # Storing the button in a list

    # Text label for the button
    CommandLabel = Label(buttonsFrame, bg=gray25, text="- pls " + CommandButtonLabelText[x], font=("Arial", 18), fg="white")
    CommandLabel.grid(row=x, column=1, sticky="NW")
    # Requirement text label
    RequirementLabel = Label(buttonsFrame, bg=gray25, text=CommandRequirementText[x], font=("Arial", 12), fg="white")
    RequirementLabel.grid(row=x, column=2, sticky="W")

buttonsFrame.grid_rowconfigure(100, weight=1)
buttonsFrame.grid_columnconfigure(2, weight=1)

##### Save and Exit buttons #####

# Parent frame to grid align the two buttons
CommandSaveExitFrame = Frame(CommandSettingsFrame, bg=gray25)
CommandSaveExitFrame.place(relx=0.5, rely=0.97, anchor="s")

# Exit function (Closes command settings)
def ExitCommandSettings():
    toggleMainPage(True)
    toggleCommandsPage(False)

## Save button ##

def SaveCommands(): # Saves commands
    SaveStorage()
    ExitCommandSettings()

saveButtonText = StringVar()
saveButton = Button(CommandSaveExitFrame, width=10, textvariable=saveButtonText, font=("Arial", 18, "bold"), bg=saveButtonColor, activebackground=greenActiveColor, fg="white", activeforeground="white", command=SaveCommands)
saveButtonText.set("Save")
saveButton.grid(row=0, column=0, padx = 10)
saveButton.bind("<Enter>", lambda event:tkinterButton_enter(event, greenHoverColor))
saveButton.bind("<Leave>", lambda event:tkinterButton_enter(event, saveButtonColor))

## Exit Button ##
exitButton = Button(CommandSaveExitFrame, width=10, text="Cancel", font=("Arial", 18, "bold"), bg=exitButtonColor, activebackground=redActiveColor, fg="white", activeforeground="white", command=ExitCommandSettings)
exitButton.grid(row=0, column=1, padx = 10)
exitButton.bind("<Enter>", lambda event:tkinterButton_enter(event, redHoverColor))
exitButton.bind("<Leave>", lambda event:tkinterButton_leave(event, exitButtonColor))




##### Powerup gui design #####

PowerupSettingsFrame = Frame(window, bg=gray25,highlightthickness=0) # Frame for powerup page

powerupTitleText = "Powerups" # Title text
powerupSubTitleText = "Select which items/powerups to use and how many" # Sub title text

powerupTitleLabel = Label(PowerupSettingsFrame, text=powerupTitleText, font=("Arial", 25), bg=gray25, fg="#fff", wraplength=rootWidth - 25, justify="center") # Title Label
powerupTitleLabel.pack()

powerupSubTitleLabel = Label(PowerupSettingsFrame, text=powerupSubTitleText, font=("Arial", 14),bg=gray25, fg="#fff", wraplength=rootWidth - 25, justify = "center") # Sub Title Label
powerupSubTitleLabel.pack()

# Button click functions
def powerupButtonClicked(powerupButton, buttonId): # Changes button color
    global PowerupsChosen
    buttonBG = powerupButton.cget("bg")
    if (buttonBG == greenColor or buttonBG == greenHoverColor):
        powerupButton.config(bg=redColor, activebackground=redHoverColor)
        PowerupsChosen[buttonId] = False
    elif (buttonBG == redColor or buttonBG == redHoverColor):
        powerupButton.config(bg=greenColor, activebackground=greenHoverColor)
        PowerupsChosen[buttonId] = True

def upAmountButtonClicked(buttonId):
    amountTextVariable = powerupAmountText[buttonId]
    amountValue = powerupAmounts[buttonId]
    if (amountValue < 99):
        amountValue = amountValue + 1
        powerupAmounts[buttonId] = amountValue
        amountTextVariable.set(str(amountValue))
    
def lowerAmountButtonClicked(buttonId):
    amountTextVariable = powerupAmountText[buttonId]
    amountValue = powerupAmounts[buttonId]
    if (amountValue > 1):
        amountValue = amountValue - 1
        powerupAmounts[buttonId] = amountValue
        amountTextVariable.set(str(amountValue))

# Frame to align everything
powerupButtonsFrame = Frame(PowerupSettingsFrame, bg=gray25)
powerupButtonsFrame.pack(side="left", fill="both", expand=False)

powerupButtons = [] # List that stores all of the command buttons
powerupButtonLabelText = [
    "Lucky Horseshoe",
    "Pizza",
    "Prestige Coin",
    "Ammo",
]
powerupTimeText = [
    "(15m)",
    "(2h)",
    "(6h)",
    "(20m)",
]

powerupAmountText = []

for x in range(4): # Creates all the command buttons, text labels, and amount buttons.
    # Button
    powerupButton = Button(powerupButtonsFrame, width = 3, height = 1)
    powerupButton.config(command=partial(powerupButtonClicked, powerupButton, x))
    if (PowerupsChosen[x] == True):
        powerupButton.config(bg=greenColor, activebackground=greenActiveColor)
    else:
        powerupButton.config(bg=redColor, activebackground=redActiveColor)
    
    powerupButton.grid(row=x, column=0, padx=(15, 5), pady=5)
    powerupButton.bind("<Enter>", tkinterOptionButton_enter)
    powerupButton.bind("<Leave>", tkinterOptionButton_leave)
    powerupButtons.append(powerupButton)

    # Text label for the button
    powerupLabel = Label(powerupButtonsFrame, bg=gray25, text=powerupButtonLabelText[x], font=("Arial", 15), fg="white")
    powerupLabel.grid(row=x, column=1, sticky="NW", padx=(0, 10))
    powerupTimeLabel = Label(powerupButtonsFrame, bg=gray25, text=powerupTimeText[x], font=("Arial", 15), fg="white")
    powerupTimeLabel.grid(row=x, column=2, padx=(0, 10))

    ## Amount button and text
    lowerAmountButton = Button(powerupButtonsFrame, width = 2, height = 1, text="-", font=("Arial", 12, "bold"), bg=gray20, activebackground=gray10, fg="white", activeforeground="white")
    lowerAmountButton.config(command=partial(lowerAmountButtonClicked, x))
    lowerAmountButton.grid(row=x, column = 3, sticky="W", padx=10)
    lowerAmountButton.bind("<Enter>", lambda event: tkinterButton_enter(event, gray15))
    lowerAmountButton.bind("<Leave>", lambda event: tkinterButton_leave(event, gray20))

    amountText = StringVar()
    amountLabel = Label(powerupButtonsFrame, bg=gray25, textvariable=amountText, font=("Arial", 15, "bold"), fg="white", width=2, height=1)
    amountLabel.grid(row=x, column=4, sticky="NW")

    upAmountButton = Button(powerupButtonsFrame, width = 2, height = 1, text="+", font=("Arial", 12, "bold"), bg=gray20, activebackground=gray10, fg="white", activeforeground="white")
    upAmountButton.config(command=partial(upAmountButtonClicked, x))
    upAmountButton.grid(row=x, column = 5, sticky="W", padx=10)
    upAmountButton.bind("<Enter>", lambda event: tkinterButton_enter(event, gray15))
    upAmountButton.bind("<Leave>", lambda event: tkinterButton_leave(event, gray20))

    powerupAmountText.append(amountText)

    amountTextData = SaveData[2][x]
    amountText.set(str(amountTextData))
    powerupAmounts.append(amountTextData)

powerupButtonsFrame.grid_rowconfigure(100, weight=1)
powerupButtonsFrame.grid_columnconfigure(2, weight=1)

#### Save and exit buttons ####

# Parent frame to grid align the two buttons
powerupSaveExitFrame = Frame(PowerupSettingsFrame, bg=gray25)
powerupSaveExitFrame.place(relx=0.5, rely=0.97, anchor="s")

# Exit function (Closes command settings)
def ExitPowerupSettings():
    toggleMainPage(True)
    togglePowerupsPage(False)

## Save button ##

savePowerupsCooldown = 1
savePowerupsCooldownActive = False

def ResetPowerupsSaveCooldown():
    global savePowerupsCooldownActive
    savePowerupsCooldownActive = False

def SavePowerups():
    global savePowerupsCooldownActive
    if (savePowerupsCooldownActive == False):
        # Cooldown management
        savePowerupsCooldownActive = True
        powerupsCooldownTimer = Timer(savePowerupsCooldown, ResetPowerupsSaveCooldown)
        powerupsCooldownTimer.start()

        # Data saving
        SaveStorage()
        ExitPowerupSettings()

powerupsSaveButtonText = StringVar()
powerupsSaveButton = Button(powerupSaveExitFrame, width=10, textvariable=powerupsSaveButtonText, font=("Arial", 18, "bold"), bg=saveButtonColor, activebackground=greenActiveColor, fg="white", activeforeground="white", command=SavePowerups)
powerupsSaveButtonText.set("Save")
powerupsSaveButton.grid(row=0, column=0, padx = 10)
powerupsSaveButton.bind("<Enter>", lambda event: tkinterButton_enter(event, greenHoverColor))
powerupsSaveButton.bind("<Leave>", lambda event: tkinterButton_leave(event, saveButtonColor))

## Exit Button ##

powerupsExitButton = Button(powerupSaveExitFrame, width=10, text="Cancel", font=("Arial", 18, "bold"), bg=exitButtonColor, activebackground=redActiveColor, fg="white", activeforeground="white", command=ExitPowerupSettings)
powerupsExitButton.grid(row=0, column=1, padx = 10)
powerupsExitButton.bind("<Enter>", lambda event: tkinterButton_enter(event, redHoverColor))
powerupsExitButton.bind("<Leave>", lambda event: tkinterButton_leave(event, redColor))





##### Positions Page #####

PositionsFrame = Frame(window, bg=gray25,highlightthickness=0)

PositionsTitleText = "Mouse Positions"
PositionsSubTitleText = "Set the mouse positions so that the automation works correctly"

PositionsTitleLabel = Label(PositionsFrame, text=PositionsTitleText, font=("Arial", 25), bg=gray25, fg="#fff", wraplength=rootWidth - 25, justify="center")
PositionsTitleLabel.pack()

PositionsSubTitleLabel = Label(PositionsFrame, text=PositionsSubTitleText, font=("Arial", 12),bg=gray25, fg="#fff", wraplength=rootWidth - 25, justify = "center")
PositionsSubTitleLabel.pack()

instructionsText = StringVar()
instructionsLabel = Label(PositionsFrame, textvariable=instructionsText, font=("Arial", 15), background=gray25, fg="white", wraplength=rootWidth - 25, justify=CENTER)
instructionsText.set("Click one of the buttons to set its position value")
instructionsLabel.pack()

positionSet = False
positionButtonId = None

def on_click(x, y, button, pressed):
    global positionSet
    global positionButtonId
    if (str(button) == "Button.left" and pressed and positionSet == True):
        positionText = PositionLabelsText[positionButtonId]
        positionText.set("Current: X = "+str(x)+", Y = "+str(y))
        global PositionValues
        PositionValues[positionButtonId][0] = x
        PositionValues[positionButtonId][1] = y
        instructionsText.set("Click one of the buttons to set its position value")
        positionSet = False



def positionsButtonClicked(buttonId):
    global positionSet
    global positionButtonId
    if (positionSet == False):
        positionSet = True
        positionButtonId = buttonId
        if (buttonId == 0):
            instructionsText.set("Now click on the Discord chat bar")
        elif (buttonId == 1):
            instructionsText.set("Now click on one of the post meme options")

PositionButtons = []
PositionLabelsText = []
PositionButtonsText = [
    "Chat Bar",
    "Post Meme Option",
]

positionButtonsFrame = Frame(PositionsFrame, bg=gray25)
positionButtonsFrame.pack(side="left", fill="both", expand=False)

for x in range(0, 2):
    # Button
    positionsButton = Button(positionButtonsFrame, text=PositionButtonsText[x], font=("Arial", 15), bg=gray20, activebackground=gray10, fg='white', activeforeground='white', width=15)
    positionsButton.config(command=partial(positionsButtonClicked, x))
    positionsButton.bind("<Enter>", lambda event:tkinterButton_enter(event, gray15))
    positionsButton.bind("<Leave>", lambda event:tkinterButton_leave(event, gray20))
    positionsButton.grid(row=x, column=0, padx=(20, 10), pady=7,sticky="nw")
    PositionButtons.append(positionsButton)
    # Label
    positionsText = StringVar()
    positionsLabel = Label(positionButtonsFrame, bg=gray25, textvariable=positionsText, font=("Arial", 13, "bold"), fg="white")

    xPosition = PositionValues[x][0]
    yPosition = PositionValues[x][1]
    positionsText.set("Current: X = "+str(xPosition)+", Y = "+str(yPosition))

    positionsLabel.grid(row=x, column=1, sticky="W")
    PositionLabelsText.append(positionsText)


#### Save and exit buttons ####

# Parent frame to grid align the two buttons
positionsSaveExitFrame = Frame(PositionsFrame, bg=gray25)
positionsSaveExitFrame.place(relx=0.5, rely=0.97, anchor="s")

# Exit function (Closes command settings)
def ExitPositionsSettings():
    toggleMainPage(True)
    togglePositionsPage(False)

## Save button ##
def SavePositions():
    SaveStorage()
    ExitPositionsSettings()

positionsSaveButton = Button(positionsSaveExitFrame, width=10, text="Save", font=("Arial", 18, "bold"), bg=saveButtonColor, activebackground=greenActiveColor, fg="white", activeforeground="white", command=SavePositions)
positionsSaveButton.grid(row=0, column=0, padx = 10)
positionsSaveButton.bind("<Enter>", lambda event: tkinterButton_enter(event, greenHoverColor))
positionsSaveButton.bind("<Leave>", lambda event: tkinterButton_leave(event, saveButtonColor))

## Exit Button ##

positionsExitButton = Button(positionsSaveExitFrame, width=10, text="Cancel", font=("Arial", 18, "bold"), bg=exitButtonColor, activebackground=redActiveColor, fg="white", activeforeground="white", command=ExitPositionsSettings)
positionsExitButton.grid(row=0, column=1, padx = 10)
positionsExitButton.bind("<Enter>", lambda event: tkinterButton_enter(event, redHoverColor))
positionsExitButton.bind("<Leave>", lambda event: tkinterButton_leave(event, redColor))


listener = positionMouse.Listener(on_click=on_click)
listener.start()





RunPageFrame = Frame(window, bg=gray25,highlightthickness=0) # Frame for everything on the main page

RunPageTitleText = "Automation is Running" # Page title text
RunPageSubTitleText = "Press shift to stop the program" # Page sub title text

RunPageTitleLabel = Label(RunPageFrame, text=RunPageTitleText, font=("Arial", 25), bg=gray25, fg="white", wraplength=rootWidth - 25, justify="center") # Page title
RunPageTitleLabel.pack()

RunPageSubTitleLabel = Label(RunPageFrame, text=RunPageSubTitleText, font=("Arial", 12),bg=gray25, fg="white", wraplength=rootWidth - 25, justify = "center") # Page sub title
RunPageSubTitleLabel.pack()

TimeRan = 0
RunTimeText = StringVar()
RunTimeText.set("Time Ran: 0 seconds")
RunTimeLabel = Label(RunPageFrame, textvariable=RunTimeText, font=("Arial", 15), bg=gray25, fg="white", wraplength=rootWidth - 25) # Settings text
RunTimeLabel.pack(anchor="nw", padx=20, pady=(5, 0))

CommandsRan = 0
RunCommandsText = StringVar()
RunCommandsText.set("Commands Ran: 0")
RunCommandsLabel = Label(RunPageFrame, textvariable=RunCommandsText, font=("Arial", 15), bg=gray25, fg="white", wraplength=rootWidth - 25) # Settings text
RunCommandsLabel.pack(anchor="nw", padx=20)

CurrencyCommandsRan = 0
RunCurrencyCommandsText = StringVar()
RunCurrencyCommandsText.set("Currency Commands Ran: 0")
RunCurrencyCommandsLabel = Label(RunPageFrame, textvariable=RunCurrencyCommandsText, font=("Arial", 15), bg=gray25, fg="white", wraplength=rootWidth - 25) # Settings text
RunCurrencyCommandsLabel.pack(anchor="nw", padx=20)

SafetyCommandsRan = 0
RunSafetyCommandsText = StringVar()
RunSafetyCommandsText.set("Safety Commands Ran: 0")
RunSafetyCommandsLabel = Label(RunPageFrame, textvariable=RunSafetyCommandsText, font=("Arial", 15), bg=gray25, fg="white", wraplength=rootWidth - 25) # Settings text
RunSafetyCommandsLabel.pack(anchor="nw", padx=20)

PowerupCommandsRan = 0
RunPowerupCommandsText = StringVar()
RunPowerupCommandsText.set("Powerup Commands Ran: 0")
RunPowerupCommandsLabel = Label(RunPageFrame, textvariable=RunPowerupCommandsText, font=("Arial", 15), bg=gray25, fg="white", wraplength=rootWidth - 25) # Settings text
RunPowerupCommandsLabel.pack(anchor="nw", padx=20)

# Command cooldowns
begCooldown = 45
fishCooldown = 40
huntCooldown = 40
digCooldown = 40
postMemeCooldown = 50
landmineCooldown = 30
padlockCooldown = 30

# Whether or not the command should run yet
runBeg = True
runFish = True
runHunt = True
runDig = True
runPostMeme = True
runLandmine = True
runPadlock = True
runLucky = True
runPizza = True
runCoin = True
runAmmo = True

# Last time the command was used
lastBeg = None
lastFish = None
lastHunt = None
lastDig = None
lastPostMeme = None
lastLandmine = None
lastPadlock = None
lastLucky = None
lastPizza = None
lastCoin = None
lastAmmo = None

# Item durations
luckyDuration = 15 * 60
pizzaDuration = 1 * 60 * 60
coinDuration = 6 * 60 * 60
ammoDuration = 20 * 60

# Item amounts
luckyAmount = 0
pizzaAmount = 0
coinAmount = 0
ammoAmmount = 0

commandWaitList = []
commandRunning = False

TimeRanIntervals = (
    ('hours', 3600),
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=2):
    result = []

    for name, count in TimeRanIntervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def timeRanLoop():
    global TimeRan
    while True:
        sleep(1)
        TimeRan = TimeRan + 1
        timeText = display_time(TimeRan)
        RunTimeText.set("Time Ran: "+timeText)

def increaseCommandCount():
    global CommandsRan
    CommandsRan = CommandsRan + 1
    RunCommandsText.set("Commands Ran: "+str(CommandsRan))
def increaseCurrencyCommandCount():
    global CurrencyCommandsRan
    CurrencyCommandsRan = CurrencyCommandsRan + 1
    RunCurrencyCommandsText.set("Currency Commands Ran: "+str(CurrencyCommandsRan))
def increaseSafetyCommandCount():
    global SafetyCommandsRan
    SafetyCommandsRan = SafetyCommandsRan + 1
    RunSafetyCommandsText.set("Safety Commands Ran: "+str(SafetyCommandsRan))
def increasePowerupCommandCount():
    global PowerupCommandsRan
    PowerupCommandsRan = PowerupCommandsRan + 1
    RunPowerupCommandsText.set("Powerup Commands Ran: "+str(PowerupCommandsRan))


def enterCommand(command):
    chatBarPos = (PositionValues[0][0], PositionValues[0][1])
    
    mouse.position = chatBarPos
    print(mouse.position)
    sleep(0.1)
    mouse.press(MouseButton.left)
    mouse.release(MouseButton.left)
    sleep(0.1)
    for character in command:
            keyboard.press(character)
            keyboard.release(character)
            sleep(0.02)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def postMemeCommand():
    enterCommand("pls pm")
    sleep(3)
    postMemeOptionPos = (PositionValues[1][0], PositionValues[1][1])
    mouse.position = postMemeOptionPos
    sleep(0.1)
    mouse.press(MouseButton.left)
    mouse.release(MouseButton.left)

def runBegCommand():
    while True:
        sleep(1)
        global runBeg
        if (runBeg == True):
            timePassed = round(time.time()) - round(lastBeg)
            if (timePassed > begCooldown):
                runBeg = False
                commandWaitList.append("beg")
def runFishCommand():
    while True:
        sleep(1)
        global runFish
        if (runFish == True):
            timePassed = round(time.time()) - round(lastFish)
            if (timePassed > fishCooldown):
                runFish = False
                commandWaitList.append("fish")
def runHuntCommand():
    while True:
        sleep(1)
        global runHunt
        if (runHunt == True):
            timePassed = round(time.time()) - round(lastHunt)
            if (timePassed > huntCooldown):
                runHunt = False
                commandWaitList.append("hunt")
def runDigCommand():
    while True:
        sleep(1)
        global runDig
        if (runDig == True):
            timePassed = round(time.time()) - round(lastDig)
            if (timePassed > digCooldown):
                runDig = False
                commandWaitList.append("dig")
def runPostMemeCommand():
    while True:
        sleep(1)
        global runPostMeme
        if (runPostMeme == True):
            timePassed = round(time.time()) - round(lastPostMeme)
            if (timePassed > postMemeCooldown):
                runPostMeme = False
                commandWaitList.append("postMeme")
def runLandmineCommand():
    while True:
        sleep(1)
        global runLandmine
        if (runLandmine == True):
            timePassed = round(time.time()) - round(lastLandmine)
            if (timePassed > landmineCooldown):
                runLandmine = False
                commandWaitList.append("landmine")
def runPadlockCommand():
    while True:
        sleep(1)
        global runPadlock
        if (runPadlock == True):
            timePassed = round(time.time()) - round(lastPadlock)
            if (timePassed > padlockCooldown):
                runPadlock = False
                commandWaitList.append("padlock")
def runLuckyCommand():
    while True:
        sleep(1)
        global runLucky
        if (runLucky == True):
            timePassed = round(time.time()) - round(lastLucky)
            if (timePassed > luckyDuration):
                runLucky = False
                commandWaitList.append("lucky")
def runPizzaCommand():
    while True:
        sleep(1)
        global runPizza
        if (runPizza == True):
            timePassed = round(time.time()) - round(lastPizza)
            if (timePassed > pizzaDuration):
                runPizza = False
                commandWaitList.append("pizza")
def runCoinCommand():
    while True:
        sleep(1)
        global runCoin
        if (runCoin == True):
            timePassed = round(time.time()) - round(lastCoin)
            if (timePassed > coinDuration):
                runCoin = False
                commandWaitList.append("coin")
def runAmmoCommand():
    while True:
        sleep(1)
        global runAmmo
        if (runAmmo == True):
            timePassed = round(time.time()) - round(lastAmmo)
            if (timePassed > ammoDuration):
                runAmmo = False
                commandWaitList.append("ammo")

def runWaitList():
    while True:
        sleep(0.2)
        global commandRunning
        if (commandRunning == False and len(commandWaitList) > 0):
            command = commandWaitList[0]
            commandRunning = True
            if (command == "beg"):
                commandWaitList.remove("beg")
                enterCommand("pls beg")
                global lastBeg
                lastBeg = time.time()
                global runBeg
                runBeg = True
                increaseCommandCount()
                increaseCurrencyCommandCount()
            elif (command == "fish"):
                commandWaitList.remove("fish")
                enterCommand("pls fish")
                global lastFish
                lastFish = time.time()
                global runFish
                runFish = True
                increaseCommandCount()
                increaseCurrencyCommandCount()
            elif (command == "hunt"):
                commandWaitList.remove("hunt")
                enterCommand("pls hunt")
                global lastHunt
                lastHunt = time.time()
                global runHunt
                runHunt = True
                increaseCommandCount()
                increaseCurrencyCommandCount()
            elif (command == "dig"):
                commandWaitList.remove("dig")
                enterCommand("pls dig")
                global lastDig
                lastDig = time.time()
                global runDig
                runDig = True
                increaseCommandCount()
                increaseCurrencyCommandCount()
            elif (command == "postMeme"):
                commandWaitList.remove("postMeme")
                postMemeCommand()
                global lastPostMeme
                lastPostMeme = time.time()
                global runPostMeme
                runPostMeme = True
                increaseCommandCount()
                increaseCurrencyCommandCount()
            elif (command == "landmine"):
                commandWaitList.remove("landmine")
                enterCommand("pls use landmine")
                global lastLandmine
                lastLandmine = time.time()
                global runLandmine
                runLandmine = True
                increaseCommandCount()
                increaseSafetyCommandCount()
            elif (command == "padlock"):
                commandWaitList.remove("padlock")
                enterCommand("pls use padlock")
                global lastPadlock
                lastPadlock = time.time()
                global runPadlock
                runPadlock = True
                increaseCommandCount()
                increaseSafetyCommandCount()


            elif (command == "lucky"):
                commandWaitList.remove("lucky")
                global luckyAmount
                if (luckyAmount > 0):
                    luckyAmount = luckyAmount - 1
                    enterCommand("pls use lucky")
                    global lastLucky
                    lastLucky = time.time()
                    global runLucky
                    runLucky = True
                increaseCommandCount()
                increasePowerupCommandCount()
                sleep(5)
            elif (command == "pizza"):
                commandWaitList.remove("pizza")
                global pizzaAmount
                if (pizzaAmount > 0):
                    pizzaAmount = pizzaAmount - 1
                    enterCommand("pls use pizza")
                    global lastPizza
                    lastPizza = time.time()
                    global runPizza
                    runPizza = True
                increaseCommandCount()
                increasePowerupCommandCount()
                sleep(5)
            elif (command == "coin"):
                commandWaitList.remove("coin")
                global coinAmount
                if (coinAmount > 0):
                    coinAmount = coinAmount - 1
                    enterCommand("pls use prestigecoin")
                    global lastCoin
                    lastCoin = time.time()
                    global runCoin
                    runCoin = True
                increaseCommandCount()
                increasePowerupCommandCount()
                sleep(5)
            elif (command == "ammo"):
                commandWaitList.remove("ammo")
                global ammoAmount
                if (coinAmount > 0):
                    ammoAmount = ammoAmount - 1
                    enterCommand("pls use ammo")
                    global lastAmmo
                    lastAmmo = time.time()
                    global runAmmo
                    runAmmo = True
                increaseCommandCount()
                increasePowerupCommandCount()
                sleep(5)
            sleep(1)
            commandRunning = False

def RunBot():
    if (UserPatreon == True):
        global begCooldown
        global fishCooldown
        global huntCooldown
        global digCooldown
        global postMemeCooldown

        begCooldown = 30
        fishCooldown = 30
        huntCooldown = 30
        digCooldown = 30
        postMemeCooldown = 45

    if (CommandsChosen[0] == True):
        global lastBeg
        lastBeg = time.time() +  1000
        commandWaitList.append("beg")
        Timer(2, runBegCommand).start()
    if (CommandsChosen[1] == True):
        global lastFish
        lastFish = time.time() + 1000
        commandWaitList.append("fish")
        Timer(2, runFishCommand).start()
    if (CommandsChosen[2] == True):
        global lastHunt
        lastHunt = time.time() + 1000
        commandWaitList.append("hunt")
        Timer(2, runHuntCommand).start()
    if (CommandsChosen[3] == True):
        global lastDig
        lastDig = time.time() + 1000
        commandWaitList.append("dig")
        Timer(2, runDigCommand).start()
    if (CommandsChosen[4] == True):
        global lastPostMeme
        lastPostMeme = time.time() + 1000
        commandWaitList.append("postMeme")
        Timer(2, runPostMemeCommand).start()
    if (CommandsChosen[5] == True):
        global lastLandmine
        lastLandmine = time.time() + 1000
        commandWaitList.append("landmine")
        Timer(2, runLandmineCommand).start()
    if (CommandsChosen[6] == True):
        global lastPadlock
        lastPadlock = time.time() + 1000
        commandWaitList.append("padlock")
        Timer(2, runPadlockCommand).start()
    

    if (PowerupsChosen[0] == True):
        global luckyAmount
        luckyAmount = powerupAmounts[0]
        global lastLucky
        lastLucky = time.time() + 1000
        commandWaitList.append("lucky")
        Timer(2, runLuckyCommand).start()
    if (PowerupsChosen[1] == True):
        global pizzaAmount
        pizzaAmount = powerupAmounts[1]
        global lastPizza
        lastPizza = time.time() + 1000
        commandWaitList.append("pizza")
        Timer(2, runPizzaCommand).start()
    if (PowerupsChosen[2] == True):
        global coinAmount
        coinAmount = powerupAmounts[2]
        global lastCoin
        lastCoin = time.time() + 1000
        commandWaitList.append("coin")
        Timer(2, runCoinCommand).start()
    if (PowerupsChosen[3] == True):
        global ammoAmount
        ammoAmount = powerupAmounts[3]
        global lastAmmo
        lastAmmo = time.time() + 1000
        commandWaitList.append("ammo")
        Timer(2, runAmmoCommand).start()

    Timer(0, runWaitList).start()
    Timer(0, timeRanLoop).start()

def runBotButtonClicked():
    toggleMainPage(False)
    toggleRunPage(True)
    RunBot()
 
runBotButton = Button(MainPageFrame, width=10, text="Run Bot", font=("Arial", 18, "bold"), bg=saveButtonColor, activebackground=greenActiveColor, fg="white", activeforeground="white", command=runBotButtonClicked)
runBotButton.bind("<Enter>", lambda event:tkinterButton_enter(event, greenHoverColor))
runBotButton.bind("<Leave>", lambda event: tkinterButton_leave(event, saveButtonColor))
runBotButton.place(relx=0.5, rely=0.95, anchor="s")

keyDetectionListener = None

def key_release(key):
    if (key == Key.shift or key == Key.shift_r):
        keyDetectionListener.stop()
        root.destroy()
def addKeyboardListener():
    with listenerKeyboard.Listener(on_release=key_release) as listener:
        global keyDetectionListener
        keyDetectionListener = listener
        listener.join()

Timer(0, addKeyboardListener).start()

import ctypes
awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)

def main_loop():
    root.wm_attributes("-topmost", True)
    root.focus()
    root.after(1, main_loop) 
main_loop()

root.mainloop()
