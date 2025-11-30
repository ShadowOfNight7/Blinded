import keyboard, random, math, time, sys, os, mouse, ctypes
from Testing.YiPyterminal import Pyterminal, assets
import Testing.Cursor as Cursor
import Testing.MouseDetect as MouseDetect
import Testing.AttackTest as AttackTest
import Assets.YiPyterminal as pyterm
from Assets.YiPyterminal import itemObjects
import Assets.YiPyterminal as YiPyterminal

# fmt: off
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
# def addItems(Item: str, Coords = (0, 0)):
#     global screen
#     lines = Item.splitlines()
#     for i in range(len(lines)):
#         for i2 in range(len(lines[i])):
#             try:
#                 screen[i + Coords[0]][i2 + Coords[1]] = lines[i][i2]
#             except IndexError:
#                 continue


# fmt: off
def PhaseChange(Phase: str):
    global phase, riseTitle, rise, Settings, SevenSins, mapOffset, InitialHold, locationMapDiff, mapOffsetCopy, TargetLocation, FocusRoom, AnimateRoomEntry, player_x, player_y
    phase = Phase
    if phase.lower() == "title":
        riseTitle = 0
        rise = False
        Settings = False
        SevenSins = False
    elif phase.lower() == "map":
        mapOffset = [0, 0]
        InitialHold = (0, 0)
        locationMapDiff = [0, 0]
        mapOffsetCopy = [0, 0]
        TargetLocation = [0, 0, 0]
        FocusRoom = {"Location": (0, 0),"id": (0, 1),"Connections": [],"Movements": [],}
        FocusRoom = False
        AnimateRoomEntry = False
    elif phase.lower() == "room":
        player_x, player_y = 0, 0
    elif phase.lower() == "puzzlemove":
        pass
    elif phase.lower() == "puzzletext":
        pass
    elif phase.lower() == "battle":
        global enemiesStatus, playersStatus, buttons
        enemiesStatus = {}
        playersStatus = {}
        buttons = ["fight", "inventory", "info", "mercy"]
        buttonBarrier = "".join(
            [
                "┬\n",
                "".join(
                    ["|\n" for _ in range(math.floor(YiPyterminal.screenHeight / 4))]
                ),
            ]
        )
        YiPyterminal.createItem(
            "center button barrier",
            [buttonBarrier],
            parentObject="screen",
            parentAnchor="bottom center",
            childAnchor="bottom center",
            isUpdateItemLocation=False,
        )
        YiPyterminal.createItem(
            "left button barrier",
            [buttonBarrier],
            parentObject=buttons[1] + " button",
            parentAnchor="left center",
            childAnchor="right center",
            isUpdateItemLocation=False,
            xBias=-1,
        )
        YiPyterminal.createItem(
            "right button barrier",
            [buttonBarrier],
            parentObject=buttons[2] + " button",
            parentAnchor="right center",
            childAnchor="left center",
            isUpdateItemLocation=False,
            xBias=1,
        )
        for buttonNum in range(len(buttons)):
            YiPyterminal.createItem(
                buttons[buttonNum] + " button",
                [
                    YiPyterminal.addBorder(
                        buttons[buttonNum]
                        .upper()
                        .center(
                            math.floor(
                                (YiPyterminal.screenWidth - len("".join(buttons))) / 4
                            ),
                            " ",
                        ),
                        bottom=False,
                        left=True if buttonNum == 0 else False,
                        right=True if buttonNum == 3 else False,
                        padding={
                            "top": math.floor(YiPyterminal.screenHeight / 8),
                            "bottom": math.floor(YiPyterminal.screenHeight / 8),
                            "left": 0,
                            "right": 0,
                        },
                        paddingCharacter=" ",
                    ),
                    YiPyterminal.addBorder(
                        (">>> " + buttons[buttonNum] + " <<<")
                        .upper()
                        .center(
                            math.floor(
                                (YiPyterminal.screenWidth - len("".join(buttons))) / 4
                            ),
                            " ",
                        ),
                        bottom=False,
                        left=True if buttonNum == 0 else False,
                        right=True if buttonNum == 3 else False,
                        padding={
                            "top": math.floor(YiPyterminal.screenHeight / 8),
                            "bottom": math.floor(YiPyterminal.screenHeight / 8),
                            "left": 0,
                            "right": 0,
                        },
                        paddingCharacter=" ",
                    ),
                ],
                parentObject=(
                    "center button barrier"
                    if buttonNum == 1 or buttonNum == 2
                    else (
                        "left button barrier"
                        if buttonNum == 0
                        else "right button barrier"
                    )
                ),
                parentAnchor=(
                    "left center"
                    if buttonNum == 1 or buttonNum == 0
                    else "right center"
                ),
                childAnchor=(
                    "right center"
                    if buttonNum == 1 or buttonNum == 0
                    else "left center"
                ),
                xBias=-1 if buttonNum == 0 or buttonNum == 1 else 1,
                isUpdateItemLocation=False,
            )
        for item in [
            "center button barrier",
            buttons[1] + " button",
            buttons[2] + " button",
            "left button barrier",
            buttons[0] + " button",
            "right button barrier",
            buttons[3] + " button",
        ]:
            YiPyterminal.updateItemLocation(item)


# fmt: off

