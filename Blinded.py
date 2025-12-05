import keyboard, random, math, time, sys, os, mouse, ctypes, copy
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


# fmt: on
def PhaseChange(Phase: str):
    global phase, riseTitle, rise, Settings, SevenSins, mapOffset, InitialHold, locationMapDiff, mapOffsetCopy, TargetLocation, FocusRoom, AnimateRoomEntry, player_x, player_y, Ui, EnteredRoom, RoomData
    phase = Phase
    if phase.lower() == "title":
        riseTitle = 0
        rise = False
        Settings = False
        SevenSins = False
        Ui = False
    elif phase.lower() == "map":
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
    elif phase.lower() == "room":
        player_x, player_y = RoomData[EnteredRoom]["SpawnLocation"]
        Ui = True
    elif phase.lower() == "puzzlemove":
        """"""
    elif phase.lower() == "puzzletext":
        pass
    elif phase.lower() == "battle":
        global mobsStatus, currentMobNum
        mobsStatus = ["Slime"]
        currentMobNum = 0
        for mobNum in range(len(mobsStatus)):
            YiPyterminal.createItem(
                mobsStatus[mobNum]["name"],
                YiPyterminal.mobInfo[mobsStatus[mobNum]["name"]]["animation frames"],
                parentAnchor="center",
                childAnchor="center",
            )
        YiPyterminal.createItem(
            "center barrier",
            YiPyterminal.assets["center barrier"],
            parentAnchor="bottom center",
            childAnchor="bottom center",
        )
        YiPyterminal.createItem(
            "items button",
            YiPyterminal.assets["items button"],
            parentObject="center barrier",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "information button",
            YiPyterminal.assets["information button"],
            parentObject="center barrier",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        YiPyterminal.createItem(
            "left center barrier",
            YiPyterminal.assets["center barrier"],
            parentObject="items button",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "right center barrier",
            YiPyterminal.assets["center barrier"],
            parentObject="information button",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        YiPyterminal.createItem(
            "fight button",
            YiPyterminal.assets["fight button"],
            parentObject="left center barrier",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "mercy button",
            YiPyterminal.assets["mercy button"],
            parentObject="right center barrier",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        YiPyterminal.createItem(
            "left barrier",
            YiPyterminal.assets["left barrier"],
            parentObject="fight button",
            parentAnchor="left center",
            childAnchor="right center",
            xBias=-1,
        )
        YiPyterminal.createItem(
            "right barrier",
            YiPyterminal.assets["right barrier"],
            parentObject="mercy button",
            parentAnchor="right center",
            childAnchor="left center",
            xBias=1,
        )
        for box in ["fight box", "items box", "information box", "mercy box"]:
            if box == "fight box":
                attacks = []
                for attackNum in range(8):
                    if EquippedAttacks["Attack" + str(attackNum)] == None:
                        attacks.append("".center(30))
                    elif LockedAttacks["Attack" + str(attackNum)] == True:
                        attacks.append("🔒".center(30))
                    else:
                        attacks.append(
                            EquippedAttacks["Attack" + str(attackNum)].center(30)
                        )
                YiPyterminal.createItem(
                    box,
                    [
                        YiPyterminal.assets[box][0]
                        .replace(">        PLACEHOLDER1        <", attacks[0])
                        .replace(">        PLACEHOLDER2        <", attacks[1])
                        .replace(">        PLACEHOLDER3        <", attacks[2])
                        .replace(">        PLACEHOLDER4        <", attacks[3])
                        .replace(">        PLACEHOLDER5        <", attacks[4])
                        .replace(">        PLACEHOLDER6        <", attacks[5])
                        .replace(">        PLACEHOLDER7        <", attacks[6])
                        .replace(">        PLACEHOLDER8        <", attacks[7])
                    ],
                    parentObject="center barrier",
                    parentAnchor="top center",
                    childAnchor="top center",
                )
                YiPyterminal.createItem(
                    "attack option 1",
                    [
                        "".center(30, "#"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom right",
                    xBias=-32,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 2",
                    [
                        "".center(30, "#"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom right",
                    xBias=-1,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 3",
                    [
                        "".center(30, "š"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom left",
                    xBias=1,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 4",
                    [
                        "".center(30, "š"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="bottom left",
                    xBias=32,
                    yBias=-1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 5",
                    [
                        "".center(30, "š"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="top right",
                    xBias=-32,
                    yBias=1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 6",
                    [
                        "".center(30, "š"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="top right",
                    xBias=-1,
                    yBias=1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 7",
                    [
                        "".center(30, "š"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
                    parentObject="fight box",
                    parentAnchor="center",
                    childAnchor="top left",
                    xBias=1,
                    yBias=1,
                    isEmptyCharacterPartOfHitbox=True,
                )
                YiPyterminal.createItem(
                    "attack option 8",
                    [
                        "".center(30, "š"),
                        "š>šššššššššššššššššššššššššš<š",
                    ],
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
                    YiPyterminal.assets[box],
                    parentObject="center barrier",
                    parentAnchor="top center",
                    childAnchor="top center",
                )


# fmt: off

#Oddly Specific Functions
def SetRoomPhase(id: tuple):
    global ClearedRooms, itemObjects, hierarchyLocations, SettingsRooms
    if (id in ClearedRooms):
        if not (assets.get("FilledBlackHole") in itemObjects[str(id)]["animation frames"]):
            itemObjects[str(id)]["animation frames"][0] = assets.get("FilledBlackHole")
            itemObjects[str(id)]["animation frames"][1] = assets.get("FilledBlackHole")
        return None
    for ids in ClearedRooms:
        for connections in hierarchyLocations[ids[0]][ids[1] - 1]["Movements"]:
            if (id == connections["id"]):
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
    global Inventory, Equipment
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
        ""#DoConsumption
        RemoveInvItem(Item)
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

def UnequipInvItem(Item):
    global Inventory, Equipment
    if Item == None:
        return True
    for types in Equipment.keys():
        if Item is Equipment[types]:
            Equipment[types] = None
            AddInvItem(Item)
            return True
    return False

def ApplyInvItemBuffs(Item):
    global player
    if Item != None:
        for stat in Item["Stats"].keys():
            player["Effects"].append({"Stat": stat, "Potency": Item["Stats"][stat], "Time": -2})
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


def PlayerAttack(Attack, Enemy):
    pass

def EnemyAttack(Attack):
    pass


timed = 9
AimTarget = []
character_size = (19, 37) #NORMAL
character_size = (9, 19) #PCS
# character_size = (12, 23) #LAPTOP
# character_size = Cursor.initialize(10)
score = 0
MainClock = 1000
FalseTime = time.time()
transparency = 1

phase = "title"
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

RoomData = {(0, 1): {"Type": "Home", "SpawnLocation": (0, 10)}}
RoomException = False

player_x, player_y = 0, 0
player_hitbox = [1, 1]
pyterm.createItem("PlayerMove", ["0"], "screen", "center", "center", 0)
room_size = [round(120), round(25)]
# pyterm.createItem("RoomSize", [pyterm.addBorder("".join("".join(" " for i2 in range(round((room_size[0] - 1)/2 + 1))) + "\n" for i3 in range(round((room_size[1] - 1)/2 + 1))), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})], "screen", "center", "center", 0)
pyterm.createItem("RoomSize", [pyterm.addBorder("".join("".join(" " for i2 in range(room_size[0])) + "\n" for i3 in range(room_size[1])), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})], "screen", "center", "center", 0)
room_walls = ["|", "-", "_", "¯", "┐", "└", "┘", "┌", "┴", "┬", "├", "┤", "┼", "#"]

UiOffset = [0, 0]
EnteredRoom = (0, 1)

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
RiseMenu = 0
RiseUi = False
InventoryUiState = 1
pyterm.createItem("Inventory", [assets.get("Inventory1"), assets.get("Inventory2"), assets.get("Inventory3"), assets.get("Inventory4"), assets.get("Inventory5")], "screen", "center", "center", yBias = -11) #-pyterm.getStrWidthAndHeight(assets.get("Inventory1"))[1]/2
DisableOther = False
Inventory = {"Armor": 
             [{"Name": "Death Star", "Type": "Weapon", "Asset": assets.get("sword"), "Stats": {"Dexterity": 1, "Strength": 1, "Accuracy": 1}, "Enchant": False, "Ultimate": {"Description": "apple"}, "Description": "A death star that's deadly and a star.", "Id": 1}], 
             "Weapon": 
             [], 
             "Offhand": 
             [{"Name": "Deather Star", "Type": "Offhand", "Asset": assets.get("sword"), "Stats": {"Dexterity": 2, "Strength": 2, "Accuracy":21}, "Enchant": False, "Ultimate": {"Description": "apple"}, "Description": "A death star that's deadly and a star.", "Id": 3}, 
              {"Name": "Deathest Star", "Type": "Weapon", "Asset": assets.get("sword"), "Stats": {"Dexterity": 999, "Strength": 999, "Accuracy": 3}, "Enchant": False, "Ultimate": {"Description": "apple"}, "Description": "A death star that's deadly and a star.", "Id": 2}], 
             "Accessory": 
             [], 
             "Misc": 
             [{"Name": "Flame", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Burning", "Description": "A flame scroll.", "Id": 4},
              {"Name": "Poison", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Poisoning", "Description": "A poison scroll.", "Id": 5},
              {"Name": "Lifesteal", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Lifesteal", "Description": "A lifesteal scroll.", "Id":6},
              {"Name": "Embued", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Embued", "Description": "An embued scroll.", "Id": 7},
              {"Name": "Swift", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Swift", "Description": "A swift scroll.", "Id": 8},
              {"Name": "Defensive", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Defensive", "Description": "A defensive scroll.", "Id": 9},
              {"Name": "Sharpened", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Sharpened", "Description": "A sharpened scroll.", "Id": 9},
              {"Name": "Dev", "Type": "Scroll", "Asset": assets.get("sword"), "Enchant": "Dev", "Description": "dev.", "Id": 10}]}
#sword = {"Name": "The Death Star", "Type": "Weapon", "Asset": assets.get(""), "Stats": {"Dexterity": 1, "Strength": 1, "Accuracy": 1}, "Ultimate": {"Description": "apple", "..."}, "Description": "A death star that's deadly and a star.", "Id": None}
#apple = {"Name": "Apple", "Type": Consumable", "Asset": "", "Effects": [{"Type": Strength, "Time": 3, "Potency": 1, "Apply": "Player"},{"Type": "Damage", "Potency": 999, "Apply": "AllEnemy"}], "Description": "Could be used to make pie", "Id": None}
Equipment = {"Armor": None, "Weapon": None, "Offhand": None, "Extra": None}
EquippedAttacks = {"Attack0": "slash", "Attack1": "heal", "Attack2": "focus", "Attack3": None, "Attack4": None, "Attack5": None,"Attack6": None,"Attack7": None,}
LockedAttacks = {"Attack0": False, "Attack1": False, "Attack2": False, "Attack3": False, "Attack4": True, "Attack5": True,"Attack6": True,"Attack7": True,}
EquippedUltimate = None
pyterm.createItem("ItemList", ["- Apple"], "Inventory", "top left", "top left", 0, 22, 26)
FocusInv = False
pyterm.createItem("ItemImg", [" "], "Inventory", "bottom right", "bottom right", 0, -2, -15)
pyterm.createItem("ItemDesc", [" "], "Inventory", "bottom right", "top left", 0, -18, -12)
pyterm.createItem("ItemButton", ["[Exit]       [Use]"], "Inventory", "bottom right", "top left", 0, -19, -2)
pyterm.createItem("Equipment", ["|!|!|!|!|!|!|!|!|!", "|!|!|!|!|!|!|!|!|!", "|!|!|!|!|!|!|!|!|!", "|!|!|!|!|!|!|!|!|!"], "Inventory", "top left", "center", 0, 11, 26)
pyterm.createItem("Settings", [assets.get("TitleSettings")], "screen", "center", "center", 0, 0, -15)

#ITS THE STATS!
light = 0
research = 0
level = 1
experience = 0
max_experience = round((math.log((math.e / 2) ** (level - 1) + math.gamma(level ** 1.35)/(level ** (level / 4)), max(10 * math.pi / level, 1 + 1/level ** 3)) + 0.798935) * 100)
#1 -> 999, 1.1 -> 10k, 10k -> 999k, 1.1mil -> ...
player = {"Health": 100, "CurrentHp": 100, "Regen": 5,
          "Defense": 0, "MagicDefense": 0, 
          "Strength": 0, "MagicPower": 0, 
          "Dexterity": 100, "CastingSpeed": 100, 
          "Skill": 0, "Intelligence": 0, 
          "CritChance": 5, "CritPower": 100, 
          "Mana": 100, "Energy": 100, 
          "ManaRegen": 10, "EnergyRegen": 10, 
          "CurrentMana": 100, "CurrentEnergy": 100, 
          "TrueAttack": 0, "TrueDefense": 0, 
          "Effects": [],
          "Passives": []} #{"Stat": "Strength", "Potency": 10, "Time": 10} or {"Stat": "Strength", "Potency": 10, "Time": -2} or {"Stat": "Health", "Potency": -2, "Time": 5, "Special": "Poison"}

attacks = {"BasicAttack": {"BasePower": 10, "Accuracy": 10, "Energy": 10, "Mana": 0, "Cooldown": 0, "Effects": [{"Stat": "Strength", "Potency": 10, "Target": "AllEnemy", "Time": 3}], "Special": None},
           "": ""}

enemies = {"Slime": {"Attacks": [{"AttackType": "BasicAttack", "Weight": 10}], "Stats": {"Health": 100, "CurrentHp": 100, "Regen": 5,
          "Defense": 0, "MagicDefense": 0, 
          "Strength": 0, "MagicPower": 0, }, "SpawnChance": 1, "Drops": [{"Item": None, "Weight": 10}], "Special": None}
}




pyterm.createItem("LevelUpStats", [assets.get("LevelUpStats")], "screen", "center", "center", 0, 0, 5)
pyterm.createItem("LevelUpTransition", ["".join(((72 - i * 3) * " " + "|" + (i * 6) * "š" + "|" + (72 - i * 3) * " " + "\n") for i2 in range(12)) for i in range(24)], "screen", "center", "center", 0, 0, 5)
pyterm.createItem("LevelUpText", [assets.get("LevelUpText")], "screen", "center", "center", 0, 0, -10)
pyterm.createItem("LevelUpHover", [assets.get("LevelUpHover" + str(i + 1)) for i in range(6)], "screen", "top left", "top left", 0, 0, 0)
LevelUp = False

# PhaseChange("battle")
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

PhaseChange("map")

YiPyterminal.initializeTerminal(1, character_size) 
YiPyterminal.startAsynchronousMouseListener()
CopyPaste = False
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
        pyterm.renderItem("EmptyBackground", createItemIfNotExists=True, createItemArgs = {"animationFrames": [assets.get("EmptyBackground")], "parentObject": "screen", "parentAnchor": "center", "childAnchor": "center"}, screenLimits = (os.get_terminal_size().columns, os.get_terminal_size().lines))

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
            if GetRoomLoc:
                hierarchyLocations.append(hierarchyLocations2)
                hierarchyLocations2 = []

        if GetRoomLoc:
            for tier in hierarchyLocations:
                for rooms in tier:
                    if rooms["id"][0] > 0:
                        RoomData[rooms["id"]] = {"Type": random.choice(["Puzzle", "Puzzle", "Puzzle", "Treasure", "Battle", "Battle", "Battle", "Battle", "Battle", "Battle"]), "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3)}
                        if rooms["id"] == (3, 1):
                            RoomData[rooms["id"]] = {"Type": "BossBattle1", "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3)}
                        elif rooms["id"] == (5, 1):
                            RoomData[rooms["id"]] = {"Type": "BossBattle2", "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3)}
                        elif rooms["id"] == (7, 1):
                            RoomData[rooms["id"]] = {"Type": "BossBattle3", "LightRequired": round((4.5 * rooms["id"][0] ** 2 - 10.5 * rooms["id"][0] + 6) * 2/3)}
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
                else:
                    itemObjects["RoomHierarchy"]["animation frames"][0] = "Hierarchy: ???"
                    itemObjects["RoomNo."]["animation frames"][0] = "Room Number: ???"
                    pyterm.changeCurrentItemFrame("RoomSidebar", 3)
                pyterm.renderItem("RoomSidebar", yBias = NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomHierarchy", xBias = -11, yBias = 6 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomNo.", xBias = -11, yBias = 7 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                pyterm.renderItem("RoomType", xBias = -11, yBias = 18 + NonCenterOffset + round((os.get_terminal_size().lines - NonCenterOffset - pyterm.getStrWidthAndHeight(assets.get("RoomSidebar"))[1])/2), screenLimits=(999, 999))
                if os.get_terminal_size().columns < 180:
                    UiOffset[0] = -10
                #pyterm.renderItem("RoomNo.", xBias = -12, yBias = 13)
        
        if AnimateRoomEntry:
            if itemObjects["RoomEntryAnimation"]["current frame"] + 1 >= 15:
                pyterm.changeCurrentItemFrame("RoomEntryAnimation", 0)
                PhaseChange("room")
                # ClearedRooms.append(AnimateRoomEntry["id"])
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
            room_size = [130, 25]
            RoomException = True
        else:
            RoomException = False
            if RoomData[EnteredRoom]["Type"] == "Puzzle":
                room_size = [120, 25]
        itemObjects["RoomSize"]["animation frames"][0] = pyterm.addBorder("".join("".join(" " for i2 in range(room_size[0])) + "\n" for i3 in range(room_size[1])), padding = {"top": 0, "bottom": 0, "left": 0, "right": 0})
        pyterm.updateItemSize("RoomSize")
        pyterm.renderItem("RoomSize", screenLimits= (999, 999))

        if RoomData[EnteredRoom]["Type"] is "Home":
            room_walls = ["|", "-", "_", "¯", "┐", "└", "┘", "┌", "┴", "┬", "├", "┤", "┼", "#", "\\", "/", "O", "◉", ">", "<", "."]
            pyterm.createItem("aA", [assets.get("EnchantHome")], "screen", "center", "center")
            pyterm.renderItem("aA")

        pyterm.renderItem("PlayerMove", xBias = round(player_x), yBias = round(player_y))

        if keyboard.is_pressed("w"):
            if pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y - 1) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                player_y -= 0.15
        if keyboard.is_pressed("s"):
            if pyterm.getLetter((round(player_x) + pyterm.getCenter("PlayerMove")[0], round(player_y + 1) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                player_y += 0.15
        if keyboard.is_pressed("a"):
            if pyterm.getLetter((round(player_x - 1) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                player_x -= 0.3
        if keyboard.is_pressed("d"):
            if pyterm.getLetter((round(player_x + 1) + pyterm.getCenter("PlayerMove")[0], round(player_y) + pyterm.getCenter("PlayerMove")[1])) not in room_walls:
                player_x += 0.3
        if not (keyboard.is_pressed("w") or keyboard.is_pressed("a") or keyboard.is_pressed("s") or keyboard.is_pressed("d")):
            player_x = round(player_x)
            player_y = round(player_y)
        


    elif phase.lower() == "battle":
        Ui = False
        YiPyterminal.renderItem(mobsStatus[currentMobNum]["name"])
        for button in [
            "items button",
            "information button",
            "fight button",
            "mercy button",
        ]:
            if (
                YiPyterminal.checkItemIsClicked(
                    button,
                    onlyCheckRelease=True,
                )
                == True
            ):
                if selectedButton == button:
                    selectedButton = None
                else:
                    selectedButton = button
            if YiPyterminal.checkItemIsHovered(button) == True and selectedButton == button:
                YiPyterminal.changeCurrentItemFrame(button, 3)
            elif selectedButton == button:
                YiPyterminal.changeCurrentItemFrame(button, 2)
            elif YiPyterminal.checkItemIsHovered(button) == True:
                YiPyterminal.changeCurrentItemFrame(button, 1)
            elif YiPyterminal.itemObjects[button]["current frame"] != 0:
                YiPyterminal.changeCurrentItemFrame(button, 0)
        currentFrameBarrier = None
        if selectedButton != None and (
            YiPyterminal.itemObjects["left barrier"]["current frame"] == 0
            or YiPyterminal.itemObjects["right barrier"]["current frame"] == 0
        ):
            currentFrameBarrier = 1
        elif selectedButton == None and (
            YiPyterminal.itemObjects["left barrier"]["current frame"] == 1
            or YiPyterminal.itemObjects["right barrier"]["current frame"] == 1
        ):
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
        boxesToButtons = {
            "fight box": "fight button",
            "items box": "items button",
            "information box": "information button",
            "mercy box": "mercy button",
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
        for option in [
            "attack option 1",
            "attack option 2",
            "attack option 3",
            "attack option 4",
            "attack option 5",
            "attack option 6",
            "attack option 7",
            "attack option 8",
        ]:
            if YiPyterminal.checkItemIsHovered(option) == True:
                if YiPyterminal.itemObjects[option]["current frame"] == 0:
                    YiPyterminal.changeCurrentItemFrame(option, 1)
            else:
                if YiPyterminal.itemObjects[option]["current frame"] == 1:
                    YiPyterminal.changeCurrentItemFrame(option, 0)
        for item in [
            "fight box",
            "attack option 1",
            "attack option 2",
            "attack option 3",
            "attack option 4",
            "attack option 5",
            "attack option 6",
            "attack option 7",
            "attack option 8",
            "items box",
            "information box",
            "mercy box",
            "center barrier",
            "items button",
            "information button",
            "left center barrier",
            "right center barrier",
            "fight button",
            "mercy button",
            "left barrier",
            "right barrier",
        ]:
            YiPyterminal.renderItem(item, screenLimits=None)

    
    if keyboard.is_pressed("v"):
        RiseEnchantBool = True
        Enchants = True
        DisableOther = True
        EnchantHelp = False

    if keyboard.is_pressed("x"):
        print(SpellCast)
        time.sleep(999)    
     
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
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 2
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 3
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 4
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + RiseMenu - round(os.get_terminal_size().lines * 3/4) + 22 + 2) and LeftClick:
                InventoryUiState = 5

            for itemNo in range(len(Inventory[list(Inventory.keys())[InventoryUiState - 1]])):
                itemInv = Inventory[list(Inventory.keys())[InventoryUiState - 1]][itemNo]
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
                itemObjects["ItemDesc"]["animation frames"][0] = str(FocusInv["Name"])
                pyterm.updateItemSize("ItemImg")
                pyterm.updateItemLocation("ItemImg")
                pyterm.renderItem("ItemImg", screenLimits=(999,999))
                pyterm.renderItem("ItemDesc", screenLimits=(999,999))
                pyterm.renderItem("ItemButton", screenLimits=(999,999))
                if (pyterm.getTopLeft("ItemButton")[0] <= location[0] <= pyterm.getTopLeft("ItemButton")[0] + 5) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                    FocusInv = False
                elif (pyterm.getBottomRight("ItemButton")[0] - 4 <= location[0] <= pyterm.getBottomRight("ItemButton")[0]) and (pyterm.getTopLeft("ItemButton")[1] is round(location[1])) and LeftClick:
                    if FocusInv["Type"] in ["Weapon", "Armor", "Extra", "Offhand"]:
                        NegateInvItemBuffs(Equipment[FocusInv["Type"]])
                        UseInvItem(FocusInv)
                        ApplyInvItemBuffs(FocusInv)
                    else:
                        ""
                    FocusInv = False
            
            for equipments in Equipment.values():
                if equipments != None:
                    itemObjects["Equipment"]["animation frames"][list(Equipment.values()).index(equipments)] = math.floor((18 - len(equipments["Name"]))/2) * " " + equipments["Name"] + math.ceil((18 - len(equipments["Name"]))/2) * " "
                    pyterm.changeCurrentItemFrame("Equipment", list(Equipment.values()).index(equipments))
                    pyterm.updateItemSize("Equipment")
                    pyterm.renderItem("Equipment", yBias = 7 * list(Equipment.values()).index(equipments), screenLimits=(999,999))

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

            if BestSpellPower <= 8 + max(len(SpellCast) - 5, 0)/1.5:
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
                    if items["Type"] not in ["Weapon", "Armor"]:
                        RemoveItems.append((items, types))
            for removed in RemoveItems:
                InventoryCopy[removed[1]].remove(removed[0])

            pyterm.changeCurrentItemFrame("Inventory", InventoryUiState - 1)
            pyterm.renderItem("Inventory", screenLimits=(999,999)) #yBias = RiseMenu - round(os.get_terminal_size().lines * 3/4)

            if (pyterm.getTopLeft("Inventory")[0] + 22 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 12) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 1
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 2
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 3
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 4
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 5

            for itemNo in range(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]])):
                itemInv = InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]][itemNo]
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
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 13 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 24) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 2
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 25 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 36) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 3
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 37 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 48) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 4
            elif (pyterm.getTopLeft("Inventory")[0] + 22 + 49 <= location[0] <= pyterm.getTopLeft("Inventory")[0] + 22 + 60) and (pyterm.getTopLeft("Inventory")[1] + 22 <= location[1] <= pyterm.getTopLeft("Inventory")[1] + 22 + 2) and LeftClick and (not OpenedFakeInv):
                InventoryUiState = 5

            for itemNo in range(len(InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]])):
                itemInv = InventoryCopy[list(InventoryCopy.keys())[InventoryUiState - 1]][itemNo]
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

    #Levels
    if LevelUp:
        DisableOther = True
        pyterm.renderItem("LevelUpStats", screenLimits=(itemObjects["LevelUpTransition"]["current frame"] * 6 ,999))
        pyterm.renderItem("LevelUpText", screenLimits=(itemObjects["LevelUpTransition"]["current frame"] * 6 ,999))
        if itemObjects["LevelUpTransition"]["current frame"] <= len(itemObjects["LevelUpTransition"]["animation frames"]) - 1:
            # pyterm.renderItem("LevelUpTransition")
            itemObjects["LevelUpTransition"]["current frame"] += 1
        else:
            if (pyterm.getTopLeft("LevelUpStats")[0] <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 23) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 0)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1])
                if LeftClick:
                    player["Health"] += 5
                    player["CurrentHealth"] = player["Health"]
                    player["Defense"] += 10
                    player["MagicDefense"] += 10
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 24 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 47) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 1)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1])
                if LeftClick:
                    player["Health"] += 5
                    player["CurrentHealth"] = player["Health"]
                    player["Strength"] += 15
                    player["MagicPower"] += 15
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 48 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 71) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 2)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1])
                if LeftClick:
                    player["Health"] += 5
                    player["CurrentHealth"] = player["Health"]
                    player["Dexterity"] += 20
                    player["CastingSpeed"] += 20
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 72 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 95) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 3)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1])
                if LeftClick:
                    player["Health"] += 5
                    player["CurrentHealth"] = player["Health"]
                    player["Skill"] += 15
                    player["Intelligence"] += 15
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 96 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 119) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 4)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1])
                if LeftClick:
                    player["Health"] += 5
                    player["CurrentHealth"] = player["Health"]
                    player["CritChance"] += 5
                    player["CritPower"] += 12.5
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            elif (pyterm.getTopLeft("LevelUpStats")[0] + 120 <= location[0] <= pyterm.getTopLeft("LevelUpStats")[0] + 143) and (pyterm.getTopLeft("LevelUpStats")[1] <= location[1] <= pyterm.getTopLeft("LevelUpStats")[1] + 11):
                pyterm.changeCurrentItemFrame("LevelUpHover", 5)
                pyterm.renderItem("LevelUpHover", xBias = location[0], yBias = location[1])
                if LeftClick:
                    player["Health"] += 5
                    player["CurrentHealth"] = player["Health"]
                    player["Mana"] += 18
                    player["Energy"] += 18
                    player["CurrentMana"] = player["Mana"]
                    player["CurrentEnergy"] = player["Energy"]
                    player["ManaRegen"] += 1.5
                    player["EnergyRegen"] += 1.5
                    DisableOther = False
                    LevelUp = False
                    itemObjects["LevelUpTransition"]["current frame"] = 0
            
    
    if keyboard.is_pressed('t'):
        experience += 1000

    pyterm.renderLiteralItem(str(location) + " " + str(LeftClick) + " " + str(RightClick) + " " + str(player["Effects"]), 0, 0, "bottom left", "bottom left")
    pyterm.renderLiteralItem("1", 78, 21, "center", "center")
    pyterm.renderLiteralItem("2", -78, -20, "center", "center")
#34, 3
    pyterm.renderScreen()
    elapsedTime = time.perf_counter() - startTime
    if elapsedTime < (1 / pyterm.FPS):
        time.sleep((1 / pyterm.FPS) - elapsedTime)
    pyterm.displayScreen()
