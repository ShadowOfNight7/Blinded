import keyboard, random, math, time, sys, os, mouse, ctypes
from Testing.YiPyterminal import Pyterminal, assets
import Testing.Cursor as Cursor
import Testing.MouseDetect as MouseDetect
import Testing.AttackTest as AttackTest
import Assets.YiPyterminal as pyterm
from Assets.YiPyterminal import itemObjects


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


def PhaseChange(Phase: str):
    global phase, riseTitle, rise, Settings, SevenSins, mapOffset, InitialHold, locationMapDiff, mapOffsetCopy
    phase = Phase
    if phase.lower() == "title":
        riseTitle = 0
        rise = False
        Settings = False
        SevenSins = False
    if phase.lower() == "map":
        mapOffset = [0, 0]
        InitialHold = (0, 0)
        locationMapDiff = [0, 0]
        mapOffsetCopy = [0, 0]







#Oddly Specific Functions
def SetRoomPhase(id: tuple):
    global ClearedRooms, itemObjects, hierarchyLocations
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
        itemObjects[str(id)]["animation frames"][0] = "".join(random.choice('*&^%$#@!') if ch=='#' else ch for ch in assets.get("FilledBlackHoleFar"))
    return None






timed = 99
AimTarget = []
character_size = (19, 37) #NORMAL
character_size = (9, 19) #PC
# character_size = Cursor.initialize(2)
score = 0

MainClock = 1000
FalseTime = time.time()
transparency = 1

phase = "map"


#Oddly Specific Variables
riseTitle = 0
rise = False
Settings = False
SevenSins = False

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