#Oddly Specific Functions
def SetRoomPhase(id: tuple):
    global ClearedRooms, itemObjects, hierarchyLocations, SettingsRooms
    if (id in ClearedRooms):
        if not (assets.get("FilledBlackHole") in itemObjects[str(id)]["animation frames"]):
            itemObjects[str(id)]["animation frames"][0] = assets.get("FilledBlackHole")
        return None
    for ids in ClearedRooms:
        for connections in hierarchyLocations[ids[0]][ids[1] - 1]["Movements"]:
            if (id == connections["id"]):
                if not (assets.get("FilledBlackHoleClose") in itemObjects[str(id)]):
                    itemObjects[str(id)]["animation frames"][0] = assets.get("FilledBlackHoleClose")
                return None
    else:
        if (SettingsRooms == 1):
            pyterm.updateItemFrame(str(id), 0)
        elif (SettingsRooms == 2):
            pyterm.updateItemFrame(str(id), 1)
        elif (SettingsRooms == 3):
            pyterm.updateItemFrame(str(id), 1)
            itemObjects[str(id)]["animation frames"][1] = "".join(random.choice('*&^%$#@!') if a=='#' else a for a in assets.get("FilledBlackHoleFar"))
    return None

timed = 99
AimTarget = []
# character_size = (19, 37) #NORMAL
character_size = (9, 19) #PCS
# character_size = Cursor.initialize(2)
score = 0
MainClock = 1000
FalseTime = time.time()
transparency = 1

phase = "map"

NonCenterOffset = 0

#Oddly Specific Variables
riseTitle = 0
rise = False
Settings = False
SevenSins = False
pyterm.createItem("SettingsRoomsNormal", [assets.get("SettingsRoomsNormal"), assets.get("SettingsRoomsNormalOn")], "screen", "center", "center", 0)
pyterm.createItem("SettingsRoomsObfuscated", [assets.get("SettingsRoomsObfuscated"), assets.get("SettingsRoomsObfuscatedOn")], "screen", "center", "center", 0)
pyterm.createItem("SettingsRoomsAnimated", [assets.get("SettingsRoomsAnimated"), assets.get("SettingsRoomsAnimatedOn")], "screen", "center", "center", 0)
SettingsRooms = 1

Hierarchy = 7
RandomAdd = []
RandomAddMini = []
for i in range(Hierarchy):
    RandomAdd.append(random.randint(0, 359))
    RandomAddMini.append([random.randint(-round(100/((i + 1) * 3 + 1)), round(100/((i + 1) * 3 + 1))) for i2 in range((i + 1) * 3 + 1)])
mapOffset = [0, 0]
hierarchyLocations = []
hierarchyLocations2 = []
InitialHold = (0, 0)
locationMapDiff = [0, 0]
mapOffsetCopy = [0, 0]
GetRoomLoc = True
LinesRooms = []
Fractured, Unfractured = random.randint(3, 10), 5
ClearedRooms = [(0, 1)]
TargetLocation = [0, 0, 0]
FocusRoom = {"Location": (0, 0), "id": (0, 1), "Connections": [], "Movements": []}
FocusRoom = False
pyterm.createItem("RoomSidebar", [assets.get("RoomSidebar"), assets.get("RoomSidebarExit"), assets.get("RoomSidebarPlay"), assets.get("RoomSidebarLocked")], "screen", "top right", "top right", 0)
RoomEntryList = []
# RoomEntryList = [assets.get("RoomAnimation1"), assets.get("RoomAnimation2"), assets.get("RoomAnimation3"), assets.get("RoomAnimation3"), assets.get("RoomAnimation3")]
for i in range(20):
    RoomEntryList.append(pyterm.addBorder("".join("".join(" " for i2 in range(round(4 * i ** 1.75 + 14))) + "\n" for i3 in range(round(2 * i ** 1.75 + 6))), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0}))
pyterm.createItem("RoomEntryAnimation", RoomEntryList, "screen", "center", "center", 0, 0, 0)
AnimateRoomEntry = False
pyterm.createItem("RoomHierarchy", ["Hierarchy: 0"], "screen", "top right", "center", 0)
pyterm.createItem("RoomNo.", ["Room Number: 1"], "screen", "top right", "center", 0)
pyterm.createItem("RoomType", ["Type: Battle"], "screen", "top right", "center", 0)
pyterm.createItem("RoomDifficulty", ["Difficulty: 1.05"], "screen", "top right", "center", 0)
pyterm.createItem("RoomRewards", ["Rewards:", "- Light", "- Gold", "- Exp"], "screen", "top right", "center", 0)

player_x, player_y = 0, 0
player_hitbox = [1, 1]
pyterm.createItem("PlayerMove", ["O"], "screen", "center", "center", 0)
room_size = [round(120), round(25)]
# pyterm.createItem("RoomSize", [pyterm.addBorder("".join("".join(" " for i2 in range(round((room_size[0] - 1)/2 + 1))) + "\n" for i3 in range(round((room_size[1] - 1)/2 + 1))), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})], "screen", "center", "center", 0)
pyterm.createItem("RoomSize", [pyterm.addBorder("".join("".join(" " for i2 in range(room_size[0])) + "\n" for i3 in range(room_size[1])), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})], "screen", "center", "center", 0)
room_walls = ["|", "-", "_", "¯", "┐", "└", "┘", "┌", "┴", "┬", "├", "┤", "┼", "#"]

#Setting Variables
RoomShadows = "Normal"#, "Obfuscated", "Animated"

#UI AND OTHER STUFF
pyterm.createItem("Ui", [assets.get("UI"), assets.get("UIInventory"), assets.get("UISettings")], "screen", "top left", "top left", 0)
pyterm.createItem("UiLevel", ["1"], "screen", "top left", "top left", 0)
pyterm.createItem("UiExp", ["(0/100)"], "screen", "top left", "top left", 0)
pyterm.createItem("UiLevelBar", ["."], "screen", "top left", "top left", 0)
pyterm.createItem("UiExpBar", ["."], "screen", "top left", "top left", 0)
pyterm.createItem("Light", ["0"], "screen", "top left", "top left", 0)
pyterm.createItem("Research", ["0"], "screen", "top left", "top left", 0)

InventoryUi = False
SettingsUi = False
InventoryUiState = 1


