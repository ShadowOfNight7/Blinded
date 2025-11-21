import keyboard, random, math, time, sys, os, mouse
from YiPyterminal import Pyterminal, assets, pyterm
import Cursor, MouseDetect, AttackTest



def colourText(rgb: list, text: str, transparency = 1, background = False):
    returntext = ""
    if not background:
        splittext = text.splitlines()
        for line in splittext:
            for characters in line:
                returntext += "\033[38;2;" + str(round(rgb[0] * transparency)) + ";" + str(round(rgb[1] * transparency)) + ";" + str(round(rgb[2] * transparency)) + "m" + characters + "\033[0m"
            if splittext.index(line) != (len(splittext) - 1):
                returntext += "\n"
        return returntext
    splittext = text.splitlines()
    for line in splittext:
        for characters in line:
            returntext += "\033[48;2;" + str(round(rgb[0] * transparency)) + ";" + str(round(rgb[1] * transparency)) + ";" + str(round(rgb[2] * transparency)) + "m" + characters + "\033[0m"
        if splittext.index(line) != (len(splittext) - 1):
            returntext += "\n"
    return returntext


def addItems(Item: str, Coords = (0, 0)):
    global screen
    lines = Item.splitlines()
    for i in range(len(lines)):
        for i2 in range(len(lines[i])):
            try:
                screen[i + Coords[0]][i2 + Coords[1]] = lines[i][i2]
            except IndexError:
                continue


def PhaseChange(Phase: str):
    global phase, riseTitle, rise, Settings, SevenSins, mapOffset
    phase = Phase
    if phase.lower() == "title":
        riseTitle = 0
        rise = False
        Settings = False
        SevenSins = False
    if phase.lower() == "map":
        mapOffset = [0, 0]





timed = 99
AimTarget = []
# character_size = (19, 37) #NORMAL
character_size = (9, 19) #PC
character_size = Cursor.initialize(2)
score = 0

MainClock = 1000
FalseTime = time.time()
transparency = 1

phase = "title"


#Oddly Specific Variables
riseTitle = 0
rise = False
Settings = False
SevenSins = False

Hierarchy = 10
RandomAdd = []
RandomAddMini = []
for i in range(Hierarchy):
    RandomAdd.append(random.randint(0, 359))
    RandomAddMini.append([random.randint(-round(100/((i + 1) * 2 + 1)), round(100/((i + 1) * 2 + 1))) for i2 in range((i + 1) * 2 + 1)])
mapOffset = [0, 0]
hierarchyLocations = []
hierarchyLocations2 = []


