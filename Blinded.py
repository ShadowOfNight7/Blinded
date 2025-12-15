import keyboard, random, math, time, sys, os, mouse, ctypes, copy
from Testing.YiPyterminal import assets
import Testing.Cursor as Cursor
import Testing.MouseDetect as MouseDetect
import Testing.AttackTest as AttackTest
import Assets.YiPyterminal as pyterm
from Assets.YiPyterminal import itemObjects
import Assets.YiPyterminal as YiPyterminal

os.system("cls")
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

battles = 0
enemiesKilled = 0
highestHierarchy = 0


# fmt: on
def PhaseChange(Phase: str):
    global phase, riseTitle, rise, Settings, SevenSins, mapOffset, InitialHold, locationMapDiff, mapOffsetCopy, TargetLocation, FocusRoom, AnimateRoomEntry, player_x, player_y, Ui, EnteredRoom, RoomData, room_push, room_invis_walls
    phase = Phase
    if phase.lower() == "title":
        riseTitle = 0
        rise = False
        Settings = False
        SevenSins = False
        Ui = False
    elif phase.lower() == "map":
        global firstFrame
        mapOffset = [0, 0]
        InitialHold = (0, 0)
        locationMapDiff = [0, 0]
        mapOffsetCopy = [0, 0]
        TargetLocation = [0, 0, 0]
        FocusRoom = {
            "Location": (0, 0),
            "id": (0, 1),
            "Connections": [],
            "Movements": [],
        }
        FocusRoom = False
        AnimateRoomEntry = False
        Ui = True
        firstFrame = copy.deepcopy(MainClock)
    elif phase.lower() == "room":
        if RoomData[EnteredRoom]["Type"] != "Puzzle":
            player_x, player_y = RoomData[EnteredRoom]["SpawnLocation"]
        else:
            player_x, player_y = RoomData[EnteredRoom]["Special"]["SpawnLocation"][0] + 3, RoomData[EnteredRoom]["Special"]["SpawnLocation"][1] + 1
        room_push = []
        room_invis_walls = []
        Ui = True
    elif phase.lower() == "puzzlemove":
        pass
    elif phase.lower() == "puzzletext":
        pass
    elif phase.lower() == "battle":
        global mobsStatus, currentMob, selectedButton, clickedMobOption, hoveredMobOption, selectedAttack, selectedMobNum, isUltimateSelected, UltimateAnimationFrame, UltimateCharge, whisperOfTheUltimate, isUltimateClicked, battleMessages, isInfoBarInMessageMode, difficulty, TotalResearch, TotalItems, TotalExp
        selectedButton = None
        clickedMobOption = None
        hoveredMobOption = None
        selectedAttack = None
        selectedMobNum = None
        isUltimateSelected = False
        isUltimateClicked = False
        whisperOfTheUltimate = None
        UltimateAnimationFrame = 1
        UltimateCharge = 0
        # mobsStatus = ["Slimea", "Slime2"]
        currentMob = 0
        battleMessages = ["Nothing has happened yet...", "", "", ""]
        isInfoBarInMessageMode = False
        for mobNum in range(len(mobsStatus)):
            mobsStatus[mobNum] = copy.deepcopy(enemies[mobsStatus[mobNum]])
        YiPyterminal.createItem(
            "center barrier",
            YiPyterminal.ASSETS["center barrier"],
            parentAnchor="bottom center",
            childAnchor="bottom center",
        )
        YiPyterminal.createItem(
            "items button",
            YiPyterminal.ASSETS["items button"],
            parentObject="center barrier",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "information button",
            YiPyterminal.ASSETS["information button"],
            parentObject="center barrier",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        YiPyterminal.createItem(
            "left center barrier",
            YiPyterminal.ASSETS["center barrier"],
            parentObject="items button",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "right center barrier",
            YiPyterminal.ASSETS["center barrier"],
            parentObject="information button",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        YiPyterminal.createItem(
            "fight button",
            YiPyterminal.ASSETS["fight button"],
            parentObject="left center barrier",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "run button",
            YiPyterminal.ASSETS["run button"],
            parentObject="right center barrier",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        YiPyterminal.createItem(
            "left barrier",
            YiPyterminal.ASSETS["left barrier"],
            parentObject="fight button",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "right barrier",
            YiPyterminal.ASSETS["right barrier"],
            parentObject="run button",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        for box in ["fight box", "items box", "information box", "run box"]:
            if box == "fight box":
                _attacks = []
                for attackNum in range(8):
                    if LockedAttacks["Attack" + str(attackNum)] == True:
                        _attacks.append("LOCKED".center(30))
                    elif EquippedAttacks["Attack" + str(attackNum)] == None:
                        _attacks.append("".center(30))
                    else:
                        _attacks.append(
                            EquippedAttacks["Attack" + str(attackNum)].center(30)
                        )
                YiPyterminal.createItem(
                    box,
                    [
                        copy.deepcopy(YiPyterminal.ASSETS[box][0])
                        .replace(">        PLACEHOLDER1        <", _attacks[0])
                        .replace(">        PLACEHOLDER2        <", _attacks[1])
                        .replace(">        PLACEHOLDER3        <", _attacks[2])
                        .replace(">        PLACEHOLDER4        <", _attacks[3])
                        .replace(">        PLACEHOLDER5        <", _attacks[4])
                        .replace(">        PLACEHOLDER6        <", _attacks[5])
                        .replace(">        PLACEHOLDER7        <", _attacks[6])
                        .replace(">        PLACEHOLDER8        <", _attacks[7]),
                        copy.deepcopy(YiPyterminal.ASSETS[box][1])
                        .replace(">        PLACEHOLDER1        <", _attacks[0])
                        .replace(">        PLACEHOLDER2        <", _attacks[1])
                        .replace(">        PLACEHOLDER3        <", _attacks[2])
                        .replace(">        PLACEHOLDER4        <", _attacks[3])
                        .replace(">        PLACEHOLDER5        <", _attacks[4])
                        .replace(">        PLACEHOLDER6        <", _attacks[5])
                        .replace(">        PLACEHOLDER7        <", _attacks[6])
                        .replace(">        PLACEHOLDER8        <", _attacks[7]),
                    ],
                    parentObject="center barrier",
                    parentAnchor="top center",
                    childAnchor="top center",
                )
                YiPyterminal.createItem(
                    "attack option 1",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack0"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack0"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack0"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack0"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom right",
                    xBias=-32,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 2",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack1"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack1"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack1"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack1"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom right",
                    xBias=-1,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 3",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack2"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack2"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack2"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack2"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom left",
                    xBias=1,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 4",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack3"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack3"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack3"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack3"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom left",
                    xBias=32,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 5",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack4"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack4"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack4"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack4"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="top right",
                    xBias=-32,
                    yBias=1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 6",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack5"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack5"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack5"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack5"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="top right",
                    xBias=-1,
                    yBias=1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 7",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack6"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack6"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack6"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack6"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="top left",
                    xBias=1,
                    yBias=1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 8",
                    (
                        [
                            "".center(30, "š"),
                            (
                                ">" + "š" * (len(EquippedAttacks["Attack7"]) + 2) + "<"
                            ).center(30, "š"),
                            "š╠"
                            + ("š" * (len(EquippedAttacks["Attack7"]) + 2)).center(
                                26, "š"
                            )
                            + "╣š",
                            "š╠"
                            + (
                                ">" + "š" * (len(EquippedAttacks["Attack7"]) + 2) + "<"
                            ).center(26, "š")
                            + "╣š",
                        ]
                        if EquippedAttacks["Attack7"] != None
                        else [
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                            "".center(30, "š"),
                        ]
                    ),
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="top left",
                    xBias=32,
                    yBias=1,
                    isEmptyCharacterPartOfHitbox=True,
                )
            else:
                YiPyterminal.createItem(
                    box,
                    YiPyterminal.ASSETS[box],
                    parentObject="center barrier",
                    parentAnchor="top center",
                    childAnchor="top center",
                )
        YiPyterminal.createItem(
            "ultimate bar",
            copy.deepcopy(YiPyterminal.ASSETS["ultimate bar"]),
            parentObject="fight box",
            parentAnchor="top center",
            childAnchor="bottom center",
            yBias=10,
        )
        YiPyterminal.createItem(
            "ultimate button",
            copy.deepcopy(YiPyterminal.ASSETS["ultimate button"]),
            parentObject="fight box",
            parentAnchor="center",
            childAnchor="center",
            yBias=100,
        )
        YiPyterminal.createItem(
            "enemy selection box",
            copy.deepcopy(YiPyterminal.ASSETS["enemy selection box"]),
            parentAnchor="left center",
            childAnchor="left center",
        )
        ChangeEnemySelection()
        YiPyterminal.createItem(
            "enemy information box",
            copy.deepcopy(YiPyterminal.ASSETS["enemy information box"]),
            parentAnchor="right center",
            childAnchor="right center",
        )
        YiPyterminal.createItem(
            "info bar",
            copy.deepcopy(YiPyterminal.ASSETS["info bar"]),
            parentAnchor="top center",
            childAnchor="top center",
            yBias=1,
        )
        for i in mobsStatus:
            for i2 in i["Stats"].keys():
                i["Stats"][i2] = round(i["Stats"][i2] * difficulty)
        TotalResearch = 0
        TotalItems = []
        TotalExp = 0

def ChangeEnemySelection():
    global mobStatus
    if len(mobsStatus) >= 1:
        YiPyterminal.createItem(
            "enemy selection option 1",
            [
                " " * 30
                + "\n"
                + mobsStatus[0]["Name"].center(30)
                + "\n"
                + " " * 30,
                " " * 30
                + "\n"
                + ("> " + mobsStatus[0]["Name"] + " <").center(30)
                + "\n"
                + " " * 30,
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    mobsStatus[0]["Name"].center(26),
                ),
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    ("> " + mobsStatus[0]["Name"] + " <").center(26),
                ),
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=1,
        )
    else:
        YiPyterminal.createItem(
            "enemy selection option 1",
            [
                " " * 30 + "\n" + " " * 30 + "\n" + " " * 30,
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=1,
        )
    if len(mobsStatus) >= 2:
        YiPyterminal.createItem(
            "enemy selection option 2",
            [
                " " * 30
                + "\n"
                + mobsStatus[1]["Name"].center(30)
                + "\n"
                + " " * 30,
                " " * 30
                + "\n"
                + ("> " + mobsStatus[1]["Name"] + " <").center(30)
                + "\n"
                + " " * 30,
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <", mobsStatus[1]["Name"].center(26)
                ),
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    ("> " + mobsStatus[1]["Name"] + " <").center(26),
                ),
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=5,
        )
    else:
        YiPyterminal.createItem(
            "enemy selection option 2",
            [
                " " * 30 + "\n" + " " * 30 + "\n" + " " * 30,
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=5,
        )
    if len(mobsStatus) >= 3:
        YiPyterminal.createItem(
            "enemy selection option 3",
            [
                " " * 30
                + "\n"
                + mobsStatus[2]["Name"].center(30)
                + "\n"
                + " " * 30,
                " " * 30
                + "\n"
                + ("> " + mobsStatus[2]["Name"] + " <").center(30)
                + "\n"
                + " " * 30,
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <", mobsStatus[2]["Name"].center(26)
                ),
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    ("> " + mobsStatus[2]["Name"] + " <").center(26),
                ),
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=9,
        )
    else:
        YiPyterminal.createItem(
            "enemy selection option 3",
            [
                " " * 30 + "\n" + " " * 30 + "\n" + " " * 30,
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=9,
        )
    if len(mobsStatus) >= 4:
        YiPyterminal.createItem(
            "enemy selection option 4",
            [
                " " * 30
                + "\n"
                + mobsStatus[3]["Name"].center(30)
                + "\n"
                + " " * 30,
                " " * 30
                + "\n"
                + ("> " + mobsStatus[3]["Name"] + " <").center(30)
                + "\n"
                + " " * 30,
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <", mobsStatus[3]["Name"].center(26)
                ),
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    ("> " + mobsStatus[3]["Name"] + " <").center(26),
                ),
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=13,
        )
    else:
        YiPyterminal.createItem(
            "enemy selection option 4",
            [
                " " * 30 + "\n" + " " * 30 + "\n" + " " * 30,
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=13,
        )
    if len(mobsStatus) >= 5:
        YiPyterminal.createItem(
            "enemy selection option 5",
            [
                " " * 30
                + "\n"
                + mobsStatus[4]["Name"].center(30)
                + "\n"
                + " " * 30,
                " " * 30
                + "\n"
                + ("> " + mobsStatus[4]["Name"] + " <").center(30)
                + "\n"
                + " " * 30,
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <", mobsStatus[4]["Name"].center(26)
                ),
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    ("> " + mobsStatus[4]["Name"] + " <").center(26),
                ),
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=17,
        )
    else:
        YiPyterminal.createItem(
            "enemy selection option 5",
            [
                " " * 30 + "\n" + " " * 30 + "\n" + " " * 30,
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=17,
        )
    if len(mobsStatus) >= 6:
        YiPyterminal.createItem(
            "enemy selection option 6",
            [
                " " * 30
                + "\n"
                + mobsStatus[5]["Name"].center(30)
                + "\n"
                + " " * 30,
                " " * 30
                + "\n"
                + ("> " + mobsStatus[5]["Name"] + " <").center(30)
                + "\n"
                + " " * 30,
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <", mobsStatus[5]["Name"].center(26)
                ),
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    ("> " + mobsStatus[5]["Name"] + " <").center(26),
                ),
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=21,
        )
    else:
        YiPyterminal.createItem(
            "enemy selection option 6",
            [
                " " * 30 + "\n" + " " * 30 + "\n" + " " * 30,
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=21,
        )
    if len(mobsStatus) >= 7:
        YiPyterminal.createItem(
            "enemy selection option 7",
            [
                " " * 30
                + "\n"
                + mobsStatus[6]["Name"].center(30)
                + "\n"
                + " " * 30,
                " " * 30
                + "\n"
                + ("> " + mobsStatus[6]["Name"] + " <").center(30)
                + "\n"
                + " " * 30,
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <", mobsStatus[6]["Name"].center(26)
                ),
                YiPyterminal.ASSETS["enemy selection option"][0].replace(
                    ">                        <",
                    ("> " + mobsStatus[6]["Name"] + " <").center(26),
                ),
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=25,
        )
    else:
        YiPyterminal.createItem(
            "enemy selection option 7",
            [
                " " * 30 + "\n" + " " * 30 + "\n" + " " * 30,
            ],
            parentObject="enemy selection box",
            parentAnchor="top center",
            childAnchor="top center",
            xBias=-2,
            yBias=25,
        )

# fmt: off

#Oddly Specific Functions
def SetRoomPhase(id: tuple):
    global ClearedRooms, itemObjects, hierarchyLocations, SettingsRooms, light, RoomData
    if (id in ClearedRooms):
        if not (assets.get("FilledBlackHole") in itemObjects[str(id)]["animation frames"]):
            itemObjects[str(id)]["animation frames"][0] = assets.get("FilledBlackHole")
            itemObjects[str(id)]["animation frames"][1] = assets.get("FilledBlackHole")
        return None
    for ids in ClearedRooms:
        for connections in hierarchyLocations[ids[0]][ids[1] - 1]["Movements"]:
            if (id == connections["id"]) and (RoomData[id]["LightRequired"] <= light):
                if not (assets.get("FilledBlackHoleClose") in itemObjects[str(id)]["animation frames"]):
                    itemObjects[str(id)]["animation frames"][0] = assets.get("FilledBlackHoleClose")
                    itemObjects[str(id)]["animation frames"][1] = assets.get("FilledBlackHoleClose")
                return None
    else:
        if (SettingsRooms == 1):
            pyterm.changeCurrentItemFrame(str(id), 0)
        elif (SettingsRooms == 2):
            pyterm.changeCurrentItemFrame(str(id), 1)
        elif (SettingsRooms == 3):
            pyterm.changeCurrentItemFrame(str(id), 1)
            itemObjects[str(id)]["animation frames"][1] = "".join(random.choice('*&^%$#@!') if a=='#' else a for a in assets.get("FilledBlackHoleFar"))
    return None

def UseInvItem(Item):
    global Inventory, Equipment, player, FocusAttack, ChooseAttack
    if Item["Type"] == "Armor":
        UnequipInvItem(Equipment["Armor"])
        Equipment["Armor"] = Item
        RemoveInvItem(Item)
    elif Item["Type"] == "Weapon":
        UnequipInvItem(Equipment["Weapon"])
        Equipment["Weapon"] = Item
        RemoveInvItem(Item)
    elif Item["Type"] == "Offhand":
        UnequipInvItem(Equipment["Offhand"])
        Equipment["Offhand"] = Item
        RemoveInvItem(Item)
    elif Item["Type"] == "Accessory":
        UnequipInvItem(Equipment["Extra"])
        Equipment["Extra"] = Item
        RemoveInvItem(Item)
    elif Item["Type"] == "Consumable":
        for effect in Item["Effects"]:
            player["Effects"].append(copy.deepcopy(effect))
        RemoveInvItem(Item)
    elif Item["Type"] == "Attack":
        ChooseAttack = True
        FocusAttack = Item["Attack"]
    else:
        return False

def AddInvItem(Item):
    global Inventory, MainClock
    if Item["Id"] == None:
        Item["Id"] = MainClock
        MainClock += 1
    if Item["Type"] == "Armor":
        Inventory["Armor"].append(Item)
    elif Item["Type"] == "Weapon":
        Inventory["Weapon"].append(Item)
    elif Item["Type"] == "Offhand":
        Inventory["Offhand"].append(Item)
    elif Item["Type"] == "Accessory":
        Inventory["Accessory"].append(Item)
    else:
        Inventory["Misc"].append(Item)

def RemoveInvItem(Item):
    global Inventory
    for types in Inventory.keys():
        if Item in Inventory[types]:
            Inventory[types].remove(Item)
            return True
    return False

def UnequipInvItem(Item, KeepItem = True):
    global Inventory, Equipment
    if Item == None:
        return True
    for types in Equipment.keys():
        if Item is Equipment[types]:
            Equipment[types] = None
            if KeepItem:
                AddInvItem(Item)
            return True
    return False

def ApplyInvItemBuffs(Item):
    global player, EquippedUltimate
    if Item != None:
        for stat in Item["Stats"].keys():
            player["Effects"].append({"Stat": stat, "Potency": Item["Stats"][stat], "Time": -2})
    if "Ultimate" in list(Item.keys()):
        EquippedUltimate = Item["Ultimate"]["Ultimate"]
    #{"Name": "The Death Star", "Type": "Weapon", "Asset": assets.get(""), "Stats": {"Dexterity": 1, "Strength": 1, "Accuracy": 1}, "Ultimate": {"Description": "apple", "..."}, "Description": "A death star that's deadly and a star.", "Id": None}

def NegateInvItemBuffs(Item):
    global player
    if Item != None:
        for stat in Item["Stats"].keys():
            player["Effects"].remove({"Stat": stat, "Potency": Item["Stats"][stat], "Time": -2})


def RenderSpell(Spell):
    for spell in range(len(Spell)):
        if spell != 0:
            itemObjects["EnchantLine"]["animation frames"][0] = pyterm.generateLine(Spell[spell], Spell[spell - 1])
            pyterm.updateItemSize("EnchantLine")
            pyterm.renderItem("EnchantLine", xBias = round((Spell[spell][0] + Spell[spell - 1][0])/2), yBias = round((Spell[spell][1] + Spell[spell - 1][1])/2), screenLimits=(73,25), screenLimitsBias=(0, -1))
            pyterm.renderItem("EnchantCircle", xBias = Spell[spell][0], yBias = Spell[spell][1], screenLimits=(73,25), screenLimitsBias=(0, -1))
        else:
            pyterm.renderItem("EnchantStar", xBias = Spell[spell][0], yBias = Spell[spell][1], screenLimits=(73,25), screenLimitsBias=(0, -1))


def PlayerAttack(Enemy: int, Attack = None, minigame = False):
    global player, mobsStatus, attacks, StatUpgrades, score, SevenBuff, location, Minigaming, SpeedMode, enemiesKilled, battles, selectedViewMobOption, hoveredMobOption, clickedMobOption, selectedMobNum, Equipment
    #Poisoning Burning Sharpened Lifesteal Embued Swift Defensive
    if Attack != None:
        if minigame:
            if attacks[Attack]["Minigames"][0] != None:
                attacks[Attack]["Minigames"][0]["Arg"]["location"] = copy.deepcopy(location)
                argsAttack = copy.deepcopy(attacks[Attack]["Minigames"][0]["Arg"])
                if SpeedMode:
                    if "Time" in list(argsAttack.keys()):
                        argsAttack["Time"] = round(argsAttack["Time"] / 2)
                        argsAttack["ScoreMulti"] *= 2
                Minigaming = Minigame(attacks[Attack]["Minigames"][0]["Name"], argsAttack)
                if Minigaming:
                    score = AttackTest.score
                else:
                    return False
                if attacks[Attack]["Minigames"][0]["Name"] in ["BlackHole", "Reaction", "Shielded", "CircleDefend", "DodgeGrid", "Rain"]:
                    score = (30 - score)
                score *= (1.2 if SevenBuff == "Envy" else 1)
                if (score >= 15) and (SevenBuff == "Pride"):
                    player["Effects"].append({"Stat": "Skill", "Potency": 30, "Time": 2})
                    player["Effects"].append({"Stat": "Intelligence", "Potency": 30, "Time": 2})
                score = max(min(score, 30), 0)
            else:
                score = 20 * (1.2 if SevenBuff == "Envy" else 1)
        else:
            score = 20 * (1.2 if SevenBuff == "Envy" else 1)

    mob = mobsStatus[Enemy]
    playercopy = copy.deepcopy(player)
    if StatUpgrades["Wisdom"]:
        playercopy["Skill"] *= 1.2
        playercopy["Intelligence"] *= 1.2
        playercopy["CritChance"] *= 1.2
        playercopy["CritPower"] *= 1.2
    if StatUpgrades["Efficient"]:
        playercopy["Dexterity"] *= 1.2
        playercopy["CastingSpeed"] *= 1.2
        playercopy["Regen"] *= 1.5
    if StatUpgrades["Truth"]:
        playercopy["TrueAttack"] *= 1.5
        playercopy["TrueDefence"] *= 1.5
    for effect in playercopy["Effects"]:
        playercopy[effect["Stat"]] += effect["Potency"] * (1.2 if SevenBuff == "Gluttony" else 1)
        if "Current" in effect["Stat"]:
            player[effect["Stat"]] += effect["Potency"] * (1.2 if SevenBuff == "Gluttony" else 1)
    for passive in playercopy["Passives"]:
        playercopy[passive["Stat"]] += passive["Potency"]
        if "Current" in passive:
            player[passive["Stat"]] += passive["Potency"]
    
    for effect in player["Effects"]:
        if effect["Time"] > 0:
            effect["Time"] -= 1
        if effect["Time"] == 0:
            effect["Time"] += 1
            if random.randint(0, 1000000) <= (200/(playercopy["Intelligence"]+200))*1000000:
                playercopy["Effects"].remove(effect)
    player["Effects"] = copy.deepcopy(playercopy["Effects"])

    player["CurrentHp"] = min(player["CurrentHp"] + playercopy["Regen"], playercopy["MaxHealth"])
    player["CurrentMana"] = min(player["CurrentMana"] + playercopy["ManaRegen"], playercopy["Mana"])
    player["CurrentEnergy"] = min(player["CurrentEnergy"] + playercopy["EnergyRegen"], playercopy["Energy"])

    #Math
    if Attack != None:
        if Equipment["Weapon"] != None:
            if "Enchant" in Equipment["Weapon"].keys():
                if "Poisoning" in Equipment["Weapon"]["Enchant"]:
                    if "+" in Equipment["Weapon"]["Enchant"]:
                        mob["Effects"].append({"Stat": "Strength", "Potency": -25, "Time": 4})
                    else:
                        mob["Effects"].append({"Stat": "Strength", "Potency": -10, "Time": 2})
                if "Burning" in Equipment["Weapon"]["Enchant"]:
                    if "+" in Equipment["Weapon"]["Enchant"]:
                        mob["Effects"].append({"Stat": "CurrentHp", "Potency": -70, "Time": 4})
                    else:
                        mob["Effects"].append({"Stat": "CurrentHp", "Potency": -30, "Time": 2})
                if "Sharpened" in Equipment["Weapon"]["Enchant"]:
                    if "+" in Equipment["Weapon"]["Enchant"]:
                        playercopy["Strength"] *= 1.25
                    else:
                        playercopy["Strength"] *= 1.1
                if "Embued" in Equipment["Weapon"]["Enchant"]:
                    if "+" in Equipment["Weapon"]["Enchant"]:
                        playercopy["MagicPower"] *= 1.25
                    else:
                        playercopy["MagicPower"] *= 1.1
                if "Swift" in Equipment["Weapon"]["Enchant"]:
                    if "+" in Equipment["Weapon"]["Enchant"]:
                        playercopy["Dexterity"] *= 1.35
                    else:
                        playercopy["Dexterity"] *= 1.15
                if "Dev" in Equipment["Weapon"]["Enchant"]:
                    if "+" in Equipment["Weapon"]["Enchant"]:
                        for i in playercopy.keys():
                            playercopy[i] *= 999999999
                        for i in player.keys():
                            player[i] *= 999999999
                    else:
                        for i in playercopy.keys():
                            playercopy[i] *= 999

            for effect in attacks[Attack]["Effects"]:
                if effect["Target"] == "Self":
                    player["Effects"].append(effect)
                elif effect["Target"] == "Enemy":
                    mob["Effects"].append(effect)
        # missed = not bool(random.randint(1, 10000) <= attacks[Attack]["Accuracy"] * 100)
        Heal = 0
        score *= (1 + playercopy["Skill"]/250)
        crit = 0
        for i in range(round(playercopy["Dexterity"]/100)):
            crit = (playercopy["CritPower"] if random.randint(1, 100) <= playercopy["CritChance"] else 0) if crit == 0 else crit
        MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + playercopy["Strength"] / 100) / (1 + mob["Stats"]["Defence"] / 100) * (1 + crit / 100) * (score / 10)
        MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + playercopy["MagicPower"] / 100) / (1 + mob["Stats"]["MagicDefence"] / 100) * (1 + crit / 100) * (score / 10)
        TrueDamage = (1 + playercopy["TrueAttack"] / 100) / (1 + mob["Stats"]["TrueDefence"] / 100) * (1 + crit / 100) * (score / 10)
        #After Specials - Lifesteal, Etc
        if attacks[Attack]["Special"] != None:
            for special in attacks[Attack]["Special"]:
                if "Pierce" in special:
                    MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + playercopy["Strength"] / 100) / (1 + mob["Stats"]["Defence"] * (1 - int(special.replace("Pierce", ""))/100) / 100) * (1 + crit / 100) * (score / 10)
                    MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + playercopy["MagicPower"] / 100) / (1 + mob["Stats"]["MagicDefence"] * (1 - int(special.replace("Pierce", ""))/100)  / 100) * (1 + crit / 100) * (score / 10)
                elif "Lifesteal" in special:
                    Heal = min(player["Health"] - player["CurrentHp"], (MagicDamage + MeleeDamage) * int(special.replace("Lifesteal", ""))/100)
                elif "Critical" in special:
                    crit = (playercopy["CritPower"] if random.randint(1, 100) * (1 - int(special.replace("Critical", ""))/100) <= playercopy["CritChance"] else 0)
                    MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + playercopy["Strength"] / 100) / (1 + mob["Stats"]["Defence"] / 100) * (1 + crit / 100) * (score / 10)
                    MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + playercopy["MagicPower"] / 100) / (1 + mob["Stats"]["MagicDefence"] / 100) * (1 + crit / 100) * (score / 10)
                    TrueDamage = (1 + playercopy["TrueAttack"] / 100) / (1 + mob["Stats"]["TrueDefence"] / 100) * (1 + crit / 100) * (score / 10)
                elif "Percent" in special:
                    MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + playercopy["Strength"] / 100) / (1 + mob["Stats"]["Defence"] / 100) * (1 + crit / 100) * (score / 10)
                    MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + playercopy["MagicPower"] / 100) / (1 + mob["Stats"]["MagicDefence"] / 100) * (1 + crit / 100) * (score / 10)
                    TrueDamage = (1 + playercopy["TrueAttack"] / 100) / (1 + mob["Stats"]["TrueDefence"] / 100) * (1 + crit / 100) * (score / 10) + mob["Stats"]["CurrentHp"] * int(special.replace("Percent", ""))/100
                elif "Status" in special:
                    MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + playercopy["Strength"] / 100) / (1 + mob["Stats"]["Defence"] / 100) * (1 + crit / 100) * (score / 10) * (1 + int(special.replace("Status", ""))/100 * len(mob["Effects"]))
                    MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + playercopy["MagicPower"] / 100) / (1 + mob["Stats"]["MagicDefence"] / 100) * (1 + crit / 100) * (score / 10) * (1 + int(special.replace("Status", ""))/100 * len(mob["Effects"]))
                    TrueDamage = (1 + playercopy["TrueAttack"] / 100) / (1 + mob["Stats"]["TrueDefence"] / 100) * (1 + crit / 100) * (score / 10) * (1 + int(special.replace("Status", ""))/100 * len(mob["Effects"]))
                elif "Damage" in special:
                    MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + playercopy["Strength"] / 100) / (1 + mob["Stats"]["Defence"] / 100) * (1 + crit / 100) * (score / 10) * (1 + int(special.replace("Damage", ""))/100)
                    MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + playercopy["MagicPower"] / 100) / (1 + mob["Stats"]["MagicDefence"] / 100) * (1 + crit / 100) * (score / 10) * (1 + int(special.replace("Damage", ""))/100)
                    TrueDamage = (1 + playercopy["TrueAttack"] / 100) / (1 + mob["Stats"]["TrueDefence"] / 100) * (1 + crit / 100) * (score / 10) * (1 + int(special.replace("Damage", ""))/100)

        if StatUpgrades["Powerful"]:
            mob["Stats"]["CurrentHp"] -= round((MeleeDamage + MagicDamage + TrueDamage) * 1.25 * (1.2 if (SevenBuff == "Wrath") and (player["CurrentHp"]/player["MaxHealth"] <= 1/3) else 1) * 10)/10
        else:
            mob["Stats"]["CurrentHp"] -= round((MeleeDamage + MagicDamage + TrueDamage) * (1.2 if (SevenBuff == "Wrath") and (player["CurrentHp"]/player["MaxHealth"] <= 1/3) else 1) * 10)/10
        if Equipment["Weapon"] != None:
            if "Enchant" in Equipment["Weapon"].keys():
                if "Lifesteal" in Equipment["Weapon"]["Enchant"]:
                    if "+" in Equipment["Weapon"]["Enchant"]:
                        Heal += 12
                    else:
                        Heal += 5
        player["CurrentHp"] += round(Heal*10)/10
        score = 0
        AttackTest.score = 0
        mobsStatus[Enemy]["Stats"]["CurrentHp"]=max(mobsStatus[Enemy]["Stats"]["CurrentHp"],0)
        if mobsStatus[Enemy]["Stats"]["CurrentHp"] <=0:
            enemiesKilled+=1
            MobDrops(Enemy)
            battleMessages.append("You killed the "+mobsStatus[Enemy]["Name"]+" You see its soul flying off as you loot what is left of it.")
            del mobsStatus[Enemy]
            selectedViewMobOption = None
            hoveredMobOption = None
            clickedMobOption = None
            ChangeEnemySelection()
            selectedMobNum = None
        if SevenBuff == "Greed":
            greedChance = random.randint(1, 1000)
            if not (500 <= greedChance <= 1000):
                AddResearch(0)
            elif not (750 <= greedChance <= 1000):
                AddResearch(10)
            elif not (875 <= greedChance <= 1000):
                AddResearch(15)
            elif not (950 <= greedChance <= 1000):
                AddResearch(25)
            elif not (975 <= greedChance <= 1000):
                AddResearch(40)
            elif not (990 <= greedChance <= 1000):
                AddResearch(70)
            elif not (995 <= greedChance <= 1000):
                AddResearch(100)
            elif not (999 <= greedChance <= 1000):
                AddResearch(120)
            else:
                AddResearch(1000)
        return (round(MeleeDamage*10 * 0.85)/10, round(MagicDamage*10 * 0.85)/10, round(TrueDamage*10 * 0.85)/10, round(Heal*10)/10)