#ITS THE STATS!
light = 0
research = 0
level = 1
experience = 0
max_experience = round((math.log((math.e / 2) ** (level - 1) + math.gamma(level ** 1.35)/(level ** (level / 4)), max(10 * math.pi / level, 1 + 1/level ** 3)) + 0.798935) * 100)
#1 -> 999, 1.1 -> 10k, 10k -> 999k, 1.1mil -> ...

# PhaseChange("battle")

YiPyterminal.initializeTerminal(repetitions=1)
YiPyterminal.startAsynchronousMouseListener()
while True:
    startTime = time.perf_counter()
    YiPyterminal.updateScreenSize()
    pyterm.clearLettersToRender()
    pyterm.updateKeyboardBindStatus()
    YiPyterminal.copyMouseStatus(resetMouseStatusAfterCopy=True)
    MainClock += 1
    ctypes.windll.user32.OpenClipboard()
    ctypes.windll.user32.EmptyClipboard()
    # ctypes.windll.user32.CloseClipboard()
    if Cursor.is_full_screen() == "maximized":
        NonCenterOffset = 1
    elif Cursor.is_full_screen():
        NonCenterOffset = 3
    else:
        NonCenterOffset = 0
    # keyboard.block_key("ctrl")
    location = Cursor.get_mouse_coords(character_size, True)
    LeftClick = MouseDetect.ClickDetect("Left", "On")
    RightClick = MouseDetect.ClickDetect("Right", "On")

    #Updating stats
    while experience >= max_experience:
        experience -= max_experience
        level = min(level + 1, math.inf)
        try:
            max_experience = round((math.log((math.e / 2) ** (level - 1) + math.gamma(level ** 1.35)/(level ** (level / 4)), max(10 * math.pi / level, 1 + 1/level)) + 0.798935) * 100)
        except OverflowError:
            max_experience = round((math.log((math.e / 2) ** (level - 1) + math.gamma(45 ** 1.35)/(level ** (level / 4)), max(10 * math.pi / level, 1 + 1/((level - 35) ** 1.75 + 1.1 ** (level - 40)))) + 0.798935) * 100)



    if phase.lower() == "title":
        pyterm.renderLiteralItem(assets["background"], 0, 0, "center", "center")
        pyterm.renderLiteralItem(assets["TitleOptions"], 40, -8 - max(riseTitle - 3, 0), "center", "center")
        pyterm.renderLiteralItem(assets["TitlePlay"], -40, -3 - max(riseTitle, 0), "center", "center")
        pyterm.renderLiteralItem(assets["Title1"], 0, -22 - max(riseTitle - 8, 0), "center", "center")
        if ((-63 + os.get_terminal_size().columns/2) <= location[0] <= (-19 + os.get_terminal_size().columns/2)) and ((8 + os.get_terminal_size().lines/2) <= location[1] <= (15 + os.get_terminal_size().lines/2)) and (riseTitle == 0) and (not (Settings or SevenSins)):
            pyterm.renderLiteralItem(assets["TitlePlayHover"], -40, -3, "center", "center")
            if LeftClick:
                rise = True
                SevenSins = True
        if ((17 + os.get_terminal_size().columns/2) <= location[0] <= (61 + os.get_terminal_size().columns/2)) and ((2 + os.get_terminal_size().lines/2) <= location[1] <= (9 + os.get_terminal_size().lines/2)) and (riseTitle == 0) and (not (Settings or SevenSins)):
            pyterm.renderLiteralItem(assets["TitleOptionsHover"], 40, -8, "center", "center")
            if LeftClick:
                rise = True
                Settings = True
        #Settings Overlay
        if Settings:
            pyterm.renderLiteralItem(assets["TitleSettings"], 0, -70 + min(riseTitle, 55), "center", "center")
            pyterm.renderLiteralItem(assets["TitleReturn"], -55, -90 + min(riseTitle, 60), "center", "center")

            #SettingsRooms
            if LeftClick and ((round(os.get_terminal_size().columns/2) - 14 - 7) <= location[0] <= (round(os.get_terminal_size().columns/2) - 14 + 7)) and ((round(os.get_terminal_size().lines/2) - 10 - 2.5) <= location[1] <= (round(os.get_terminal_size().lines/2) - 10 + .5)):
                SettingsRooms = 1
            elif LeftClick and ((round(os.get_terminal_size().columns/2) - 0 - 7) <= location[0] <= (round(os.get_terminal_size().columns/2) - 0 + 7)) and ((round(os.get_terminal_size().lines/2) - 10 - 2.5) <= location[1] <= (round(os.get_terminal_size().lines/2) - 10 + .5)):
                SettingsRooms = 2
            elif LeftClick and ((round(os.get_terminal_size().columns/2) + 14 - 7) <= location[0] <= (round(os.get_terminal_size().columns/2) + 14 + 7)) and ((round(os.get_terminal_size().lines/2) - 10 - 2.5) <= location[1] <= (round(os.get_terminal_size().lines/2) - 10 + .5)):
                SettingsRooms = 3


            if SettingsRooms == 1:
                pyterm.updateItemFrame("SettingsRoomsNormal", 1)
                pyterm.updateItemFrame("SettingsRoomsObfuscated", 0)
                pyterm.updateItemFrame("SettingsRoomsAnimated", 0)
            elif SettingsRooms == 2:
                pyterm.updateItemFrame("SettingsRoomsNormal", 0)
                pyterm.updateItemFrame("SettingsRoomsObfuscated", 1)
                pyterm.updateItemFrame("SettingsRoomsAnimated", 0)
            elif SettingsRooms == 3:
                pyterm.updateItemFrame("SettingsRoomsNormal", 0)
                pyterm.updateItemFrame("SettingsRoomsObfuscated", 0)
                pyterm.updateItemFrame("SettingsRoomsAnimated", 1)
            pyterm.renderItem("SettingsRoomsNormal", xBias=-14, yBias= -65 + min(riseTitle, 55))
            pyterm.renderItem("SettingsRoomsObfuscated", xBias=0, yBias= -65 + min(riseTitle, 55))
            pyterm.renderItem("SettingsRoomsAnimated", xBias=14, yBias=-65 + min(riseTitle, 55))


            if ((os.get_terminal_size().columns/2 - 55 - 17.5) <= location[0] <= (os.get_terminal_size().columns/2 - 55 + 17.5)) and ((os.get_terminal_size().lines/2 - 30 + 17.5 - 2.5 - 3) <= location[1] <= (os.get_terminal_size().lines/2 - 30 + 17.5 + 2.5 - 3)) and (riseTitle == 70):
                pyterm.renderLiteralItem(assets["TitleReturnHover"], -55, -90 + min(riseTitle, 60), "center", "center")
                if LeftClick:
                    rise = False
            if (riseTitle == 0) and (not rise):
                Settings = False
        
        #7Sins Overlay
        if SevenSins:
            if keyboard.is_pressed("v"):
                PhaseChange("map")
            GreedLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 60, -73 + min(riseTitle, 64), "center", "center")
            PrideLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 40, -76 + min(riseTitle, 61), "center", "center")
            EnvyLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 20, -67 + min(riseTitle, 58), "center", "center")
            SlothLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 0, -70 + min(riseTitle, 55), "center", "center")
            DesireLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), -20, -61 + min(riseTitle, 52), "center", "center")
            GluttonyLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), -40, -64 + min(riseTitle, 49), "center", "center")
            WrathLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), -60, -55 + min(riseTitle, 46), "center", "center")
            #7sins buttondetect
            if (math.hypot((WrathLoc[0] - location[0]), 2 * (WrathLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("X", -60, -55 + min(riseTitle, 46) + 15, "center", "center")
            else:
                pyterm.renderLiteralItem("UNYIELDING", -60, -55 + min(riseTitle, 46) + 15, "center", "center")
            if (math.hypot((GluttonyLoc[0] - location[0]), 2 * (GluttonyLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("X", -40, -64 + min(riseTitle, 49) + 15, "center", "center")
            else:
                pyterm.renderLiteralItem("SWEET TOOTH", -40, -64 + min(riseTitle, 49) + 15, "center", "center")
            if (math.hypot((DesireLoc[0] - location[0]), 2 * (DesireLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("X", -20, -61 + min(riseTitle, 52) + 15, "center", "center")
            else:
                pyterm.renderLiteralItem("CHARISMATIC", -20, -61 + min(riseTitle, 52) + 15, "center", "center")
            if (math.hypot((SlothLoc[0] - location[0]), 2 * (SlothLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("X", 0, -70 + min(riseTitle, 55) + 15, "center", "center")
            else:
                pyterm.renderLiteralItem("LAID BACK", 0, -70 + min(riseTitle, 55) + 15, "center", "center")
            if (math.hypot((EnvyLoc[0] - location[0]), 2 * (EnvyLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("X", 20, -67 + min(riseTitle, 58) + 15, "center", "center")
            else:
                pyterm.renderLiteralItem("ATTENTIVE", 20, -67 + min(riseTitle, 58) + 15, "center", "center")
            if (math.hypot((PrideLoc[0] - location[0]), 2 * (PrideLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("X", 40, -76 + min(riseTitle, 61) + 15, "center", "center")
            else:
                pyterm.renderLiteralItem("PERFECTIONISM", 40, -76 + min(riseTitle, 61) + 15, "center", "center")
            if (math.hypot((GreedLoc[0] - location[0]), 2 * (GreedLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("X", 60, -73 + min(riseTitle, 64) + 15, "center", "center")
            else:
                pyterm.renderLiteralItem("LUCKY", 60, -73 + min(riseTitle, 64) + 15, "center", "center")

            pyterm.renderLiteralItem(assets.get("Title7Sins"), 0, -92 + min(riseTitle, 66), "center", "center")
            pyterm.renderLiteralItem(assets["TitleReturn"], -55, -100 + riseTitle, "center", "center")
            if ((os.get_terminal_size().columns/2 - 55 - 17.5) <= location[0] <= (os.get_terminal_size().columns/2 - 55 + 17.5)) and ((os.get_terminal_size().lines/2 - 30 + 17.5 - 2.5 - 3) <= location[1] <= (os.get_terminal_size().lines/2 - 30 + 17.5 + 2.5 - 3)) and (riseTitle == 70):
                pyterm.renderLiteralItem(assets["TitleReturnHover"], -55, -90 + min(riseTitle, 60), "center", "center")
                if LeftClick:
                    rise = False
            if (riseTitle == 0) and (not rise):
                SevenSins = False

        #Chain Up/Down Animation
        if rise and (riseTitle != 70):
            riseTitle += 2
        elif (not rise) and (riseTitle != 0):
            riseTitle -= 2

    elif phase.lower() == "map":
        
        if not GetRoomLoc:
            for Line in LinesRooms:
                # pyterm.renderItem(Line["Line"], xBias = round(Line["Pos"][0]) + mapOffset[0], yBias = round(Line["Pos"][1]) + mapOffset[1])
                pyterm.renderItem(str(Line["Pos1"]) + str(Line["Pos2"]), xBias=mapOffset[0], yBias=mapOffset[1], screenLimits=(999, 999))

        if GetRoomLoc:
            pyterm.createItem(str((0, 1)), [assets["FilledBlackHole"]], "screen", "center", "center", 0, 0, 0)
            hierarchyLocations.append([{"Location": (0, 0), "id": (0, 1), "Connections": [], "Movements": []}])
        pyterm.renderItem(str((0, 1)), xBias = mapOffset[0], yBias = mapOffset[1], screenLimits=(999, 999))
        if (os.get_terminal_size().columns/2 + mapOffset[0] - 8 <= location[0] <= os.get_terminal_size().columns/2 + mapOffset[0] + 8 - 1) and (os.get_terminal_size().lines/2 + mapOffset[1] - 4 <= location[1] <= os.get_terminal_size().lines/2 + mapOffset[1] + 4):
            pyterm.renderLiteralItem("AAA", round(mapOffset[0]), round(mapOffset[1]), "center", "center")
        else:
            pyterm.renderLiteralItem("x", round(mapOffset[0]), round(mapOffset[1]), "center", "center")
        for i in range(Hierarchy):
            MaxRooms = (i + 1) * 3 + 1
            Angle = 360/MaxRooms
            for i2 in range(MaxRooms):
                if GetRoomLoc:
                    roomLoc = pyterm.renderLiteralItem(assets.get("FilledBlackHole"), round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3) + mapOffset[0]), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2 + mapOffset[1]), "center", "center")
                    pyterm.createItem(str((i + 1, i2 + 1)), [assets["FilledBlackHoleFar"], "".join(random.choice('*&^%$#@!') if a=='#' else a for a in assets.get("FilledBlackHoleFar"))], "screen", "center", "center", 0, round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2))
                    hierarchyLocations2.append({"Location": (round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2)), "id": (i + 1, i2 + 1), "Connections": [], "Movements": []}) #Connections: [{"id": (_, _), "Location": (_, _)}]
                else:
                    # if math.dist(hierarchyLocations[i][i2]["Location"], (-mapOffset[0], -mapOffset[1])) <= (10 + math.hypot(os.get_terminal_size().columns/2, os.get_terminal_size().lines/2)):
                    if AnimateRoomEntry:
                        if not ((i + 1, i2 + 1) == AnimateRoomEntry["id"]):
                            pyterm.renderItem(str((i + 1, i2 + 1)), xBias = mapOffset[0], yBias = mapOffset[1], screenLimits=(999, 999))
                    else:
                        pyterm.renderItem(str((i + 1, i2 + 1)), xBias = mapOffset[0], yBias = mapOffset[1], screenLimits=(999, 999))
                    # pyterm.renderLiteralItem(str(hierarchyLocations[i + 1][i2]["Movements"]), round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3) + mapOffset[0]), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2 + mapOffset[1]), "center", "center")
                    # pyterm.renderLiteralItem(assets.get("FilledBlackHole"), round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3) + mapOffset[0]), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2 + mapOffset[1]), "center", "center")
            if GetRoomLoc == True:
                hierarchyLocations.append(hierarchyLocations2)
                hierarchyLocations2 = []

        if GetRoomLoc:
            for tier in hierarchyLocations:
                for rooms in tier:
                    if rooms["id"][0] > 0:
                        leastDistanceRoom = 10**100
                        ClosestPastRoom = ""
                        for pastrooms in hierarchyLocations[rooms["id"][0] - 1]: 
                            if ((pastrooms["Location"][0] - rooms["Location"][0]) ** 2 + (pastrooms["Location"][1] - rooms["Location"][1]) ** 2) < leastDistanceRoom:
                                leastDistanceRoom = (pastrooms["Location"][0] - rooms["Location"][0]) ** 2 + (pastrooms["Location"][1] - rooms["Location"][1]) ** 2
                                ClosestPastRoom = pastrooms
                        rooms["Connections"].append({"id": ClosestPastRoom["id"], "Location": ClosestPastRoom["Location"]})
                        rooms["Movements"].append({"id": ClosestPastRoom["id"], "Location": ClosestPastRoom["Location"]})
                        ClosestPastRoom["Movements"].append({"id": rooms["id"], "Location": rooms["Location"]})
                        #Connect To Neighbours:
                        if (random.randint(1, Fractured) <= Unfractured) and (rooms["id"][0] > 1):
                            leastDistanceRoom = 10**100
                            ClosestCurrentRoom = ""
                            for otherRooms in hierarchyLocations[rooms["id"][0]]:
                                if otherRooms["id"] != rooms["id"]:
                                    if ((otherRooms["Location"][0] - rooms["Location"][0]) ** 2 + (otherRooms["Location"][1] - rooms["Location"][1]) ** 2) < leastDistanceRoom:
                                        leastDistanceRoom = (otherRooms["Location"][0] - rooms["Location"][0]) ** 2 + (otherRooms["Location"][1] - rooms["Location"][1]) ** 2
                                        ClosestCurrentRoom = otherRooms
                            #TypeError: string indices must be integers, not 'str'
                            if (not ({"id": ClosestCurrentRoom["id"], "Location": ClosestCurrentRoom["Location"]}) in rooms["Connections"]) and (not ({"id": ClosestCurrentRoom["id"], "Location": ClosestCurrentRoom["Location"]}) in rooms["Movements"]):
                                # if (((10 + (rooms["id"][0] - 1)/3) * ((rooms["id"][0]) * 3 + 1) + 3) ** 2 < ((10 + (rooms["id"][0])/3) * ((rooms["id"][0] + 1) * 3 + 1) ** 2 + (0.5 * math.dist(ClosestCurrentRoom["Location"], rooms["Location"])) ** 2)):
                                    rooms["Connections"].append({"id": ClosestCurrentRoom["id"], "Location": ClosestCurrentRoom["Location"]})
                                    rooms["Movements"].append({"id": ClosestCurrentRoom["id"], "Location": ClosestCurrentRoom["Location"]})
                                    ClosestCurrentRoom["Movements"].append({"id": rooms["id"], "Location": rooms["Location"]})
        if GetRoomLoc:
            for tier in hierarchyLocations:
                for rooms in tier:
                    for connect in rooms["Connections"]:
                        LinesRooms.append({"Line": pyterm.generateLine(rooms["Location"], connect["Location"]), "Pos1": rooms["Location"], "Pos2": connect["Location"], "Id": rooms["id"]})
            for Line in LinesRooms:
                if min(Line["Pos1"][0], Line["Pos2"][0]) == Line["Pos1"][0]:
                    if min(Line["Pos1"][1], Line["Pos2"][1]) == Line["Pos1"][1]:
                        pyterm.createItem(str(Line["Pos1"]) + str(Line["Pos2"]), [Line["Line"]], str(Line["Id"]), "center", "top left")
                    else:
                        pyterm.createItem(str(Line["Pos1"]) + str(Line["Pos2"]), [Line["Line"]], str(Line["Id"]), "center", "bottom left")
                elif min(Line["Pos1"][1], Line["Pos2"][1]) == Line["Pos1"][1]:
                    pyterm.createItem(str(Line["Pos1"]) + str(Line["Pos2"]), [Line["Line"]], str(Line["Id"]), "center", "top right")
                else:
                    pyterm.createItem(str(Line["Pos1"]) + str(Line["Pos2"]), [Line["Line"]], str(Line["Id"]), "center", "bottom right")
        GetRoomLoc = False

        #Set Room Phases
        for tier in hierarchyLocations:
            for rooms in tier:
                SetRoomPhase(rooms["id"])

        #DetectRooms
        



        for tier in hierarchyLocations:
            for room in tier:
                if (room["Location"][0] + os.get_terminal_size().columns/2 + mapOffset[0] - 8 <= location[0] <= room["Location"][0] + os.get_terminal_size().columns/2 + mapOffset[0] + 8 - 1) and (room["Location"][1] + os.get_terminal_size().lines/2 + mapOffset[1] - 4 <= location[1] <= room["Location"][1] + os.get_terminal_size().lines/2 + mapOffset[1] + 4):
                    if LeftClick and not (FocusRoom and (os.get_terminal_size().columns - 24 <= location[0] <= os.get_terminal_size().columns)):
                        TargetLocation[2] = 1
                        TargetLocation[0] = -room["Location"][0]
                        TargetLocation[1] = -room["Location"][1]
                        FocusRoom = room

        if FocusRoom:
            pyterm.updateItemFrame("RoomSidebar", 0)
            if (os.get_terminal_size().columns - 24 <= location[0] <= os.get_terminal_size().columns) and (NonCenterOffset + 39 + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2) <= location[1] <= NonCenterOffset + 43 + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2)):
                pyterm.updateItemFrame("RoomSidebar", 1)
                if LeftClick and not (TargetLocation[2] is 1):
                    FocusRoom = False
            elif (os.get_terminal_size().columns - 24 <= location[0] <= os.get_terminal_size().columns) and (10 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2) <= location[1] <= 14 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2)):
                if ((itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHole")) or (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHoleClose"))):
                    pyterm.updateItemFrame("RoomSidebar", 2)
                    if (LeftClick) and not (TargetLocation[2] is 1):
                        AnimateRoomEntry = FocusRoom
                        TargetLocation[2] = 1
                        TargetLocation[0] = -FocusRoom["Location"][0]
                        TargetLocation[1] = -FocusRoom["Location"][1]
            elif keyboard.is_pressed("x"):
                FocusRoom = False
            elif keyboard.is_pressed("e") and ((itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHole")) or (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHoleClose"))):
                AnimateRoomEntry = FocusRoom
                TargetLocation[2] = 1
                TargetLocation[0] = -FocusRoom["Location"][0]
                TargetLocation[1] = -FocusRoom["Location"][1]
            if FocusRoom:
                pyterm.renderItem("RoomSelect", xBias = FocusRoom["Location"][0] + mapOffset[0], yBias = FocusRoom["Location"][1] +  mapOffset[1], screenLimits = (999, 999), createItemIfNotExists = True, createItemArgs = {"animationFrames": [assets.get("RoomSelect")], "parentObject": "screen", "parentAnchor": "center", "childAnchor": "center", "currentFrame": 0})
                if (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHole")) or (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHoleClose")):
                    itemObjects["RoomHierarchy"]["animation frames"][0] = "Hierarchy: " + str(FocusRoom["id"][0])
                    itemObjects["RoomNo."]["animation frames"][0] = "Room Number: " + str(FocusRoom["id"][1])
                else:
                    itemObjects["RoomHierarchy"]["animation frames"][0] = "Hierarchy: ???"
                    itemObjects["RoomNo."]["animation frames"][0] = "Room Number: ???"
                    pyterm.updateItemFrame("RoomSidebar", 3)
                pyterm.renderItem("RoomSidebar", yBias = NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomHierarchy", xBias = -11, yBias = 6 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomNo.", xBias = -11, yBias = 7 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomType", xBias = -11, yBias = 18 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                #pyterm.renderItem("RoomNo.", xBias = -12, yBias = 13)
        
        if AnimateRoomEntry:
            if itemObjects["RoomEntryAnimation"]["current frame"] + 1 >= 15:
                pyterm.updateItemFrame("RoomEntryAnimation", 0)
                ClearedRooms.append(AnimateRoomEntry["id"])
                AnimateRoomEntry = False
                FocusRoom = False
                # PhaseChange("Battle")
            else:
                pyterm.renderItem("RoomEntryAnimation", xBias = AnimateRoomEntry["Location"][0] + mapOffset[0], yBias = AnimateRoomEntry["Location"][1] + mapOffset[1], screenLimits= (999, 999))
                pyterm.updateItemFrame("RoomEntryAnimation", itemObjects["RoomEntryAnimation"]["current frame"] + 1)

        # pyterm.renderLiteralItem("X", FocusRoom["Location"][0] + mapOffset[0], FocusRoom["Location"][1] + mapOffset[1], "center", "center")

        if not MouseDetect.ClickDetect("Right", "Held"):
            InitialHold = location
            mapOffsetCopy = mapOffset.copy()
        else:
            locationMapDiff = [location[0] - InitialHold[0], location[1] - InitialHold[1]]
            mapOffset = [mapOffsetCopy[0] + locationMapDiff[0], mapOffsetCopy[1] + locationMapDiff[1]]
            TargetLocation[2] = 0

        if keyboard.is_pressed("w"):
            mapOffset[1] += 2
            TargetLocation[2] = 0
        if keyboard.is_pressed("s"):
            mapOffset[1] -= 2
            TargetLocation[2] = 0
        if keyboard.is_pressed("a"):
            mapOffset[0] += 4
            TargetLocation[2] = 0
        if keyboard.is_pressed("d"):
            mapOffset[0] -= 4
            TargetLocation[2] = 0
        if keyboard.is_pressed("q"):
            TargetLocation = [0, 0, 1]
        
        if TargetLocation[2] == 1:
            if (abs(TargetLocation[0] - mapOffset[0]) <= 2) and (abs(TargetLocation[1] - mapOffset[1]) <= 2):
                TargetLocation[2] = 0
                mapOffset[0] = round(TargetLocation[0])
                mapOffset[1] = round(TargetLocation[1])
            else:
                mapOffset[0] += round((TargetLocation[0] - mapOffset[0])/3 + 1 * (TargetLocation[0] - mapOffset[0])/max(abs(TargetLocation[0] - mapOffset[0]), 0.1))
                mapOffset[1] += round((TargetLocation[1] - mapOffset[1])/3 + 1 * (TargetLocation[1] - mapOffset[1])/max(abs(TargetLocation[1] - mapOffset[1]), 0.1))
    
    




    elif phase.lower() == "room":

        # itemObjects["RoomSize"]["animation frames"][0] = pyterm.addBorder("".join("".join(" " for i2 in range(round((room_size[0] - 1)/2 + 1))) + "\n" for i3 in range(round((room_size[1] - 1)/2 + 1))), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})
        itemObjects["RoomSize"]["animation frames"][0] = pyterm.addBorder("".join("".join(" " for i2 in range(room_size[0])) + "\n" for i3 in range(room_size[1])), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})

        pyterm.renderItem("RoomSize", screenLimits= (999, 999))

        pyterm.renderItem("PlayerMove", xBias = round(player_x), yBias = round(player_y))

        if keyboard.is_pressed("w"):
            if pyterm.getLetter((round(player_x + os.get_terminal_size().columns/2), round(player_y - 1 + os.get_terminal_size().lines/2))) not in room_walls:
                player_y -= 0.15 / ((math.sqrt(2) - 1) * (keyboard.is_pressed("a") or keyboard.is_pressed("d")) + 1)
        if keyboard.is_pressed("s"):
            if pyterm.getLetter((round(player_x + os.get_terminal_size().columns/2), round(player_y + 1 + os.get_terminal_size().lines/2))) not in room_walls:
                player_y += 0.15 / ((math.sqrt(2) - 1) * (keyboard.is_pressed("a") or keyboard.is_pressed("d")) + 1)
        if keyboard.is_pressed("a"):
            if pyterm.getLetter((round(player_x - 1 + os.get_terminal_size().columns/2), round(player_y + os.get_terminal_size().lines/2))) not in room_walls:
                player_x -= 0.3 / ((math.sqrt(2) - 1) * (keyboard.is_pressed("w") or keyboard.is_pressed("s")) + 1)
        if keyboard.is_pressed("d"):
            if pyterm.getLetter((round(player_x + 1 + os.get_terminal_size().columns/2), round(player_y + os.get_terminal_size().lines/2))) not in room_walls:
                player_x += 0.3 / ((math.sqrt(2) - 1) * (keyboard.is_pressed("w") or keyboard.is_pressed("s")) + 1)


    # fmt: on
    elif phase.lower() == "battle":
        for button in buttons:
            button=button+" button"
            if YiPyterminal.checkItemIsHovered(button):
                YiPyterminal.updateItemFrame(button,1)
            else:
                if YiPyterminal.itemObjects[button]["current frame"]==1:
                    YiPyterminal.updateItemFrame(button,0)
            YiPyterminal.renderItem(button,screenLimits=None)
        for item in ["center button barrier","left button barrier","right button barrier"]:
            YiPyterminal.renderItem(item,screenLimits=None)
        
    # fmt: off

    #Ui
    if Ui:
        if (round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 68 + UiOffset[0] <= location[0] <= round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 86 + UiOffset[0]) and (NonCenterOffset + UiOffset[1] <= location[1] <= NonCenterOffset + 5 + UiOffset[1]):
            pyterm.updateItemFrame("Ui", 1)
        elif (round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 88 + UiOffset[0] <= location[0] <= round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 106 + UiOffset[0]) and (NonCenterOffset + UiOffset[1] <= location[1] <= NonCenterOffset + 5 + UiOffset[1]):
            pyterm.updateItemFrame("Ui", 2)
        else:
            pyterm.updateItemFrame("Ui", 0)
        pyterm.renderItem("Ui", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + UiOffset[0], yBias = NonCenterOffset + UiOffset[1], screenLimits=(999, 999))

    itemObjects["UiLevel"]["animation frames"][0] = str(level)
    if experience < 10**3:
        experience_copy = str(experience)
    elif 10**3 <= experience < 10**4:
        experience_copy = str(round(experience/10**2)/10) + "k"
    elif 10**3 <= experience < 10**6:
        experience_copy = str(round(experience/10**3)) + "k"
    elif 10**6 <= experience < 10**7:
        experience_copy = str(round(experience/10**5)/10) + "m"
    elif 10**6 <= experience < 10**9:
        experience_copy = str(round(experience/10**6)) + "m"
    elif 10**9 <= experience < 10**10:
        experience_copy = str(round(experience/10**8)/10) + "b"
    elif 10**9 <= experience < 10**12:
        experience_copy = str(round(experience/10**9)) + "b"
    elif 10**12 <= experience < 10**13:
        experience_copy = str(round(experience/10**11)/10) + "t"
    elif 10**12 <= experience < 10**15:
        experience_copy = str(round(experience/10**12)) + "t"
    else:
        experience_copy = "NaneInf"
    if max_experience < 10**3:
        max_experience_copy = str(max_experience)
    elif 10**3 <= max_experience < 10**4:
        max_experience_copy = str(round(max_experience/10**2)/10) + "k"
    elif 10**3 <= max_experience < 10**6:
        max_experience_copy = str(round(max_experience/10**3)) + "k"
    elif 10**6 <= max_experience < 10**7:
        max_experience_copy = str(round(max_experience/10**5)/10) + "m"
    elif 10**6 <= max_experience < 10**9:
        max_experience_copy = str(round(max_experience/10**6)) + "m"
    elif 10**9 <= max_experience < 10**10:
        max_experience_copy = str(round(max_experience/10**8)/10) + "b"
    elif 10**9 <= max_experience < 10**12:
        max_experience_copy = str(round(max_experience/10**9)) + "b"
    elif 10**12 <= max_experience < 10**13:
        max_experience_copy = str(round(max_experience/10**11)/10) + "t"
    elif 10**12 <= max_experience < 10**15:
        max_experience_copy = str(round(max_experience/10**12)) + "t"
    else:
        max_experience_copy = "NaneInf"
    
    if light < 10**3:
        light_copy = str(light)
    elif 10**3 <= light < 10**4:
        light_copy = str(round(light/10**2)/10) + "k"
    elif 10**3 <= light < 10**6:
        light_copy = str(round(light/10**3)) + "k"
    elif 10**6 <= light < 10**7:
        light_copy = str(round(light/10**5)/10) + "m"
    elif 10**6 <= light < 10**9:
        light_copy = str(round(light/10**6)) + "m"
    elif 10**9 <= light < 10**10:
        light_copy = str(round(light/10**8)/10) + "b"
    elif 10**9 <= light < 10**12:
        light_copy = str(round(light/10**9)) + "b"
    elif 10**12 <= light < 10**13:
        light_copy = str(round(light/10**11)/10) + "t"
    elif 10**12 <= light < 10**15:
        light_copy = str(round(light/10**12)) + "t"
    else:
        light_copy = "NaneInf"
    if research < 10**3:
        research_copy = str(research)
    elif 10**3 <= research < 10**4:
        research_copy = str(round(research/10**2)/10) + "k"
    elif 10**3 <= research < 10**6:
        research_copy = str(round(research/10**3)) + "k"
    elif 10**6 <= research < 10**7:
        research_copy = str(round(research/10**5)/10) + "m"
    elif 10**6 <= research < 10**9:
        research_copy = str(round(research/10**6)) + "m"
    elif 10**9 <= research < 10**10:
        research_copy = str(round(research/10**8)/10) + "b"
    elif 10**9 <= research < 10**12:
        research_copy = str(round(research/10**9)) + "b"
    elif 10**12 <= research < 10**13:
        research_copy = str(round(research/10**11)/10) + "t"
    elif 10**12 <= research < 10**15:
        research_copy = str(round(research/10**12)) + "t"
    else:
        research_copy = "NaneInf"
    
    itemObjects["UiLevelBar"]["animation frames"][0] = min(round(level / 2), 15) * "*"
    itemObjects["UiExpBar"]["animation frames"][0] = round(15 * experience / max_experience) * "*"

    itemObjects["UiExp"]["animation frames"][0] = "(" + str(experience_copy) + "/" + str(max_experience_copy) + ")"
    itemObjects["Light"]["animation frames"][0] = str(light_copy)
    itemObjects["Research"]["animation frames"][0] = str(research_copy)
    pyterm.renderItem("UiLevel", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 34, yBias = NonCenterOffset + 2, screenLimits=(999, 999))
    pyterm.renderItem("UiExp", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 34, yBias = NonCenterOffset + 3, screenLimits=(999, 999))
    pyterm.renderItem("UiLevelBar", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 17, yBias = NonCenterOffset + 2, screenLimits=(999, 999))
    pyterm.renderItem("UiExpBar", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 17, yBias = NonCenterOffset + 3, screenLimits=(999, 999))
    pyterm.renderItem("Light", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 57, yBias = NonCenterOffset + 2, screenLimits=(999, 999))
    pyterm.renderItem("Research", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 57, yBias = NonCenterOffset + 3, screenLimits=(999, 999))

    




    # pyterm.renderLiteralItem(assets["EmptyBackground"], 0, 0, "center", "center")
    pyterm.renderLiteralItem(str(location) + " " + str(LeftClick) + " " + str(RightClick) + " " + str(character_size) + str(max_experience) + " " + str(level), 0, 0, "bottom left", "bottom left")
    pyterm.renderLiteralItem("1", 78, 21, "center", "center")
    pyterm.renderLiteralItem("2", -78, -20, "center", "center")
#34, 3
    pyterm.renderScreen()
    elapsedTime = time.perf_counter() - startTime
    if elapsedTime < (1 / pyterm.FPS):
        time.sleep((1 / pyterm.FPS) - elapsedTime)
    pyterm.displayScreen()