while True:
    startTime = time.perf_counter()
    pyterm.clearLetters()
    pyterm.updateKeys()
    MainClock += 1

    #Code Start
    
    keyboard.block_key("ctrl")
    location = Cursor.get_mouse_coords(character_size, True)
    
    # addItems(assets["background"])

    # for i in range(len(screen)):
    #     sys.stdout.write("\033[" + str(i+1) +";1f" + ''.join(screen[i])[:(os.get_terminal_size().columns - 1)])
    #     sys.stdout.write(f"\033[{os.get_terminal_size().lines};{os.get_terminal_size().columns}f")
    #     sys.stdout.flush()

    if phase.lower() == "title":
        pyterm.addItem(assets["background"], 0, 0, "center", "center")
        pyterm.addItem(assets["TitleOptions"], 40, -8 - max(riseTitle - 3, 0), "center", "center")
        pyterm.addItem(assets["TitlePlay"], -40, -3 - max(riseTitle, 0), "center", "center")
        pyterm.addItem(assets["Title1"], 0, -22 - max(riseTitle - 8, 0), "center", "center")
        if ((-63 + os.get_terminal_size().columns/2) <= location[0] <= (-19 + os.get_terminal_size().columns/2)) and ((8 + os.get_terminal_size().lines/2) <= location[1] <= (14 + os.get_terminal_size().lines/2)) and (riseTitle == 0) and (not (Settings or SevenSins)):
            pyterm.addItem(assets["TitlePlayHover"], -40, -3, "center", "center")
            if MouseDetect.ClickDetect("Left", "On"):
                rise = True
                SevenSins = True
        if ((17 + os.get_terminal_size().columns/2) <= location[0] <= (61 + os.get_terminal_size().columns/2)) and ((1 + os.get_terminal_size().lines/2) <= location[1] <= (8 + os.get_terminal_size().lines/2)) and (riseTitle == 0) and (not (Settings or SevenSins)):
            pyterm.addItem(assets["TitleOptionsHover"], 40, -8, "center", "center")
            if MouseDetect.ClickDetect("Left", "On"):
                rise = True
                Settings = True
        #Settings Overlay
        if Settings:
            pyterm.addItem(assets["TitleSettings"], 0, -70 + min(riseTitle, 55), "center", "center")
            pyterm.addItem(assets["TitleReturn"], -55, -100 + riseTitle, "center", "center")
            if ((-73 + os.get_terminal_size().columns/2) <= location[0] <= (-39 + os.get_terminal_size().columns/2)) and ((-18 + os.get_terminal_size().lines/2) <= location[1] <= (-14 + os.get_terminal_size().lines/2)):
                pyterm.addItem(assets["TitleReturnHover"], -55, -100 + riseTitle, "center", "center")
                if MouseDetect.ClickDetect("Left", "On"):
                    rise = False
            if (riseTitle == 0) and (not rise):
                Settings = False
        
        #7Sins Overlay
        if SevenSins:
            GreedLoc = pyterm.addItem(assets.get("TitleHexagon"), 60, -73 + min(riseTitle, 64), "center", "center")
            PrideLoc = pyterm.addItem(assets.get("TitleHexagon"), 40, -76 + min(riseTitle, 61), "center", "center")
            EnvyLoc = pyterm.addItem(assets.get("TitleHexagon"), 20, -67 + min(riseTitle, 58), "center", "center")
            SlothLoc = pyterm.addItem(assets.get("TitleHexagon"), 0, -70 + min(riseTitle, 55), "center", "center")
            DesireLoc = pyterm.addItem(assets.get("TitleHexagon"), -20, -61 + min(riseTitle, 52), "center", "center")
            GluttonyLoc = pyterm.addItem(assets.get("TitleHexagon"), -40, -64 + min(riseTitle, 49), "center", "center")
            WrathLoc = pyterm.addItem(assets.get("TitleHexagon"), -60, -55 + min(riseTitle, 46), "center", "center")
            #7sins buttondetect
            if (math.hypot((WrathLoc[0] - location[0]), 2 * (WrathLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.addItem("X", -60, -55 + min(riseTitle, 46) + 15, "center", "center")
            else:
                pyterm.addItem("UNYIELDING", -60, -55 + min(riseTitle, 46) + 15, "center", "center")
            if (math.hypot((GluttonyLoc[0] - location[0]), 2 * (GluttonyLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.addItem("X", -40, -64 + min(riseTitle, 49) + 15, "center", "center")
            else:
                pyterm.addItem("SWEET TOOTH", -40, -64 + min(riseTitle, 49) + 15, "center", "center")
            if (math.hypot((DesireLoc[0] - location[0]), 2 * (DesireLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.addItem("X", -20, -61 + min(riseTitle, 52) + 15, "center", "center")
            else:
                pyterm.addItem("CHARISMATIC", -20, -61 + min(riseTitle, 52) + 15, "center", "center")
            if (math.hypot((SlothLoc[0] - location[0]), 2 * (SlothLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.addItem("X", 0, -70 + min(riseTitle, 55) + 15, "center", "center")
            else:
                pyterm.addItem("LAID BACK", 0, -70 + min(riseTitle, 55) + 15, "center", "center")
            if (math.hypot((EnvyLoc[0] - location[0]), 2 * (EnvyLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.addItem("X", 20, -67 + min(riseTitle, 58) + 15, "center", "center")
            else:
                pyterm.addItem("ATTENTIVE", 20, -67 + min(riseTitle, 58) + 15, "center", "center")
            if (math.hypot((PrideLoc[0] - location[0]), 2 * (PrideLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.addItem("X", 40, -76 + min(riseTitle, 61) + 15, "center", "center")
            else:
                pyterm.addItem("PERFECTIONISM", 40, -76 + min(riseTitle, 61) + 15, "center", "center")
            if (math.hypot((GreedLoc[0] - location[0]), 2 * (GreedLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.addItem("X", 60, -73 + min(riseTitle, 64) + 15, "center", "center")
            else:
                pyterm.addItem("LUCKY", 60, -73 + min(riseTitle, 64) + 15, "center", "center")

            pyterm.addItem(assets.get("Title7Sins"), 0, -92 + min(riseTitle, 66), "center", "center")
            pyterm.addItem(assets["TitleReturn"], -55, -100 + riseTitle, "center", "center")
            if ((-73 + os.get_terminal_size().columns/2) <= location[0] <= (-39 + os.get_terminal_size().columns/2)) and ((-18 + os.get_terminal_size().lines/2) <= location[1] <= (-14 + os.get_terminal_size().lines/2)):
                pyterm.addItem(assets["TitleReturnHover"], -55, -100 + riseTitle, "center", "center")
                if MouseDetect.ClickDetect("Left", "On"):
                    rise = False
            if (riseTitle == 0) and (not rise):
                SevenSins = False

        #Chain Up/Down Animation
        if rise and (riseTitle != 70):
            riseTitle += 2
        elif (not rise) and (riseTitle != 0):
            riseTitle -= 2
            





    elif phase.lower() == "map":
        pyterm.addItem(assets["BlackHole"], round(mapOffset[0]), round(mapOffset[1]), "center", "center")
        pyterm.addItem("x", round(mapOffset[0]), round(mapOffset[1]), "center", "center")
        for i in range(Hierarchy):
            MaxRooms = (i + 1) * 2 + 1
            Angle = 360/MaxRooms
            for i2 in range(MaxRooms):
                roomLoc = pyterm.addItem(assets.get("BlackHole"), round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * 10 + mapOffset[0]), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * 10/2 + mapOffset[1]), "center", "center")
                hierarchyLocations2.append(roomLoc)
            hierarchyLocations.append(hierarchyLocations2)
            hierarchyLocations2 = []
        
        if keyboard.is_pressed("w"):
            mapOffset[1] += 1
        if keyboard.is_pressed("s"):
            mapOffset[1] -= 1
        if keyboard.is_pressed("a"):
            mapOffset[0] += 2
        if keyboard.is_pressed("d"):
            mapOffset[0] -= 2



    pyterm.addItem(assets["EmptyBackground"], 0, 0, "center", "center")
    pyterm.addItem(str(location) + " " + str(MouseDetect.ClickDetect("Left", "On")), 0, 0, "bottom left", "bottom left")
    


    pyterm.renderScreen()
    elapsedTime = time.perf_counter() - startTime
    if elapsedTime < (1 / pyterm.fps):
        time.sleep((1 / pyterm.fps) - elapsedTime)
    pyterm.displayScreen()