while True:
    startTime = time.perf_counter()
    pyterm.clearLettersToRender()
    pyterm.updateKeyboardBindStatus()
    MainClock += 1

    #Code Start

    ctypes.windll.user32.OpenClipboard()
    ctypes.windll.user32.EmptyClipboard()
    # ctypes.windll.user32.CloseClipboard()

    # keyboard.block_key("ctrl")
    location = Cursor.get_mouse_coords(character_size, True)
    

    if phase.lower() == "title":
        pyterm.renderLiteralItem(assets["background"], 0, 0, "center", "center")
        pyterm.renderLiteralItem(assets["TitleOptions"], 40, -8 - max(riseTitle - 3, 0), "center", "center")
        pyterm.renderLiteralItem(assets["TitlePlay"], -40, -3 - max(riseTitle, 0), "center", "center")
        pyterm.renderLiteralItem(assets["Title1"], 0, -22 - max(riseTitle - 8, 0), "center", "center")
        if ((-63 + os.get_terminal_size().columns/2) <= location[0] <= (-19 + os.get_terminal_size().columns/2)) and ((8 + os.get_terminal_size().lines/2) <= location[1] <= (14 + os.get_terminal_size().lines/2)) and (riseTitle == 0) and (not (Settings or SevenSins)):
            pyterm.renderLiteralItem(assets["TitlePlayHover"], -40, -3, "center", "center")
            if MouseDetect.ClickDetect("Left", "On"):
                rise = True
                SevenSins = True
        if ((17 + os.get_terminal_size().columns/2) <= location[0] <= (61 + os.get_terminal_size().columns/2)) and ((1 + os.get_terminal_size().lines/2) <= location[1] <= (8 + os.get_terminal_size().lines/2)) and (riseTitle == 0) and (not (Settings or SevenSins)):
            pyterm.renderLiteralItem(assets["TitleOptionsHover"], 40, -8, "center", "center")
            if MouseDetect.ClickDetect("Left", "On"):
                rise = True
                Settings = True
        #Settings Overlay
        if Settings:
            pyterm.renderLiteralItem(assets["TitleSettings"], 0, -70 + min(riseTitle, 55), "center", "center")
            pyterm.renderLiteralItem(assets["TitleReturn"], -55, -90 + min(riseTitle, 60), "center", "center")
            if ((-73 + os.get_terminal_size().columns/2) <= location[0] <= (-39 + os.get_terminal_size().columns/2)) and ((-18 + os.get_terminal_size().lines/2) <= location[1] <= (-14 + os.get_terminal_size().lines/2)):
                pyterm.renderLiteralItem(assets["TitleReturnHover"], -55, -90 + min(riseTitle, 60), "center", "center")
                if MouseDetect.ClickDetect("Left", "On"):
                    rise = False
            if (riseTitle == 0) and (not rise):
                Settings = False
        
        #7Sins Overlay
        if SevenSins:
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
            if ((-73 + os.get_terminal_size().columns/2) <= location[0] <= (-39 + os.get_terminal_size().columns/2)) and ((-18 + os.get_terminal_size().lines/2) <= location[1] <= (-14 + os.get_terminal_size().lines/2)):
                pyterm.renderLiteralItem(assets["TitleReturnHover"], -55, -100 + riseTitle, "center", "center")
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
        
        if not GetRoomLoc:
            for Line in LinesRooms:
                # pyterm.renderItem(Line["Line"], xBias = round(Line["Pos"][0]) + mapOffset[0], yBias = round(Line["Pos"][1]) + mapOffset[1])
                pyterm.renderItem(str(Line["Pos1"]) + str(Line["Pos2"]), xBias=mapOffset[0], yBias=mapOffset[1])

        if GetRoomLoc:
            roomLoc = pyterm.renderLiteralItem(assets.get("FilledBlackHole"), 0, 0, "center", "center")
            pyterm.createItem(str((0, 1)), [assets["FilledBlackHole"]], "screen", "center", "center", 0, 0, 0)
            hierarchyLocations.append([{"Location": roomLoc, "id": (0, 1), "Connections": [], "Movements": []}])
        pyterm.renderItem(str((0, 1)), xBias = mapOffset[0], yBias = mapOffset[1])
        pyterm.renderLiteralItem("x", round(mapOffset[0]), round(mapOffset[1]), "center", "center")
        for i in range(Hierarchy):
            MaxRooms = (i + 1) * 3 + 1
            Angle = 360/MaxRooms
            for i2 in range(MaxRooms):
                if GetRoomLoc:
                    roomLoc = pyterm.renderLiteralItem(assets.get("FilledBlackHole"), round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3) + mapOffset[0]), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2 + mapOffset[1]), "center", "center")
                    pyterm.createItem(str((i + 1, i2 + 1)), [assets.get("FilledBlackHole")], "screen", "center", "center", 0, round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2))
                    hierarchyLocations2.append({"Location": roomLoc, "id": (i + 1, i2 + 1), "Connections": [], "Movements": []}) #Connections: [{"id": (_, _), "Location": (_, _)}]
                else:
                    # if math.dist(hierarchyLocations[i][i2]["Location"], (-mapOffset[0], -mapOffset[1])) <= (10 + math.hypot(os.get_terminal_size().columns/2, os.get_terminal_size().lines/2)):
                    pyterm.renderItem(str((i + 1, i2 + 1)), xBias = mapOffset[0], yBias = mapOffset[1])
                    # pyterm.renderLiteralItem(str(hierarchyLocations[i + 1][i2]["Movements"]), round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3) + mapOffset[0]), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2 + mapOffset[1]), "center", "center")
                    # pyterm.renderLiteralItem(assets.get("FilledBlackHole"), round(math.cos(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3) + mapOffset[0]), round(math.sin(math.radians(Angle * i2 + RandomAdd[i] + RandomAddMini[i][i2])) * MaxRooms * (10 + i/3)/2 + mapOffset[1]), "center", "center")
            if GetRoomLoc == True:
                hierarchyLocations.append(hierarchyLocations2)
                hierarchyLocations2 = []

        if GetRoomLoc:
            for tier in hierarchyLocations:
                for rooms in tier:
                    if rooms["id"][0] != 0:
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
                        if random.randint(1, Fractured) <= Unfractured:
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

        if MouseDetect.ClickDetect("Right", "On"):
            InitialHold = location
            mapOffsetCopy = mapOffset.copy()
        elif MouseDetect.ClickDetect("Right", "Held"):
            locationMapDiff = [location[0] - InitialHold[0], location[1] - InitialHold[1]]
            mapOffset = [mapOffsetCopy[0] + locationMapDiff[0], mapOffsetCopy[1] + locationMapDiff[1]]

        if keyboard.is_pressed("w"):
            mapOffset[1] += 2
        if keyboard.is_pressed("s"):
            mapOffset[1] -= 2
        if keyboard.is_pressed("a"):
            mapOffset[0] += 4
        if keyboard.is_pressed("d"):
            mapOffset[0] -= 4



    pyterm.renderLiteralItem(assets["EmptyBackground"], 0, 0, "center", "center")
    pyterm.renderLiteralItem(str(location) + " " + str(MouseDetect.ClickDetect("Left", "On")), 0, 0, "bottom left", "bottom left")


    pyterm.renderScreen()
    elapsedTime = time.perf_counter() - startTime
    if elapsedTime < (1 / pyterm.FPS):
        time.sleep((1 / pyterm.FPS) - elapsedTime)
    pyterm.displayScreen()