def EnemyAttack(Attack, Enemy: int, guard = False):
    global player, mobsStatus, attacks, StatUpgrades, score, Equipment

    # if not Minigame(Attack["Minigames"]["Name"], Attack["Minigames"]["Arg"]):
    #     return False
    # if not (Attack["Minigames"]["Name"] in ["BlackHole", "Reaction", "Shielded", "CircleDefend", "DodgeGrid", "Rain"]):
    #     score = (20 - score)
    # score = max(min(score, 20), 0)

    mob = mobsStatus[Enemy]
    mobcopy = copy.deepcopy(mob)
    for effect in mobcopy["Effects"]:
        mobcopy["Stats"][effect["Stat"]] += effect["Potency"]
        if "Current" in effect["Stat"]:
            mob["Stats"][effect["Stat"]] += effect["Potency"]
    for effect in mob["Effects"]:
        if effect["Time"] > 0:
            effect["Time"] -= 1
        if effect["Time"] == 0:
            effect["Time"] += 1

    #Math
    if Equipment["Weapon"] != None:
        if "Enchant" in Equipment["Weapon"].keys():
            if "Defensive" in Equipment["Weapon"]["Enchant"]:
                if "+" in Equipment["Weapon"]["Enchant"]:
                    mobcopy["Stats"]["Strength"] -= 30
                    mobcopy["Stats"]["MagicPower"] -= 30
                else:
                    mobcopy["Stats"]["Strength"] -= 12
                    mobcopy["Stats"]["MagicPower"] -= 12
    for effect in attacks[Attack]["Effects"]:
            if effect["Target"] == "Self":
                mob["Effects"].append(effect)
            elif effect["Target"] == "Enemy":
                player["Effects"].append(effect)
    mob["Stats"]["CurrentHp"] = min(mob["Stats"]["CurrentHp"] + mobcopy["Stats"]["Regen"], mobcopy["Stats"]["MaxHealth"])
    missed = not bool(random.randint(1, 10000) <= attacks[Attack]["Accuracy"] * 100)
    Heal = 0
    crit = (mobcopy["Stats"]["CritPower"] if random.randint(1, 100) <= mobcopy["Stats"]["CritChance"] else 0)
    MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + mobcopy["Stats"]["Strength"] / 100) / (1 + player["Defence"] / 100) * (1 + crit / 100) * 0.35
    MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + mobcopy["Stats"]["MagicPower"] / 100) / (1 + player["MagicDefence"] / 100) * (1 + crit / 100) * 0.35
    TrueDamage = (1 + mobcopy["Stats"]["TrueAttack"] / 100) / (1 + player["TrueDefence"] / 100) * (1 + crit / 100) * 0.35
    #After Specials - Lifesteal, Etc
    if attacks[Attack]["Special"] != None:
        for special in attacks[Attack]["Special"]:
            if "Pierce" in special:
                MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + mobcopy["Stats"]["Strength"] / 100) / (1 + player["Defence"] * (1 - int(special.replace("Pierce", ""))/100) / 100) * (1 + crit / 100) * 0.35
                MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + mobcopy["Stats"]["MagicPower"] / 100) / (1 + player["MagicDefence"] * (1 - int(special.replace("Pierce", ""))/100)  / 100) * (1 + crit / 100) * 0.35
            elif "Lifesteal" in special:
                Heal = min(mob["Stats"]["Health"] - mob["Stats"]["CurrentHp"], (MagicDamage + MeleeDamage) * int(special.replace("Lifesteal", ""))/100)
            elif "Critical" in special:
                crit = (mobcopy["Stats"]["CritPower"] if random.randint(1, 100) * (1 - int(special.replace("Critical", ""))/100) <= mobcopy["Stats"]["CritChance"] else 0)
                MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + mobcopy["Stats"]["Strength"] / 100) / (1 + player["Defence"] / 100) * (1 + crit / 100) * 0.35
                MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + mobcopy["Stats"]["MagicPower"] / 100) / (1 + player["MagicDefence"] / 100) * (1 + crit / 100) * 0.35
                TrueDamage = (1 + mobcopy["Stats"]["TrueAttack"] / 100) / (1 + player["TrueDefence"] / 100) * (1 + crit / 100) * 0.35
            elif "Percent" in special:
                MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + mobcopy["Stats"]["Strength"] / 100) / (1 + player["Defence"] / 100) * (1 + crit / 100) * 0.35
                MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + mobcopy["Stats"]["MagicPower"] / 100) / (1 + player["MagicDefence"] / 100) * (1 + crit / 100) * 0.35
                TrueDamage = (1 + mobcopy["Stats"]["TrueAttack"] / 100) / (1 + player["TrueDefence"] / 100) * (1 + crit / 100) * 0.35 + player["CurrentHp"] * int(special.replace("Percent", ""))/100
            elif "Status" in special:
                MeleeDamage = attacks[Attack]["BasePowerMelee"] * (1 + mobcopy["Stats"]["Strength"] / 100) / (1 + player["Defence"] / 100) * (1 + crit / 100) * 0.35 * (1 + int(special.replace("Status", ""))/100 * len(player["Effects"]))
                MagicDamage = attacks[Attack]["BasePowerMagic"] * (1 + mobcopy["Stats"]["MagicPower"] / 100) / (1 + player["MagicDefence"] / 100) * (1 + crit / 100) * 0.35 * (1 + int(special.replace("Status", ""))/100 * len(player["Effects"]))
                TrueDamage = (1 + mobcopy["Stats"]["TrueAttack"] / 100) / (1 + player["TrueDefence"] / 100) * (1 + crit / 100) * 0.35 * (1 + int(special.replace("Status", ""))/100 * len(mob["Effects"]))
    if StatUpgrades["Tank"]:
        player["CurrentHp"] -= round((MeleeDamage + MagicDamage + TrueDamage) * 0.8 * 10)/10 * (1 if not missed else 0) / (1.6 if guard else 1)
    else:
        player["CurrentHp"] -= round((MeleeDamage + MagicDamage + TrueDamage) * 10)/10 * (1 if not missed else 0) / (1.6 if guard else 1)
    mob["Stats"]["CurrentHp"] += round(Heal*10)/10
    if not missed:
        battleMessages.append(mob["Name"] + " used " + str(attacks[Attack]["Name"]) + " to deal " + str(round((MeleeDamage + MagicDamage + TrueDamage) / (1.5 if guard else 1) * 10)/10) + " damage and healed " + str(Heal) + " health.")
    return (round(MeleeDamage*10)/10, round(MagicDamage*10)/10, round(TrueDamage*10)/10, round(Heal*10)/10, missed)


def Minigame(Name: str, Args: dict):
    global score
    if Name == "Targets":
        if not AttackTest.Targets(**Args):
            return True
    elif Name == "CircleStay":
        if not AttackTest.CircleStay(**Args):
            return True
    elif Name == "Aim":
        if not AttackTest.AimMinigame(**Args):
            return True
    elif Name == "Keyboard":
        if not AttackTest.KeyboardMinigame(**Args):
            return True
    elif Name == "Spam":
        if not AttackTest.Spam(**Args):
            return True
    elif Name == "SimonSays":
        if not AttackTest.SimonSays(**Args):
            return True
    elif Name == "BlackHole":
        if not AttackTest.BlackHole(**Args):
            return True
    elif Name == "Reaction":
        if not AttackTest.Reaction(**Args):
            return True
    elif Name == "Shielded":
        if not AttackTest.Shielded(**Args):
            return True
    elif Name == "CircleDefend":
        if not AttackTest.CircleDefend(**Args):
            return True
    elif Name == "DodgeGrid":
        if not AttackTest.DodgeGrid(**Args):
            return True
    elif Name == "Rain":
        if not AttackTest.TrackingMinigame(**Args):
            return True
    return False
    

def MobDrops(MobNum):
    global player, mobsStatus, research, enemiesKilled, experience, Items, TotalItems, TotalResearch, TotalExp, Inventory
    mob = mobsStatus[MobNum]["Drops"]
    weight = 0
    for drop in mob:
        if drop["Item"] == "Research":
            addedRESEARCH = AddResearch(random.randint(round(drop["Min"]), round(drop["Max"])) * (math.log(enemiesKilled/3 + 3, 3) if SevenBuff == "Desire" else 1))
            research += addedRESEARCH
            TotalResearch += addedRESEARCH
        elif drop["Item"] == "Exp":
            experience_1 = random.randint(round(drop["Min"]), round(drop["Max"])) * (math.log(enemiesKilled/3 + 1, 3) if SevenBuff == "Desire" else 1)
            TotalExp += experience_1
            experience += experience_1
        else:
            weight += drop["Weight"]
    for i in range(round(math.log10(enemiesKilled/2) + 1) if SevenBuff == "Desire" else 1):
        for drop in mob:
            if (drop["Item"] != "Research") and (drop["Item"] != None) and (drop["Item"] != "Exp"):
                if random.randint(1, 1000000) <= drop["Weight"]/weight*1000000:
                    if not (Items[drop["Item"]] in Inventory["Armor"]) and not (Items[drop["Item"]] in Inventory["Weapon"]) and not (Items[drop["Item"]] in Inventory["Offhand"]) and not (Items[drop["Item"]] in Inventory["Accessory"]) and not (Items[drop["Item"]] in Inventory["Misc"]):
                        AddInvItem(Items[drop["Item"]])
                    TotalItems.append(drop["Item"])



score = 0
timed = 9
AimTarget = []
character_size = (19, 37) #NORMAL
# character_size = (9, 19) #PCS
# character_size = (12, 23) #LAPTOP
character_size = Cursor.initialize(2)
score = 0
MainClock = 1000
FalseTime = time.time()
transparency = 1

phase = "title"
NonCenterOffset = 0

mobsStatus = []
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
pyterm.createItem("RoomLightRequirements", ["Light Needed: 1"], "screen", "top right", "center", 0)
pyterm.createItem("RoomRewards", ["Rewards:", "- Light", "- Gold", "- Exp"], "screen", "top right", "center", 0)

RoomData = {(0, 1): {"Type": "Home", "SpawnLocation": (0, 10), "LightRequired": 0}}
RoomException = False

player_x, player_y = 0, 0
player_hitbox = [1, 1]
pyterm.createItem("PlayerMove", ["0"], "screen", "center", "center", 0)
room_size = [round(120), round(25)]
# pyterm.createItem("RoomSize", [pyterm.addBorder("".join("".join(" " for i2 in range(round((room_size[0] - 1)/2 + 1))) + "\n" for i3 in range(round((room_size[1] - 1)/2 + 1))), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})], "screen", "center", "center", 0)
pyterm.createItem("RoomSize", [pyterm.addBorder("".join("".join(" " for i2 in range(room_size[0])) + "\n" for i3 in range(room_size[1])), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})], "screen", "center", "center", 0)
room_walls = ["|", "-", "_", "¯", "┐", "└", "┘", "┌", "┴", "┬", "├", "┤", "┼", "#"]
# room_invis_walls = [((1, 1), (2, 2), True)]
room_invis_walls = []
room_push = []
# room_push = [{"Character": "#", "Location": (-60, -12)}, {"Character": "%", "Location": (1, 1)}]
pyterm.createItem("Pushable", ["#"], "screen", "center", "center", 0)

UiOffset = [0, 0]
EnteredRoom = (0, 1)

#Setting Variables
RoomShadows = "Normal"#, "Obfuscated", "Animated"
SpeedMode = True

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
RiseMenu = 0
RiseUi = False
InventoryUiState = 1
pyterm.createItem("Inventory", [assets.get("Inventory1"), assets.get("Inventory2"), assets.get("Inventory3"), assets.get("Inventory4"), assets.get("Inventory5")], "screen", "center", "center", yBias = -11) #-pyterm.getStrWidthAndHeight(assets.get("Inventory1"))[1]/2
DisableOther = False
Inventory = {"Armor": 
             [], 
             "Weapon": 
             [], 
             "Offhand": 
             [], 
             "Accessory": 
             [], 
             "Misc": 
             []}

Items = {"Apple": {"Name": "Apple", "Type": "Consumable", "Asset": assets.get("sword"), "Effects": [{"Stat": "CurrentHp", "Potency": 30, "Time": 1}], "Description": "Yum, an apple!", "Id": None},
        #  "Iron Chestplate": {"Name": "Iron Chestplate", "Type": "Armor", "Asset": assets.get("sword"), "Stats": {"Defence": 20, "Magic Defence": 5, "Dexterity": -5}, "Enchant": False, "Description": "A tough chestplate", "Id": None},
         "Flame": {"Name": "Flame Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Burning", "Description": "A flame scroll.", "Id": None},
         "Poison": {"Name": "Poison Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Poisoning", "Description": "A scroll embued with the strongest poisons.", "Id": None},
         "Lifesteal": {"Name": "Lifesteal Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Lifesteal", "Description": "A scroll which seems to drain your life force.", "Id": None},
         "Embued": {"Name": "Embued Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Embued", "Description": "A scroll embued with overflowing magic.", "Id": None},
         "Swift": {"Name": "Swift Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Swift", "Description": "A scroll which shakes in your hands.", "Id": None},
         "Defensive": {"Name": "Defensive Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Defensive", "Description": "A really hard piece of paper.", "Id": None},
         "Sharpened": {"Name": "Sharpened Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Sharpened", "Description": "A thing that keeps giving you paper cuts.", "Id": None},
         "Dev": {"Name": "Dev Scroll", "Type": "Scroll", "Asset": assets.get("Scroll"), "Enchant": "Dev", "Description": "You shouldn't have this.", "Id": None},
         "Acidify Scroll": {"Name": "Acidify Scroll", "Type": "Attack", "Asset": assets.get("Scroll"), "Attack": "Acidify", "Description": "A scroll of acidification.", "Id": None},
        #  "Sword": {"Name": "Sword", "Type": "Weapon", "Asset": assets.get("sword"), "Stats": {"Skill": 30, "Strength": 10, "Dexterity": 5}, "Enchant": False, "Ultimate": {"Description": "apple"}, "Description": "A powerful sword", "Id": None},
        #  "Sword": {"Name": "Sword", "Type": "Weapon", "Asset": assets.get("sword"), "Stats": {"Skill": 30, "Strength": 10, "Dexterity": 5}, "Enchant": False, "Ultimate": {"Description": "apple"}, "Description": "A powerful sword", "Id": None},
        #  "Sword": {"Name": "Sword", "Type": "Weapon", "Asset": assets.get("sword"), "Stats": {"Skill": 30, "Strength": 10, "Dexterity": 5}, "Enchant": False, "Ultimate": {"Description": "apple"}, "Description": "A powerful sword", "Id": None},
         "Monocle": {"Name": "Monocle", "Type": "Extra", "Asset": assets.get("Monocle"), "Stats": {"MagicPower": 30, "CurrentHp": -5}, "Enchant": False, "Description": "Who left this here? Strange glistens show within the monocle, almost shining with aura. Boosts Magic Power, at a cost of -5 hp per turn.", "Id": None},
         "Miracle Gem": {"Name": "Miracle Gem", "Type": "Extra", "Asset": assets.get("Miracle Gem"), "Stats": {"CurrentHp": -1, "CurrentMana": 5}, "Enchant": False, "Description": "A gem that feels like it’s pulsating attached to a thin string of pure mana. Once on, it almost feels draining, yet replenishing? -1 hp +5 mana per turn.", "Id": None},
         "Delicate Flower": {"Name": "Delicate Flower", "Type": "Extra", "Asset": assets.get("Delicate Flower"), "Stats": {"CurrentHp": 5}, "Enchant": False, "Description": "A calming yet almost fragile peace emanates from the petals of this small bloom. Heals 5 hp per turn.", "Id": None},
         "Creepy Idol": {"Name": "Creepy Idol", "Type": "Offhand", "Asset": assets.get("Creepy Idol"), "Stats": {"Intelligence": 100}, "Enchant": False, "Description": "An ominous glare observes your every move. It seems to increase your intelligence...", "Id": None},
         "Shield": {"Name": "Shield", "Type": "Offhand", "Asset": assets.get("Shield"), "Stats": {"Defence": 30, "MagicDefence": 30}, "Enchant": False, "Description": "A shield made of pure void. It looks like it can swallow anything, like a black hole. Boosts defence and magic defence.", "Id": None},
         "Pocket Watch": {"Name": "Pocket Watch", "Type": "Offhand", "Asset": assets.get("Pocket Watch"), "Stats": {"Dexterity": 50}, "Enchant": False, "Description": "A golden, scratched watch with a long golden chain. Opening it reveals the glass cracked and endless sand pouring out. Boosts dexterity by a ton.", "Id": None},

         "Iron Chestplate": {"Name": "Iron Chestplate", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 50, "MagicDefence": 20, "Regen": 0}, "Enchant": False, "Description": "A tough, silver chestplate that defends against melee attacks well.", "Id": None},
         "Gilded Chestplate": {"Name": "Golden Chestplate", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 70, "MagicDefence": 30, "Regen": 10}, "Enchant": False, "Description": "Made of strange, enhanced gold. Withstands absurd damage.", "Id": None},
         "Crystal Chestplate": {"Name": "Pocket Watch", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 20, "MagicDefence": 50, "Regen": 0}, "Enchant": False, "Description": "Refracts the damage into a trillion pieces, making it easier to deal with.", "Id": None},
         "Florescent Chestplate": {"Name": "Florescent Chestplate", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 30, "MagicDefence": 70, "Regen": 10}, "Enchant": False, "Description": "Converts energy and damage into light!", "Id": None},
         "Eternality": {"Name": "Eternality", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 100, "MagicDefence": 100, "Regen": 20}, "Enchant": False, "Description": "Lasts for eternity. Gives you a mere fraction of its strength.", "Id": None},


         "Sword": {"Name": "Sword", "Type": "Weapon", "Asset": assets.get("sword"), "Stats": {"Skill": 30, "Strength": 10, "Dexterity": 5}, "Enchant": False, "Ultimate": {"Description": "Power.", "Ultimate": "Blade of Glory"}, "Description": "The most trusty companion a warrior could have. A weapon of precision and dexterity.", "Id": None},
         "Axe": {"Name": "Axe", "Type": "Weapon", "Asset": assets.get("Axe"), "Stats": {"Skill": 5, "Strength": 30, "Dexterity": -5}, "Enchant": False, "Ultimate": {"Description": "Pierce through the skies.", "Ultimate": "Piercing Power"}, "Description": "A strength based alternative to the sword. Shield breaker and mighty log smasher.", "Id": None},
         "Spear": {"Name": "Spear", "Type": "Weapon", "Asset": assets.get("Spear"), "Stats": {"Skill": 15, "Strength": 0, "Dexterity": 45}, "Enchant": False, "Ultimate": {"Description": "And even further.", "Ultimate": "Strike the Heavens"}, "Description": "Precise and accurate polearm. Deadly in the right hands. Harmless in some.", "Id": None},
         "Wand": {"Name": "Wand", "Type": "Weapon", "Asset": assets.get("Wand"), "Stats": {"Intelligence": 10, "MagicPower": 10, "CastingSpeed": 40}, "Enchant": False, "Ultimate": {"Description": "Shocking", "Ultimate": "Storms of Lighting"}, "Description": "A small stick that emits a warmth when touched. Mana is quickly processed through the wand and shot out at lightning quick rates.", "Id": None},
         "Staff": {"Name": "Staff", "Type": "Weapon", "Asset": assets.get("Staff"), "Stats": {"Intelligence": 10, "MagicPower": 30, "CastingSpeed": 10}, "Enchant": False, "Ultimate": {"Description": "You feel as if you are filled with pure electricity.", "Ultimate": "Overcharge"}, "Description": "A large staff with a magical core fused into the centre, letting mana compound inside its wooden head.", "Id": None},
         "Mace": {"Name": "Mace", "Type": "Weapon", "Asset": assets.get("Mace"), "Stats": {"Intelligence": 100, "MagicPower": 15, "CastingSpeed": 5}, "Enchant": False, "Ultimate": {"Description": "Power.", "Ultimate": "Laser of Retribution"}, "Description": "A blade weapon not meant for strength. Each point on its surface concentrates the mana within it multiple-fold.", "Id": None},
         "Ring": {"Name": "Ring", "Type": "Weapon", "Asset": assets.get("Ring"), "Stats": {"Skill": 15, "Strength": 15, "Dexterity": 15, "Intelligence": 15, "MagicPower": 15, "CastingSpeed": 15}, "Enchant": False, "Ultimate": {"Description": "Power.", "Ultimate": "Balance"}, "Description": "A Wearable object with glyphs and symbols etched into it. Glows faintly when touched", "Id": None},

         "Health Potion": {"Name": "Health Potion", "Type": "Consumable", "Asset": assets.get("PotionHealth"), "Effects": [{"Stat": "CurrentHp", "Potency": 20, "Time": 1}], "Description": "A green potion which heals 20hp.", "Id": None},
         "Mana Potion": {"Name": "Mana Potion", "Type": "Consumable", "Asset": assets.get("PotionMana"), "Effects": [{"Stat": "CurrentMana", "Potency": 30, "Time": 1}], "Description": "A blue potion which gives 30 mana.", "Id": None},
         "Strength Potion": {"Name": "Strength Potion", "Type": "Consumable", "Asset": assets.get("PotionStrength"), "Effects": [{"Stat": "Strength", "Potency": 30, "Time": 2}], "Description": "A red potion which gives 30 strength for 2 turns.", "Id": None},
         "Mystery Potion": {"Name": "Mystery Potion", "Type": "Consumable", "Asset": assets.get("PotionMystery"), "Effects": [{"Stat": "CurrentHp", "Potency": -30, "Time": 1}, {"Stat": "MagicPower", "Potency": 30, "Time": 3}], "Description": "A yellow potion which does something idk.", "Id": None},
         "Net": {"Name": "Net", "Type": "Consumable", "Asset": assets.get("Net"), "Effects": [{"Stat": "CritChance", "Potency": 100, "Time": 2}], "Description": "A net which makes critical hits certain for 2 turns!", "Id": None},
         "Smoke Bomb": {"Name": "Smoke Bomb", "Type": "Consumable", "Asset": assets.get("SmokeBomb"), "Effects": [{"Stat": "CritPower", "Potency": 70, "Time": 5}], "Description": "A smokebomb which makes critical hits deal +70% more power.", "Id": None},
         "Focus Tomb": {"Name": "Focus Tomb", "Type": "Consumable", "Asset": assets.get("FocusTomb"), "Effects": [{"Stat": "Skill", "Potency": 50, "Time": 3}, {"Stat": "Intelligence", "Potency": 100, "Time": 3}], "Description": "Helps you concentrate. Gain more int and skill for 3 turns.", "Id": None},
         "Mirror Shard": {"Name": "Mirror Shard", "Type": "Consumable", "Asset": assets.get("MirrorShard"), "Effects": [{"Stat": "MagicDefence", "Potency": 30, "Time": 2}], "Description": "A reflective shard. It boosts magic defence by 30 for 2 turns.", "Id": None},
         "Bottled Mist": {"Name": "Bottled Mist", "Type": "Consumable", "Asset": assets.get("BottledMist"), "Effects": [{"Stat": "Defence", "Potency": 30, "Time": 2}], "Description": "Some wierd vial of some misty substance. Boosts defence by 30 for 2 turns.", "Id": None},
         "Dynamite": {"Name": "Dynamite", "Type": "Consumable", "Asset": assets.get("Dynamite"), "Effects": [{"Stat": "Dexterity", "Potency": 50, "Time": 3}], "Description": "A non-functional bomb. Can be used for scaring though, increasing dexterity by 50 for 3 turns.", "Id": None},

         
         }

#sword = {"Name": "The Death Star", "Type": "Weapon", "Asset": assets.get(""), "Stats": {"Dexterity": 1, "Strength": 1, "Accuracy": 1}, "Ultimate": {"Description": "apple", "..."}, "Description": "A death star that's deadly and a star.", "Id": None}
#apple = {"Name": "Apple", "Type": Consumable", "Asset": "", "Effects": [{"Type": Strength, "Time": 3, "Potency": 1, "Apply": "Player"},{"Type": "Damage", "Potency": 999, "Apply": "AllEnemy"}], "Description": "Could be used to make pie", "Id": None}
Equipment = {"Armor": None, "Weapon": None, "Offhand": None, "Extra": None}
EquippedAttacks = {"Attack0": "Punch", "Attack1": "", "Attack2": "", "Attack3": "", "Attack4": "", "Attack5": "","Attack6": "","Attack7": "",}
LockedAttacks = {"Attack0": False, "Attack1": False, "Attack2": False, "Attack3": False, "Attack4": True, "Attack5": True,"Attack6": True,"Attack7": True,}
EquippedUltimate = "Punch++"
pyterm.createItem("ItemList", ["- Apple"], "Inventory", "top left", "top left", 0, 22, 26)
FocusInv = False
pyterm.createItem("ItemImg", [" "], "Inventory", "bottom right", "center", 0, -10, -21)
pyterm.createItem("ItemDesc", [" "], "Inventory", "bottom right", "top left", 0, -18, -12)
pyterm.createItem("ItemDesc2", [" "], "Inventory", "bottom right", "top left", 0, -18, -9)
pyterm.createItem("ItemButton", ["[Exit]       [Use]"], "Inventory", "bottom right", "top left", 0, -19, -2)
pyterm.createItem("Equipment", ["|!|!|!|!|!|!|!|!|!", "|!|!|!|!|!|!|!|!|!", "|!|!|!|!|!|!|!|!|!", "|!|!|!|!|!|!|!|!|!"], "Inventory", "top left", "center", 0, 11, 26)
pyterm.createItem("Settings", [assets.get("TitleSettings")], "screen", "center", "center", 0, 0, -15)







        #  "Iron Chestplate": {"Name": "Iron Chestplate", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 50, "MagicDefence": 20, "Regen": 0}, "Enchant": False, "Description": "A tough, silver chestplate that defends against melee attacks well.", "Id": None},
        #  "Gilded Chestplate": {"Name": "Golden Chestplate", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 70, "MagicDefence": 30, "Regen": 10}, "Enchant": False, "Description": "Made of strange, enhanced gold. Withstands absurd damage.", "Id": None},
        #  "Crystal Chestplate": {"Name": "Pocket Watch", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 20, "MagicDefence": 50, "Regen": 0}, "Enchant": False, "Description": "Refracts the damage into a trillion pieces, making it easier to deal with.", "Id": None},
        #  "Florescent Chestplate": {"Name": "Florescent Chestplate", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 30, "MagicDefence": 70, "Regen": 10}, "Enchant": False, "Description": "Converts energy and damage into light!", "Id": None},
        #  "Eternality": {"Name": "Eternality", "Type": "Armor", "Asset": assets.get("Chestplate"), "Stats": {"Defence": 100, "MagicDefence": 100, "Regen": 20}, "Enchant": False, "Description": "Lasts for eternity. Gives you a mere fraction of its strength.", "Id": None},






CraftingRecipes = {"Sword": {"Ingredients": [{"Item": "Strength Potion", "Amount": 1}, {"Item": "Mystery Potion", "Amount": 1}], "Research": 300, "Researchlook": "[300.0 Research]", "LightRequirements": 1},
                   "Axe": {"Ingredients": [{"Item": "Strength Potion", "Amount": 2}, {"Item": "Apple", "Amount": 1}], "Research": 500, "Researchlook": "[500.0 Research]", "LightRequirements": 3},
                   "Spear": {"Ingredients": [{"Item": "Mystery Potion", "Amount": 2}, {"Item": "Smoke Bomb", "Amount": 1}], "Research": 400, "Researchlook": "[400.0 Research]", "LightRequirements": 10},
                   "Wand": {"Ingredients": [{"Item": "Mana Potion", "Amount": 2}, {"Item": "Mirror Shard", "Amount": 1}], "Research": 600, "Researchlook": "[600.0 Research]", "LightRequirements": 3},
                   "Mace": {"Ingredients": [{"Item": "Mana Potion", "Amount": 1}, {"Item": "Dynamite", "Amount": 1}], "Research": 800, "Researchlook": "[800.0 Research]", "LightRequirements": 10},
                   "Staff": {"Ingredients": [{"Item": "Bottled Mist", "Amount": 1}, {"Item": "Mirror Shard", "Amount": 1}], "Research": 700, "Researchlook": "[700.0 Research]", "LightRequirements": 1},
                   "Ring": {"Ingredients": [{"Item": "Mana Potion", "Amount": 1}, {"Item": "Health Potion", "Amount": 1}, {"Item": "Focus Tomb", "Amount": 1}], "Research": 300000, "Researchlook": "[300k  Research]", "LightRequirements": 25},

                   "Defensive": {"Ingredients": [{"Item": "Health Potion", "Amount": 3}, {"Item": "Apple", "Amount": 2}], "Research": 200000, "Researchlook": "[200k  Research]", "LightRequirements": 35},
                   "Sharpened": {"Ingredients": [{"Item": "Strength Potion", "Amount": 3}], "Research": 1000000, "Researchlook": "[1.00m Research]", "LightRequirements": 25},
                   "Swift": {"Ingredients": [{"Item": "Net", "Amount": 2}], "Research": 2500000, "Researchlook": "[2.50m Research]", "LightRequirements": 10},
                   "Embued": {"Ingredients": [{"Item": "Mirror Shard", "Amount": 2}], "Research": 200000, "Researchlook": "[200k  Research]", "LightRequirements": 20},
                   "Lifesteal": {"Ingredients": [{"Item": "Dynamite", "Amount": 2}, {"Item": "Strength Potion", "Amount": 1}], "Research": 10000000, "Researchlook": "[10.0m Research]", "LightRequirements": 50},
                   "Poison": {"Ingredients": [{"Item": "Mystery Potion", "Amount": 3}], "Research": 1500000, "Researchlook": "[1.50m Research]", "LightRequirements": 40},
                   "Flame": {"Ingredients": [{"Item": "Smoke Bomb", "Amount": 2}], "Research": 3000000, "Researchlook": "[3.00m Research]", "LightRequirements": 35},
                   
                   "Iron Chestplate": {"Ingredients": [{"Item": "Smoke Bomb", "Amount": 1}, {"Item": "Health Potion", "Amount": 1}], "Research": 5000, "Researchlook": "[5.00k Research]", "LightRequirements": 10},
                   "Crystal Chestplate": {"Ingredients": [{"Item": "Swift", "Amount": 1}, {"Item": "Mana Potion", "Amount": 1}], "Research": 5000, "Researchlook": "[5.00k Research]", "LightRequirements": 10},
                   "Gilded Chestplate": {"Ingredients": [{"Item": "Bottled Mist", "Amount": 2}, {"Item": "Dynamite", "Amount": 1}], "Research": 300000, "Researchlook": "[300k  Research]", "LightRequirements": 25},
                   "Florescent Chestplate": {"Ingredients": [{"Item": "Mirror Shard", "Amount": 2}, {"Item": "Focus Tomb", "Amount": 1}], "Research": 300000, "Researchlook": "[300k  Research]", "LightRequirements": 25},
                   "Eternality": {"Ingredients": [{"Item": "Shield", "Amount": 1}, {"Item": "Ring", "Amount": 1}, {"Item": "Health Potion", "Amount": 1}, {"Item": "Bottled Mist", "Amount": 1}, {"Item": "Mirror Shard", "Amount": 1}], "Research": 150000000, "Researchlook": "[150m  Research]", "LightRequirements": 50},

                   
                   
                   
                   
                   
                   
                   }
AvaliableRecipes = []

#ITS THE STATS!
light = 1
research = 0
level = 1
experience = 0
max_experience = round((math.log((math.e / 2) ** (level - 1) + math.gamma(level ** 1.35)/(level ** (level / 4)), max(10 * math.pi / level, 1 + 1/level ** 3)) + 0.798935) * 100)
#1 -> 999, 1.1 -> 10k, 10k -> 999k, 1.1mil -> ...
player = {"MaxHealth": 100, "CurrentHp": 100, "Regen": 0,
          "Defence": 0, "MagicDefence": 0, 
          "Strength": 0, "MagicPower": 0, 
          "Dexterity": 100, "CastingSpeed": 100, 
          "Skill": 0, "Intelligence": 0, 
          "CritChance": 5, "CritPower": 40, 
          "Mana": 100, "Energy": 100, 
          "ManaRegen": 10, "EnergyRegen": 10, 
          "CurrentMana": 100, "CurrentEnergy": 100, 
          "TrueAttack": 1, "TrueDefence": 0, 
          "Effects": [],
          "Passives": []} #{"Stat": "Strength", "Potency": 10, "Time": 10} or {"Stat": "Strength", "Potency": 10, "Time": -2} or {"Stat": "Health", "Potency": -2, "Time": 5, "Special": "Poison"}

attacks = {"BasicAttack": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": None},
            #Slime (Reg) + (Large) + (Giga) + (Corrupted) + (Defensive) + (Attack)
            "Slime Leap": {"BasePowerMelee": 15, "BasePowerMagic": 0, "Accuracy": 80, "Energy": 10, "Mana": 10, "Cooldown": 0, "Minigames": [{"Name": "CircleStay", "Weight": 1, "Arg": {"Time": 10 * pyterm.FPS, "Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Speed": 0.5, "Unpredictability": 25, "ScoreMulti": 1}}], "Effects": [], "Special": ["Damage100"]}, #15 * 1.3 = 19.5dmg * 80% acc = 15.6dmg avg
            "Slime Shot": {"BasePowerMelee": 25, "BasePowerMagic": 0, "Accuracy": 50, "Energy": 15, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "Shielded", "Weight": 1, "Arg": {"Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Time": 10 * pyterm.FPS, "Unpredictability": 60, "MaxWait": 1 * pyterm.FPS, "ScoreMulti": 1}}], "Effects": [], "Special": ["Damage50"]}, #25 * 1.3 = 32.5dmg * 50% acc = 16.25dmg avg
            "Acidify": {"BasePowerMelee": 0, "BasePowerMagic": 10, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "DodgeGrid", "Weight": 1, "Arg": {"Character": "O", "SpeedRange": (10, 70), "Time": 20 * pyterm.FPS, "SpawnRate": 0.025 * pyterm.FPS, "InverseBias": 4, "ScoreMulti": 1}}], "Effects": [], "Special": ["Damage100"]},
            "Tackle": {"BasePowerMelee": 10, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "CircleStay", "Weight": 1, "Arg": {"Time": 8 * pyterm.FPS, "Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Speed": 0.5, "Unpredictability": 25, "ScoreMulti": 1.25}}], "Effects": [], "Special": ["Damage120"]}, #10 * 1.3 = 13dmg avg
            "Slime Heat-Seeking Missile": {"BasePowerMelee": 150, "BasePowerMagic": 150, "Accuracy": 999, "Energy": 100, "Mana": 100, "Cooldown": 0, "Minigames": [{"Name": "Shielded", "Weight": 1, "Arg": {"Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Time": 10 * pyterm.FPS, "Unpredictability": 60, "MaxWait": 0.5 * pyterm.FPS, "ScoreMulti": 1}}], "Effects": [], "Special": None}, #150 * 1.3 = 195dmg avg
            #Slime (Large) + (Giga) + (Defensive) + (Attack)
            "Crush": {"BasePowerMelee": 20, "BasePowerMagic": 0, "Accuracy": 80, "Energy": 30, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "CircleStay", "Weight": 1, "Arg": {"Time": 15 * pyterm.FPS, "Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Speed": 0.5, "Unpredictability": 25, "ScoreMulti": 0.7}}], "Effects": [], "Special": ["Damage100"]}, #20 * 1.5 = 30dmg * 80% acc = 24dmg avg (Low Weight)
            #Slime (Giga)
            "Devour": {"BasePowerMelee": 15, "BasePowerMagic": 15, "Accuracy": 100, "Energy": 30, "Mana": 20, "Cooldown": 0, "Minigames": [{"Name": "Shielded", "Weight": 1, "Arg": {"Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Time": 15 * pyterm.FPS, "Unpredictability": 60, "MaxWait": 1 * pyterm.FPS, "ScoreMulti": 0.7}}], "Effects": [], "Special": ["Damage100"]}, #15 * 1.6 = 24dmg avg
            #Slime (Corrosive)
            "Corrode": {"BasePowerMelee": 0, "BasePowerMagic": 20, "Accuracy": 100, "Energy": 0, "Mana": 20, "Cooldown": 0, "Minigames": [{"Name": "DodgeGrid", "Weight": 1, "Arg": {"Character": "O", "SpeedRange": (30, 65), "Time": 10 * pyterm.FPS, "SpawnRate": 0.01 * pyterm.FPS, "InverseBias": 4, "ScoreMulti": 2}}], "Effects": [], "Special": ["Damage100"]}, #
            "Dissolve": {"BasePowerMelee": 10, "BasePowerMagic": 30, "Accuracy": 65, "Energy": 0, "Mana": 30, "Cooldown": 0, "Minigames": [{"Name": "Rain", "Weight": 1, "Arg": {"Character": "O", "SpawnRate": 0.025 * pyterm.FPS, "SpeedRange": (15, 25), "DespawnRate": 4 * pyterm.FPS, "Time": 20 * pyterm.FPS, "ScoreMulti": 1}}], "Effects": [], "Special": ["Damage100"]}, #10 * 1.5 = 15 dmg * 65% acc = 9.75dmg, 
            #Slime (Defensive)
            "Reinforce": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 90, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Defense", "Potency": 15, "Target": "Self", "Time": 3},{"Stat": "MagicDefense", "Potency": 15, "Target": "Self", "Time": 3}], "Special": None},
            "Intimidate": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 50, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicPower", "Potency": -20, "Target": "Enemy", "Time": 5}], "Special": None},
            #Slime (Attack)
            "Piercing Slime": {"BasePowerMelee": 12, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "Reaction", "Weight": 1, "Arg": {"TimeRange": (1 * pyterm.FPS, 3 * pyterm.FPS), "Repetitions": 3, "ScoreMulti": 1}}], "Effects": [], "Special": ["Pierce100"]}, #15 * 2.5 = 30dmg avg
            "Enlarge": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 50, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": 50, "Target": "Self", "Time": 3}], "Special": None},
            "Slime Rollout": {"BasePowerMelee": 30, "BasePowerMagic": 0, "Accuracy": 95, "Energy": 50, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "Shielded", "Weight": 1, "Arg": {"Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Time": 20 * pyterm.FPS, "Unpredictability": 60, "MaxWait": 1 * pyterm.FPS, "ScoreMulti": 0.5}}], "Effects": [], "Special": ["Damage100"]}, #30 * 2.5 = 70 dmg * 95% acc = 66.5dmg avg (Lower Weight)
            
            #Goblin
            "Stab": {"BasePowerMelee": 12, "BasePowerMagic": 5, "Accuracy": 100, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Pierce20", "Damage100"]},
            "Charge": {"BasePowerMelee": 15, "BasePowerMagic": 5, "Accuracy": 100, "Energy": 5, "Mana": 5, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            "Headbutt": {"BasePowerMelee": 25, "BasePowerMagic": 5, "Accuracy": 80, "Energy": 30, "Mana": 5, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": -30, "Target": "Enemy", "Time": 2}], "Special": ["Damage100"]},
            #Range
            "Shoot": {"BasePowerMelee": 25, "BasePowerMagic": 15, "Accuracy": 50, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Pierce50", "Damage50"]},
            "Fire": {"BasePowerMelee": 20, "BasePowerMagic": 5, "Accuracy": 65, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "CurrentHp", "Potency": -10, "Target": "Enemy", "Time": 3}], "Special": ["Damage50"]},
            #Dart
            "Blowdart": {"BasePowerMelee": 35, "BasePowerMagic": 0, "Accuracy": 30, "Energy": 60, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Pierce50", "Damage50"]},
            "Breathe": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": 10, "Target": "Self", "Time": 3}], "Special": None},

            #Wolf
            "Howl": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Defence", "Potency": -20, "Target": "Enemy", "Time": 3}], "Special": ["Pierce20"]},
            "Bite": {"BasePowerMelee": 20, "BasePowerMagic": 10, "Accuracy": 95, "Energy": 15, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            "Ferocious Swipe": {"BasePowerMelee": 25, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 20, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Percent5"]},
            #Silver
            "Claw": {"BasePowerMelee": 5, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "CurrentHp", "Potency": -10, "Target": "Enemy", "Time": 3}], "Special": ["Damage200"]},
            "Shining Ram": {"BasePowerMelee": 20, "BasePowerMagic": 20, "Accuracy": 70, "Energy": 20, "Mana": 20, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            #Alpha
            "Endurance": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 95, "Energy": 10, "Mana": 10, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Defence", "Potency": 20, "Target": "Self", "Time": 3}, {"Stat": "MagicDefence", "Potency": 20, "Target": "Self", "Time": 3}], "Special": None},
            "Shread": {"BasePowerMelee": 30, "BasePowerMagic": 10, "Accuracy": 80, "Energy": 30, "Mana": 10, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Percent10"]},

            #Orc
            "Smack": {"BasePowerMelee": 20, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 15, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            "Stomp": {"BasePowerMelee": 25, "BasePowerMagic": 0, "Accuracy": 90, "Energy": 20, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            "Shockwave": {"BasePowerMelee": 30, "BasePowerMagic": 5, "Accuracy": 80, "Energy": 25, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            #Cyclops
            "Focus": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 20, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicPower", "Potency": 30, "Target": "Self", "Time": 3}], "Special": ["Damage100"]},
            "Eye Beam": {"BasePowerMelee": 15, "BasePowerMagic": 15, "Accuracy": 90, "Energy": 0, "Mana": 25, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            "Hypnotise": {"BasePowerMelee": 25, "BasePowerMagic": 25, "Accuracy": 60, "Energy": 0, "Mana": 30, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "CritChance", "Potency": -10, "Target": "Enemy", "Time": 5}], "Special": ["Damage100"]},
            #Armored
            "Slam": {"BasePowerMelee": 35, "BasePowerMagic": 0, "Accuracy": 80, "Energy": 30, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            "Guard": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 50, "Energy": 20, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Defence", "Potency": 50, "Target": "Self", "Time": 5}], "Special": ["Damage100"]},
            #All-seeing
            "Intense Glare": {"BasePowerMelee": 0, "BasePowerMagic": 20, "Accuracy": 95, "Energy": 0, "Mana": 10, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},
            "Honed Club": {"BasePowerMelee": 20, "BasePowerMagic": 35, "Accuracy": 90, "Energy": 15, "Mana": 30, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Damage100"]},

            #Spider
            "Poison": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "CurrentHp", "Potency": -15, "Target": "Enemy", "Time": 3}], "Special": ["Damage100"]},
            "Crawl": {"BasePowerMelee": 20, "BasePowerMagic": 0, "Accuracy": 90, "Energy": 5, "Mana": 5, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": -15, "Target": "Enemy", "Time": 3}], "Special": ["Damage100"]},
            "Web Shot": {"BasePowerMelee": 15, "BasePowerMagic": 15, "Accuracy": 100, "Energy": 10, "Mana": 10, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "CritPower", "Potency": -50, "Target": "Enemy", "Time": 3}], "Special": ["Damage100"]},
            #Silkweaver
            "Silk-Blade": {"BasePowerMelee": 25, "BasePowerMagic": 5, "Accuracy": 80, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "CurrentHp", "Potency": -5, "Target": "Enemy", "Time": 5}], "Special": None},
            "Blood Drain": {"BasePowerMelee": 20, "BasePowerMagic": 0, "Accuracy": 80, "Energy": 30, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": -15, "Target": "Enemy", "Time": 3}], "Special": ["Lifesteal15", "Damage100"]},
            #Jump
            "Jump": {"BasePowerMelee": 10, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 20, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Lifesteal25", "Damage100"]},
            "Leap": {"BasePowerMelee": 11, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 20, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Lifesteal20", "Damage100"]},


            #Player Attacks
            "Punch": {"BasePowerMelee": 30, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "CircleStay", "Weight": 1, "Arg": {"Time": 12.5 * pyterm.FPS, "Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Speed": 0.5, "Unpredictability": 25, "ScoreMulti": 0.8}}], "Effects": [], "Special": None},
            "Slash": {"BasePowerMelee": 45, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "CircleStay", "Weight": 1, "Arg": {"Time": 10 * pyterm.FPS, "Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Speed": 0.5, "Unpredictability": 25, "ScoreMulti": 1}}], "Effects": [], "Special": None},
            "Bash": {"BasePowerMelee": 50, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "Shielded", "Weight": 1, "Arg": {"Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Time": 10 * pyterm.FPS, "Unpredictability": 60, "MaxWait": 1 * pyterm.FPS, "ScoreMulti": 1}}], "Effects": [], "Special": None},
            "Mash": {"BasePowerMelee": 75, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 30, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "Spam", "Weight": 1, "Arg": {"Time": 8 * pyterm.FPS, "ScoreMulti": 1}}], "Effects": [], "Special": None},
            "Meteoric Strike": {"BasePowerMelee": 0, "BasePowerMagic": 100, "Accuracy": 100, "Energy": 0, "Mana": 60, "Cooldown": 0, "Minigames": [{"Name": "Keyboard", "Weight": 1, "Arg": {"Inputs": "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" "), "Speed": 0.7 * pyterm.FPS, "Time": 8 * pyterm.FPS, "ScoreMulti": 1.2}}], "Effects": [], "Special": None},
            "Blast": {"BasePowerMelee": 0, "BasePowerMagic": 50, "Accuracy": 100, "Energy": 0, "Mana": 10, "Cooldown": 0, "Minigames": [{"Name": "Spam", "Weight": 1, "Arg": {"Time": 10 * pyterm.FPS, "ScoreMulti": 0.8}}], "Effects": [], "Special": None},
            "Fireball": {"BasePowerMelee": 10, "BasePowerMagic": 40, "Accuracy": 100, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "BlackHole", "Weight": 1, "Arg": {"Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Strength": 300, "Unpredictability": 30, "Time": 8.5 * pyterm.FPS, "ScoreMulti": 0.8}}], "Effects": [{"Stat": "CurrentHp", "Potency": -20, "Time": 3, "Target": "Enemy"}], "Special": None},
            "Sweeping Edge": {"BasePowerMelee": 50, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 20, "Mana": 0, "Cooldown": 0, "Minigames": [{"Name": "Targets", "Weight": 1, "Arg": {"Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Duration": 1 * pyterm.FPS, "Time": 20 * pyterm.FPS, "ScoreMulti": 1}}], "Effects": [], "Special": ["Percent8"]},
            "Lightning": {"BasePowerMelee": 10, "BasePowerMagic": 30, "Accuracy": 100, "Energy": 0, "Mana": 30, "Cooldown": 0, "Minigames": [{"Name": "CircleStay", "Weight": 1, "Arg": {"Time": 5 * pyterm.FPS, "Range": (round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), "Speed": 0.6, "Unpredictability": 10, "ScoreMulti": 2}}], "Effects": [{"Stat": "Strength", "Potency": -30, "Time": 3, "Target": "Enemy"}, {"Stat": "MagicPower", "Potency": -20, "Time": 3, "Target": "Enemy"}], "Special": None},
            "Aim": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": 50, "Time": 5, "Target": "Self"}], "Special": None},
            "Premonition": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 0, "Mana": 10, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicPower", "Potency": 50, "Time": 5, "Target": "Self"}], "Special": None},
            "Weaken": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": -50, "Time": 10, "Target": "Enemy"}], "Special": None},
            "Stab": {"BasePowerMelee": 40, "BasePowerMagic": 0, "Accuracy": 100, "Energy": 5, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": 10, "Time": 7, "Target": "Self"}], "Special": None},
            "Splash": {"BasePowerMelee": 0, "BasePowerMagic": 20, "Accuracy": 100, "Energy": 10, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicPower", "Potency": 20, "Time": 4, "Target": "Self"}, {"Stat": "MagicDefence", "Potency": -20, "Time": 3, "Target": "Enemy"}], "Special": None},
            "Tracking Missile": {"BasePowerMelee": 0, "BasePowerMagic": 60, "Accuracy": 100, "Energy": 0, "Mana": 35, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicPower", "Potency": 60, "Time": 2, "Target": "Self"}], "Special": ["Pierce40"]},



            "Blade of Glory": {"BasePowerMelee": 160, "BasePowerMagic": 0, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": 20, "Time": 3, "Target": "Self"}], "Special": ["Pierce20"]},
            "Piercing Power": {"BasePowerMelee": 120, "BasePowerMagic": 0, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [], "Special": ["Pierce100"]},
            "Strike the Heavens": {"BasePowerMelee": 140, "BasePowerMagic": 0, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "Strength", "Potency": -100, "Time": 2, "Target": "Enemy"}], "Special": ["Lifesteal15"]},
            "Storms of Lightning": {"BasePowerMelee": 0, "BasePowerMagic": 130, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicDefence", "Potency": -50, "Time": 2, "Target": "Enemy"}], "Special": None},
            "Overcharge": {"BasePowerMelee": 0, "BasePowerMagic": 0, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicDefence", "Potency": 100, "Time": 2, "Target": "Self"}, {"Stat": "MagicPower", "Potency": 150, "Time": 3, "Target": "Self"}], "Special": None},
            "Laser of Retribution": {"BasePowerMelee": 0, "BasePowerMagic": 170, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicDefence", "Potency": -50, "Time": 2, "Target": "Enemy"}], "Special": None},
            "Balance": {"BasePowerMelee": 100, "BasePowerMagic": 100, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicDefence", "Potency": 80, "Time": 3, "Target": "Self"}, {"Stat": "Defence", "Potency": 80, "Time": 3, "Target": "Self"}], "Special": None},
            "Punch++": {"BasePowerMelee": 100, "BasePowerMagic": 0, "Accuracy": 999, "Energy": 0, "Mana": 0, "Cooldown": 0, "Minigames": [None], "Effects": [{"Stat": "MagicDefence", "Potency": -50, "Time": 3, "Target": "Enemy"}, {"Stat": "Defence", "Potency": -50, "Time": 3, "Target": "Enemy"}], "Special": None}

            }

for attack in attacks.keys():
    Items[attack + " Scroll"] = {"Name": attack + " Scroll", "Type": "Attack", "Asset": assets.get("Scroll"), "Attack": attack, "Description": "An attack scroll.", "Id": None}

enemies = {
"Slime": {"Attacks": [{"AttackType": "Slime Leap", "Weight": 100}, {"AttackType": "Slime Shot", "Weight": 100}, {"AttackType": "Acidify", "Weight": 100}, {"AttackType": "Tackle", "Weight": 100}, {"AttackType": "Slime Heat-Seeking Missile", "Weight": 1}], "Stats": {"MaxHealth": 150, "CurrentHp": 150, "Regen": 0,
          "Defence": 10, "MagicDefence": 40, 
          "Strength": 25, "MagicPower": 10, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": "Research", "Min": 10, "Max": 100, "Weight": 0}, {"Item": "Exp", "Min": 100, "Max": 150, "Weight": 0}, {"Item": "Acidify Scroll", "Weight": 10}, {"Item": "Slime Leap Scroll", "Weight": 10}, {"Item": None, "Weight": 10}], "Effects": [], "Asset": assets.get("Slime"), "Special": None}
,"Large Slime": {"Attacks": [{"AttackType": "Slime Leap", "Weight": 100}, {"AttackType": "Slime Shot", "Weight": 100}, {"AttackType": "Acidify", "Weight": 100}, {"AttackType": "Tackle", "Weight": 100}, {"AttackType": "Crush", "Weight": 30}, {"AttackType": "Slime Heat-Seeking Missile", "Weight": 1}], "Stats": {"MaxHealth": 300, "CurrentHp": 300, "Regen": 0,
          "Defence": 30, "MagicDefence": 100, 
          "Strength": 45, "MagicPower": 15, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 80, "Max": 300, "Weight": 0}, {"Item": "Exp", "Min": 200, "Max": 300, "Weight": 0}, {"Item": "Slime Shot Scroll", "Weight": 3}, {"Item": "Crush Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("LargeSlime"), "Special": None}
,"Corrosive Slime": {"Attacks": [{"AttackType": "Dissolve", "Weight": 100}, {"AttackType": "Slime Shot", "Weight": 100}, {"AttackType": "Acidify", "Weight": 100}, {"AttackType": "Corrode", "Weight": 100}, {"AttackType": "Slime Heat-Seeking Missile", "Weight": 1}], "Stats": {"MaxHealth": 100, "CurrentHp": 100, "Regen": 0,
          "Defence": 200, "MagicDefence": 10, 
          "Strength": 35, "MagicPower": 30, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 150, "Max": 400, "Weight": 0}, {"Item": "Exp", "Min": 150, "Max": 225, "Weight": 0}, {"Item": "Corrode Scroll", "Weight": 3}, {"Item": "Dissolve Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("CorrosiveSlime"), "Special": None}
,"Defensive Slime": {"Attacks": [{"AttackType": "Slime Leap", "Weight": 100}, {"AttackType": "Slime Shot", "Weight": 100}, {"AttackType": "Acidify", "Weight": 100}, {"AttackType": "Tackle", "Weight": 100}, {"AttackType": "Crush", "Weight": 50}, {"AttackType": "Reinforce", "Weight": 150}, {"AttackType": "Intimidate", "Weight": 150}], "Stats": {"MaxHealth": 500, "CurrentHp": 500, "Regen": 5,
          "Defence": 100, "MagicDefence": 30, 
          "Strength": 20, "MagicPower": 10, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 5}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 1000, "Max": 1500, "Weight": 0}, {"Item": "Exp", "Min": 700, "Max": 1000, "Weight": 0}, {"Item": "Intimidate Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("DefensiveSlime"),"Special": None}
,"Offensive Slime": {"Attacks": [{"AttackType": "Slime Leap", "Weight": 100}, {"AttackType": "Slime Shot", "Weight": 100}, {"AttackType": "Acidify", "Weight": 100}, {"AttackType": "Tackle", "Weight": 100}, {"AttackType": "Slime Rollout", "Weight": 150}, {"AttackType": "Piercing Shot", "Weight": 150}, {"AttackType": "Enlarge", "Weight": 150}], "Stats": {"MaxHealth": 300, "CurrentHp": 300, "Regen": 0,
          "Defence": 0, "MagicDefence": 0, 
          "Strength": 100, "MagicPower": 75, "CritChance": 5, "CritPower": 100, "TrueAttack": 5, "TrueDefence": 1}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 1000, "Max": 1500, "Weight": 0}, {"Item": "Exp", "Min": 700, "Max": 1000, "Weight": 0}, {"Item": "Piercing Slime Scroll", "Weight": 3}, {"Item": "Slime Rollout Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("OffensiveSlime"), "Special": None}
,"Giga Slime": {"Attacks": [{"AttackType": "Slime Leap", "Weight": 100}, {"AttackType": "Slime Shot", "Weight": 100}, {"AttackType": "Acidify", "Weight": 100}, {"AttackType": "Tackle", "Weight": 100}, {"AttackType": "Crush", "Weight": 100}, {"AttackType": "Devour", "Weight": 100}], "Stats": {"MaxHealth": 400, "CurrentHp": 400, "Regen": 0,
          "Defence": 20, "MagicDefence": 70, 
          "Strength": 55, "MagicPower": 20, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 300, "Max": 500, "Weight": 0}, {"Item": "Exp", "Min": 300, "Max": 400, "Weight": 0}, {"Item": "Devour Scroll", "Weight": 5}], "Effects": [], "Asset": assets.get("GigaSlime"), "Special": None}
        
,"Goblin": {"Attacks": [{"AttackType": "Stab", "Weight": 10}, {"AttackType": "Charge", "Weight": 10}, {"AttackType": "Headbutt", "Weight": 10}], "Stats": {"MaxHealth": 150, "CurrentHp": 150, "Regen": 1,
          "Defence": 50, "MagicDefence": 10, 
          "Strength": 20, "MagicPower": 15, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 10, "Max": 150, "Weight": 0}, {"Item": "Exp", "Min": 150, "Max": 300, "Weight": 0}, {"Item": "Stab Scroll", "Weight": 3}, {"Item": "Charge Scroll", "Weight": 3}, {"Item": "Headbutt Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("Goblin"), "Special": None}
,"Ranged Goblin": {"Attacks": [{"AttackType": "Stab", "Weight": 10}, {"AttackType": "Charge", "Weight": 10}, {"AttackType": "Headbutt", "Weight": 10}, {"AttackType": "Shoot", "Weight": 10}, {"AttackType": "Fire", "Weight": 10}], "Stats": {"MaxHealth": 120, "CurrentHp": 120, "Regen": 2,
          "Defence": 30, "MagicDefence": 0, 
          "Strength": 40, "MagicPower": 20, "CritChance": 5, "CritPower": 130, "TrueAttack": 1, "TrueDefence": 1}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 10, "Max": 150, "Weight": 0}, {"Item": "Exp", "Min": 150, "Max": 300, "Weight": 0}, {"Item": "Fire Scroll", "Weight": 3}, {"Item": "Shoot Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("RangedGoblin"), "Special": None}
,"Dart Goblin": {"Attacks": [{"AttackType": "Stab", "Weight": 10}, {"AttackType": "Charge", "Weight": 10}, {"AttackType": "Headbutt", "Weight": 10}, {"AttackType": "Blowdart", "Weight": 10}, {"AttackType": "Breathe", "Weight": 10}], "Stats": {"MaxHealth": 80, "CurrentHp": 80, "Regen": 5,
          "Defence": 10, "MagicDefence": 10, 
          "Strength": 70, "MagicPower": 25, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 1}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 100, "Max": 200, "Weight": 0}, {"Item": "Exp", "Min": 225, "Max": 375, "Weight": 0}, {"Item": "Blowdart Scroll", "Weight": 3}, {"Item": "Breathe Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("DartGoblin"), "Special": None}

,"Wolf": {"Attacks": [{"AttackType": "Howl", "Weight": 10}, {"AttackType": "Bite", "Weight": 10}, {"AttackType": "Ferocious Swipe", "Weight": 10}], "Stats": {"MaxHealth": 140, "CurrentHp": 140, "Regen": 5,
          "Defence": 50, "MagicDefence": 50, 
          "Strength": 30, "MagicPower": 30, "CritChance": 5, "CritPower": 150, "TrueAttack": 1, "TrueDefence": 1}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 200, "Max": 300, "Weight": 0}, {"Item": "Exp", "Min": 200, "Max": 350, "Weight": 0}, {"Item": "Howl Scroll", "Weight": 3}, {"Item": "Bite Scroll", "Weight": 3}, {"Item": "Ferocious Swipe Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("Wolf"), "Special": None}
,"Silver Wolf": {"Attacks": [{"AttackType": "Howl", "Weight": 10}, {"AttackType": "Bite", "Weight": 10}, {"AttackType": "Ferocious Swipe", "Weight": 10}, {"AttackType": "Shining Ram", "Weight": 10}, {"AttackType": "Claw", "Weight": 10}], "Stats": {"MaxHealth": 300, "CurrentHp": 300, "Regen": 5,
          "Defence": 40, "MagicDefence": 40, 
          "Strength": 40, "MagicPower": 40, "CritChance": 5, "CritPower": 200, "TrueAttack": 1, "TrueDefence": 1}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 250, "Max": 400, "Weight": 0}, {"Item": "Exp", "Min": 300, "Max": 500, "Weight": 0}, {"Item": "Claw Scroll", "Weight": 3}, {"Item": "Shining Ram Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("SilverWolf"), "Special": None}
,"Alpha Wolf": {"Attacks": [{"AttackType": "Howl", "Weight": 10}, {"AttackType": "Bite", "Weight": 10}, {"AttackType": "Ferocious Swipe", "Weight": 10}, {"AttackType": "Shining Ram", "Weight": 10}, {"AttackType": "Claw", "Weight": 10}, {"AttackType": "Shread", "Weight": 30}, {"AttackType": "Endurance", "Weight": 30}], "Stats": {"MaxHealth": 1000, "CurrentHp": 1000, "Regen": 10,
          "Defence": 50, "MagicDefence": 50, 
          "Strength": 50, "MagicPower": 50, "CritChance": 10, "CritPower": 230, "TrueAttack": 10, "TrueDefence": 10}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 1800, "Max": 2500, "Weight": 0}, {"Item": "Exp", "Min": 1800, "Max": 2500, "Weight": 0}, {"Item": "Endurance Scroll", "Weight": 3}, {"Item": "Shread Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("AlphaWolf"), "Special": None}

,"Orc": {"Attacks": [{"AttackType": "Smack", "Weight": 10}, {"AttackType": "Stomp", "Weight": 10}, {"AttackType": "Shockwave", "Weight": 10}], "Stats": {"MaxHealth": 240, "CurrentHp": 240, "Regen": 5,
          "Defence": 40, "MagicDefence": 40, 
          "Strength": 60, "MagicPower": 10, "CritChance": 5, "CritPower": 100, "TrueAttack": 10, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 300, "Max": 500, "Weight": 0}, {"Item": "Exp", "Min": 500, "Max": 700, "Weight": 0}, {"Item": "Smack Scroll", "Weight": 3}, {"Item": "Stomp Scroll", "Weight": 3}, {"Item": "Shockwave Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("Orc"), "Special": None}
,"Cyclops": {"Attacks": [{"AttackType": "Eye Beam", "Weight": 10}, {"AttackType": "Focus", "Weight": 10}, {"AttackType": "Hypnotise", "Weight": 10}], "Stats": {"MaxHealth": 500, "CurrentHp": 500, "Regen": 10,
          "Defence": 20, "MagicDefence": 20, 
          "Strength": 50, "MagicPower": 20, "CritChance": 5, "CritPower": 100, "TrueAttack": 20, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 300, "Max": 500, "Weight": 0}, {"Item": "Exp", "Min": 500, "Max": 700, "Weight": 0}, {"Item": "Focus Scroll", "Weight": 3}, {"Item": "Eye Beam Scroll", "Weight": 3}, {"Item": "Hypnotise Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("Cyclops"), "Special": None}
,"Armored Orc": {"Attacks": [{"AttackType": "Smack", "Weight": 10}, {"AttackType": "Stomp", "Weight": 10}, {"AttackType": "Shockwave", "Weight": 10}, {"AttackType": "Slam", "Weight": 10}, {"AttackType": "Guard", "Weight": 10}], "Stats": {"MaxHealth": 250, "CurrentHp": 250, "Regen": 10,
          "Defence": 200, "MagicDefence": 200, 
          "Strength": 40, "MagicPower": 35, "CritChance": 5, "CritPower": 100, "TrueAttack": 25, "TrueDefence": 0}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 400, "Max": 650, "Weight": 0}, {"Item": "Exp", "Min": 900, "Max": 1600, "Weight": 0}, {"Item": "Slam Scroll", "Weight": 3}, {"Item": "Guard Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("ArmoredOrc"), "Special": None}
,"All-Seeing Orc": {"Attacks": [{"AttackType": "Eye Beam", "Weight": 10}, {"AttackType": "Focus", "Weight": 10}, {"AttackType": "Hypnotise", "Weight": 10}, {"AttackType": "Intense Glare", "Weight": 10}, {"AttackType": "Honed Club", "Weight": 10}], "Stats": {"MaxHealth": 200, "CurrentHp": 200, "Regen": 10,
          "Defence": -20, "MagicDefence": -20, 
          "Strength": 50, "MagicPower": 150, "CritChance": 5, "CritPower": 100, "TrueAttack": 1, "TrueDefence": 25}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 400, "Max": 800, "Weight": 0}, {"Item": "Exp", "Min": 900, "Max": 2000, "Weight": 0}, {"Item": "Intense Glare Scroll", "Weight": 3}, {"Item": "Honed Club Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("All-Seeing Orc"), "Special": None}

,"Spider": {"Attacks": [{"AttackType": "Web Shot", "Weight": 10}, {"AttackType": "Poison", "Weight": 10}, {"AttackType": "Crawl", "Weight": 10}], "Stats": {"MaxHealth": 100, "CurrentHp": 100, "Regen": 20,
          "Defence": 50, "MagicDefence": 50, 
          "Strength": 100, "MagicPower": 110, "CritChance": 5, "CritPower": 100, "TrueAttack": 10, "TrueDefence": 10}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 300, "Max": 500, "Weight": 0}, {"Item": "Exp", "Min": 800, "Max": 1000, "Weight": 0}, {"Item": "Poison Scroll", "Weight": 3}, {"Item": "Crawl Scroll", "Weight": 3}, {"Item": "Web Shot Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("Spider"), "Special": None}
,"Silkweaver": {"Attacks": [{"AttackType": "Web Shot", "Weight": 10}, {"AttackType": "Poison", "Weight": 10}, {"AttackType": "Crawl", "Weight": 10}, {"AttackType": "Silk-Blade", "Weight": 10}, {"AttackType": "Blood Drain", "Weight": 10}], "Stats": {"MaxHealth": 120, "CurrentHp": 120, "Regen": 20,
          "Defence": 80, "MagicDefence": 80, 
          "Strength": 120, "MagicPower": 150, "CritChance": 5, "CritPower": 100, "TrueAttack": 15, "TrueDefence": 50}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 300, "Max": 500, "Weight": 0}, {"Item": "Exp", "Min": 800, "Max": 1000, "Weight": 0}, {"Item": "Silk-Blade Scroll", "Weight": 3}, {"Item": "Blood Drain Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("Silkweaver"), "Special": None}
,"Jumping Spider": {"Attacks": [{"AttackType": "Web Shot", "Weight": 10}, {"AttackType": "Poison", "Weight": 10}, {"AttackType": "Crawl", "Weight": 10}, {"AttackType": "Jump", "Weight": 10}, {"AttackType": "Leap", "Weight": 10}], "Stats": {"MaxHealth": 50, "CurrentHp": 50, "Regen": 20,
          "Defence": 100, "MagicDefence": 100, 
          "Strength": 200, "MagicPower": 250, "CritChance": 5, "CritPower": 100, "TrueAttack": 50, "TrueDefence": 10}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 400, "Max": 600, "Weight": 0}, {"Item": "Exp", "Min": 1000, "Max": 2500, "Weight": 0}, {"Item": "Jump Scroll", "Weight": 3}, {"Item": "Leap Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("JumpingSpider"), "Special": None}


,"Dave (Angry)": {"Attacks": [{"AttackType": "Web Shot", "Weight": 10}], "Stats": {"MaxHealth": 9998, "CurrentHp": 9998, "Regen": 8,
          "Defence": 88, "MagicDefence": 88, 
          "Strength": 2, "MagicPower": 2, "CritChance": 2, "CritPower": 222, "TrueAttack": 2, "TrueDefence": 99}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 1, "Max": 10, "Weight": 0}, {"Item": "Exp", "Min": 1, "Max": 10, "Weight": 0}], "Effects": [], "Asset": assets.get("JumpingSpider"), "Special": None}
,"Dave (Normal)": {"Attacks": [{"AttackType": "Web Shot", "Weight": 10}], "Stats": {"MaxHealth": 10000, "CurrentHp": 10000, "Regen": 10,
          "Defence": 100, "MagicDefence": 100, 
          "Strength": 1, "MagicPower": 1, "CritChance": 0, "CritPower": 0, "TrueAttack": 1, "TrueDefence": 100}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 1, "Max": 10, "Weight": 0}, {"Item": "Exp", "Min": 1, "Max": 10, "Weight": 0}], "Effects": [], "Asset": assets.get("JumpingSpider"), "Special": None}
,"Dave (Displeased)": {"Attacks": [{"AttackType": "Web Shot", "Weight": 10}], "Stats": {"MaxHealth": 9999, "CurrentHp": 9999, "Regen": 9,
          "Defence": 99, "MagicDefence": 99, 
          "Strength": 1, "MagicPower": 1, "CritChance": 1, "CritPower": 111, "TrueAttack": 1, "TrueDefence": 99}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 1, "Max": 10, "Weight": 0}, {"Item": "Exp", "Min": 1, "Max": 10, "Weight": 0}], "Effects": [], "Asset": assets.get("JumpingSpider"), "Special": None}


,"Door": {"Attacks": [{"AttackType": "Web Shot", "Weight": 10}], "Stats": {"MaxHealth": 99999, "CurrentHp": 99999, "Regen": 100,
          "Defence": 100000, "MagicDefence": 100000, 
          "Strength": 100, "MagicPower": 100, "CritChance": 0, "CritPower": 0, "TrueAttack": 1, "TrueDefence": 100000}, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}, {"Item": "Research", "Min": 400, "Max": 600, "Weight": 0}, {"Item": "Exp", "Min": 1000, "Max": 2500, "Weight": 0}, {"Item": "Jump Scroll", "Weight": 3}, {"Item": "Leap Scroll", "Weight": 3}], "Effects": [], "Asset": assets.get("JumpingSpider"), "Special": None}


}
for dictionary in [attacks,enemies]:
    for key in dictionary:
        dictionary[key]["Name"]=key



pyterm.createItem("LevelUpStats", [assets.get("LevelUpStats")], "screen", "center", "center", 0, 0, 5)
pyterm.createItem("LevelUpTransition", ["".join(((72 - i * 3) * " " + "|" + (i * 6) * "š" + "|" + (72 - i * 3) * " " + "\n") for i2 in range(12)) for i in range(24)], "screen", "center", "center", 0, 0, 5)
pyterm.createItem("LevelUpText", [assets.get("LevelUpText")], "screen", "center", "center", 0, 0, -10)
pyterm.createItem("LevelUpHover", [assets.get("LevelUpHover" + str(i + 1)) for i in range(6)], "screen", "top left", "top left", 0, 0, 0)
LevelUp = False

#Enchanting
Enchants = False
pyterm.createItem("Enchant", [assets.get("Enchanting")], "screen", "center", "center", 0, 0, -11)
pyterm.createItem("EnchantCircle", [assets.get("EnchantCircle")], "Enchant", "top left", "center", 0, 0, 0)#73, 25
pyterm.createItem("EnchantStar", [assets.get("EnchantStar")], "Enchant", "top left", "center", 0, 0, 0)
RiseEnchantBool = False
RiseEnchant = 0
SpellCast = [False]
pyterm.createItem("EnchantLine", [""], "Enchant", "top left", "center", 0, 0, 0)
pyterm.createItem("EnchantItem", [""], "Enchant", "bottom right", "center", 0, -8, -15)
pyterm.createItem("EnchantScroll", [""], "Enchant", "bottom right", "center", 0, -100, -15)
pyterm.createItem("EnchantHelp", [assets.get("EnchantHelp")], "screen", "center", "center", 0, 0, 0)
FakeInv = False
FakeInv2 = False
FocusEnchant = False
FocusScroll = False
CastedSpells = {"Poisoning": [(27, 27), (80, 34), (27, 37), (69, 46), (53, 26)], 
                "Burning": [(26, 46), (35, 26), (54, 36), (75, 27), (83, 46)], 
                "Sharpened": [(81, 45), (81, 26), (24, 29), (71, 33), (25, 39), (71, 40)], 
                "Lifesteal": [(24, 26), (25, 45), (80, 36), (38, 27), (68, 44), (36, 36)], 
                "Embued": [(41, 44), (30, 36), (44, 28), (63, 28), (74, 36)], 
                "Swift": [(44, 27), (82, 37), (27, 46), (51, 36), (25, 27)], 
                "Defensive": [(33, 26), (71, 26), (71, 37), (53, 45), (33, 37), (33, 32)], 
                "Dev": [(24, 27), (23, 35), (77, 27), (77, 35), (24, 41), (37, 46), (61, 47), (75, 41), (37, 27), (37, 39), (63, 39), (61, 27), (49, 27), (23, 46), (83, 46), (48, 35)]}
#
#Home
pyterm.createItem("HomeEnchant", [assets.get("EnchantHome")], "screen", "center", "center", 0, -35, -8)
pyterm.createItem("HomeCraft", [assets.get("CraftHome")], "screen", "center", "center", 0, 35, -7)
pyterm.createItem("HomeShop", [assets.get("ShopHome")], "screen", "center", "center", 0, -35, 9)
pyterm.createItem("HomeEnchantRuin", [assets.get("EnchantHomeRuin")], "screen", "center", "center", 0, -35, -8)
pyterm.createItem("HomeCraftRuin", [assets.get("CraftHomeRuin")], "screen", "center", "center", 0, 35, -7)
pyterm.createItem("HomeShopRuin", [assets.get("ShopHomeRuin")], "screen", "center", "center", 0, -35, 9)

pyterm.createItem("RoomUi", [assets.get("RoomUi")], "screen", "center", "center", 0, 0, 16)
pyterm.createItem("HomeResearch", [assets.get("ResearchHome")], "screen", "center", "center", 0, 35, 8)
pyterm.createItem("Altar", [assets.get("Altar")], "screen", "center", "center", 0, 0, 0)

pyterm.createItem("RoomInteract", ["Press [E] into Interact"], "RoomUi", "center", "center", 0, 0, 0)
pyterm.createItem("LeaveRoom", [assets.get("LeaveRoom")], "screen", "center", "center", 0, 0, 0)


## ResearchUpgrades
ResearchUps = False
ResearchUpgrades = {"2xResearch": False, "Kills": False, "Light": False, "Level": False, "3xResearch": False, "Hierarchy": False, "Battle": False, "Research": False, "N/A1": None, "N/A2": None, "N/A3": None, "N/A4": None}
MechanicUpgrades = {"Crafting": False, "Attacks56": False, "Shop": False, "Enchanting": False, "Attacks78": False, "PerfectEnchants": False, "ResetStatUpgrades": False, "N/A1": None, "N/A2": None, "N/A3": None, "N/A4": None, "N/A5": None}
StatUpgrades = {"Strength1": False, "Strength2": False, "Strength3": False, "MagicPower1": False, "MagicPower2": False, "MagicPower3": False, #Powerful
                "Defence1": False, "Defence2": False, "MagicDefence1": False, "MagicDefence2": False, "Health1": False, "N/A1": None, #Tank
                "Skill1": False, "Skill2": False, "Intelligence1": False, "Intelligence2": False, "CritPower1": False, "CritChance1": False, #Wisdom
                "Dexterity1": False, "Dexterity2": False, "CastingSpeed1": False, "CastingSpeed2": False, "Regen1": False, "Regen2": False, #Efficient
                "Mana1": False, "Mana2": False, "Energy1": False, "Energy2": False, "ManaRegen1": False, "EnergyRegen1": False, #Stamina
                "TrueAttack1": False, "TrueDefence1": False, "N/A2": None, "N/A3": None, "N/A4": None, "N/A5": None, #Truth
                "Powerful": False, "Tank": False, "Wisdom": False, "Efficient": False, "Stamina": False, "Truth": False}
ResearchScreen = {"Type": "Research", "Screen": 0}
pyterm.createItem("ResearchUps", [assets.get("ResearchUpgrades"), assets.get("MechanicUpgrades"), assets.get("StatUpgrades")], "screen", "center", "center", 0, 4, 0)
pyterm.createItem("ResearchButtons", [assets["R-U" + str(i+1)] for i in range(8)]+["", "", "", ""], "ResearchUps", "top left", "top left", 0, 1, 3)
pyterm.createItem("MechanicButtons", [assets["M-U" + str(i+1)] for i in range(7)]+["", "", "", "", ""], "ResearchUps", "top left", "top left", 0, 1, 3)
pyterm.createItem("StatButtons", [assets["S-U" + str(i+1)] for i in range(6)]+[assets["S-U" + str(i+7)] for i in range(5)]+[""]+[assets["S-U" + str(i+12)] for i in range(6)]+[assets["S-U" + str(i+18)] for i in range(6)]+[assets["S-U" + str(i+24)] for i in range(6)]+[assets["S-U" + str(i+30)] for i in range(2)]+["","","",""]+[assets["S-U" + str(i+32)] for i in range(6)], "ResearchUps", "top left", "top left", 0, 1, 3)
pyterm.createItem("BoughtButtons", ["  Bought!  "], "ResearchButtons", "top left", "top left", 0, 1, 1)

def AddResearch(Research: int):
    global light, battles, enemiesKilled, level, highestHierarchy, ResearchUpgrades, research
    for upgrade in ResearchUpgrades.keys():
        if ResearchUpgrades[upgrade]:
            if str(upgrade) is "2xResearch":
                Research *= 2
            elif str(upgrade) is "Kills":
                Research *= (1 + 0.1 * enemiesKilled)
            elif str(upgrade) is "Light":
                Research *= 1.1 ** light
            elif str(upgrade) is "Level":
                Research *= (1 + 0.3 * level)
            elif str(upgrade) is "3xResearch":
                Research *= 3
            elif str(upgrade) is "Hierarchy":
                Research *= highestHierarchy
            elif str(upgrade) is "Battle":
                Research *= (1 + 0.5 * battles)
            elif str(upgrade) is "Research":
                Research *= (1 + research ** 0.125)
    return Research * 2

def BuyUpgrade(Type: str, Number: int):
    global ResearchUpgrades, MechanicUpgrades, StatUpgrades, research, player, LockedAttacks
    if Type is "Research":
        Upgrade = str(list(ResearchUpgrades.keys())[Number])
        if ResearchUpgrades[Upgrade] == False:
            if Upgrade is "2xResearch":
                if CheckResearchUpgrade(100):
                    ResearchUpgrades[Upgrade] = True
            if Upgrade is "Kills":
                if CheckResearchUpgrade(500):
                    ResearchUpgrades[Upgrade] = True
            if Upgrade is "Light":
                if CheckResearchUpgrade(5000):
                    ResearchUpgrades[Upgrade] = True
            if Upgrade is "Level":
                if CheckResearchUpgrade(25000):
                    ResearchUpgrades[Upgrade] = True
            if Upgrade is "3xResearch":
                if CheckResearchUpgrade(100000):
                    ResearchUpgrades[Upgrade] = True
            if Upgrade is "Hierarchy":
                if CheckResearchUpgrade(1500000):
                    ResearchUpgrades[Upgrade] = True
            if Upgrade is "Battle":
                if CheckResearchUpgrade(3000000):
                    ResearchUpgrades[Upgrade] = True
            if Upgrade is "Research":
                if CheckResearchUpgrade(99900000):
                    ResearchUpgrades[Upgrade] = True

    elif Type is "Mechanic":
        Upgrade = str(list(MechanicUpgrades.keys())[Number])
        if MechanicUpgrades[Upgrade] == False:
            if Upgrade is "Crafting":
                if CheckResearchUpgrade(2000):
                    MechanicUpgrades[Upgrade] = True
            if Upgrade is "Attacks56":
                if CheckResearchUpgrade(7500):
                    LockedAttacks["Attack4"] = False
                    LockedAttacks["Attack5"] = False
                    MechanicUpgrades[Upgrade] = True
            if Upgrade is "Shop":
                if CheckResearchUpgrade(10000):
                    MechanicUpgrades[Upgrade] = True
            if Upgrade is "Enchanting":
                if CheckResearchUpgrade(1000000):
                    MechanicUpgrades[Upgrade] = True
            if Upgrade is "Attacks78":
                if CheckResearchUpgrade(2000000):
                    LockedAttacks["Attack6"] = False
                    LockedAttacks["Attack7"] = False
                    MechanicUpgrades[Upgrade] = True
            if Upgrade is "PerfectEnchants":
                if CheckResearchUpgrade(25000000):
                    MechanicUpgrades[Upgrade] = True
            if Upgrade is "ResetStatUpgrades":
                if not (False in StatUpgrades.values()):
                    if CheckResearchUpgrade(10^9):
                        MechanicUpgrades[Upgrade] = True
                        for statupgrade in StatUpgrades.keys():
                            StatUpgrades[statupgrade] = False
                
    elif Type is "Stat":
        Upgrade = str(list(StatUpgrades.keys())[Number])
        if StatUpgrades[Upgrade] == False:
            if Upgrade is "Strength1":
                if CheckResearchUpgrade(5000):
                    StatUpgrades[Upgrade] = True
                    player["Strength"] += 10
            if Upgrade is "Strength2":
                if CheckResearchUpgrade(350000):
                    StatUpgrades[Upgrade] = True
                    player["Strength"] += 10
            if Upgrade is "Strength3":
                if CheckResearchUpgrade(3000000):
                    StatUpgrades[Upgrade] = True
                    player["Strength"] += 10
            if Upgrade is "MagicPower1":
                if CheckResearchUpgrade(5000):
                    StatUpgrades[Upgrade] = True
                    player["MagicPower"] += 10
            if Upgrade is "MagicPower2":
                if CheckResearchUpgrade(350000):
                    StatUpgrades[Upgrade] = True
                    player["MagicPower"] += 10
            if Upgrade is "MagicPower3":
                if CheckResearchUpgrade(3000000):
                    StatUpgrades[Upgrade] = True
                    player["MagicPower"] += 10

            if Upgrade is "Defence1":
                if CheckResearchUpgrade(25000):
                    StatUpgrades[Upgrade] = True
                    player["Defence"] += 15
            if Upgrade is "Defence2":
                if CheckResearchUpgrade(1000000):
                    StatUpgrades[Upgrade] = True
                    player["Defence"] += 15
            if Upgrade is "MagicDefence1":
                if CheckResearchUpgrade(25000):
                    StatUpgrades[Upgrade] = True
                    player["MagicDefence"] += 15
            if Upgrade is "MagicDefence2":
                if CheckResearchUpgrade(1000000):
                    StatUpgrades[Upgrade] = True
                    player["MagicDefence"] += 15
            if Upgrade is "Health1":
                if CheckResearchUpgrade(100000):
                    StatUpgrades[Upgrade] = True
                    player["MaxHealth"] += 25
                    player["CurrentHp"] += 25

            if Upgrade is "Skill1":
                if CheckResearchUpgrade(10000):
                    StatUpgrades[Upgrade] = True
                    player["Skill"] += 15
            if Upgrade is "Skill2":
                if CheckResearchUpgrade(750000):
                    StatUpgrades[Upgrade] = True
                    player["Skill"] += 15
            if Upgrade is "Intelligence1":
                if CheckResearchUpgrade(10000):
                    StatUpgrades[Upgrade] = True
                    player["Intelligence"] += 15
            if Upgrade is "Intelligence2":
                if CheckResearchUpgrade(750000):
                    StatUpgrades[Upgrade] = True
                    player["Intelligence"] += 15
            if Upgrade is "CritPower1":
                if CheckResearchUpgrade(150000):
                    StatUpgrades[Upgrade] = True
                    player["CritPower"] += 30
            if Upgrade is "CritChance1":
                if CheckResearchUpgrade(600000):
                    StatUpgrades[Upgrade] = True
                    player["CritChance"] += 5

            if Upgrade is "Dexterity1":
                if CheckResearchUpgrade(75000):
                    StatUpgrades[Upgrade] = True
                    player["Dexterity"] += 15
            if Upgrade is "Dexterity2":
                if CheckResearchUpgrade(2000000):
                    StatUpgrades[Upgrade] = True
                    player["Dexterity"] += 15
            if Upgrade is "CastingSpeed1":
                if CheckResearchUpgrade(75000):
                    StatUpgrades[Upgrade] = True
                    player["CastingSpeed"] += 15
            if Upgrade is "CastingSpeed2":
                if CheckResearchUpgrade(2000000):
                    StatUpgrades[Upgrade] = True
                    player["CastingSpeed"] += 15
            if Upgrade is "Regen1":
                if CheckResearchUpgrade(1000):
                    StatUpgrades[Upgrade] = True
                    player["Regen"] += 3
            if Upgrade is "Regen2":
                if CheckResearchUpgrade(1000000):
                    StatUpgrades[Upgrade] = True
                    player["Regen"] += 3
            
            if Upgrade is "Mana1":
                if CheckResearchUpgrade(1500):
                    StatUpgrades[Upgrade] = True
                    player["Mana"] += 20
            if Upgrade is "Mana2":
                if CheckResearchUpgrade(750000):
                    StatUpgrades[Upgrade] = True
                    player["Mana"] += 20
            if Upgrade is "Energy1":
                if CheckResearchUpgrade(1500):
                    StatUpgrades[Upgrade] = True
                    player["Energy"] += 20
            if Upgrade is "Energy2":
                if CheckResearchUpgrade(750000):
                    StatUpgrades[Upgrade] = True
                    player["Energy"] += 20
            if Upgrade is "ManaRegen1":
                if CheckResearchUpgrade(2000000):
                    StatUpgrades[Upgrade] = True
                    player["ManaRegen"] += 10
            if Upgrade is "EnergyRegen1":
                if CheckResearchUpgrade(2000000):
                    StatUpgrades[Upgrade] = True
                    player["EnergyRegen"] += 10
            
            if Upgrade is "TrueAttack1":
                if CheckResearchUpgrade(999000):
                    StatUpgrades[Upgrade] = True
                    player["TrueAttack"] += 5
            if Upgrade is "TrueDefence1":
                if CheckResearchUpgrade(999000):
                    StatUpgrades[Upgrade] = True
                    player["TrueDefence"] += 5

            if Upgrade is "Powerful":
                if CheckResearchUpgrade(2000000):
                    StatUpgrades[Upgrade] = True
            if Upgrade is "Tank":
                if CheckResearchUpgrade(2000000):
                    StatUpgrades[Upgrade] = True
            if Upgrade is "Wisdom":
                if CheckResearchUpgrade(100000):
                    StatUpgrades[Upgrade] = True
            if Upgrade is "Efficient":
                if CheckResearchUpgrade(100000):
                    StatUpgrades[Upgrade] = True
            if Upgrade is "Stamina":
                if CheckResearchUpgrade(500000):
                    StatUpgrades[Upgrade] = True
                    player["Energy"] += 30
                    player["Mana"] += 30
                    player["EnergyRegen"] += 15
                    player["ManaRegen"] += 15
            if Upgrade is "Truth":
                if CheckResearchUpgrade(20000000):
                    StatUpgrades[Upgrade] = True

def CheckResearchUpgrade(Number: int):
    global research
    if research < Number:
        return False
    research -= Number
    return True

SevenBuff = None
pyterm.createItem("Passives", [assets.get("WrathPassive"), assets.get("GluttonyPassive"), assets.get("DesirePassive"), assets.get("SlothPassive"), assets.get("EnvyPassive"), assets.get("PridePassive"), assets.get("GreedPassive")])

_attacks = []
for attackNum in range(8):
    if LockedAttacks["Attack" + str(attackNum)] == True:
        _attacks.append("LOCKED".center(30))
    elif EquippedAttacks["Attack" + str(attackNum)] == None or EquippedAttacks["Attack" + str(attackNum)] == "":
        _attacks.append("".center(30))
    else:
        _attacks.append(EquippedAttacks["Attack" + str(attackNum)].center(30))
pyterm.createItem("FightBox", [copy.deepcopy(YiPyterminal.ASSETS["fight box"][0])
                               .replace(">        PLACEHOLDER1        <", _attacks[0])
                               .replace(">        PLACEHOLDER2        <", _attacks[1])
                               .replace(">        PLACEHOLDER3        <", _attacks[2])
                               .replace(">        PLACEHOLDER4        <", _attacks[3])
                               .replace(">        PLACEHOLDER5        <", _attacks[4])
                               .replace(">        PLACEHOLDER6        <", _attacks[5])
                               .replace(">        PLACEHOLDER7        <", _attacks[6])
                               .replace(">        PLACEHOLDER8        <", _attacks[7])
                               +"\n└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘"], "screen", "center", "center", 0)

ChooseAttack = False
FocusAttack = False
Minigaming = True

FocusPlayerAttack = []

pyterm.createItem("MinigameUi", ["""┌----------------------------------------------------------------------------------------------------------------------------------┐
|                                                                                                                                  |
|                                                                                                                                  |
|                                                                                                                                  |
└----------------------------------------------------------------------------------------------------------------------------------┘"""], "screen", "center", "center", 0, 0, -17)
pyterm.createItem("MinigameScore", ["Score: 0"], "MinigameUi", "center", "center", 0, 0, 1)
pyterm.createItem("MinigameName", ["          "], "MinigameUi", "center", "center", 0, 0, -1)
pyterm.createItem("MinigameDesc", ["          "], "MinigameUi", "center", "center", 0, 0, 0)
CurrentRoom = None

pyterm.createItem("Enemy", [""], "screen", "center", "center", 0, 0, 0)

Crafting = False
RiseCrafting = 0
RiseCraftingBool = False
pyterm.createItem("Crafting", [assets.get("CraftingUi")], "screen", "center", "center", 0, 0, -11)
pyterm.createItem("CraftingHelp", [assets.get("CraftingHelp")], "screen", "center", "center", 0, 0, 0)
CraftingHelp = False
FocusCraft = False
pyterm.createItem("CraftRecipe", [""], "Crafting", "top left", "top left", 0, 4, 25)
pyterm.createItem("CraftRecipeResearch", ["[       ]"], "Crafting", "top left", "top right", 0, 84, 25)
CraftingCurrent = 0
FakeInv3 = False
pyterm.createItem("CraftingImg", [" "], "Crafting", "bottom right", "center", 0, -10, -21)
pyterm.createItem("CraftingDesc", [" "], "Crafting", "bottom right", "top left", 0, -18, -12)
pyterm.createItem("CraftingDesc2", [" "], "Crafting", "bottom right", "top left", 0, -18, -9)
FakeInv3Buffer = False

Shop = False
pyterm.createItem("ShopTime", [assets.get("ShopTime")], "screen", "center", "center", 0, 0, 0)
pyterm.createItem("ShopItems", [" "], "ShopTime", "top left", "top left", 0, 5, 9)
ShopItems = [{"Item": "Apple", "Price": 1}, {"Item": "Apple", "Price": 1}, {"Item": "Apple", "Price": 1}, {"Item": "Apple", "Price": 1}, {"Item": "Apple", "Price": 1}]

ShopList = {"Apple": {"PriceRange": (1000, 5000), "LightRequired": 1, "Weight": 10}, 
            "Punch Scroll": {"PriceRange": (1000, 2000), "LightRequired": 1, "Weight": 5},
            "Slash Scroll": {"PriceRange": (2000, 6000), "LightRequired": 5, "Weight": 5},
            "Bash Scroll": {"PriceRange": (50000, 100000), "LightRequired": 25, "Weight": 5},
            "Mash Scroll": {"PriceRange": (300000, 800000), "LightRequired": 30, "Weight": 5},
            "Meteoric Strike Scroll": {"PriceRange": (10000000, 30000000), "LightRequired": 40, "Weight": 5},
            "Blast Scroll": {"PriceRange": (12252, 12515), "LightRequired": 12, "Weight": 5},
            "Fireball Scroll": {"PriceRange": (3000, 15000), "LightRequired": 7, "Weight": 5},
            "Sweeping Edge Scroll": {"PriceRange": (15000, 18000), "LightRequired": 16, "Weight": 5},
            "Lightning Scroll": {"PriceRange": (10000, 12000), "LightRequired": 13, "Weight": 5},
            "Aim Scroll": {"PriceRange": (30000, 70000), "LightRequired": 18, "Weight": 5},
            "Premonition Scroll": {"PriceRange": (30000, 70000), "LightRequired": 18, "Weight": 5},
            "Weaken Scroll": {"PriceRange": (40000, 150000), "LightRequired": 21, "Weight": 5},
            "Stab Scroll": {"PriceRange": (300000, 850000), "LightRequired": 31, "Weight": 5},
            "Splash Scroll": {"PriceRange": (300000, 850000), "LightRequired": 31, "Weight": 5},
            "Health Potion": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Mana Potion": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Strength Potion": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Mystery Potion": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Net": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Smoke Bomb": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Focus Tomb": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Mirror Shard": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Bottled Mist": {"PriceRange": (10000, 15000), "LightRequired": 10, "Weight": 7},
            "Dynamite": {"PriceRange": (14000, 17000), "LightRequired": 15, "Weight": 7},

            "Monocle": {"PriceRange": (100000, 200000), "LightRequired": 12, "Weight": 5},
            "Miracle Gem": {"PriceRange": (100000, 200000), "LightRequired": 12, "Weight": 5},
            "Delicate Flower": {"PriceRange": (100000, 200000), "LightRequired": 12, "Weight": 5},
            "Creepy Idol": {"PriceRange": (100000, 200000), "LightRequired": 12, "Weight": 5},
            "Shield": {"PriceRange": (100000, 200000), "LightRequired": 12, "Weight": 3},
            "Pocket Watch": {"PriceRange": (100000, 200000), "LightRequired": 12, "Weight": 5}
}
        #  "Monocle": {"Name": "Monocle", "Type": "Extra", "Asset": assets.get("Monocle"), "Stats": {"MagicPower": 30, "CurrentHp": -5}, "Enchant": False, "Description": "Who left this here? Strange glistens show within the monocle, almost shining with aura. Boosts Magic Power, at a cost of -5 hp per turn.", "Id": None},
        #  "Miracle Gem": {"Name": "Miracle Gem", "Type": "Extra", "Asset": assets.get("Miracle Gem"), "Stats": {"CurrentHp": -1, "CurrentMana": 5}, "Enchant": False, "Description": "A gem that feels like it’s pulsating attached to a thin string of pure mana. Once on, it almost feels draining, yet replenishing? -1 hp +5 mana per turn.", "Id": None},
        #  "Delicate Flower": {"Name": "Delicate Flower", "Type": "Extra", "Asset": assets.get("Delicate Flower"), "Stats": {"CurrentHp": 5}, "Enchant": False, "Description": "A calming yet almost fragile peace emanates from the petals of this small bloom. Heals 5 hp per turn.", "Id": None},
        #  "Creepy Idol": {"Name": "Creepy Idol", "Type": "Offhand", "Asset": assets.get("Creepy Idol"), "Stats": {"Intelligence": 100}, "Enchant": False, "Description": "An ominous glare observes your every move. It seems to increase your intelligence...", "Id": None},
        #  "Shield": {"Name": "Shield", "Type": "Offhand", "Asset": assets.get("Shield"), "Stats": {"Defence": 30, "MagicDefence": 30}, "Enchant": False, "Description": "A shield made of pure void. It looks like it can swallow anything, like a black hole. Boosts defence and magic defence.", "Id": None},
        #  "Pocket Watch": {"Name": "Pocket Watch", "Type": "Offhand", "Asset": assets.get("Pocket Watch"), "Stats": {"Dexterity": 50}, "Enchant": False, "Description": "A golden, scratched watch with a long golden chain. Opening it reveals the glass cracked and endless sand pouring out. Boosts dexterity by a ton.", "Id": None},





def RefreshShop():
    global ShopList, ShopItems, light
    weight = []
    for i in ShopList.keys():
        if ShopList[i]["LightRequired"] <= light:
            for i2 in range(ShopList[i]["Weight"]):
                weight.append(i)
    ShopItems = []
    for i in range(5):
        chosenItem = random.choice(weight)
        ShopItems.append({"Item": chosenItem, "Price": random.randint(ShopList[chosenItem]["PriceRange"][0], ShopList[chosenItem]["PriceRange"][1])})

RefreshShop()

difficulty = 0

pyterm.createItem("BattleRewards", [assets.get("BattleRewards"), assets.get("BattleRewards2"), assets.get("PuzzleRewards")], "screen", "center", "center", 0, 0, 0)
pyterm.createItem("LightRewards", ["+ 1 Light", "+ 0 Light (Already Cleared)"], "BattleRewards", "top left", "top left", 0, 2, 4)
pyterm.createItem("ResearchRewards", ["+ 1 Research"], "BattleRewards", "top left", "top left", 0, 2, 5)
pyterm.createItem("ExpRewards", ["+ 1 Exp"], "BattleRewards", "top left", "top left", 0, 2, 6)
pyterm.createItem("ItemRewards", ["+ Item "], "BattleRewards", "top left", "top left", 0, 2, 7)
TotalResearch = 0
TotalItems = []
TotalExp = 0
RanAway = False

ConsumeInv = False
ConsumeInvBuffer = False

pyterm.createItem("EnemyBorder", [assets.get("EnemyBorder")], "screen", "center", "center", 0, 0, 0)

#Mazes
Mazes = [{"Maze1": """┌---┐|┌┬┬┬-|||-┬-
└┐||├┴┘|||┌┘└┤┌┤|
┌┘├┘├-┌-┘|└-┐├┘└┤
├-┘┌┴┐||-┴┐|└┘┌-┤
||┌┼-|└┼-┐└┘┌┐|||
|└┘└-┘┌┴-└--┘└-┴┘""", "Maze2": """◉*******5***X****
*****************
**************7**
***********#*****
***************** 
#****%***&*******""", "MazeRender1": [], "MazeRender2": [], "MazeBlocks": [], "SpawnLocation": (0, 0), "End": (0, 0), "InvisWalls": []}]

# room_push = [{"Character": "#", "Location": (0, 0)}, {"Character": "%", "Location": (1, 1)}]

pyterm.createItem("Maze", [assets.get("Maze")], "screen", "center", "center", 0, 0, 0)
pyterm.createItem("MazeContent", [""], "Maze", "center", "center", 0, 0, 0)
pyterm.createItem("MazeOther", [""], "Maze", "center", "top left", 0, 0, 0)

def MakeMaze(MazeNum: int):
    global Mazes, room_push
    MainMaze = Mazes[MazeNum]
    Maze1 = MainMaze["Maze1"].splitlines()
    Maze2 = MainMaze["Maze2"].splitlines()
    for mazeline in range(len(Maze1)):
        for char in range(len(Maze1[mazeline])):
            MainMaze["MazeRender1"].append({"Img": assets.get("Maze" + str(Maze1[mazeline][char])), "Location": (-57 + 7 * char, -10 + 4 * mazeline)})
    for mazeline in range(len(Maze2)):
        for char in range(len(Maze2[mazeline])):
            if Maze2[mazeline][char] == "#":
                MainMaze["MazeBlocks"].append({"Character": "#", "Location": (-60 - 4 + 7 + 7 * char, -12 + 2 + 4 * mazeline)})
            elif Maze2[mazeline][char] == "$":
                MainMaze["MazeRender2"].append({"Img": " $$$$ \n $$$$ \n $$$$ ", "Location": (-59 + 7 * char, -11 + 4 * mazeline)})
            elif Maze2[mazeline][char] == "%":
                MainMaze["MazeRender2"].append({"Img": " %%%% \n %%%% \n %%%% ", "Location": (-59 + 7 * char, -11 + 4 * mazeline)})
            elif Maze2[mazeline][char] == "&":
                MainMaze["MazeRender2"].append({"Img": " &&&& \n &&&& \n &&&& ", "Location": (-59 + 7 * char, -11 + 4 * mazeline)})
            elif Maze2[mazeline][char] == "4":
                MainMaze["MazeRender2"].append({"Img": "$$$$$$\n$    $\n$$$$$$", "Location": (-59 + 7 * char, -11 + 4 * mazeline), "Type": "$", "Render": True})
                MainMaze["InvisWalls"].append([[-59 + 7 * char, -11 + 4 * mazeline], [-59 + 7 * char + 5, -11 + 4 * mazeline + 2], True, "$"])
            elif Maze2[mazeline][char] == "5":
                MainMaze["MazeRender2"].append({"Img": "%%%%%%\n%    %\n%%%%%%", "Location": (-59 + 7 * char, -11 + 4 * mazeline), "Type": "%", "Render": True})
                MainMaze["InvisWalls"].append([[-59 + 7 * char, -11 + 4 * mazeline], [-59 + 7 * char + 5, -11 + 4 * mazeline + 2], True, "%"])
            elif Maze2[mazeline][char] == "7":
                MainMaze["MazeRender2"].append({"Img": "&&&&&&\n&    &\n&&&&&&", "Location": (-59 + 7 * char, -11 + 4 * mazeline), "Type": "&", "Render": True})
                MainMaze["InvisWalls"].append([[-59 + 7 * char, -11 + 4 * mazeline], [-59 + 7 * char + 5, -11 + 4 * mazeline + 2], True, "&"])
            elif Maze2[mazeline][char] == "◉":
                MainMaze["MazeRender2"].append({"Img": "◉", "Location": (-56 + 7 * char, -10 + 4 * mazeline)})
                MainMaze["SpawnLocation"] = (-59 + 7 * char, -11 + 4 * mazeline)
            elif Maze2[mazeline][char] == "X":
                MainMaze["MazeRender2"].append({"Img": "X", "Location": (-56 + 7 * char, -10 + 4 * mazeline)})
                MainMaze["End"] = (-59 + 7 * char, -11 + 4 * mazeline)

for i in range(len(Mazes)):
    MakeMaze(i)
WonPuzzle = False
addedResearch = 0

pyterm.createItem("RoomPuzzleHints", ["Try to reach the 'X' by pushing the '#'s onto the pressure plates (Filled in). Press 'R' to reset."], "RoomUi", "center", "center", 0, 0, -1)
pyterm.createItem("RoomPuzzleHints2", ["Note: You may sometimes noclip through push blocks. That is due to their totally special properties."], "RoomUi", "center", "center", 0, 0, 1)

InventoryState = 0

pyterm.createItem("Ending", [assets.get("Ending")], "screen", "center", "center", 0, 0, 0)
def End():
    global DisableOther, LeftClick, LeftClickCopy, location, light
    DisableOther = True
    LeftClick = LeftClickCopy
    pyterm.renderItem("Ending")
    if (pyterm.getBottomLeft()[0] + 1 <= location[0] <= pyterm.getBottomLeft()[0] + 16) and (round(location[1]) == pyterm.getBottomLeft()[0] - 1) and LeftClick:
        light = 100
        DisableOther = False
    elif (pyterm.getBottomRight()[0] - 1 <= location[0] <= pyterm.getBottomRight()[0] - 16) and (round(location[1]) == pyterm.getBottomLeft()[0] - 1) and LeftClick:
        os.sys("exit")
    


PhaseChange("battle")
PhaseChange("title")

YiPyterminal.initializeTerminal(1, character_size) 
YiPyterminal.startAsynchronousMouseListener()
CopyPaste = True
while True:
    startTime = time.perf_counter()
    YiPyterminal.updateScreenSize()
    pyterm.clearLettersToRender()
    pyterm.updateKeyboardBindStatus()
    YiPyterminal.copyMouseStatus(resetMouseStatusAfterCopy=True)
    MainClock += 1

    if CopyPaste:
        ctypes.windll.user32.OpenClipboard()
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.CloseClipboard()
    if Cursor.is_full_screen() == "maximized":
        NonCenterOffset = 1
    elif Cursor.is_full_screen():
        NonCenterOffset = 3
    else:
        NonCenterOffset = 0
    keyboard.block_key("ctrl")
    location = Cursor.get_mouse_coords(character_size, True)
    LeftClick = MouseDetect.ClickDetect("Left", "On")
    RightClick = MouseDetect.ClickDetect("Right", "On")
    LeftClickCopy = LeftClick
    RightClickCopy = RightClick
    if DisableOther:
        LeftClick = False
        RightClick = False

    UiOffset = [0, 0]
    Ui = True

    #Updating stats
    if (experience >= max_experience) and (not LevelUp):
        experience -= max_experience
        level = min(level + 1, math.inf)
        try:
            max_experience = round((math.log((math.e / 2) ** (level - 1) + math.gamma(level ** 1.35)/(level ** (level / 4)), max(10 * math.pi / level, 1 + 1/level)) + 0.798935) * 100)
        except OverflowError:
            max_experience = round((math.log((math.e / 2) ** (level - 1) + math.gamma(45 ** 1.35)/(level ** (level / 4)), max(10 * math.pi / level, 1 + 1/((level - 35) ** 1.75 + 1.1 ** (level - 40)))) + 0.798935) * 100)
        LevelUp = True
    light = len(ClearedRooms)
    research = round(research)
    for i in ClearedRooms:
        if highestHierarchy < i[0]:
            highestHierarchy = i[0]
    experience = round(experience)
    player["CurrentHp"] = min(player["CurrentHp"], player["MaxHealth"])
    player["CurrentMana"] = min(player["CurrentMana"], player["Mana"])
    player["CurrentEnergy"] = min(player["CurrentEnergy"], player["Energy"])
    for craft in CraftingRecipes.keys():
        if light >= CraftingRecipes[craft]["LightRequirements"]:
            if not (craft in AvaliableRecipes):
                AvaliableRecipes.append(craft)


    if phase.lower() == "title":
        Ui = False
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
                pyterm.changeCurrentItemFrame("SettingsRoomsNormal", 1)
                pyterm.changeCurrentItemFrame("SettingsRoomsObfuscated", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsAnimated", 0)
            elif SettingsRooms == 2:
                pyterm.changeCurrentItemFrame("SettingsRoomsNormal", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsObfuscated", 1)
                pyterm.changeCurrentItemFrame("SettingsRoomsAnimated", 0)
            elif SettingsRooms == 3:
                pyterm.changeCurrentItemFrame("SettingsRoomsNormal", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsObfuscated", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsAnimated", 1)
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
            GreedLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 60, -73 + min(riseTitle, 64), "center", "center")
            PrideLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 40, -76 + min(riseTitle, 61), "center", "center")
            EnvyLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 20, -67 + min(riseTitle, 58), "center", "center")
            SlothLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), 0, -70 + min(riseTitle, 55), "center", "center")
            DesireLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), -20, -61 + min(riseTitle, 51), "center", "center")
            GluttonyLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), -40, -64 + min(riseTitle, 49), "center", "center")
            WrathLoc = pyterm.renderLiteralItem(assets.get("TitleHexagon"), -60, -55 + min(riseTitle, 46), "center", "center")
            #7sins buttondetect
            if (math.hypot((WrathLoc[0] - location[0]), 2 * (WrathLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("UNYIELDING", -60, -55 + min(riseTitle, 46) + 15, "center", "center")
                pyterm.changeCurrentItemFrame("Passives", 0)
                pyterm.renderItem("Passives", xBias = location[0], yBias = location[1], screenLimits=None)
                if LeftClick:
                    PhaseChange("map")
                    SevenBuff = "Wrath"
            else:
                pyterm.renderLiteralItem("UNYIELDING", -60, -55 + min(riseTitle, 46) + 15, "center", "center")
            if (math.hypot((GluttonyLoc[0] - location[0]), 2 * (GluttonyLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("SWEET TOOTH", -40, -64 + min(riseTitle, 49) + 15, "center", "center")
                pyterm.changeCurrentItemFrame("Passives", 1)
                pyterm.renderItem("Passives", xBias = location[0], yBias = location[1], screenLimits=None)
                if LeftClick:
                    PhaseChange("map")
                    SevenBuff = "Gluttony"
            else:
                pyterm.renderLiteralItem("SWEET TOOTH", -40, -64 + min(riseTitle, 49) + 15, "center", "center")
            if (math.hypot((DesireLoc[0] - location[0]), 2 * (DesireLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("CHARISMATIC", -20, -61 + min(riseTitle, 51) + 15, "center", "center")
                pyterm.changeCurrentItemFrame("Passives", 2)
                pyterm.renderItem("Passives", xBias = location[0], yBias = location[1], screenLimits=None)
                if LeftClick:
                    PhaseChange("map")
                    SevenBuff = "Desire"
            else:
                pyterm.renderLiteralItem("CHARISMATIC", -20, -61 + min(riseTitle, 51) + 15, "center", "center")
            if (math.hypot((SlothLoc[0] - location[0]), 2 * (SlothLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("LAID BACK", 0, -70 + min(riseTitle, 55) + 15, "center", "center")
                pyterm.changeCurrentItemFrame("Passives", 3)
                pyterm.renderItem("Passives", xBias = location[0], yBias = location[1], screenLimits=None)
                if LeftClick:
                    PhaseChange("map")
                    SevenBuff = "Sloth"
            else:
                pyterm.renderLiteralItem("LAID BACK", 0, -70 + min(riseTitle, 55) + 15, "center", "center")
            if (math.hypot((EnvyLoc[0] - location[0]), 2 * (EnvyLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("ATTENTIVE", 20, -67 + min(riseTitle, 58) + 15, "center", "center")
                pyterm.changeCurrentItemFrame("Passives", 4)
                pyterm.renderItem("Passives", xBias = location[0], yBias = location[1], screenLimits=None)
                if LeftClick:
                    PhaseChange("map")
                    SevenBuff = "Envy"
            else:
                pyterm.renderLiteralItem("ATTENTIVE", 20, -67 + min(riseTitle, 58) + 15, "center", "center")
            if (math.hypot((PrideLoc[0] - location[0]), 2 * (PrideLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("PERFECTIONISM", 40, -76 + min(riseTitle, 61) + 15, "center", "center")
                pyterm.changeCurrentItemFrame("Passives", 5)
                pyterm.renderItem("Passives", xBias = location[0] - 27, yBias = location[1], screenLimits=None)
                if LeftClick:
                    PhaseChange("map")
                    SevenBuff = "Pride"
            else:
                pyterm.renderLiteralItem("PERFECTIONISM", 40, -76 + min(riseTitle, 61) + 15, "center", "center")
            if (math.hypot((GreedLoc[0] - location[0]), 2 * (GreedLoc[1] + 14.5 - location[1])) <= 11.5) and (riseTitle == 70):
                pyterm.renderLiteralItem("LUCKY", 60, -73 + min(riseTitle, 64) + 15, "center", "center")
                pyterm.changeCurrentItemFrame("Passives", 6)
                pyterm.renderItem("Passives", xBias = location[0] - 27, yBias = location[1], screenLimits=None)
                if LeftClick:
                    PhaseChange("map")
                    SevenBuff = "Greed"
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
        pyterm.renderItem("EmptyBackground", createItemIfNotExists=True, createItemArgs = {"animationFrames": [assets.get("EmptyBackground")], "parentObject": "screen", "parentAnchor": "center", "childAnchor": "center"}, screenLimits = (os.get_terminal_size().columns, os.get_terminal_size().lines))


    elif phase.lower() == "map":
        Minigaming = True
        if MainClock- firstFrame>=100:
            YiPyterminal.clearDebugMessages() 
        if not GetRoomLoc:
            for Line in LinesRooms:
                # pyterm.renderItem(Line["Line"], xBias = round(Line["Pos"][0]) + mapOffset[0], yBias = round(Line["Pos"][1]) + mapOffset[1])
                pyterm.renderItem(str(Line["Pos1"]) + str(Line["Pos2"]), xBias=mapOffset[0], yBias=mapOffset[1], screenLimits=(999, 999))

        if GetRoomLoc:
            pyterm.createItem(str((0, 1)), [assets["FilledBlackHole"]], "screen", "center", "center", 0, 0, 0)
            hierarchyLocations.append([{"Location": (0, 0), "id": (0, 1), "Connections": [], "Movements": []}])
        pyterm.renderItem(str((0, 1)), xBias = mapOffset[0], yBias = mapOffset[1], screenLimits=(999, 999))
        if (os.get_terminal_size().columns/2 + mapOffset[0] - 8 <= location[0] <= os.get_terminal_size().columns/2 + mapOffset[0] + 8 - 1) and (os.get_terminal_size().lines/2 + mapOffset[1] - 4 <= location[1] <= os.get_terminal_size().lines/2 + mapOffset[1] + 4):
            # pyterm.renderLiteralItem("AAA", round(mapOffset[0]), round(mapOffset[1]), "center", "center")
            pyterm.renderLiteralItem("Home", round(mapOffset[0]), round(mapOffset[1]), "center", "center")
        else:
            pyterm.renderLiteralItem("Home", round(mapOffset[0]), round(mapOffset[1]), "center", "center")
        for i in range(Hierarchy):
            MaxRooms = (i + 1) * 3 + 1 #4, 7, 10, 13, 16, 19, 22 = 91 Rooms
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
            if GetRoomLoc:
                hierarchyLocations.append(hierarchyLocations2)
                hierarchyLocations2 = []

        if GetRoomLoc:
            for tier in hierarchyLocations:
                for rooms in tier:
                    if rooms["id"][0] > 0:
                        RoomData[copy.deepcopy(rooms["id"])] = {"Type": random.choice(["Treasure" for i in range(0)] +["Puzzle" for i in range(2)] + ["Battle" for i in range(7)]), "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3), "SpawnLocation": (0, 0), "Difficulty": random.randint(80, 120)/100}
                        if rooms["id"] == (3, 1):
                            RoomData[copy.deepcopy(rooms["id"])] = {"Type": "BossBattle1", "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3), "SpawnLocation": (0, 0), "Difficulty": 1}
                        elif rooms["id"] == (5, 1):
                            RoomData[copy.deepcopy(rooms["id"])] = {"Type": "BossBattle2", "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3), "SpawnLocation": (0, 0), "Difficulty": 1}
                        elif rooms["id"] == (7, 1):
                            RoomData[copy.deepcopy(rooms["id"])] = {"Type": "BossBattle3", "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3), "SpawnLocation": (0, 0), "Difficulty": 1}
                        elif rooms["id"] == (1, 1):
                            RoomData[copy.deepcopy(rooms["id"])] = {"Type": "Battle", "LightRequired": 1, "SpawnLocation": (0, 0), "Difficulty": random.randint(80, 120)/100}
                        elif rooms["id"] == (1, 2):
                            RoomData[copy.deepcopy(rooms["id"])] = {"Type": "Battle", "LightRequired": 1, "SpawnLocation": (0, 0), "Difficulty": random.randint(80, 120)/100}
                        elif rooms["id"] == (1, 3):
                            RoomData[copy.deepcopy(rooms["id"])] = {"Type": "Battle", "LightRequired": 1, "SpawnLocation": (0, 0), "Difficulty": random.randint(80, 120)/100}
                        elif rooms["id"] == (1, 4):
                            RoomData[copy.deepcopy(rooms["id"])] = {"Type": "Puzzle", "LightRequired": 1, "SpawnLocation": (0, 0), "Difficulty": random.randint(80, 120)/100}
                        if RoomData[rooms["id"]]["Type"] == "Puzzle":
                            RoomData[rooms["id"]]["Special"] = random.choice(Mazes)
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
            pyterm.changeCurrentItemFrame("RoomSidebar", 0)
            if (os.get_terminal_size().columns - 24 <= location[0] <= os.get_terminal_size().columns) and (NonCenterOffset + 39 + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2) <= location[1] <= NonCenterOffset + 43 + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2)):
                pyterm.changeCurrentItemFrame("RoomSidebar", 1)
                if LeftClick and not (TargetLocation[2] is 1):
                    FocusRoom = False
            #Play
            if (os.get_terminal_size().columns - 24 <= location[0] <= os.get_terminal_size().columns) and (10 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2) <= location[1] <= 14 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2)):
                if ((itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHole")) or (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHoleClose"))):
                    pyterm.changeCurrentItemFrame("RoomSidebar", 2)
                    if (LeftClick) and not (TargetLocation[2] is 1):
                        AnimateRoomEntry = FocusRoom
                        TargetLocation[2] = 1
                        TargetLocation[0] = -FocusRoom["Location"][0]
                        TargetLocation[1] = -FocusRoom["Location"][1]
                        EnteredRoom = FocusRoom["id"]
                        FocusRoom = False
            if keyboard.is_pressed("x"):
                FocusRoom = False
            #Play
            if keyboard.is_pressed("e") and ((itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHole")) or (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHoleClose"))):
                AnimateRoomEntry = FocusRoom
                TargetLocation[2] = 1
                TargetLocation[0] = -FocusRoom["Location"][0]
                TargetLocation[1] = -FocusRoom["Location"][1]
                EnteredRoom = FocusRoom["id"]
                FocusRoom = False
            if FocusRoom:
                pyterm.renderItem("RoomSelect", xBias = FocusRoom["Location"][0] + mapOffset[0], yBias = FocusRoom["Location"][1] +  mapOffset[1], screenLimits = (999, 999), createItemIfNotExists = True, createItemArgs = {"animationFrames": [assets.get("RoomSelect")], "parentObject": "screen", "parentAnchor": "center", "childAnchor": "center", "currentFrame": 0})
                if (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHole")) or (itemObjects[str(FocusRoom["id"])]["animation frames"][itemObjects[str(FocusRoom["id"])]["current frame"]] is assets.get("FilledBlackHoleClose")):
                    itemObjects["RoomHierarchy"]["animation frames"][0] = "Hierarchy: " + str(FocusRoom["id"][0])
                    itemObjects["RoomNo."]["animation frames"][0] = "Room Number: " + str(FocusRoom["id"][1])
                    if "Difficulty" in RoomData[FocusRoom["id"]].keys():
                        itemObjects["RoomDifficulty"]["animation frames"][0] = "Difficulty: " + str(RoomData[FocusRoom["id"]]["Difficulty"])
                    else:
                        itemObjects["RoomDifficulty"]["animation frames"][0] = "Difficulty: N/A"
                    itemObjects["RoomLightRequirements"]["animation frames"][0] = "Light Required: " + str(RoomData[FocusRoom["id"]]["LightRequired"])
                else:
                    itemObjects["RoomHierarchy"]["animation frames"][0] = "Hierarchy: ???"
                    itemObjects["RoomNo."]["animation frames"][0] = "Room Number: ???"
                    itemObjects["RoomDifficulty"]["animation frames"][0] = "Difficulty: ???"
                    itemObjects["RoomLightRequirements"]["animation frames"][0] = "Light Required: " + str(RoomData[FocusRoom["id"]]["LightRequired"])
                    pyterm.changeCurrentItemFrame("RoomSidebar", 3)
                pyterm.changeItemFrameContent("RoomType", "Type: " + str(RoomData[FocusRoom["id"]]["Type"]))
                pyterm.updateItemSize("RoomDifficulty")
                pyterm.updateItemSize("RoomLightRequirements")
                pyterm.updateItemSize("RoomType")
                pyterm.renderItem("RoomSidebar", yBias = NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomHierarchy", xBias = -11, yBias = 6 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomNo.", xBias = -11, yBias = 7 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomType", xBias = -11, yBias = 18 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomDifficulty", xBias = -11, yBias = 19 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomLightRequirements", xBias = -11, yBias = 20 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                if os.get_terminal_size().columns < 180:
                    UiOffset[0] = -10
                #pyterm.renderItem("RoomNo.", xBias = -12, yBias = 13)
        
        if AnimateRoomEntry:
            if itemObjects["RoomEntryAnimation"]["current frame"] + 1 >= 15:
                pyterm.changeCurrentItemFrame("RoomEntryAnimation", 0)
                if "Difficulty" in RoomData[AnimateRoomEntry["id"]].keys():
                    difficulty = RoomData[AnimateRoomEntry["id"]]["Difficulty"]
                else:
                    difficulty = 1
                if RoomData[AnimateRoomEntry["id"]]["Type"] == "Puzzle":
                    PhaseChange("room")
                elif RoomData[AnimateRoomEntry["id"]]["Type"] == "Battle":
                    if (AnimateRoomEntry["id"][0] == 1):
                        mobsStatus = [random.choice(["Slime", "Slime", "Slime", "Large Slime", "Large Slime", "Corrosive Slime"]) for i in range(1)]
                    if (AnimateRoomEntry["id"][0] == 2):
                        mobsStatus = [random.choice(["Slime", "Slime", "Slime", "Large Slime", "Large Slime", "Corrosive Slime", "Corrosive Slime", "Giga Slime"]) for i in range(2)]
                    if (AnimateRoomEntry["id"][0] == 3):
                        mobsStatus = [random.choice(["Slime", "Slime", "Slime", "Large Slime", "Large Slime", "Corrosive Slime", "Corrosive Slime", "Giga Slime", "Goblin", "Goblin", "Ranged Goblin", "Ranged Goblin", "Dart Goblin"]) for i in range(3)]
                    if (AnimateRoomEntry["id"][0] == 4):
                        mobsStatus = [random.choice(["All-Seeing Orc", "Armored Orc", "Cyclops", "Orc", "Silver Wolf", "Silver Wolf", "Orc", "Cyclops", "Wolf", "Wolf", "Wolf"]) for i in range(3)]
                    if (AnimateRoomEntry["id"][0] == 5):
                        mobsStatus = [random.choice(["All-Seeing Orc", "Armored Orc", "All-Seeing Orc", "Armored Orc", "Cyclops", "Orc", "Silver Wolf", "Orc", "Cyclops", "Wolf"]) for i in range(3)]
                    if (AnimateRoomEntry["id"][0] == 6):
                        mobsStatus = [random.choice(["Spider", "Spider", "Spider", "Silkweaver", "Silkweaver", "Silkweaver", "Jumping Spider", "Jumping Spider", "Jumping Spider"]) for i in range(3)]
                    if (AnimateRoomEntry["id"][0] == 7):
                        mobsStatus = [random.choice(["All-Seeing Orc", "Armored Orc", "All-Seeing Orc", "Armored Orc", "Cyclops", "Orc", "Spider", "Spider", "Spider", "Silkweaver", "Silkweaver", "Silkweaver", "Jumping Spider", "Jumping Spider", "Jumping Spider", "Orc", "Cyclops"]) for i in range(4)]

                    PhaseChange("battle")
                elif RoomData[AnimateRoomEntry["id"]]["Type"] == "Treasure":
                    PhaseChange("room")
                elif RoomData[AnimateRoomEntry["id"]]["Type"] == "BossBattle1":
                    mobsStatus = ["Offensive Slime", "Defensive Slime", "Giga Slime", "Corrosive Slime"]
                    PhaseChange("battle")
                elif RoomData[AnimateRoomEntry["id"]]["Type"] == "BossBattle2":
                    mobsStatus = ["Alpha Wolf", "Silver Wolf", "Wolf"]
                    PhaseChange("battle")
                elif RoomData[AnimateRoomEntry["id"]]["Type"] == "BossBattle3":
                    mobsStatus = ["Orc", "Cyclops", "Armored Orc", "All-Seeing Orc", "Spider", "Silkweaver", "Jumping Spider"]
                    PhaseChange("battle")
                elif RoomData[AnimateRoomEntry["id"]]["Type"] == "Home":
                    PhaseChange("room")
                # ClearedRooms.append(AnimateRoomEntry["id"])
                CurrentRoom = AnimateRoomEntry["id"]
                AnimateRoomEntry = False
                FocusRoom = False
                # PhaseChange("Battle")
            else:
                pyterm.renderItem("RoomEntryAnimation", xBias = AnimateRoomEntry["Location"][0] + mapOffset[0], yBias = AnimateRoomEntry["Location"][1] + mapOffset[1], screenLimits= (999, 999))
                pyterm.changeCurrentItemFrame("RoomEntryAnimation", itemObjects["RoomEntryAnimation"]["current frame"] + 1)

        # pyterm.renderLiteralItem("X", FocusRoom["Location"][0] + mapOffset[0], FocusRoom["Location"][1] + mapOffset[1], "center", "center")

        if not DisableOther:
            if not MouseDetect.ClickDetect("Right", "Held"):
                InitialHold = location
                mapOffsetCopy = mapOffset.copy()
            else:
                locationMapDiff = [location[0] - InitialHold[0], location[1] - InitialHold[1]]
                mapOffset = [mapOffsetCopy[0] + locationMapDiff[0], mapOffsetCopy[1] + locationMapDiff[1]]
                TargetLocation[2] = 0

        if not DisableOther:
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
        if RoomData[EnteredRoom]["Type"] == "Home":
            room_size = [100, 25]
            RoomException = True
        else:
            RoomException = False
            if RoomData[EnteredRoom]["Type"] == "Puzzle":
                room_size = [118, 23]
                room_walls = ["|", "-", "_", "¯", "┐", "└", "┘", "┌", "┴", "┬", "├", "┤", "┼", "#", "\\", "/", "O", "●", ">", "<", ".", "[", "]", "{", "}", "="]
        itemObjects["RoomSize"]["animation frames"][0] = pyterm.addBorder("".join("".join(" " for i2 in range(room_size[0])) + "\n" for i3 in range(room_size[1])), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})
        pyterm.updateItemSize("RoomSize")
        pyterm.renderItem("RoomSize", screenLimits= (999, 999))

        pyterm.renderItem("RoomUi")
        pyterm.renderItem("LeaveRoom", xBias = -round(room_size[0]/2) - 4)
        if (pyterm.getTopLeft("LeaveRoom")[0]-round(room_size[0]/2) - 4 <= location[0] <= pyterm.getBottomRight("LeaveRoom")[0]-round(room_size[0]/2) - 4) and (pyterm.getTopLeft("LeaveRoom")[1] <= location[1] <= pyterm.getBottomRight("LeaveRoom")[1]) and LeftClick:
            PhaseChange("map")

        #Home
        if RoomData[EnteredRoom]["Type"] is "Home":
            room_walls = ["|", "-", "_", "¯", "┐", "└", "┘", "┌", "┴", "┬", "├", "┤", "┼", "#", "\\", "/", "O", "◉", ">", "<", ".", "[", "]", "{", "}", "="]

            if MechanicUpgrades["Enchanting"]:
                pyterm.renderItem("HomeEnchant")
                if (pyterm.getTopLeft("HomeEnchant")[0] + 3 <= pyterm.getCenter("PlayerMove")[0]+round(player_x) <= pyterm.getTopLeft("HomeEnchant")[0] + 11) and (pyterm.getTopLeft("HomeEnchant")[1] + 1 <= pyterm.getCenter("PlayerMove")[1]+round(player_y) <= pyterm.getTopLeft("HomeEnchant")[1] + 5):
                    pyterm.renderItem("RoomInteract")
                    if keyboard.is_pressed("e"):
                        RiseEnchantBool = True
                        Enchants = True
                        DisableOther = True
                        EnchantHelp = False
            else:
                pyterm.renderItem("HomeEnchantRuin")

            if MechanicUpgrades["Crafting"]:
                pyterm.renderItem("HomeCraft")
                if (pyterm.getTopLeft("HomeCraft")[0] <= pyterm.getCenter("PlayerMove")[0]+round(player_x) <= pyterm.getBottomRight("HomeCraft")[0]) and (pyterm.getTopLeft("HomeCraft")[1] <= pyterm.getCenter("PlayerMove")[1]+round(player_y) <= pyterm.getBottomRight("HomeCraft")[1]):
                    pyterm.renderItem("RoomInteract")
                    if keyboard.is_pressed("e"):
                        Crafting = True
                        DisableOther = True
                        RiseCraftingBool = True
                        CraftingHelp = False
                        FocusCraft = False
                        CraftingCurrent = 0
                        FakeInv3 = False
                        FakeInv3Buffer = False
            else:
                pyterm.renderItem("HomeCraftRuin")

            if MechanicUpgrades["Shop"]:
                pyterm.renderItem("HomeShop")
                if (pyterm.getTopLeft("HomeShop")[0] - 1 <= pyterm.getCenter("PlayerMove")[0]+round(player_x) <= pyterm.getBottomRight("HomeShop")[0] + 1) and (pyterm.getTopLeft("HomeShop")[1] - 1 <= pyterm.getCenter("PlayerMove")[1]+round(player_y) <= pyterm.getBottomRight("HomeShop")[1] + 1):
                    pyterm.renderItem("RoomInteract")
                    if keyboard.is_pressed("e"):
                        Shop = True
                        DisableOther = True

            else:
                pyterm.renderItem("HomeShopRuin")

            pyterm.renderItem("HomeResearch")
            if (pyterm.getTopLeft("HomeResearch")[0] - 1 <= pyterm.getCenter("PlayerMove")[0]+round(player_x) <= pyterm.getTopRight("HomeResearch")[0] + 1) and (pyterm.getTopLeft("HomeResearch")[1] - 1 <= pyterm.getCenter("PlayerMove")[1]+round(player_y) <= pyterm.getBottomLeft("HomeResearch")[1] + 1):
                pyterm.renderItem("RoomInteract")
                if keyboard.is_pressed("e"):
                    ResearchUps = True
                    DisableOther = True
            pyterm.renderItem("Altar")

        #Puzzle
        elif RoomData[EnteredRoom]["Type"] is "Puzzle":
            pyterm.renderItem("RoomPuzzleHints")
            pyterm.renderItem("RoomPuzzleHints2")
            for mazerend in RoomData[EnteredRoom]["Special"]["MazeRender1"]:
                itemObjects["MazeContent"]["animation frames"][0] = mazerend["Img"]
                pyterm.updateItemSize("MazeContent")
                pyterm.renderItem("MazeContent", screenLimits = (999, 999), xBias = mazerend["Location"][0] + 1, yBias = mazerend["Location"][1])
            for mazerend in RoomData[EnteredRoom]["Special"]["MazeRender2"]:
                if not ("Type" in list(mazerend.keys())):
                    itemObjects["MazeOther"]["animation frames"][0] = mazerend["Img"]
                    pyterm.renderItem("MazeOther", screenLimits = (999, 999), xBias = mazerend["Location"][0], yBias = mazerend["Location"][1])
                elif mazerend["Render"]:
                    itemObjects["MazeOther"]["animation frames"][0] = mazerend["Img"]
                    pyterm.renderItem("MazeOther", screenLimits = (999, 999), xBias = mazerend["Location"][0], yBias = mazerend["Location"][1])
            if room_push == []:
                for i in RoomData[EnteredRoom]["Special"]["MazeBlocks"]:
                    room_push.append(copy.deepcopy(i))
            if room_invis_walls == []:
                for i in RoomData[EnteredRoom]["Special"]["InvisWalls"]:
                    room_invis_walls.append(copy.deepcopy(i))
            pyterm.renderItem("Maze")
            #Pressure
            for mazerend in RoomData[EnteredRoom]["Special"]["MazeRender2"]:
                if "Type" in list(mazerend.keys()):
                    mazerend["Render"] = True
            for i in room_invis_walls:
                i[2] = True
            for i in room_push:
                if pyterm.getLetter((i["Location"][0] + round(os.get_terminal_size().columns/2), i["Location"][1] + round(os.get_terminal_size().lines/2))) == "$":
                    for i2 in room_invis_walls:
                        if i2[3] == "$":
                            i2[2] = False
                            for mazerend in RoomData[EnteredRoom]["Special"]["MazeRender2"]:
                                if "Type" in list(mazerend.keys()):
                                    if mazerend["Type"] == "$":
                                        mazerend["Render"] = False
                            break
                    else:
                        i2[2] = True
                elif pyterm.getLetter((i["Location"][0] + round(os.get_terminal_size().columns/2), i["Location"][1] + round(os.get_terminal_size().lines/2))) == "%":
                    for i2 in room_invis_walls:
                        if i2[3] == "%":
                            i2[2] = False
                            for mazerend in RoomData[EnteredRoom]["Special"]["MazeRender2"]:
                                if "Type" in list(mazerend.keys()):
                                    if mazerend["Type"] == "%":
                                        mazerend["Render"] = False
                            break
                    else:
                        i2[2] = True
                elif pyterm.getLetter((i["Location"][0] + round(os.get_terminal_size().columns/2), i["Location"][1] + round(os.get_terminal_size().lines/2))) == "&":
                    for i2 in room_invis_walls:
                        if i2[3] == "&":
                            i2[2] = False
                            for mazerend in RoomData[EnteredRoom]["Special"]["MazeRender2"]:
                                if "Type" in list(mazerend.keys()):
                                    if mazerend["Type"] == "&":
                                        mazerend["Render"] = False
                            break
                    else:
                        i2[2] = True
            if pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) in ["$", "%", "&"]:
                for i2 in room_invis_walls:
                    if i2[3] == pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])):
                        i2[2] = False
                        for mazerend in RoomData[EnteredRoom]["Special"]["MazeRender2"]:
                            if "Type" in list(mazerend.keys()):
                                if mazerend["Type"] == pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])):
                                    mazerend["Render"] = False
                        break
            #Win
            if pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) == "X":
                addedResearch = AddResearch(random.randint(round(1.3 ** (EnteredRoom[0] - 1) * 150), round(1.3 ** (EnteredRoom[0] - 1) * 250)))
                research += addedResearch
                WonPuzzle = True
                pyterm.changeCurrentItemFrame("LightRewards", 1)
                if not EnteredRoom in ClearedRooms:
                    ClearedRooms.append(EnteredRoom)
                    pyterm.changeCurrentItemFrame("LightRewards", 0)
                PhaseChange("map")
            if keyboard.is_pressed("r"):
                PhaseChange("room")



        pyterm.renderItem("PlayerMove", xBias = round(player_x), yBias = round(player_y))

        #Movement
        if not DisableOther:
            if keyboard.is_pressed("w"):
                if pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y - 1) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                    for i in room_invis_walls:
                        if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y - 1) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                            break
                    else:
                        if (round(player_x), round(player_y - 1)) in [i["Location"] for i in room_push]:
                            pushed = 0
                            moved_pushed = []
                            while True:
                                pushed += 1
                                if (round(player_x), round(player_y - pushed)) in [i["Location"] for i in room_push]:
                                    moved_pushed.append((round(player_x), round(player_y - pushed)))
                                    continue
                                elif pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y - pushed) + pyterm.getCenter("PlayerMove")[1])) in room_walls:
                                    break
                                for i in room_invis_walls:
                                    if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y - pushed) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                                        break
                                else:
                                    if round(player_y - 1) == round(player_y - 0.15):
                                        for box in room_push:
                                            if box["Location"] in moved_pushed:
                                                box["Location"] = (box["Location"][0], box["Location"][1] - 1)
                                    player_y -= 0.15
                                    break
                                break
                        else:
                            player_y -= 0.15
            if keyboard.is_pressed("s"):
                if pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y + 1) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                    for i in room_invis_walls:
                        if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y + 1) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                            break
                    else:
                        if (round(player_x), round(player_y + 1)) in [i["Location"] for i in room_push]:
                            pushed = 0
                            moved_pushed = []
                            while True:
                                pushed += 1
                                if (round(player_x), round(player_y + pushed)) in [i["Location"] for i in room_push]:
                                    moved_pushed.append((round(player_x), round(player_y + pushed)))
                                    continue
                                elif pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y + pushed) + pyterm.getCenter("PlayerMove")[1])) in room_walls:
                                    break
                                for i in room_invis_walls:
                                    if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y + pushed) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                                        break
                                else:
                                    if round(player_y + 1) == round(player_y + 0.15):
                                        for box in room_push:
                                            if box["Location"] in moved_pushed:
                                                box["Location"] = (box["Location"][0], box["Location"][1] + 1)
                                    player_y += 0.15
                                    break
                                break
                        else:
                            player_y += 0.15
            if keyboard.is_pressed("a"):
                if pyterm.getLetter((round(player_x - 1) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                    for i in room_invis_walls:
                        if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x - 1) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                            break
                    else:
                        if (round(player_x - 1), round(player_y)) in [i["Location"] for i in room_push]:
                            pushed = 0
                            moved_pushed = []
                            while True:
                                pushed += 1
                                if (round(player_x - pushed), round(player_y)) in [i["Location"] for i in room_push]:
                                    moved_pushed.append((round(player_x - pushed), round(player_y)))
                                    continue
                                elif pyterm.getLetter((round(player_x - pushed) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) in room_walls:
                                    break
                                for i in room_invis_walls:
                                    if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x - pushed) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                                        break
                                else:
                                    if round(player_x - 1) == round(player_x - 0.3):
                                        for box in room_push:
                                            if box["Location"] in moved_pushed:
                                                box["Location"] = (box["Location"][0] - 1, box["Location"][1])
                                    player_x -= 0.3
                                    break
                                break
                        else:
                            player_x -= 0.3
            if keyboard.is_pressed("d"):
                if pyterm.getLetter((round(player_x + 1) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                    for i in room_invis_walls:
                        if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x + 1) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                            break
                    else:
                        if (round(player_x + 1), round(player_y)) in [i["Location"] for i in room_push]:
                            pushed = 0
                            moved_pushed = []
                            while True:
                                pushed += 1
                                if (round(player_x + pushed), round(player_y)) in [i["Location"] for i in room_push]:
                                    moved_pushed.append((round(player_x + pushed), round(player_y)))
                                    continue
                                elif pyterm.getLetter((round(player_x + pushed) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) in room_walls:
                                    break
                                for i in room_invis_walls:
                                    if (i[0][0] + round(os.get_terminal_size().columns/2) <= round(player_x + pushed) + pyterm.getCenter("PlayerMove")[0] <= i[1][0] + round(os.get_terminal_size().columns/2)) and (i[0][1] + round(os.get_terminal_size().lines/2) <= round(player_y) + pyterm.getCenter("PlayerMove")[1] <= i[1][1] + round(os.get_terminal_size().lines/2)) and (i[2]):
                                        break
                                else:
                                    if round(player_x + 1) == round(player_x + 0.3):
                                        for box in room_push:
                                            if box["Location"] in moved_pushed:
                                                box["Location"] = (box["Location"][0] + 1, box["Location"][1])
                                    player_x += 0.3
                                    break
                                break
                        else:
                            player_x += 0.3
            if not (keyboard.is_pressed("w") or keyboard.is_pressed("a") or keyboard.is_pressed("s") or keyboard.is_pressed("d")):
                player_x = round(player_x)
                player_y = round(player_y)
        
        for push in room_push:
            pyterm.changeItemFrameContent("Pushable", push["Character"], 0)
            pyterm.renderItem("Pushable", xBias = push["Location"][0], yBias = push["Location"][1])

    elif (phase.lower() == "battle") and (Minigaming):
        Ui = False
        pyterm.renderItem("EnemyBorder")
        for button in [
            "items button",
            "information button",
            "fight button",
            "run button",
        ]:
            if (
                YiPyterminal.checkItemIsClicked(
                    button,
                    onlyCheckRelease=True,
                )
                == True
            ) and not DisableOther:
                if selectedButton == button:
                    selectedButton = None
                else:
                    selectedButton = button
                if selectedButton != "fight button":
                    isUltimateSelected=False
                    isUltimateClicked=False
                if selectedButton == "run button":
                    YiPyterminal.moveItem("ultimate button",y=100,absoluteBias=True)
                    UltimateCharge = 0
                    selectedAttack = None
                    selectedMobNum = None
                    player["CurrentHp"] = player["MaxHealth"]
                    player["CurrentMana"] = player["Mana"]
                    player["CurrentEnergy"] = player["Energy"]
                    RanAway = True
                    PhaseChange("map")
                    continue
                if selectedButton == "items button":
                    ConsumeInv = True
                    DisableOther = True
                    ConsumeInvBuffer = True
                if selectedButton == "information button":
                    playercopy = copy.deepcopy(player)
                    player["CurrentHp"] = round(min(player["CurrentHp"] + playercopy["Regen"] * (1.35 if SevenBuff == "Sloth" else 1), playercopy["MaxHealth"]))
                    player["CurrentMana"] = round(min(player["CurrentMana"] + playercopy["ManaRegen"] * (1.35 if SevenBuff == "Sloth" else 1), playercopy["Mana"]))
                    player["CurrentEnergy"] = round(min(player["CurrentEnergy"] + playercopy["EnergyRegen"] * (1.35 if SevenBuff == "Sloth" else 1), playercopy["Energy"]))
                    for effect in playercopy["Effects"]:
                        playercopy[effect["Stat"]] += effect["Potency"] * (1.2 if SevenBuff == "Gluttony" else 1)
                        if "Current" in effect["Stat"]:
                            player[effect["Stat"]] += effect["Potency"] * (1.2 if SevenBuff == "Gluttony" else 1)
                    for passive in playercopy["Passives"]:
                        playercopy[passive["Stat"]] += passive["Potency"]
                        if "Current" in passive:
                            player[passive["Stat"]] += passive["Potency"]
                    
                    for effect in player["Effects"]:
                        if effect["Time"] > 0:
                            effect["Time"] -= 1
                        if effect["Time"] == 0:
                            effect["Time"] += 1
                            if random.randint(0, 1000000) <= (200/(playercopy["Intelligence"]+200))*1000000:
                                try:
                                    if effect in player["Effects"]:
                                        player["Effects"].remove(effect)
                                except:
                                    ""
                    player["Effects"] = copy.deepcopy(playercopy["Effects"])
                    UltimateCharge+=(20 if SevenBuff == "Sloth" else 15)
                    UltimateCharge=min(UltimateCharge,100)
                    if selectedAttack == EquippedUltimate:
                        UltimateCharge=0
                        isUltimateClicked=False
                        isUltimateSelected=False
                        YiPyterminal.moveItem("ultimate button",y=100,absoluteBias=True)
                    selectedAttack = None
                    for mobNum in range(len(mobsStatus)):
                        if mobsStatus[mobNum]["Stats"]["CurrentHp"] > 0:
                            selectedMobAttack = random.choices(
                                population=[attack["AttackType"] for attack in mobsStatus[mobNum]["Attacks"]],
                                weights=[attack["Weight"] for attack in mobsStatus[mobNum]["Attacks"]],
                                k=1,
                            )[0]

                            EnemyAttack(selectedMobAttack, mobNum, True)
                    selectedButton = None
                    isInfoBarInMessageMode = True

            if YiPyterminal.checkItemIsHovered(button) == True and selectedButton == button and not DisableOther:
                YiPyterminal.changeCurrentItemFrame(button, 3)
            elif selectedButton == button:
                YiPyterminal.changeCurrentItemFrame(button, 2)
            elif YiPyterminal.checkItemIsHovered(button) == True and not DisableOther:
                YiPyterminal.changeCurrentItemFrame(button, 1)
            elif YiPyterminal.itemObjects[button]["current frame"] != 0:
                YiPyterminal.changeCurrentItemFrame(button, 0)
        currentFrameBarrier = None
        if (selectedButton != None and selectedButton != "") and (
            YiPyterminal.itemObjects["left barrier"]["current frame"] == 0
            or YiPyterminal.itemObjects["right barrier"]["current frame"] == 0
        ):
            currentFrameBarrier = 1
        elif (selectedButton == None or selectedButton == "") and (
            YiPyterminal.itemObjects["left barrier"]["current frame"] == 1
            or YiPyterminal.itemObjects["right barrier"]["current frame"] == 1
        ):
            currentFrameBarrier = 0
        if (selectedButton == "items button"):
            currentFrameBarrier = 0
        if currentFrameBarrier != None:
            for barrier in [
                "left barrier",
                "right barrier",
                "center barrier",
                "left center barrier",
                "right center barrier",
            ]:
                YiPyterminal.changeCurrentItemFrame(barrier, currentFrameBarrier)
        if not YiPyterminal.getBottomCenter("fight box")[1]+1==YiPyterminal.getTopCenter("center barrier")[1]:
            YiPyterminal.moveItem("ultimate bar",y=1)
            if YiPyterminal.getTopCenter("ultimate bar")[1]<YiPyterminal.getTopCenter("fight box")[1]:
                YiPyterminal.moveItem("ultimate bar",y=1)
            elif YiPyterminal.getTopCenter("ultimate bar")[1]>YiPyterminal.getTopCenter("fight box")[1]:
                YiPyterminal.moveItem("ultimate bar",y=-1)
            if YiPyterminal.itemObjects["fight box"]["current frame"]!=0:
                YiPyterminal.changeCurrentItemFrame("fight box",0)
        if YiPyterminal.getBottomCenter("fight box")[1]+1==YiPyterminal.getTopCenter("center barrier")[1] and EquippedUltimate!=None:
            if YiPyterminal.getBottomCenter("ultimate bar")[1]+1>YiPyterminal.getTopCenter("fight box")[1]:
                YiPyterminal.moveItem("ultimate bar",y=-1)
            if YiPyterminal.getBottomCenter("ultimate bar")[1]+1==YiPyterminal.getTopCenter("fight box")[1]:
                if UltimateCharge>=100:
                    if YiPyterminal.checkItemIsClicked("ultimate bar",onlyCheckRelease=True) and not DisableOther:
                        isUltimateSelected = not isUltimateSelected
                        if isUltimateSelected == True:
                            YiPyterminal.moveItem("ultimate button",y=0,absoluteBias=True)
                            whispersOfTheUltimate=["Make them pay.","Avenge your brothers in arms.","Unleash true power.","Only you are left.","One clean strike.","Show them your might.","Do you still remember that fateful day?","Take revenge.","Do not hold back.","Do not let the flame fade.","You must do what you have to.","Revenge at ALL costs.","Do not let them die in vain.","Do not let their sacrifice go to waste.","They didn't pay the ultimate price for nothing.","You did not come this far to give up.","Finish it.","Do not disappoint them, for they are waiting.","Do it.","Now is not the time to stand around.","End this. ONCE. AND. FOR. ALL.","Embrace the power.","Your hands are already stained.","Show them the light.","They did this to you.","It's not your fault.","Remember the fallen.","Channel your anguish.","Let your rage take over.","Remember what you are fighting for.","We are nearly there.","Can you still hear their cries?","You will reunite with them soon.","Push forth.","There will be light at the end of the tunnel.","Carry out the will of your brothers in arms.","This is what they would have wanted.","Give them what they deserve.","You need shackle your anger no more.","Let your fury strike.","They only deserve what they did to your crew.","History will talk greatly of you.",]
                            if whisperOfTheUltimate != None:
                                whispersOfTheUltimate.remove(whisperOfTheUltimate)
                            whisperOfTheUltimate = random.choice(whispersOfTheUltimate)
                        if isUltimateSelected == False:
                            YiPyterminal.moveItem("ultimate button",y=100,absoluteBias=True)
                    if isUltimateSelected == True:
                        if whisperOfTheUltimate != None:
                            YiPyterminal.changeItemFrameContent("ultimate bar",copy.deepcopy(YiPyterminal.ASSETS["ultimate bar"][0]).replace("            Whispers Of The Ultimate           ",whisperOfTheUltimate.center(47)))
                        UltimateAnimationFrame+=0.35
                    elif isUltimateSelected == False:
                        YiPyterminal.changeItemFrameContent("ultimate bar",copy.deepcopy(YiPyterminal.ASSETS["ultimate bar"][0]).replace("            Whispers Of The Ultimate           ","                U L T I M A T E                "))
                    UltimateAnimationFrame+=0.20
                    roundedUltimateAnimationFrame=round(UltimateAnimationFrame)
                    YiPyterminal.changeItemFrameContent(
                        "ultimate bar",
                        copy.deepcopy(YiPyterminal.itemObjects["ultimate bar"]["animation frames"][0])
                        .replace("                                                   ","___________________________________________________")
                        .replace(
                            "___________________________________________________",
                            YiPyterminal.replaceNthLetterInStr(
                                YiPyterminal.replaceNthLetterInStr(
                                    YiPyterminal.replaceNthLetterInStr(
                                        "___________________________________________________",
                                        "▓",
                                        (roundedUltimateAnimationFrame - 1) % 51,
                                    ),
                                    "▓",
                                    (roundedUltimateAnimationFrame + 1) % 51,
                                ),
                                "░",
                                roundedUltimateAnimationFrame % 51,
                            ),
                            1,
                        )
                        .replace(
                            "___________________________________________________",
                            YiPyterminal.replaceNthLetterInStr(
                                YiPyterminal.replaceNthLetterInStr(
                                    YiPyterminal.replaceNthLetterInStr(
                                        "___________________________________________________",
                                        "▓",
                                        roundedUltimateAnimationFrame % 51,
                                    ),
                                    "▓",
                                    (roundedUltimateAnimationFrame + 2) % 51,
                                ),
                                "░",
                                (roundedUltimateAnimationFrame + 1) % 51,
                            ),
                            1,
                        ).replace("_","█"),
                    )
                    if roundedUltimateAnimationFrame > 51:
                        UltimateAnimationFrame=1
                elif UltimateCharge<100:
                    bar = "█"*math.floor(UltimateCharge/(100/51))
                    if 0.125<=((UltimateCharge/(100/51)-math.floor(UltimateCharge/(100/51)))/(100/51))<0.375:
                        bar+="░"
                    elif 0.375<=((UltimateCharge/(100/51)-math.floor(UltimateCharge/(100/51)))/(100/51))<0.625:
                        bar+="▒"
                    elif 0.625<=((UltimateCharge/(100/51)-math.floor(UltimateCharge/(100/51)))/(100/51))<0.875:
                        bar+="▓"
                    bar += (51-len(bar))*" "
                    YiPyterminal.changeItemFrameContent(
                        "ultimate bar",
                        copy.deepcopy(YiPyterminal.ASSETS["ultimate bar"][0]).replace("                                                   ",bar).replace("            Whispers Of The Ultimate           ","                U L T I M A T E                "))
            if YiPyterminal.checkItemIsClicked("ultimate button",onlyCheckRelease=True) == True and not DisableOther:
                isUltimateClicked = not isUltimateClicked
                if isUltimateClicked == True:
                    selectedAttack = EquippedUltimate
            if YiPyterminal.checkItemIsHovered("ultimate button") == True or isUltimateClicked == True and not DisableOther:
                YiPyterminal.changeItemFrameContent("ultimate button",copy.deepcopy(YiPyterminal.ASSETS["ultimate button"][0]).replace("○","●").replace("✧                                          ✧","✦"+EquippedUltimate.center(42)+"✦"))
            else:
                YiPyterminal.changeItemFrameContent("ultimate button",copy.deepcopy(YiPyterminal.ASSETS["ultimate button"][0]))
            if isUltimateClicked == False:
                YiPyterminal.changeItemFrameContent("ultimate button",copy.deepcopy(YiPyterminal.itemObjects["ultimate button"]["animation frames"][0]).replace("║"," ").replace("╔"," ").replace("╚"," ").replace("╗"," ").replace("╝"," "))
            if YiPyterminal.itemObjects["fight box"]["current frame"]!=1:
                YiPyterminal.changeCurrentItemFrame("fight box",1)
        boxesToButtons = {
            "fight box": "fight button",
            "items box": "items button",
            "information box": "information button",
            "run box": "run button",
        }
        for box in boxesToButtons:
            if boxesToButtons[box] == selectedButton:
                if (
                    YiPyterminal.getBottomCenter(box)[1]
                    >= YiPyterminal.getTopCenter("center barrier")[1]
                ):
                    YiPyterminal.moveItem(box, y=-1)
            else:
                if YiPyterminal.itemObjects[box]["y bias"] < 0:
                    YiPyterminal.moveItem(box, y=1)
        attackOptions=[
            "attack option 1",
            "attack option 2",
            "attack option 3",
            "attack option 4",
            "attack option 5",
            "attack option 6",
            "attack option 7",
            "attack option 8",
        ]
        if YiPyterminal.getBottomCenter("fight box")[1]+1==YiPyterminal.getTopCenter("center barrier")[1] and isUltimateSelected==False:
            for optionNum in range(len(attackOptions)):
                if LockedAttacks["Attack"+str(optionNum)]==False and EquippedAttacks["Attack"+str(optionNum)]!=None and EquippedAttacks["Attack"+str(optionNum)]!="":
                    if selectedAttack== EquippedAttacks["Attack"+str(optionNum)]:
                        if YiPyterminal.checkItemIsHovered(attackOptions[optionNum]) == True and not DisableOther:
                            if YiPyterminal.itemObjects[attackOptions[optionNum]]["current frame"] != 3:
                                YiPyterminal.changeCurrentItemFrame(attackOptions[optionNum], 3)
                        else:
                            if YiPyterminal.itemObjects[attackOptions[optionNum]]["current frame"] != 2:
                                YiPyterminal.changeCurrentItemFrame(attackOptions[optionNum], 2)
                    elif YiPyterminal.checkItemIsHovered(attackOptions[optionNum]) == True and not DisableOther:
                        if YiPyterminal.itemObjects[attackOptions[optionNum]]["current frame"] != 1:
                            YiPyterminal.changeCurrentItemFrame(attackOptions[optionNum], 1)
                    else:
                        if YiPyterminal.itemObjects[attackOptions[optionNum]]["current frame"] != 0:
                            YiPyterminal.changeCurrentItemFrame(attackOptions[optionNum], 0)
                    if YiPyterminal.checkItemIsClicked(attackOptions[optionNum],onlyCheckRelease=True) == True and not DisableOther:
                        selectedAttack = EquippedAttacks["Attack"+str(optionNum)]
        hoveredMobOption = None
        for option in [
            "enemy selection option 1",
            "enemy selection option 2",
            "enemy selection option 3",
            "enemy selection option 4",
            "enemy selection option 5",
            "enemy selection option 6",
            "enemy selection option 7",
            # "enemy selection option 8",
            ]:
            if len(YiPyterminal.itemObjects[option]["animation frames"])!=1:
                if YiPyterminal.checkItemIsClicked(option,onlyCheckRelease=True) == True and not DisableOther:
                    if clickedMobOption != option:
                        clickedMobOption = option
                        selectedMobNum = int(clickedMobOption[-1])-1
                    else:
                        clickedMobOption = None
                        selectedMobNum = None
                if YiPyterminal.checkItemIsHovered(option)==True and not DisableOther:
                    hoveredMobOption = option
                if clickedMobOption == option and hoveredMobOption == option:
                    if YiPyterminal.itemObjects[option]["current frame"]!=3:
                        YiPyterminal.changeCurrentItemFrame(option, 3)
                elif clickedMobOption == option:
                    if YiPyterminal.itemObjects[option]["current frame"]!=2:
                        YiPyterminal.changeCurrentItemFrame(option, 2)
                elif hoveredMobOption == option:
                    if YiPyterminal.itemObjects[option]["current frame"]!=1:
                        YiPyterminal.changeCurrentItemFrame(option, 1)
                else:
                    if YiPyterminal.itemObjects[option]["current frame"]!=0:
                        YiPyterminal.changeCurrentItemFrame(option, 0)
        if hoveredMobOption==None and clickedMobOption==None:
            if YiPyterminal.itemObjects["enemy information box"]["current frame"]!=0:
                YiPyterminal.changeCurrentItemFrame("enemy information box",0)
        else:
            if hoveredMobOption != None:
                selectedViewMobOption = hoveredMobOption
            elif selectedViewMobOption != None:
                selectedViewMobOption=clickedMobOption
            selectedViewMobOption=int(selectedViewMobOption[-1])-1
            YiPyterminal.changeItemFrameContent(
                "enemy information box",
                YiPyterminal.ASSETS["enemy information box"][1]
                .replace(">      PLACEHOLDERNAME       <",str(mobsStatus[selectedViewMobOption]["Name"]).center(30))
                .replace("[hp]",str(round(mobsStatus[selectedViewMobOption]["Stats"]["CurrentHp"],2)))
                .replace("[max hp]",str(mobsStatus[selectedViewMobOption]["Stats"]["MaxHealth"]))
                .replace("[hp regen]",str(mobsStatus[selectedViewMobOption]["Stats"]["Regen"]))
                .replace("[def]",str(mobsStatus[selectedViewMobOption]["Stats"]["Defence"]))
                .replace("[magic def]",str(mobsStatus[selectedViewMobOption]["Stats"]["MagicDefence"]))
                .replace("[strength]",str(mobsStatus[selectedViewMobOption]["Stats"]["Strength"]))
                .replace("[magic power]",str(mobsStatus[selectedViewMobOption]["Stats"]["MagicPower"]))
                .replace("[crit chance]",str(mobsStatus[selectedViewMobOption]["Stats"]["CritChance"]))
                .replace("[crit power]",str(mobsStatus[selectedViewMobOption]["Stats"]["CritPower"]))
                .replace("[true attack]",str(mobsStatus[selectedViewMobOption]["Stats"]["TrueAttack"]))
                .replace("[true def]",str(mobsStatus[selectedViewMobOption]["Stats"]["TrueDefence"]))
                ,1)
            YiPyterminal.changeCurrentItemFrame("enemy information box",1)
        if (selectedAttack != None and selectedAttack != "" and selectedMobNum != None) and (mobsStatus != []):
            if player["CurrentMana"]>=attacks[selectedAttack]["Mana"] and player["CurrentEnergy"]>= attacks[selectedAttack]["Energy"] and mobsStatus[selectedMobNum]["Stats"]["CurrentHp"]>0:
                player["CurrentMana"]-=attacks[selectedAttack]["Mana"]
                player["CurrentEnergy"]-= attacks[selectedAttack]["Energy"]
                if not ((attacks[selectedAttack]["Minigames"][0] == None) or (selectedAttack == EquippedUltimate)):
                    PlayerBattleResults = PlayerAttack(selectedMobNum, selectedAttack, True)
                else:
                    PlayerBattleResults = PlayerAttack(selectedMobNum, selectedAttack, False)
                    battleMessages.append("You dealt " + str(PlayerBattleResults[0] + PlayerBattleResults[1] + PlayerBattleResults[2]) + " damage, and healed " + str(PlayerBattleResults[3]) + " health.")
                    isInfoBarInMessageMode = True
                FocusPlayerAttack = [selectedMobNum, selectedAttack]
                UltimateCharge+=15
                UltimateCharge=min(UltimateCharge,100)
                if selectedAttack == EquippedUltimate:
                    UltimateCharge=0
                    isUltimateClicked=False
                    isUltimateSelected=False
                    YiPyterminal.moveItem("ultimate button",y=100,absoluteBias=True)
                selectedAttack = None
                for mobNum in range(len(mobsStatus)):
                    if mobsStatus[mobNum]["Stats"]["CurrentHp"] > 0:
                        selectedMobAttack = random.choices(
                            population=[attack["AttackType"] for attack in mobsStatus[mobNum]["Attacks"]],
                            weights=[attack["Weight"] for attack in mobsStatus[mobNum]["Attacks"]],
                            k=1,
                        )[0]

                        EnemyAttack(selectedMobAttack, mobNum)
            else:
                if mobsStatus[selectedMobNum]["Stats"]["CurrentHp"] <=0:
                    battleMessages.append("The "+mobsStatus[selectedMobNum]["Name"]+"'s soul is long gone... Its in a better place now...")
                    selectedMobNum=None
                elif player["CurrentMana"]<attacks[selectedAttack]["Mana"] and player["CurrentEnergy"]<attacks[selectedAttack]["Energy"]:
                    battleMessages.append("You feel tired and your mana weak. You do not have enough energy nor mana to use "+selectedAttack+".")
                    selectedAttack=None
                elif player["CurrentMana"]<attacks[selectedAttack]["Mana"]:
                    battleMessages.append("You feel dizzy and your mana weak. You do not have enough mana to use "+selectedAttack+".")
                    selectedAttack=None
                elif player["CurrentEnergy"]<attacks[selectedAttack]["Energy"]:
                    battleMessages.append("You feel tired. You should rest. You do not have energy mana to use "+selectedAttack+".")
                    selectedAttack=None
                isInfoBarInMessageMode = True
        if mobsStatus == []:
            if (CurrentRoom != None):
                pyterm.changeCurrentItemFrame("LightRewards", 1)
            if not (CurrentRoom in ClearedRooms) and (CurrentRoom != None):
                ClearedRooms.append(copy.deepcopy(CurrentRoom))
                pyterm.changeCurrentItemFrame("LightRewards", 0)
            DisableOther = True
            battles += 1
            player["CurrentHp"] = player["MaxHealth"]
            player["CurrentMana"] = player["Mana"]
            player["CurrentEnergy"] = player["Energy"]
            pyterm.changeCurrentItemFrame("BattleRewards", 0)
            RefreshShop()
            itemObjects["ResearchRewards"]["animation frames"][0] = "+ " + str(round(TotalResearch)) + " Research"
            itemObjects["ExpRewards"]["animation frames"][0] = "+ " + str(round(TotalExp)) + " Exp"
            if (CurrentRoom != None):
                itemObjects["ItemRewards"]["animation frames"][0] = ""
                for i in TotalItems:
                    itemObjects["ItemRewards"]["animation frames"][0] += str("+ " + str(i))[:38] + "\n"
            pyterm.renderItem("BattleRewards")
            pyterm.renderItem("LightRewards")
            pyterm.renderItem("ResearchRewards")
            pyterm.renderItem("ExpRewards")
            pyterm.renderItem("ItemRewards")
            CurrentRoom = None
            if (pyterm.getBottomLeft("BattleRewards")[0] + 16 <= location[0] <= pyterm.getBottomLeft("BattleRewards")[0] + 25) and (pyterm.getBottomLeft("BattleRewards")[1] - 1 - 4 == round(location[1])) and LeftClickCopy:
                TotalResearch = 0
                TotalItems = []
                TotalExp = 0
                DisableOther = False
                PhaseChange("map")
        if player["CurrentHp"] <= 0:
            YiPyterminal.moveItem("ultimate button",y=100,absoluteBias=True)
            UltimateCharge = 0
            selectedAttack = None
            selectedMobNum = None
            player["CurrentHp"] = player["MaxHealth"]
            player["CurrentMana"] = player["Mana"]
            player["CurrentEnergy"] = player["Energy"]
            RanAway = True
            Minigaming = False
            PhaseChange("map")
            continue
        try:
            if YiPyterminal.checkItemIsClicked("info bar",onlyCheckRelease = True) and not DisableOther:
                isInfoBarInMessageMode = not isInfoBarInMessageMode
            if isInfoBarInMessageMode ==False:
                bar = str(("─"*(61-math.floor(max(player["CurrentHp"]/player["MaxHealth"],0)*61)))+"●"+(math.ceil(max(player["CurrentHp"]/player["MaxHealth"],0)*61)*"─"))[:62]
                bar2 = str((math.ceil(max(player["CurrentHp"]/player["MaxHealth"],0)*61)*"─")+"●"+("─"*(61-math.floor(max(player["CurrentHp"]/player["MaxHealth"],0)*61))))[:62]
                bar3 = str(((49-math.floor(max(player["CurrentEnergy"]/player["Energy"],0)*49))*"◇")+(math.ceil(max(player["CurrentEnergy"]/player["Energy"],0)*49)*"◆"))[:49]
                bar4 = str((math.ceil(max(player["CurrentMana"]/player["Mana"],0)*49)*"◆")+((49-math.floor(max(player["CurrentMana"]/player["Mana"],0)*49))*"◇"))[:49]
                if YiPyterminal.itemObjects["info bar"]["current frame"]!=0:
                    YiPyterminal.changeCurrentItemFrame("info bar",0)
                YiPyterminal.changeItemFrameContent("info bar",copy.deepcopy(YiPyterminal.ASSETS["info bar"][0]).replace("[bar]",bar).replace("[bar2]",bar2).replace("[hp]",str(round(player["CurrentHp"],2)).rjust(8)).replace("[maxhp]",str(round(player["MaxHealth"],2)).ljust(8)).replace("[bar3]",bar3).replace("[bar4]",bar4).replace("[energy]",str(player["CurrentEnergy"]).rjust(4)).replace("[maxenergy]",str(player["Energy"]).ljust(4)).replace("[mana]",str(player["CurrentMana"]).rjust(4)).replace("[maxmana]",str(player["Mana"]).ljust(4)))
            if isInfoBarInMessageMode == True:
                if YiPyterminal.itemObjects["info bar"]["current frame"]!=1:
                    YiPyterminal.changeCurrentItemFrame("info bar",1)
                YiPyterminal.changeItemFrameContent("info bar",copy.deepcopy(YiPyterminal.ASSETS["info bar"][1]).replace("                                                                         1                                                                         ",battleMessages[len(battleMessages)-4].center(147)).replace("                                                                        2                                                                        ",battleMessages[len(battleMessages)-3].center(145)).replace("                                                                       3                                                                       ",battleMessages[len(battleMessages)-2].center(143)).replace("                                                                      4                                                                      ",battleMessages[len(battleMessages)-1].center(141)),1)
        except:
            pass
        if selectedMobNum != "" and selectedMobNum != None:
            pyterm.changeItemFrameContent("Enemy", mobsStatus[selectedMobNum]["Asset"])
            pyterm.updateItemSize("Enemy")
            pyterm.renderItem("Enemy")

        for item in [
            "enemy selection box",
            "enemy selection option 1",
            "enemy selection option 2",
            "enemy selection option 3",
            "enemy selection option 4",
            "enemy selection option 5",
            "enemy selection option 6",
            "enemy selection option 7",
            # "enemy selection option 8",
            "ultimate bar",
            "fight box",
            "attack option 1",
            "attack option 2",
            "attack option 3",
            "attack option 4",
            "attack option 5",
            "attack option 6",
            "attack option 7",
            "attack option 8",
            # "items box",
            # "information box",
            # "run box",
            "center barrier",
            "items button",
            "information button",
            "left center barrier",
            "right center barrier",
            "fight button",
            "run button",
            "left barrier",
            "right barrier",
            "ultimate button",
            "enemy information box",
            "info bar"
        ]:
            YiPyterminal.renderItem(item, screenLimits=None)
        # YiPyterminal.addDebugMessage("Player Health: "+str(player["CurrentHp"])+"/"+str(player["MaxHealth"])+" | "+str(UltimateCharge))

    # if keyboard.is_pressed("c"):
    #     research += AddResearch(1)
    #     research *= 2
    
    # if keyboard.is_pressed("v"):
    #     Shop = True
    #     DisableOther = True

    if not Minigaming and not (phase.lower() == "map"):
        Ui = False
        pyterm.renderItem("MinigameUi")
        if attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] in ["BlackHole", "Reaction", "Shielded", "CircleDefend", "DodgeGrid", "Rain"]:
            pyterm.changeItemFrameContent("MinigameScore", "Score: " + str(30-round(AttackTest.score*10)/10))
        else:
            pyterm.changeItemFrameContent("MinigameScore", "Score: " + str(round(AttackTest.score*10)/10))
        pyterm.updateItemSize("MinigameScore")
        pyterm.renderItem("MinigameScore")
        if attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "Targets":
            pyterm.changeItemFrameContent("MinigameDesc", "Click on the targets.")
            pyterm.changeItemFrameContent("MinigameName", "Targets")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "CircleStay":
            pyterm.changeItemFrameContent("MinigameDesc", "Keep your cursor in the circle.")
            pyterm.changeItemFrameContent("MinigameName", "Circle")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "Aim":
            pyterm.changeItemFrameContent("MinigameDesc", "Time your clicks when the bar is filled.")
            pyterm.changeItemFrameContent("MinigameName", "Aim")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "Keyboard":
            pyterm.changeItemFrameContent("MinigameDesc", "Click the corresponding keyboard keys.")
            pyterm.changeItemFrameContent("MinigameName", "Keyboard")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "Spam":
            pyterm.changeItemFrameContent("MinigameDesc", "Click the button fast!")
            pyterm.changeItemFrameContent("MinigameName", "Spam")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "SimonSays":
            pyterm.changeItemFrameContent("MinigameDesc", "Click the squares in the order shown.")
            pyterm.changeItemFrameContent("MinigameName", "Simon Says")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "BlackHole":
            pyterm.changeItemFrameContent("MinigameDesc", "Keep your cursor away from the circle.")
            pyterm.changeItemFrameContent("MinigameName", "Black Hole")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "Reaction":
            pyterm.changeItemFrameContent("MinigameDesc", "Click when the screen flashes.")
            pyterm.changeItemFrameContent("MinigameName", "Reaction")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "Shielded":
            pyterm.changeItemFrameContent("MinigameDesc", "Keep your cursor behind the shield.")
            pyterm.changeItemFrameContent("MinigameName", "Shield")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "CircleDefend":
            pyterm.changeItemFrameContent("MinigameDesc", "Hover your cursor over the hashtags to stop them from reaching the central circle.")
            pyterm.changeItemFrameContent("MinigameName", "Defend the centre")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "DodgeGrid":
            pyterm.changeItemFrameContent("MinigameDesc", "Avoid the falling objects!")
            pyterm.changeItemFrameContent("MinigameName", "Rain")
        elif attacks[FocusPlayerAttack[1]]["Minigames"][0]["Name"] == "Rain":
            pyterm.changeItemFrameContent("MinigameDesc", "Run away from the objects!")
            pyterm.changeItemFrameContent("MinigameName", "Tracking")
        pyterm.updateItemSize("MinigameDesc")
        pyterm.renderItem("MinigameDesc")
        pyterm.updateItemSize("MinigameName")
        pyterm.renderItem("MinigameName")

        PlayerBattleResults = PlayerAttack(FocusPlayerAttack[0], FocusPlayerAttack[1], True)
        if PlayerBattleResults:
            selectedAttack = None
            battleMessages.append("You dealt " + str(PlayerBattleResults[0] + PlayerBattleResults[1] + PlayerBattleResults[2]) + " damage, and healed " + str(PlayerBattleResults[3]) + " health.")
            isInfoBarInMessageMode = True

    #Ui
    if Ui:
        LeftClick = LeftClickCopy
        RightClick = RightClickCopy
        if (round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 68 + UiOffset[0] <= location[0] <= round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 86 + UiOffset[0]) and (NonCenterOffset + UiOffset[1] <= location[1] <= NonCenterOffset + 5 + UiOffset[1]) and (not DisableOther):
            pyterm.changeCurrentItemFrame("Ui", 1)
            if LeftClick and (not SettingsUi):
                InventoryUi = True
                RiseUi = True
                DisableOther = True
        elif (round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 88 + UiOffset[0] <= location[0] <= round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 106 + UiOffset[0]) and (NonCenterOffset + UiOffset[1] <= location[1] <= NonCenterOffset + 5 + UiOffset[1]) and (not DisableOther):
            pyterm.changeCurrentItemFrame("Ui", 2)
            if LeftClick and (not InventoryUi):
                SettingsUi = True
                RiseUi = True
                DisableOther = True
        else:
            pyterm.changeCurrentItemFrame("Ui", 0)
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
        pyterm.renderItem("UiLevel", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 34 + UiOffset[0], yBias = NonCenterOffset + 2 + UiOffset[1], screenLimits=(999, 999))
        pyterm.renderItem("UiExp", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 34 + UiOffset[0], yBias = NonCenterOffset + 3 + UiOffset[1], screenLimits=(999, 999))
        pyterm.renderItem("UiLevelBar", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 17 + UiOffset[0], yBias = NonCenterOffset + 2 + UiOffset[1], screenLimits=(999, 999))
        pyterm.renderItem("UiExpBar", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 17 + UiOffset[0], yBias = NonCenterOffset + 3 + UiOffset[1], screenLimits=(999, 999))
        pyterm.renderItem("Light", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 57 + UiOffset[0], yBias = NonCenterOffset + 2 + UiOffset[1], screenLimits=(999, 999))
        pyterm.renderItem("Research", xBias = round((os.get_terminal_size().columns - pyterm.getStrWidthAndHeight(assets.get("UI"))[0])/2) + 57 + UiOffset[0], yBias = NonCenterOffset + 3 + UiOffset[1], screenLimits=(999, 999))

        #Inv
        if InventoryUi:
            pyterm.changeCurrentItemFrame("Inventory", InventoryUiState - 1)
            pyterm.renderItem("Inventory", screenLimits=(999,999), yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4))
            pyterm.renderLiteralItem(assets["TitleReturn"], 10, -29 + RiseMenu - round(os.get_terminal_size().lines * 3/4), "top left", "top left")

            if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 12) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 1
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 2
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 3
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 4
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 5
                InventoryState = 0
            elif (pyterm.getBottomLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 + RiseMenu - round(os.get_terminal_size().lines * 3/4) == round(location[1])) and LeftClick:
                InventoryState -= 1
                if InventoryState < 0:
                    InventoryState = math.floor(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])/23)
            elif (pyterm.getBottomRight("Inventory")[0] - 22 <= location[0] <= pyterm.getBottomRight("Inventory")[0] - 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 + RiseMenu - round(os.get_terminal_size().lines * 3/4) == round(location[1])) and LeftClick:
                InventoryState += 1
                if InventoryState > math.floor(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])/23):
                    InventoryState = 0


            # for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])):
            for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]][0 + InventoryState*23:22 + InventoryState*23])):
                itemInv = Inventory[list(Inventory.keys())[InventoryUiState - 1]][itemNo + InventoryState * 23]
                if ("Enchant" in itemInv.keys()) and (itemInv["Type"] != "Scroll"):
                    if itemInv["Enchant"]:
                        itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"]) + " (" + str(itemInv["Enchant"]) + ")"
                    else:
                        itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
                else:
                    itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
                pyterm.renderItem("ItemList", yBias = itemNo + RiseMenu - round(os.get_terminal_size().lines * 3/4), screenLimits=(999,999))
                if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 65) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 26 + itemNo == round(location[1])) and LeftClick:
                    FocusInv = itemInv
            if (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 7 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 1) and LeftClick:
                if Equipment["Extra"] != None:
                    FocusInv = Equipment["Extra"]
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 14 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 8) and LeftClick:
                if Equipment["Offhand"] != None:
                    FocusInv = Equipment["Offhand"]
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 21 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 15) and LeftClick:
                if Equipment["Weapon"] != None:
                    FocusInv = Equipment["Weapon"]
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 28 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 22) and LeftClick:
                if Equipment["Armor"] != None:
                    FocusInv = Equipment["Armor"]

            if FocusInv:
                itemObjects["ItemImg"]["animation frames"][0] = str(FocusInv["Asset"])
                FocusInvNameList = FocusInv["Name"].split()
                FocusInvName = ""
                for i in FocusInvNameList:
                    OldFocusInvName = FocusInvName
                    FocusInvName += i
                    if len(FocusInvName.splitlines()[-1]) >= 16:
                        FocusInvName = OldFocusInvName + "\n" + i
                    FocusInvName += " "
                if "Description" in list(FocusInv.keys()):
                    FocusInvDescList = FocusInv["Description"].split()
                    FocusInvDesc = ""
                    for i in FocusInvDescList:
                        OldFocusInvDesc = FocusInvDesc
                        FocusInvDesc += i
                        if len(FocusInvDesc.splitlines()[-1]) >= 16:
                            FocusInvDesc = OldFocusInvDesc + "\n" + i
                        FocusInvDesc += " "
                else:
                    FocusInvDesc = ""
                itemObjects["ItemDesc"]["animation frames"][0] = FocusInvName
                itemObjects["ItemDesc2"]["animation frames"][0] = FocusInvDesc
                pyterm.updateItemSize("ItemImg")
                pyterm.updateItemLocation("ItemImg")
                pyterm.updateItemSize("ItemDesc")
                pyterm.updateItemSize("ItemDesc2")
                pyterm.renderItem("ItemImg", screenLimits=(999,999), yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4))
                pyterm.renderItem("ItemDesc", screenLimits=(999,999), yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4))
                pyterm.renderItem("ItemDesc2", screenLimits=(999,999), yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4))
                pyterm.renderItem("ItemButton", screenLimits=(999,999), yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4))
                if (pyterm.getTopLeft("ItemButton")[0] <= location[0] <= pyterm.getTopLeft("ItemButton")[0] + 5) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                    FocusInv = False
                elif (pyterm.getBottomRight("ItemButton")[0] - 4 <= location[0] <= pyterm.getBottomRight("ItemButton")[0]) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                    if FocusInv["Type"] in ["Weapon", "Armor", "Extra", "Offhand"]:
                        NegateInvItemBuffs(Equipment[FocusInv["Type"]])
                        UseInvItem(FocusInv)
                        ApplyInvItemBuffs(FocusInv)
                    elif FocusInv["Type"] in ["Consumable", "Attack"]:
                        UseInvItem(FocusInv)
                    FocusInv = False
            
            for equipments in Equipment.values():
                if equipments != None:
                    itemObjects["Equipment"]["animation frames"][list(Equipment.values()).index(equipments)] = math.floor((18 - len(equipments["Name"]))/2) * " " + equipments["Name"] + math.ceil((18 - len(equipments["Name"]))/2) * " "
                    pyterm.changeCurrentItemFrame("Equipment", list(Equipment.values()).index(equipments))
                    pyterm.updateItemSize("Equipment")
                    pyterm.renderItem("Equipment", yBias = 7 * list(Equipment.values()).index(equipments) + RiseMenu - round(os.get_terminal_size().lines * 3/4), screenLimits=(999,999))

            if (10 <= location[0] <= 10 + pyterm.getStrWidthAndHeight(assets["TitleReturn"])[0]) and (-29 + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 30 <= location[1] <= -29 + RiseMenu - round(os.get_terminal_size().lines * 3/4) + pyterm.getStrWidthAndHeight(assets.get("TitleReturnHover"))[1]):
                pyterm.renderLiteralItem(assets["TitleReturnHover"], 10, -29 + RiseMenu - round(os.get_terminal_size().lines * 3/4), "top left", "top left")
                if LeftClick:
                    DisableOther = False
                    RiseUi = False
            if (not RiseUi) and (RiseMenu == 0):
                InventoryUi = False
                FocusInv = False
        
        if SettingsUi:
            pyterm.renderItem("Settings", screenLimits=(999,999), yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4))
            pyterm.renderLiteralItem(assets["TitleReturn"], 10, -29 + RiseMenu - round(os.get_terminal_size().lines * 3/4), "top left", "top left")

            if LeftClick and ((round(os.get_terminal_size().columns/2) - 14 - 7) <= location[0] <= (round(os.get_terminal_size().columns/2) - 14 + 7)) and ((round(os.get_terminal_size().lines/2) - 10 - 2.5) <= location[1] <= (round(os.get_terminal_size().lines/2) - 10 + .5)):
                SettingsRooms = 1
            elif LeftClick and ((round(os.get_terminal_size().columns/2) - 0 - 7) <= location[0] <= (round(os.get_terminal_size().columns/2) - 0 + 7)) and ((round(os.get_terminal_size().lines/2) - 10 - 2.5) <= location[1] <= (round(os.get_terminal_size().lines/2) - 10 + .5)):
                SettingsRooms = 2
            elif LeftClick and ((round(os.get_terminal_size().columns/2) + 14 - 7) <= location[0] <= (round(os.get_terminal_size().columns/2) + 14 + 7)) and ((round(os.get_terminal_size().lines/2) - 10 - 2.5) <= location[1] <= (round(os.get_terminal_size().lines/2) - 10 + .5)):
                SettingsRooms = 3


            if SettingsRooms == 1:
                pyterm.changeCurrentItemFrame("SettingsRoomsNormal", 1)
                pyterm.changeCurrentItemFrame("SettingsRoomsObfuscated", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsAnimated", 0)
            elif SettingsRooms == 2:
                pyterm.changeCurrentItemFrame("SettingsRoomsNormal", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsObfuscated", 1)
                pyterm.changeCurrentItemFrame("SettingsRoomsAnimated", 0)
            elif SettingsRooms == 3:
                pyterm.changeCurrentItemFrame("SettingsRoomsNormal", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsObfuscated", 0)
                pyterm.changeCurrentItemFrame("SettingsRoomsAnimated", 1)
            pyterm.renderItem("SettingsRoomsNormal", xBias=-14, yBias= -10 + RiseMenu - round(os.get_terminal_size().lines * 3/4), screenLimits=(999,999))
            pyterm.renderItem("SettingsRoomsObfuscated", xBias=0, yBias= -10 + RiseMenu - round(os.get_terminal_size().lines * 3/4), screenLimits=(999,999))
            pyterm.renderItem("SettingsRoomsAnimated", xBias=14, yBias= -10 + RiseMenu - round(os.get_terminal_size().lines * 3/4), screenLimits=(999,999))


            if (10 <= location[0] <= 10 + pyterm.getStrWidthAndHeight(assets["TitleReturn"])[0]) and (-29 + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 30 <= location[1] <= -29 + RiseMenu - round(os.get_terminal_size().lines * 3/4) + pyterm.getStrWidthAndHeight(assets.get("TitleReturnHover"))[0]):
                pyterm.renderLiteralItem(assets["TitleReturnHover"], 10, -29 + RiseMenu - round(os.get_terminal_size().lines * 3/4), "top left", "top left")
                if LeftClick:
                    DisableOther = False
                    RiseUi = False
            if (not RiseUi) and (RiseMenu == 0):
                SettingsUi = False
                FocusInv = False

        if RiseUi:
            RiseMenu = min(RiseMenu + round(os.get_terminal_size().lines / 20), round(os.get_terminal_size().lines * 3/4))
        else:
            RiseMenu = max(RiseMenu - round(os.get_terminal_size().lines / 20), 0)

    #RanAway
    if RanAway:
        LeftClick = LeftClickCopy
        DisableOther = True
        pyterm.changeCurrentItemFrame("BattleRewards", 1)
        itemObjects["ResearchRewards"]["animation frames"][0] = "+ " + str(round(TotalResearch)) + " Research"
        itemObjects["ExpRewards"]["animation frames"][0] = "+ " + str(round(TotalExp)) + " Exp"
        if (CurrentRoom != None):
            itemObjects["ItemRewards"]["animation frames"][0] = ""
            for i in TotalItems:
                itemObjects["ItemRewards"]["animation frames"][0] += str("+ " + str(i))[:38] + "\n"
        pyterm.renderItem("BattleRewards")
        pyterm.renderItem("ResearchRewards", yBias = -1)
        pyterm.renderItem("ExpRewards", yBias = -1)
        pyterm.renderItem("ItemRewards", yBias = -1)
        CurrentRoom = None
        if (pyterm.getBottomLeft("BattleRewards")[0] + 16 <= location[0] <= pyterm.getBottomLeft("BattleRewards")[0] + 25) and (pyterm.getBottomLeft("BattleRewards")[1] - 1 == round(location[1])) and LeftClick:
            TotalResearch = 0
            TotalItems = []
            TotalExp = 0
            DisableOther = False
            RanAway = False

#   WONPUZZLE
    if WonPuzzle:
        LeftClick = LeftClickCopy
        DisableOther = True
        pyterm.changeCurrentItemFrame("BattleRewards", 2)
        itemObjects["ResearchRewards"]["animation frames"][0] = "+ " + str(round(addedResearch)) + " Research"
        pyterm.renderItem("BattleRewards")
        pyterm.renderItem("LightRewards")
        pyterm.renderItem("ResearchRewards")
        EnteredRoom = None
        if (pyterm.getBottomLeft("BattleRewards")[0] + 16 <= location[0] <= pyterm.getBottomLeft("BattleRewards")[0] + 25) and (pyterm.getBottomLeft("BattleRewards")[1] - 1 == round(location[1])) and LeftClick:
            addedResearch = 0
            DisableOther = False
            WonPuzzle = False

    #ConsumeInv
    if ConsumeInv:
        LeftClick = LeftClickCopy
        InventoryCopy3 = copy.deepcopy(Inventory)
        removeItems = []
        for i in InventoryCopy3.keys():
            for i2 in InventoryCopy3[i]:
                if i2["Type"] != "Consumable":
                    removeItems.append([i2, i])
        for i in removeItems:
            InventoryCopy3[i[1]].remove(i[0])
        pyterm.changeCurrentItemFrame("Inventory", InventoryUiState - 1)
        pyterm.renderItem("Inventory", screenLimits=(999,999), yBias = 0)

        if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 12) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
            InventoryUiState = 1
            InventoryState = 0
        elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
            InventoryUiState = 2
            InventoryState = 0
        elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
            InventoryUiState = 3
            InventoryState = 0
        elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
            InventoryUiState = 4
            InventoryState = 0
        elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
            InventoryUiState = 5
            InventoryState = 0
        elif (pyterm.getBottomLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
            InventoryState -= 1
            if InventoryState < 0:
                InventoryState = math.floor(len(InventoryCopy3[list(InventoryCopy3.keys())[InventoryUiState - 1]])/23)
        elif (pyterm.getBottomRight("Inventory")[0] - 22 <= location[0] <= pyterm.getBottomRight("Inventory")[0] - 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
            InventoryState += 1
            if InventoryState > math.floor(len(InventoryCopy3[list(InventoryCopy3.keys())[InventoryUiState - 1]])/23):
                InventoryState = 0


        # for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])):
        for itemNo in range(len(InventoryCopy3[list(InventoryCopy3.keys())[InventoryUiState - 1]][0 + InventoryState*23:22 + InventoryState*23])):
            itemInv = InventoryCopy3[list(InventoryCopy3.keys())[InventoryUiState - 1]][itemNo + InventoryState * 23]
            if ("Enchant" in itemInv.keys()) and (itemInv["Type"] != "Scroll"):
                if itemInv["Enchant"]:
                    itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"]) + " (" + str(itemInv["Enchant"]) + ")"
                else:
                    itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
            else:
                itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
            pyterm.renderItem("ItemList", yBias = itemNo + 0, screenLimits=(999,999))
            if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 65) and (pyterm.getTopLeft("Inventory")[1] + 0 + 26 + itemNo == round(location[1])) and LeftClick:
                FocusInv = itemInv

        if FocusInv:
            itemObjects["ItemImg"]["animation frames"][0] = str(FocusInv["Asset"])
            FocusInvNameList = FocusInv["Name"].split()
            FocusInvName = ""
            for i in FocusInvNameList:
                OldFocusInvName = FocusInvName
                FocusInvName += i
                if len(FocusInvName.splitlines()[-1]) >= 16:
                    FocusInvName = OldFocusInvName + "\n" + i
                FocusInvName += " "
            if "Description" in list(FocusInv.keys()):
                FocusInvDescList = FocusInv["Description"].split()
                FocusInvDesc = ""
                for i in FocusInvDescList:
                    OldFocusInvDesc = FocusInvDesc
                    FocusInvDesc += i
                    if len(FocusInvDesc.splitlines()[-1]) >= 16:
                        FocusInvDesc = OldFocusInvDesc + "\n" + i
                    FocusInvDesc += " "
            else:
                FocusInvDesc = ""
            itemObjects["ItemDesc"]["animation frames"][0] = FocusInvName
            itemObjects["ItemDesc2"]["animation frames"][0] = FocusInvDesc
            pyterm.updateItemSize("ItemImg")
            pyterm.updateItemLocation("ItemImg")
            pyterm.updateItemSize("ItemDesc")
            pyterm.updateItemSize("ItemDesc2")
            pyterm.renderItem("ItemImg", screenLimits=(999,999), yBias = 0)
            pyterm.renderItem("ItemDesc", screenLimits=(999,999), yBias = 0)
            pyterm.renderItem("ItemDesc2", screenLimits=(999,999), yBias = 0)
            pyterm.renderItem("ItemButton", screenLimits=(999,999), yBias = 0)
            if (pyterm.getTopLeft("ItemButton")[0] <= location[0] <= pyterm.getTopLeft("ItemButton")[0] + 5) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                FocusInv = False
            elif (pyterm.getBottomRight("ItemButton")[0] - 4 <= location[0] <= pyterm.getBottomRight("ItemButton")[0]) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                if FocusInv["Type"] in ["Consumable"]:
                    UseInvItem(FocusInv)
                    playercopy = copy.deepcopy(player)
                    player["CurrentHp"] = min(player["CurrentHp"] + playercopy["Regen"], playercopy["MaxHealth"])
                    player["CurrentMana"] = min(player["CurrentMana"] + playercopy["ManaRegen"], playercopy["Mana"])
                    player["CurrentEnergy"] = min(player["CurrentEnergy"] + playercopy["EnergyRegen"], playercopy["Energy"])
                    for effect in playercopy["Effects"]:
                        playercopy[effect["Stat"]] += effect["Potency"] * (1.2 if SevenBuff == "Gluttony" else 1)
                        if "Current" in effect["Stat"]:
                            player[effect["Stat"]] += effect["Potency"] * (1.2 if SevenBuff == "Gluttony" else 1)
                    for passive in playercopy["Passives"]:
                        playercopy[passive["Stat"]] += passive["Potency"]
                        if "Current" in passive:
                            player[passive["Stat"]] += passive["Potency"]
                    
                    for effect in player["Effects"]:
                        if effect["Time"] > 0:
                            effect["Time"] -= 1
                        if effect["Time"] == 0:
                            effect["Time"] += 1
                            if random.randint(0, 1000000) <= (200/(playercopy["Intelligence"]+200))*1000000:
                                playercopy["Effects"].remove(effect)
                    player["Effects"] = copy.deepcopy(playercopy["Effects"])

                    DisableOther = False
                    ConsumeInv = False
                    selectedButton = None
                    battleMessages.append("You used the "+FocusInv["Name"]+".")
                    UltimateCharge+=15
                    UltimateCharge=min(UltimateCharge,100)
                    if selectedAttack == EquippedUltimate:
                        UltimateCharge=0
                        isUltimateClicked=False
                        isUltimateSelected=False
                        YiPyterminal.moveItem("ultimate button",y=100,absoluteBias=True)
                    selectedAttack = None
                    for mobNum in range(len(mobsStatus)):
                        if mobsStatus[mobNum]["Stats"]["CurrentHp"] > 0:
                            selectedMobAttack = random.choices(
                                population=[attack["AttackType"] for attack in mobsStatus[mobNum]["Attacks"]],
                                weights=[attack["Weight"] for attack in mobsStatus[mobNum]["Attacks"]],
                                k=1,
                            )[0]

                            EnemyAttack(selectedMobAttack, mobNum)
                    isInfoBarInMessageMode = True

                FocusInv = False
        for equipments in Equipment.values():
            if equipments != None:
                itemObjects["Equipment"]["animation frames"][list(Equipment.values()).index(equipments)] = math.floor((18 - len(equipments["Name"]))/2) * " " + equipments["Name"] + math.ceil((18 - len(equipments["Name"]))/2) * " "
                pyterm.changeCurrentItemFrame("Equipment", list(Equipment.values()).index(equipments))
                pyterm.updateItemSize("Equipment")
                pyterm.renderItem("Equipment", yBias = 7 * list(Equipment.values()).index(equipments) + 0, screenLimits=(999,999))

        if not ConsumeInvBuffer:
            for button in ["items button", "information button", "fight button", "run button"]:
                if (YiPyterminal.checkItemIsClicked(button, onlyCheckRelease=True,) == True):
                    if selectedButton == button:
                        selectedButton = None
                    else:
                        selectedButton = button
                    if selectedButton != "items button":
                        DisableOther = False
                        ConsumeInv = False
                        FocusInv = False
                        if selectedButton == "run button":
                            UltimateCharge = 0
                            selectedAttack = None
                            selectedMobNum = None
                            player["CurrentHp"] = player["MaxHealth"]
                            player["CurrentMana"] = player["Mana"]
                            player["CurrentEnergy"] = player["Energy"]
                            RanAway = True
                            PhaseChange("map")
        ConsumeInvBuffer = False


    #Enchants
    if Enchants:
        LeftClick = LeftClickCopy
        RightClick = RightClickCopy
        pyterm.renderItem("Enchant", screenLimits=(999,999), yBias = RiseEnchant - round(os.get_terminal_size().lines * 3/4))
        pyterm.renderLiteralItem(assets["TitleReturn"], 10, -30 + RiseEnchant - round(os.get_terminal_size().lines * 3/4), "top left", "top left")
    
        if (pyterm.getBottomLeft("Enchant")[0] + 2 <= location[0] <= pyterm.getBottomLeft("Enchant")[0] + 14) and (pyterm.getBottomLeft("Enchant")[1] - 18 <= location[1] <= pyterm.getBottomLeft("Enchant")[1] - 12) and (not FakeInv) and (not FakeInv2) and (not EnchantHelp) and LeftClick: #Scroll
            FakeInv2 = True
            OpenedFakeInv = True
        elif (pyterm.getBottomRight("Enchant")[0] - 14 <= location[0] <= pyterm.getBottomRight("Enchant")[0] - 2) and (pyterm.getBottomRight("Enchant")[1] - 18 <= location[1] <= pyterm.getBottomRight("Enchant")[1] - 12) and (not FakeInv) and (not FakeInv2) and (not EnchantHelp) and LeftClick: #EnchantedItem
            FakeInv = True
            OpenedFakeInv = True
        elif (pyterm.getBottomLeft("Enchant")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Enchant")[0] + 6) and (pyterm.getBottomLeft("Enchant")[1] - 29 is round(location[1])) and (not FakeInv) and (not FakeInv2) and (not EnchantHelp) and LeftClick:
            EnchantHelp = True
        elif (pyterm.getBottomRight("Enchant")[0] - 60 <= location[0] <= pyterm.getBottomRight("Enchant")[0] - 48) and (pyterm.getBottomRight("Enchant")[1] - 1 is round(location[1])) and (not FakeInv) and (not FakeInv2) and (not EnchantHelp) and LeftClick:
            SpellCast = [False]
        elif (pyterm.getBottomRight("Enchant")[0] - 57 <= location[0] <= pyterm.getBottomRight("Enchant")[0] - 51) and (pyterm.getBottomRight("Enchant")[1] - 29 is round(location[1])) and (not FakeInv) and (not FakeInv2) and (not EnchantHelp) and (FocusEnchant != None) and (FocusEnchant != False) and LeftClick:
            BestSpellPower = math.inf
            BestSpell = False
            for Cast in CastedSpells.keys():
                SpellPower = 0
                if len(SpellCast) != len(CastedSpells[Cast]):
                    continue
                for spell in SpellCast:
                    SpellPower += math.sqrt((CastedSpells[Cast][SpellCast.index(spell)][0] - spell["Location"][0]) ** 2 + (CastedSpells[Cast][SpellCast.index(spell)][1] - spell["Location"][1]) ** 2)
                if SpellPower < BestSpellPower:
                    BestSpellPower = SpellPower
                    BestSpell = Cast

            if (BestSpellPower <= 8 + max(len(SpellCast) - 5, 0)/1.5) and (MechanicUpgrades["PerfectEnchants"]):
                for types in Inventory.keys():
                    if FocusEnchant in Inventory[types]:
                        Inventory[types][Inventory[types].index(FocusEnchant)]["Enchant"] = BestSpell + "+"
                        break
                else:
                    Equipment[FocusEnchant["Type"]]["Enchant"] = BestSpell + "+"
                FocusEnchant = False
                SpellCast = [False]
            elif BestSpellPower <= 20 + max(len(SpellCast) - 5, 0):
                for types in Inventory.keys():
                    if FocusEnchant in Inventory[types]:
                        Inventory[types][Inventory[types].index(FocusEnchant)]["Enchant"] = BestSpell
                        break
                else:
                    Equipment[FocusEnchant["Type"]]["Enchant"] = BestSpell
                FocusEnchant = False
                SpellCast = [False]
            else:
                FocusEnchant = False
                SpellCast = [False]

        if FocusEnchant:
            FocusName = FocusEnchant["Name"][:11]
            itemObjects["EnchantItem"]["animation frames"][0] = math.floor(5.5 - len(FocusName)/2) * " " + FocusName + math.ceil(5.5 - len(FocusName)/2) * " "
            pyterm.updateItemSize("EnchantItem")
            pyterm.renderItem("EnchantItem")


    #Spells
        
        if (pyterm.getBottomRight("Enchant")[0] - 90 <= location[0] <= pyterm.getBottomRight("Enchant")[0] - 18) and (pyterm.getBottomRight("Enchant")[1] - 27 <= location[1] <= pyterm.getBottomRight("Enchant")[1] - 3) and (not FakeInv) and (not FakeInv2) and LeftClick:
            if not SpellCast[0]:
                SpellCast =[{"Type": "Star", "Location": (location[0] - pyterm.getTopLeft("Enchant")[0], location[1] - pyterm.getTopLeft("Enchant")[1])}] 
            else:
                for spell in SpellCast:
                    if location == spell["Location"]:
                        break
                else:
                    SpellCast.append({"Type": "Circle", "Location": (location[0] - pyterm.getTopLeft("Enchant")[0], location[1] - pyterm.getTopLeft("Enchant")[1])})

        if (not FakeInv) and (FocusScroll):
            FocusName = FocusScroll["Name"][:11]
            itemObjects["EnchantScroll"]["animation frames"][0] = math.floor(5.5 - len(FocusName)/2) * " " + FocusName + math.ceil(5.5 - len(FocusName)/2) * " "
            pyterm.updateItemSize("EnchantScroll")
            pyterm.renderItem("EnchantScroll")
            if (not SpellCast[0]) and (RiseEnchant is round(os.get_terminal_size().lines * 3/4)):
                RenderSpell(CastedSpells[FocusScroll["Enchant"]])

        if SpellCast[0] and (RiseEnchant is round(os.get_terminal_size().lines * 3/4)):
            for spell in SpellCast:
                if spell["Type"] != "Star":
                    itemObjects["EnchantLine"]["animation frames"][0] = pyterm.generateLine(spell["Location"], SpellCast[SpellCast.index(spell) - 1]["Location"])
                    pyterm.updateItemSize("EnchantLine")
                    pyterm.renderItem("EnchantLine", xBias = round((spell["Location"][0] + SpellCast[SpellCast.index(spell) - 1]["Location"][0])/2), yBias = round((spell["Location"][1] + SpellCast[SpellCast.index(spell) - 1]["Location"][1])/2), screenLimits=(73,25), screenLimitsBias=(0, -1))
                pyterm.renderItem("Enchant" + spell["Type"], xBias = spell["Location"][0], yBias = spell["Location"][1], screenLimits=(73,25), screenLimitsBias=(0, -1))
        
        if FakeInv:
            #Inv1start
            InventoryCopy = copy.deepcopy(Inventory)
            RemoveItems = []
            for types in InventoryCopy.keys():
                for items in InventoryCopy[types]:
                    if items["Type"] not in ["Weapon"]:
                        RemoveItems.append((items, types))
            for removed in RemoveItems:
                InventoryCopy[removed[1]].remove(removed[0])

            pyterm.changeCurrentItemFrame("Inventory", InventoryUiState - 1)
            pyterm.renderItem("Inventory", screenLimits=(999,999)) #yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4)

            if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 12) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 1
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 2
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 3
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 4
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 5
                InventoryState = 0
            elif (pyterm.getBottomLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
                InventoryState -= 1
                if InventoryState < 0:
                    InventoryState = math.floor(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]])/23)
            elif (pyterm.getBottomRight("Inventory")[0] - 22 <= location[0] <= pyterm.getBottomRight("Inventory")[0] - 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
                InventoryState += 1
                if InventoryState > math.floor(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]])/23):
                    InventoryState = 0


        # for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])):
            for itemNo in range(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]][0 + InventoryState*23:22 + InventoryState*23])):
                itemInv = InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]][itemNo + InventoryState * 23]
                if "Enchant" in itemInv.keys():
                    if itemInv["Enchant"]:
                        itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"]) + " (" + str(itemInv["Enchant"]) + ")"
                    else:
                        itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
                else:
                    itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
                pyterm.renderItem("ItemList", yBias = itemNo, screenLimits=(999,999))
                if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 65) and (pyterm.getTopLeft("Inventory")[1] + 26 + itemNo == round(location[1])) and LeftClick and (not OpenedFakeInv) and (itemInv["Type"] in ["Weapon", "Armor"]):
                    FocusEnchant = itemInv
                    FakeInv = False
            if (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 7 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 1) and LeftClick and (not OpenedFakeInv) and (itemInv["Type"] in ["Weapon", "Armor"]):
                if Equipment["Extra"] != None:
                    FocusEnchant = Equipment["Extra"]
                    FakeInv = False
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 14 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 8) and LeftClick and (not OpenedFakeInv) and (itemInv["Type"] in ["Weapon", "Armor"]):
                if Equipment["Offhand"] != None:
                    FocusEnchant = Equipment["Offhand"]
                    FakeInv = False
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 21 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 15) and LeftClick and (not OpenedFakeInv) and (itemInv["Type"] in ["Weapon", "Armor"]):
                if Equipment["Weapon"] != None:
                    FocusEnchant = Equipment["Weapon"]
                    FakeInv = False
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 28 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 22) and LeftClick and (not OpenedFakeInv) and (itemInv["Type"] in ["Weapon", "Armor"]):
                if Equipment["Armor"] != None:
                    FocusEnchant = Equipment["Armor"]
                    FakeInv = False
            
            for equipments in Equipment.values():
                if equipments != None:
                    itemObjects["Equipment"]["animation frames"][list(Equipment.values()).index(equipments)] = math.floor((18 - len(equipments["Name"]))/2) * " " + equipments["Name"] + math.ceil((18 - len(equipments["Name"]))/2) * " "
                    pyterm.changeCurrentItemFrame("Equipment", list(Equipment.values()).index(equipments))
                    pyterm.updateItemSize("Equipment")
                    pyterm.renderItem("Equipment", yBias = 7 * list(Equipment.values()).index(equipments), screenLimits=(999,999))

            OpenedFakeInv = False
            #Inv1end

        if FakeInv2:
            #Inv2start
            InventoryCopy = copy.deepcopy(Inventory)
            RemoveItems = []
            for types in InventoryCopy.keys():
                for items in InventoryCopy[types]:
                    if items["Type"] not in ["Scroll"]:
                        RemoveItems.append((items, types))
            for removed in RemoveItems:
                InventoryCopy[removed[1]].remove(removed[0])

            pyterm.changeCurrentItemFrame("Inventory", InventoryUiState - 1)
            pyterm.renderItem("Inventory", screenLimits=(999,999)) #yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4)

            if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 12) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 1
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 2
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 3
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 4
                InventoryState = 0
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 5
                InventoryState = 0
            elif (pyterm.getBottomLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
                InventoryState -= 1
                if InventoryState < 0:
                    InventoryState = math.floor(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]])/23)
            elif (pyterm.getBottomRight("Inventory")[0] - 22 <= location[0] <= pyterm.getBottomRight("Inventory")[0] - 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
                InventoryState += 1
                if InventoryState > math.floor(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]])/23):
                    InventoryState = 0


        # for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])):
            for itemNo in range(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]][0 + InventoryState*23:22 + InventoryState*23])):
                itemInv = InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]][itemNo + InventoryState * 23]
                itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
                pyterm.renderItem("ItemList", yBias = itemNo, screenLimits=(999,999))
                if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 65) and (pyterm.getTopLeft("Inventory")[1] + 26 + itemNo == round(location[1])) and LeftClick and (not OpenedFakeInv):
                    FocusScroll = itemInv
                    FakeInv2 = False
            
            for equipments in Equipment.values():
                if equipments != None:
                    itemObjects["Equipment"]["animation frames"][list(Equipment.values()).index(equipments)] = math.floor((18 - len(equipments["Name"]))/2) * " " + equipments["Name"] + math.ceil((18 - len(equipments["Name"]))/2) * " "
                    pyterm.changeCurrentItemFrame("Equipment", list(Equipment.values()).index(equipments))
                    pyterm.updateItemSize("Equipment")
                    pyterm.renderItem("Equipment", yBias = 7 * list(Equipment.values()).index(equipments), screenLimits=(999,999))
            OpenedFakeInv = False
            #Inv2end

        if EnchantHelp:
            pyterm.renderItem("EnchantHelp")
            if (pyterm.getTopLeft("EnchantHelp")[0] + 1 <= location[0] <= pyterm.getTopLeft("EnchantHelp")[0] + 4) and (pyterm.getTopLeft("EnchantHelp")[1] + 1 is round(location[1])) and LeftClick:
                EnchantHelp = False

        #End
        if (10 <= location[0] <= 10 + pyterm.getStrWidthAndHeight(assets["TitleReturn"])[0]) and (-29 - 1 + RiseEnchant - round(os.get_terminal_size().lines * 3/4) + 30 <= location[1] <= -29 - 1 + RiseEnchant - round(os.get_terminal_size().lines * 3/4) + pyterm.getStrWidthAndHeight(assets.get("TitleReturnHover"))[1]):
            pyterm.renderLiteralItem(assets["TitleReturnHover"], 10, -30 + RiseEnchant - round(os.get_terminal_size().lines * 3/4), "top left", "top left")
            if LeftClick:
                DisableOther = False
                RiseEnchantBool = False
                FakeInv = False
                FakeInv2 = False
                FocusEnchant = False
                FocusScroll = False
        if (not RiseEnchantBool) and (RiseEnchant is 0):
            Enchants = False


        if RiseEnchantBool:
            RiseEnchant = min(RiseEnchant + round(os.get_terminal_size().lines / 20), round(os.get_terminal_size().lines * 3/4))
        else:
            RiseEnchant = max(RiseEnchant - round(os.get_terminal_size().lines / 20), 0)

    #ResearchUpgrades
    if ResearchUps:
        LeftClick = LeftClickCopy
        RightClick = RightClickCopy
        if ResearchScreen["Type"] == "Research":
            pyterm.changeCurrentItemFrame("ResearchUps", 0)
        elif ResearchScreen["Type"] == "Mechanic":
            pyterm.changeCurrentItemFrame("ResearchUps", 1)
        else:
            pyterm.changeCurrentItemFrame("ResearchUps", 2)
        pyterm.renderItem("ResearchUps")

        if (pyterm.getTopRight("ResearchUps")[0] >= location[0] >= pyterm.getTopRight("ResearchUps")[0] - 8) and (pyterm.getTopRight("ResearchUps")[1] + 1 <= location[1] <= pyterm.getTopRight("ResearchUps")[1] + 3) and LeftClick:
            ResearchScreen["Type"] = "Research"
            ResearchScreen["Screen"] = 0
        elif (pyterm.getTopRight("ResearchUps")[0] >= location[0] >= pyterm.getTopRight("ResearchUps")[0] - 8) and (pyterm.getTopRight("ResearchUps")[1] + 4 <= location[1] <= pyterm.getTopRight("ResearchUps")[1] + 6) and LeftClick:
            ResearchScreen["Type"] = "Mechanic"
            ResearchScreen["Screen"] = 0
        elif (pyterm.getTopRight("ResearchUps")[0] >= location[0] >= pyterm.getTopRight("ResearchUps")[0] - 8) and (pyterm.getTopRight("ResearchUps")[1] + 7 <= location[1] <= pyterm.getTopRight("ResearchUps")[1] + 9) and LeftClick:
            ResearchScreen["Type"] = "Stat"
            ResearchScreen["Screen"] = 0
        elif (pyterm.getBottomLeft("ResearchUps")[0] + 2 <= location[0] <= pyterm.getBottomLeft("ResearchUps")[0] + 6) and (pyterm.getBottomLeft("ResearchUps")[1] - 1 == round(location[1])) and LeftClick:
            ResearchScreen["Screen"] -= 1
            if ResearchScreen["Screen"] < 0:
                ResearchScreen["Screen"] = int(len(itemObjects[ResearchScreen["Type"]+"Buttons"]["animation frames"])/6 - 1)
        elif (pyterm.getBottomLeft("ResearchUps")[0] + 35 <= location[0] <= pyterm.getBottomLeft("ResearchUps")[0] + 39) and (pyterm.getBottomLeft("ResearchUps")[1] - 1 == round(location[1])) and LeftClick:
            ResearchScreen["Screen"] += 1
            if ResearchScreen["Screen"] > len(itemObjects[ResearchScreen["Type"]+"Buttons"]["animation frames"])/6 - 1:
                ResearchScreen["Screen"] = 0
        # print(len(itemObjects[ResearchScreen["Type"]+"Buttons"]["animation frames"])/6 - 1)

        if ResearchScreen["Type"] == "Research":
            for button in range(6):
                pyterm.changeCurrentItemFrame("ResearchButtons", 6 * ResearchScreen["Screen"] + button)
                pyterm.renderItem("ResearchButtons", yBias = button * 3)
                if ResearchUpgrades[list(ResearchUpgrades.keys())[6 * ResearchScreen["Screen"] + button]] == True:
                    pyterm.renderItem("BoughtButtons", yBias = button * 3)
                if (pyterm.getTopLeft("ResearchButtons")[0] <= location[0] <= pyterm.getTopLeft("ResearchButtons")[0] + 12) and (pyterm.getTopLeft("ResearchButtons")[1] + button * 3 <= location[1] <= pyterm.getTopLeft("ResearchButtons")[1] + button * 3 + 2) and LeftClick:
                    BuyUpgrade(ResearchScreen["Type"], 6 * ResearchScreen["Screen"] + button)
        elif ResearchScreen["Type"] == "Mechanic":
            for button in range(6):
                pyterm.changeCurrentItemFrame("MechanicButtons", 6 * ResearchScreen["Screen"] + button)
                pyterm.renderItem("MechanicButtons", yBias = button * 3)
                if MechanicUpgrades[list(MechanicUpgrades.keys())[6 * ResearchScreen["Screen"] + button]] == True:
                    pyterm.renderItem("BoughtButtons", yBias = button * 3)
                if (pyterm.getTopLeft("ResearchButtons")[0] <= location[0] <= pyterm.getTopLeft("ResearchButtons")[0] + 12) and (pyterm.getTopLeft("ResearchButtons")[1] + button * 3 <= location[1] <= pyterm.getTopLeft("ResearchButtons")[1] + button * 3 + 2) and LeftClick:
                    BuyUpgrade(ResearchScreen["Type"], 6 * ResearchScreen["Screen"] + button)
        elif ResearchScreen["Type"] == "Stat":
            for button in range(6):
                pyterm.changeCurrentItemFrame("StatButtons", 6 * ResearchScreen["Screen"] + button)
                pyterm.renderItem("StatButtons", yBias = button * 3)
                if StatUpgrades[list(StatUpgrades.keys())[6 * ResearchScreen["Screen"] + button]] == True:
                    pyterm.renderItem("BoughtButtons", yBias = button * 3)
                if (pyterm.getTopLeft("ResearchButtons")[0] <= location[0] <= pyterm.getTopLeft("ResearchButtons")[0] + 12) and (pyterm.getTopLeft("ResearchButtons")[1] + button * 3 <= location[1] <= pyterm.getTopLeft("ResearchButtons")[1] + button * 3 + 2) and LeftClick:
                    BuyUpgrade(ResearchScreen["Type"], 6 * ResearchScreen["Screen"] + button)
        
        if (pyterm.getTopLeft("ResearchUps")[1] + 1 == round(location[1])) and (pyterm.getTopLeft("ResearchUps")[0] + 1 <= location[0] <= pyterm.getTopLeft("ResearchUps")[0] + 3) and LeftClick:
            ResearchUps = False
            DisableOther = False

    #Crafts
    if Crafting:
        LeftClick = LeftClickCopy
        RightClick = RightClickCopy
        pyterm.renderItem("Crafting", screenLimits=(999,999), yBias = RiseCrafting - round(os.get_terminal_size().lines * 3/4))
        if not FakeInv3:
            pyterm.renderLiteralItem(assets["TitleReturn"], 10, -30 + RiseCrafting - round(os.get_terminal_size().lines * 3/4), "top left", "top left")

        if (pyterm.getBottomLeft("Crafting")[0] + 40 <= location[0] <= pyterm.getBottomLeft("Crafting")[0] + 47) and (pyterm.getBottomLeft("Crafting")[1] - 29 is round(location[1])) and LeftClick and RiseCraftingBool and FocusCraft:
            if CraftingRecipes[FocusCraft]["Research"] <= research:
                InventoryCopy2 = copy.deepcopy(Inventory)
                EquipmentCopy2 = copy.deepcopy(Equipment)
                PlayerCopy2 = copy.deepcopy(player)
                for i in CraftingRecipes[FocusCraft]["Ingredients"]:
                    for i4 in range(i["Amount"]):
                        for i2 in InventoryCopy2.keys():
                            for i3 in InventoryCopy2[i2]:
                                if i["Item"] == i3["Name"]:
                                    InventoryCopy2[i2].remove(i3)
                                    break
                            else:
                                continue
                            break
                        else:
                            for i2 in EquipmentCopy2.keys():
                                if EquipmentCopy2[i2] != None:
                                    if i["Item"] == EquipmentCopy2[i2]["Name"]:
                                        for stat in EquipmentCopy2[i2]["Stats"].keys():
                                            PlayerCopy2["Effects"].remove({"Stat": stat, "Potency": EquipmentCopy2[i2]["Stats"][stat], "Time": -2})
                                        EquipmentCopy2[i2] = None
                                        break
                            else:
                                break
                    else:
                        continue
                    break
                else:
                    Inventory = copy.deepcopy(InventoryCopy2)
                    Equipment = copy.deepcopy(EquipmentCopy2)
                    player = copy.deepcopy(PlayerCopy2)
                    AddInvItem(Items[FocusCraft])
                    research -= CraftingRecipes[FocusCraft]["Research"]
                    FocusCraft = False
        elif (pyterm.getBottomLeft("Crafting")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Crafting")[0] + 6) and (pyterm.getBottomLeft("Crafting")[1] - 29 is round(location[1])) and LeftClick and RiseCraftingBool and not FakeInv3:
            CraftingHelp = True
        elif (pyterm.getBottomLeft("Crafting")[0] + 2 <= location[0] <= pyterm.getBottomLeft("Crafting")[0] + 6) and (pyterm.getBottomLeft("Crafting")[1] - 2 is round(location[1])) and LeftClick and RiseCraftingBool and not FakeInv3:
            CraftingCurrent -= 1
            if CraftingCurrent < 0:
                CraftingCurrent = math.floor(len(AvaliableRecipes)/8 - 0.1)
        elif (pyterm.getBottomLeft("Crafting")[0] + 81 <= location[0] <= pyterm.getBottomLeft("Crafting")[0] + 85) and (pyterm.getBottomLeft("Crafting")[1] - 2 is round(location[1])) and LeftClick and RiseCraftingBool and not FakeInv3:
            CraftingCurrent += 1
            if CraftingCurrent > math.floor(len(AvaliableRecipes)/8 - 0.1):
                CraftingCurrent = 0
        elif (pyterm.getBottomLeft("Crafting")[0] + 35 <= location[0] <= pyterm.getBottomLeft("Crafting")[0] + 52) and (pyterm.getBottomLeft("Crafting")[1] - 2 is round(location[1])) and LeftClick and RiseCraftingBool and not FakeInv3:
            FakeInv3 = True



        for recipe in AvaliableRecipes[0+CraftingCurrent*8:8+CraftingCurrent*8]:
            itemObjects["CraftRecipe"]["animation frames"][0] = recipe
            itemObjects["CraftRecipeResearch"]["animation frames"][0] = CraftingRecipes[recipe]["Researchlook"]
            pyterm.updateItemSize("CraftRecipe")
            pyterm.updateItemSize("CraftRecipeResearch")
            pyterm.renderItem("CraftRecipe", screenLimits=(999,999), yBias=AvaliableRecipes[0+CraftingCurrent*8:8+CraftingCurrent*8].index(recipe)*3 + RiseCrafting - round(os.get_terminal_size().lines * 3/4))
            pyterm.renderItem("CraftRecipeResearch", screenLimits=(999,999), yBias=AvaliableRecipes[0+CraftingCurrent*8:8+CraftingCurrent*8].index(recipe)*3 + RiseCrafting - round(os.get_terminal_size().lines * 3/4))
            if (pyterm.getTopLeft("CraftRecipe")[0] <= location[0] <= pyterm.getTopRight("CraftRecipeResearch")[0]) and (pyterm.getTopLeft("CraftRecipe")[1] + AvaliableRecipes[0+CraftingCurrent*8:8+CraftingCurrent*8].index(recipe)*3 - 1 <= round(location[1]) <= pyterm.getTopLeft("CraftRecipe")[1] + AvaliableRecipes[0+CraftingCurrent*8:8+CraftingCurrent*8].index(recipe)*3 + 1) and LeftClick and not FakeInv3:
                FocusCraft = recipe

        if FocusCraft:
            itemObjects["CraftingImg"]["animation frames"][0] = str(Items[FocusCraft]["Asset"])
            FocusInvNameList = Items[FocusCraft]["Name"].split()
            FocusInvName = ""
            for i in FocusInvNameList:
                OldFocusInvName = FocusInvName
                FocusInvName += i
                if len(FocusInvName.splitlines()[-1]) >= 16:
                    FocusInvName = OldFocusInvName + "\n" + i
                FocusInvName += " "
            FocusInvDesc = ""
            for i in CraftingRecipes[FocusCraft]["Ingredients"]:
                FocusInvDesc += (str(i["Amount"]) + " " + i["Item"])[:16] + "\n"
            itemObjects["CraftingDesc"]["animation frames"][0] = FocusInvName
            itemObjects["CraftingDesc2"]["animation frames"][0] = FocusInvDesc
            pyterm.updateItemSize("CraftingImg")
            pyterm.updateItemLocation("CraftingImg")
            pyterm.updateItemSize("CraftingDesc")
            pyterm.updateItemSize("CraftingDesc2")
            pyterm.renderItem("CraftingImg", screenLimits=(999,999))
            pyterm.renderItem("CraftingDesc", screenLimits=(999,999))
            pyterm.renderItem("CraftingDesc2", screenLimits=(999,999)) 


        if FakeInv3:
            pyterm.changeCurrentItemFrame("Inventory", InventoryUiState - 1)
            pyterm.renderItem("Inventory", screenLimits=(999,999), yBias = 0)
            pyterm.renderLiteralItem(assets["TitleReturn"], 10, -29 + 0, "top left", "top left")

            if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 12) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
                InventoryUiState = 1
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
                InventoryUiState = 2
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
                InventoryUiState = 3
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
                InventoryUiState = 4
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + 0 + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 0 + 22 + 2) and LeftClick:
                InventoryUiState = 5
            elif (pyterm.getBottomLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
                InventoryState -= 1
                if InventoryState < 0:
                    InventoryState = math.floor(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])/23)
            elif (pyterm.getBottomRight("Inventory")[0] - 22 <= location[0] <= pyterm.getBottomRight("Inventory")[0] - 26) and (pyterm.getBottomLeft("Inventory")[1] + 2 == round(location[1])) and LeftClick:
                InventoryState += 1
                if InventoryState > math.floor(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])/23):
                    InventoryState = 0


        # for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])):
            for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]][0 + InventoryState*23:22 + InventoryState*23])):
                itemInv = Inventory[list(Inventory.keys())[InventoryUiState - 1]][itemNo + InventoryState * 23]
                if ("Enchant" in itemInv.keys()) and (itemInv["Type"] != "Scroll"):
                    if itemInv["Enchant"]:
                        itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"]) + " (" + str(itemInv["Enchant"]) + ")"
                    else:
                        itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
                else:
                    itemObjects["ItemList"]["animation frames"][0] = " - " + str(itemInv["Name"])
                pyterm.renderItem("ItemList", yBias = itemNo + 0, screenLimits=(999,999))
                if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 65) and (pyterm.getTopLeft("Inventory")[1] + 0 + 26 + itemNo == round(location[1])) and LeftClick:
                    FocusInv = itemInv
            if (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 7 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 1) and LeftClick:
                if Equipment["Extra"] != None:
                    FocusInv = Equipment["Extra"]
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 14 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 8) and LeftClick:
                if Equipment["Offhand"] != None:
                    FocusInv = Equipment["Offhand"]
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 21 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 15) and LeftClick:
                if Equipment["Weapon"] != None:
                    FocusInv = Equipment["Weapon"]
            elif (pyterm.getBottomLeft("Inventory")[0] + 1 <= location[0] <= pyterm.getBottomLeft("Inventory")[0] + 20) and (pyterm.getBottomLeft("Inventory")[1] - 28 <= location[1] <= pyterm.getBottomLeft("Inventory")[1] - 22) and LeftClick:
                if Equipment["Armor"] != None:
                    FocusInv = Equipment["Armor"]

            if FocusInv:
                itemObjects["ItemImg"]["animation frames"][0] = str(FocusInv["Asset"])
                FocusInvNameList = FocusInv["Name"].split()
                FocusInvName = ""
                for i in FocusInvNameList:
                    OldFocusInvName = FocusInvName
                    FocusInvName += i
                    if len(FocusInvName.splitlines()[-1]) >= 16:
                        FocusInvName = OldFocusInvName + "\n" + i
                    FocusInvName += " "
                if "Description" in list(FocusInv.keys()):
                    FocusInvDescList = FocusInv["Description"].split()
                    FocusInvDesc = ""
                    for i in FocusInvDescList:
                        OldFocusInvDesc = FocusInvDesc
                        FocusInvDesc += i
                        if len(FocusInvDesc.splitlines()[-1]) >= 16:
                            FocusInvDesc = OldFocusInvDesc + "\n" + i
                        FocusInvDesc += " "
                else:
                    FocusInvDesc = ""
                itemObjects["ItemDesc"]["animation frames"][0] = FocusInvName
                itemObjects["ItemDesc2"]["animation frames"][0] = FocusInvDesc
                pyterm.updateItemSize("ItemImg")
                pyterm.updateItemLocation("ItemImg")
                pyterm.updateItemSize("ItemDesc")
                pyterm.updateItemSize("ItemDesc2")
                pyterm.renderItem("ItemImg", screenLimits=(999,999), yBias = 0)
                pyterm.renderItem("ItemDesc", screenLimits=(999,999), yBias = 0)
                pyterm.renderItem("ItemDesc2", screenLimits=(999,999), yBias = 0)
                pyterm.renderItem("ItemButton", screenLimits=(999,999), yBias = 0)
                if (pyterm.getTopLeft("ItemButton")[0] <= location[0] <= pyterm.getTopLeft("ItemButton")[0] + 5) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                    FocusInv = False
                elif (pyterm.getBottomRight("ItemButton")[0] - 4 <= location[0] <= pyterm.getBottomRight("ItemButton")[0]) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                    if FocusInv["Type"] in ["Weapon", "Armor", "Extra", "Offhand"]:
                        NegateInvItemBuffs(Equipment[FocusInv["Type"]])
                        UseInvItem(FocusInv)
                        ApplyInvItemBuffs(FocusInv)
                    elif FocusInv["Type"] in ["Consumable", "Attack"]:
                        UseInvItem(FocusInv)
                    FocusInv = False
            
            for equipments in Equipment.values():
                if equipments != None:
                    itemObjects["Equipment"]["animation frames"][list(Equipment.values()).index(equipments)] = math.floor((18 - len(equipments["Name"]))/2) * " " + equipments["Name"] + math.ceil((18 - len(equipments["Name"]))/2) * " "
                    pyterm.changeCurrentItemFrame("Equipment", list(Equipment.values()).index(equipments))
                    pyterm.updateItemSize("Equipment")
                    pyterm.renderItem("Equipment", yBias = 7 * list(Equipment.values()).index(equipments) + 0, screenLimits=(999,999))

            if (10 <= location[0] <= 10 + pyterm.getStrWidthAndHeight(assets["TitleReturn"])[0]) and (-29 + 0 + 30 <= location[1] <= -29 + 0 + pyterm.getStrWidthAndHeight(assets.get("TitleReturnHover"))[1]):
                pyterm.renderLiteralItem(assets["TitleReturnHover"], 10, -29 + 0, "top left", "top left")
                if LeftClick:
                    FakeInv3 = False
                    FakeInv3Buffer = True

        if CraftingHelp:
            pyterm.renderItem("CraftingHelp")
            if (pyterm.getTopLeft("CraftingHelp")[0] + 1 <= location[0] <= pyterm.getTopLeft("CraftingHelp")[0] + 4) and (pyterm.getTopLeft("CraftingHelp")[1] + 1 is round(location[1])) and LeftClick and RiseCraftingBool and not FakeInv3:
                CraftingHelp = False


        #End
        if (10 <= location[0] <= 10 + pyterm.getStrWidthAndHeight(assets["TitleReturn"])[0]) and (-29 - 1 + RiseCrafting - round(os.get_terminal_size().lines * 3/4) + 30 <= location[1] <= -29 - 1 + RiseCrafting - round(os.get_terminal_size().lines * 3/4) + pyterm.getStrWidthAndHeight(assets.get("TitleReturnHover"))[1]) and RiseCraftingBool and not FakeInv3:
            pyterm.renderLiteralItem(assets["TitleReturnHover"], 10, -30 + RiseCrafting - round(os.get_terminal_size().lines * 3/4), "top left", "top left")
            if LeftClick and not FakeInv3Buffer:
                DisableOther = False
                RiseCraftingBool = False
                FocusCraft = False
                CraftingHelp = False
                CraftingCurrent = 0
                FakeInv3 = False
            else:
                FakeInv3Buffer = False
        if (not RiseCraftingBool) and (RiseCrafting is 0):
            Crafting = False




        if RiseCraftingBool:
            RiseCrafting = min(RiseCrafting + round(os.get_terminal_size().lines / 20), round(os.get_terminal_size().lines * 3/4))
        else:
            RiseCrafting = max(RiseCrafting - round(os.get_terminal_size().lines / 20), 0)

    #Shop Time
    if Shop:
        LeftClick = LeftClickCopy
        RightClick = RightClickCopy
        pyterm.renderItem("ShopTime", screenLimits=(999,999))
        pyterm.renderLiteralItem(assets["TitleReturn"], 10, -30, "top left", "top left")

        for shopitem in range(len(ShopItems)):
            if ShopItems[shopitem]:
                itemObjects["ShopItems"]["animation frames"][0] = ShopItems[shopitem]["Item"] + " - " + str(ShopItems[shopitem]["Price"]) + " Research\n"
                itemObjects["ShopItems"]["animation frames"][0] += str(Items[ShopItems[shopitem]["Item"]]["Description"])[:68]
                pyterm.updateItemSize("ShopItems")
                pyterm.renderItem("ShopItems", yBias = 4 * shopitem)
                if (pyterm.getTopLeft("ShopTime")[0] + 68 <= location[0] <= pyterm.getTopLeft("ShopTime")[0] + 72) and (pyterm.getTopLeft("ShopTime")[1] + 9 + 4 * shopitem == round(location[1])) and LeftClick:
                    if CheckResearchUpgrade(ShopItems[shopitem]["Price"]):
                        AddInvItem(copy.deepcopy(Items[ShopItems[shopitem]["Item"]]))
                        ShopItems[shopitem] = False
            else:
                itemObjects["ShopItems"]["animation frames"][0] = "Sold Out"
                pyterm.updateItemSize("ShopItems")
                pyterm.renderItem("ShopItems", yBias = 4 * shopitem)

        itemObjects["ShopItems"]["animation frames"][0] = str(research)
        pyterm.updateItemSize("ShopItems")
        pyterm.renderItem("ShopItems", yBias = 19, xBias = 27)

        #End
        if (10 <= location[0] <= 10 + pyterm.getStrWidthAndHeight(assets["TitleReturn"])[0]) and (-29 - 1 + 30 <= location[1] <= -29 - 1 + pyterm.getStrWidthAndHeight(assets.get("TitleReturnHover"))[1]):
            pyterm.renderLiteralItem(assets["TitleReturnHover"], 10, -30, "top left", "top left")
            if LeftClick:
                DisableOther = False
                Shop = False

    #ChooseATTACK
    if ChooseAttack:
        DisableOther = True
        LeftClick = LeftClickCopy
        RightClick = RightClickCopy

        _attacks = []
        for attackNum in range(8):
            if LockedAttacks["Attack" + str(attackNum)] == True:
                _attacks.append("LOCKED".center(30))
            elif EquippedAttacks["Attack" + str(attackNum)] == None or EquippedAttacks["Attack" + str(attackNum)] == "":
                _attacks.append("".center(30))
            else:
                _attacks.append(EquippedAttacks["Attack" + str(attackNum)].center(30))
        pyterm.createItem("FightBox", [copy.deepcopy(YiPyterminal.ASSETS["fight box"][0])
                                    .replace(">        PLACEHOLDER1        <", _attacks[0])
                                    .replace(">        PLACEHOLDER2        <", _attacks[1])
                                    .replace(">        PLACEHOLDER3        <", _attacks[2])
                                    .replace(">        PLACEHOLDER4        <", _attacks[3])
                                    .replace(">        PLACEHOLDER5        <", _attacks[4])
                                    .replace(">        PLACEHOLDER6        <", _attacks[5])
                                    .replace(">        PLACEHOLDER7        <", _attacks[6])
                                    .replace(">        PLACEHOLDER8        <", _attacks[7])
                                    +"\n└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘"], "screen", "center", "center", 0)

        pyterm.renderItem("FightBox", screenLimits=None)
        if (pyterm.getTopLeft("FightBox")[0] + 1 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 30) and (pyterm.getTopLeft("FightBox")[1] + 1 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[0]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[0]] = FocusAttack
                ChooseAttack = False
        elif (pyterm.getTopLeft("FightBox")[0] + 32 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 61) and (pyterm.getTopLeft("FightBox")[1] + 1 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[1]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[1]] = FocusAttack
                ChooseAttack = False
        elif (pyterm.getTopLeft("FightBox")[0] + 63 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 92) and (pyterm.getTopLeft("FightBox")[1] + 1 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[2]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[2]] = FocusAttack
                ChooseAttack = False
        elif (pyterm.getTopLeft("FightBox")[0] + 94 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 123) and (pyterm.getTopLeft("FightBox")[1] + 1 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[3]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[3]] = FocusAttack
                ChooseAttack = False
        elif (pyterm.getTopLeft("FightBox")[0] + 1 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 30) and (pyterm.getTopLeft("FightBox")[1] + 3 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[4]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[4]] = FocusAttack
                ChooseAttack = False
        elif (pyterm.getTopLeft("FightBox")[0] + 32 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 61) and (pyterm.getTopLeft("FightBox")[1] + 3 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[5]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[5]] = FocusAttack
                ChooseAttack = False
        elif (pyterm.getTopLeft("FightBox")[0] + 63 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 92) and (pyterm.getTopLeft("FightBox")[1] + 3 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[6]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[6]] = FocusAttack
                ChooseAttack = False
        elif (pyterm.getTopLeft("FightBox")[0] + 94 <= location[0] <= pyterm.getTopLeft("FightBox")[0] + 123) and (pyterm.getTopLeft("FightBox")[1] + 3 == round(location[1])):
            if (not LockedAttacks[list(LockedAttacks.keys())[7]]) and LeftClick:
                EquippedAttacks[list(LockedAttacks.keys())[7]] = FocusAttack
                ChooseAttack = False
        

    #Levels
    if LevelUp:
        DisableOther = True
        LeftClick = LeftClickCopy
        RightClick = RightClickCopy
        pyterm.renderItem("LevelUpStats", screenLimits=(itemObjects["LevelUpTransition"]["current frame"] * 6 ,999))
        pyterm.renderItem("LevelUpText", screenLimits=(itemObjects["LevelUpTransition"]["current frame"] * 6 ,999))
        if itemObjects["LevelUpTransition"]["current frame"] <= len(itemObjects["LevelUpTransition"]["animation frames"]) - 1:
            # pyterm.renderItem("LevelUpTransition")
            itemObjects["LevelUpTransition"]["current frame"] += 1
        else:
            if (pyterm.getTopLeft("LevelUpStats")[0] <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 23) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 0)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1], screenLimits=(999,999))
                if LeftClick:
                    player["MaxHealth"] += 5
                    player["CurrentHp"] += 5
                    player["Defence"] += 12
                    player["MagicDefence"] += 12
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 24 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 47) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 1)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1], screenLimits=(999,999))
                if LeftClick:
                    player["MaxHealth"] += 5
                    player["CurrentHp"] += 5
                    player["Strength"] += 15
                    player["MagicPower"] += 15
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 48 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 71) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 2)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1], screenLimits=(999,999))
                if LeftClick:
                    player["MaxHealth"] += 5
                    player["CurrentHp"] += 5
                    player["Dexterity"] += 20
                    player["CastingSpeed"] += 20
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 72 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 95) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 3)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1], screenLimits=(999,999))
                if LeftClick:
                    player["MaxHealth"] += 5
                    player["CurrentHp"] += 5
                    player["Skill"] += 15
                    player["Intelligence"] += 15
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 96 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 119) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 4)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1], screenLimits=(999,999))
                if LeftClick:
                    player["MaxHealth"] += 5
                    player["CurrentHp"] += 5
                    player["CritChance"] += 5
                    player["CritPower"] += 12.5
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 120 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 143) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 5)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1], screenLimits=(999,999))
                if LeftClick:
                    player["MaxHealth"] += 5
                    player["CurrentHp"] += 5
                    player["Mana"] += 18
                    player["Energy"] += 18
                    player["CurrentMana"] += 18
                    player["CurrentEnergy"] += 18
                    player["ManaRegen"] += 1.5
                    player["EnergyRegen"] += 1.5
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            

    if 99 >= light >= 91:
        End()

    # pyterm.renderLiteralItem(str(location) + " " + str(LeftClick) + " " + str(RightClick) + " " + str(player["Effects"]), 0, 0, "bottom left", "bottom left")
    # pyterm.renderLiteralItem("1", 78, 21, "center", "center")
    # pyterm.renderLiteralItem("2", -78, -20, "center", "center")

    if keyboard.is_pressed("t"):
        pyterm.renderLiteralItem("#", location[0], location[1])
#34, 3
    pyterm.renderScreen(displayDebugMessages=True,debugDisplayMessageLimit=1,debugIsdisplayMessageLimit=False)
    elapsedTime = time.perf_counter() - startTime
    if elapsedTime < (1 / pyterm.FPS):
        time.sleep((1 / pyterm.FPS) - elapsedTime)
    pyterm.displayScreen()
