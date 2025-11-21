import keyboard, random, threading, math, time, sys, os, pygetwindow, mouse
from YiPyterminal import Pyterminal, assets, pyterm
import Cursor, mousedetect

MainClock = 1000
FalseTime = time.time()

#6 Games
def AddAttackAim(Range: tuple, Duration: int, Clickable = True):
    global MainClock
    RandomizerX = random.randint(-Range[0], Range[0])
    RandomizerY = random.randint(-Range[1], Range[1])
    AimTarget.append({"Phase": "Target1", "MaxDuration": Duration, "CurrentDuration": Duration, "X": RandomizerX, "Y": RandomizerY, "Coords": (0, 0), "Clickable": Clickable, "Id": MainClock})
    Coords = pyterm.addItem("Target1", RandomizerX, RandomizerY, "center", "center")
    CreateButton((Coords[0] + 2 ,Coords[1] + 1), (Coords[0] - 2 ,Coords[1] - 1), MainClock)
    MainClock += 1

def AttackAim():
    score = 0
    for i in AimTarget:
        i["Coords"] = pyterm.addItem(assets[i["Phase"]], i["X"], i["Y"], "center", "center")
        i["CurrentDuration"] -= 1
        if (CheckButton(i["Id"], False) and (i["Clickable"] == False)) or (CheckButton(i["Id"]) and i["Clickable"]):
            AimTarget.remove(i)
            RemoveButton(i["Id"])
            score += (5 - int(i["Phase"].replace("Target", ""))) / 1.5
            break
        if i["CurrentDuration"] == 0:
            i["Phase"] = i["Phase"].replace("Target", "")
            i["Phase"] = "Target" + str(int(i["Phase"]) + 1)
            i["CurrentDuration"] = i["MaxDuration"]
            if i["Phase"] == "Target5":
                AimTarget.remove(i)
                RemoveButton(i["Id"])
    return score

def CreateButton(point1: tuple, point2: tuple, id):
    buttons.append({"Point1": point1, "Point2": point2, "Id": id})

def CheckButton(ButtonId, Click = True) -> bool:
    global clickbuffer
    for i in buttons:
        if (i["Id"] == ButtonId):
            if ((i["Point1"][0] >= location[0] >= i["Point2"][0]) or (i["Point1"][0] <= location[0] <= i["Point2"][0])) and ((i["Point1"][1] >= location[1] >= i["Point2"][1]) or (i["Point1"][1] <= location[1] <= i["Point2"][1])):
                if Click:
                    if (mousedetect.ClickDetect()) and (clickbuffer == False): 
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        
def RemoveButton(ButtonId):
    for i in buttons:
        if i["Id"] == ButtonId:
            buttons.remove(i)
            break

def CircleStay(Range: tuple, Duration: int, Speed: float, Unpredictability: int):
    global score, location
    if circleStay["Time"] == 0:
        circleStay["Time"] = Duration
        circleStay["location"] = (random.randint(-Range[0], Range[0]), random.randint(-Range[1], Range[1]))
        circleStay["rotation"] = random.randint(0, 359)
    if (random.randint(1, Unpredictability) == 1):
        circleStay["rotation"] = random.randint(0, 359)
    if not ((Range[0] >= circleStay["location"][0] >= -Range[0]) and (Range[1] >= circleStay["location"][1] >= -Range[1])):
        circleStay["location"] = (circleStay["location"][0] / 1.025, circleStay["location"][1] / 1.025)
        circleStay["rotation"] = random.randint(0, 359)
    circleStay["location"] = (circleStay["location"][0] + math.cos(math.radians(circleStay["rotation"])) * Speed, circleStay["location"][1] + math.sin(math.radians(circleStay["rotation"])) * Speed)
    circleStay["absoluteloc"] = pyterm.addItem(assets["CircleStay"], round(circleStay["location"][0]), round(circleStay["location"][1]), "center", "center")
    
    if ((circleStay["absoluteloc"][0] + 3.5) >= location[0] >= (circleStay["absoluteloc"][0] - 3.5)) and ((circleStay["absoluteloc"][1] + 3.5) >= location[1] >= (circleStay["absoluteloc"][1] - 3.5)):
        score += 0.0925

    circleStay["Time"] -= 1
    if circleStay["Time"] <= 0:
        return False
    return True

def AimMinigame(Speedrange: tuple, Repeats = 1):
    global score, clickbuffer
    if aimMinigame["Repeats"] == 0:
        aimMinigame["Speed"] = random.randint(Speedrange[0], Speedrange[1])
        aimMinigame["Repeats"] = Repeats
        aimMinigame["CurrentFrame"] = 0
        aimMinigame["CurrentWait"] = 0
        return False
    elif (aimMinigame["CurrentFrame"] >= 11) and (aimMinigame["CurrentWait"] >= aimMinigame["Speed"]):
        aimMinigame["Repeats"] -= 1
        aimMinigame["CurrentFrame"] = 0
        aimMinigame["CurrentWait"] = 0
        aimMinigame["Speed"] = random.randint(Speedrange[0], Speedrange[1])
    if aimMinigame["Repeats"] == 0:
        return True
    if aimMinigame["CurrentWait"] >= aimMinigame["Speed"]:
        aimMinigame["CurrentFrame"] += 1
        aimMinigame["CurrentWait"] = 0
    aimMinigame["CurrentWait"] += 1
    pyterm.addItem(assets["AimMinigame"].splitlines()[aimMinigame["CurrentFrame"] - 1], 0, 7, "center", "center")

    if (mousedetect.ClickDetect("Left", "On") or mousedetect.GeneralDetect(32, "On")) and (clickbuffer == False):
        score += aimMinigame["CurrentFrame"] / 6
        aimMinigame["Repeats"] -= 1
        aimMinigame["CurrentFrame"] = 0
        aimMinigame["CurrentWait"] = 0
        aimMinigame["Speed"] = random.randint(Speedrange[0], Speedrange[1])    
        if aimMinigame["Repeats"] == 0:
            return True
    return False

def KeyboardMinigame(Inputs: list, Speed: int, Time: int):
    global score
    if keyboardMinigame["TotalTime"] <= 0:
        keyboardMinigame["Speed"] = Speed
        keyboardMinigame["TotalTime"] = Time
        keyboardMinigame["Next"] = 0
        keyboardMinigame["CurrentKey"] = random.choice(Inputs)
    Inputs.remove(keyboardMinigame["CurrentKey"])
    for i in Inputs:
        if mousedetect.KeyboardDetect(i, "On"):
            Inputs.remove(i)
            keyboardMinigame["Next"] = 0
            keyboardMinigame["CurrentKey"] = random.choice(Inputs)
            score -= 0.5
            score = max(score, 0)
    if mousedetect.KeyboardDetect(keyboardMinigame["CurrentKey"], "On"):
        keyboardMinigame["Next"] = 0
        keyboardMinigame["CurrentKey"] = random.choice(Inputs)
        score += 0.75
    elif keyboardMinigame["Next"] >= keyboardMinigame["Speed"]:
        keyboardMinigame["Next"] = 0
        keyboardMinigame["CurrentKey"] = random.choice(Inputs)
        score -= 0.5
        score = max(score, 0)
    keyboardMinigame["TotalTime"] -= 1
    keyboardMinigame["Next"] += 1
    pyterm.addItem("Press " + str(keyboardMinigame["CurrentKey"]), 0, 7, "center", "center")
    if keyboardMinigame["TotalTime"] <= 0:
        return True
    return False

def Spam(Time: int, Type = 32, Message = "Spam Spacebar!"):
    global score
    if spamMinigame["Time"] <= 0:
        spamMinigame["Time"] = Time
        spamMinigame["Key"] = Type
    if mousedetect.GeneralDetect(spamMinigame["Key"], "On"):
        score += 0.125
    spamMinigame["Time"] -= 1
    pyterm.addItem(Message, 0, 7, "center", "center")
    if spamMinigame["Time"] <= 0:
        return True
    return False
    
def SimonSays(Amount: int, InitialSpeed: int, Time: int):
    global score, location, Previous
    if simonSays["Time"] == 0:
        simonSays["Order"] = []
        for i in range(Amount):
            simonSays["Order"].append(random.choice(["BL", "TL", "BR", "TR"]))
        simonSays["Phase"] = "Initial"
        simonSays["Time"] = Time
        simonSays["InitialSpeed"] = InitialSpeed
        simonSays["PhaseInitialTime"] = 0
        simonSays["PhaseInitialFrame"] = 0
        simonSays["PlayerFrame"] = 0
        Previous = 0
    
    if simonSays["Phase"] == "Initial":
        if simonSays["PhaseInitialTime"] < (simonSays["InitialSpeed"] - 2):
            pyterm.addItem(assets["Grid" + str(simonSays["Order"][simonSays["PhaseInitialFrame"]])], 0, 0, "center", "center")
        else:
            pyterm.addItem(assets["Grid"], 0, 0, "center", "center")
        simonSays["PhaseInitialTime"] += 1
        if simonSays["PhaseInitialTime"] >= simonSays["InitialSpeed"]:
            pyterm.addItem(assets["Grid"], 0, 0, "center", "center")
            simonSays["PhaseInitialTime"] = 0
            simonSays["PhaseInitialFrame"] += 1
        if simonSays["PhaseInitialFrame"] == len(simonSays["Order"]):
            simonSays["Phase"] = "Gameplay"
    
    elif simonSays["Phase"] == "Gameplay":
        GridCenter = pyterm.addItem(assets["Grid"], 0, 0, "center", "center")
        pyterm.addItem(str(simonSays["Order"][simonSays["PlayerFrame"]]), 0, 0, "bottom left", "bottom left")
        if (GridCenter[0] - 20 <= location[0] <= GridCenter[0] - 1) and (GridCenter[1] - 7 <= location[1] <= GridCenter[1] - 1) and (mousedetect.ClickDetect("Left", "On")): #y7, x9
            if (simonSays["Order"][simonSays["PlayerFrame"]] == "TL"):
                simonSays["PlayerFrame"] += 1
                pyterm.addItem(assets["GridTL"], 0, 0, "center", "center")
                score += 1
            else:
                score = max(score - 1, 0)
        elif (GridCenter[0] - 20 <= location[0] <= GridCenter[0] - 1) and (GridCenter[1] + 7 >= location[1] >= GridCenter[1] + 1) and (mousedetect.ClickDetect("Left", "On")): #y7, x9
            if (simonSays["Order"][simonSays["PlayerFrame"]] == "BL"):
                simonSays["PlayerFrame"] += 1
                pyterm.addItem(assets["GridBL"], 0, 0, "center", "center")
                score += 1
            else:
                score = max(score - 1, 0)
        elif (GridCenter[0] + 20 >= location[0] >= GridCenter[0] + 1) and (GridCenter[1] - 7 <= location[1] <= GridCenter[1] - 1) and (mousedetect.ClickDetect("Left", "On")): #y7, x9
            if (simonSays["Order"][simonSays["PlayerFrame"]] == "TR"):
                simonSays["PlayerFrame"] += 1
                pyterm.addItem(assets["GridTR"], 0, 0, "center", "center")
                score += 1
            else:
                score = max(score - 1, 0)
        elif (GridCenter[0] + 20 >= location[0] >= GridCenter[0] + 1) and (GridCenter[1] + 7 >= location[1] >= GridCenter[1] + 1) and (mousedetect.ClickDetect("Left", "On")): #y7, x9
            if (simonSays["Order"][simonSays["PlayerFrame"]] == "BR"):
                simonSays["PlayerFrame"] += 1
                pyterm.addItem(assets["GridBR"], 0, 0, "center", "center")
                score += 1
            else:
                score = max(score - 1, 0)
        if simonSays["PlayerFrame"] == len(simonSays["Order"]):
            score *= 1.25
            simonSays["Time"] = 0
            return True
        simonSays["Time"] -= 1
        if simonSays["Time"] == 0:
            return True
    return False


def BlackHole(Range: float, Strength: float, Unpredictability: int, Time: int):
    global score, character_size
    if blackHole["Time"] == 0:
        blackHole["Time"] = Time
        blackHole["Location"] = (random.randint(-Range[0], Range[0]), random.randint(-Range[1], Range[1]))
    if random.randint(1, Unpredictability) == 1:
        blackHole["Location"] = (random.randint(-Range[0], Range[0]), random.randint(-Range[1], Range[1]))
    blackholeTextCoords = pyterm.addItem(str(assets["BlackHole"]), blackHole["Location"][0], blackHole["Location"][1], "center", "center")
    blackholeCoords = Cursor.get_pixel_coords(character_size, blackholeTextCoords)
    if math.sqrt((blackholeCoords[0] - mouse.get_position()[0]) ** 2 + (blackholeCoords[1] - mouse.get_position()[1]) ** 2) <= Strength:
        mouse.move(blackholeCoords[0], blackholeCoords[1])
    else:
        mouse.move((blackholeCoords[0] - mouse.get_position()[0]) * Strength / max(math.sqrt((blackholeCoords[0] - mouse.get_position()[0]) ** 2 + (blackholeCoords[1] - mouse.get_position()[1]) ** 2) ** 1.35 / 5, 0.1), (blackholeCoords[1] - mouse.get_position()[1]) * Strength / max(math.sqrt((blackholeCoords[0] - mouse.get_position()[0]) ** 2 + (blackholeCoords[1] - mouse.get_position()[1]) ** 2) ** 1.35 / 5, 0.1), False)
    # pyterm.addItem(str((blackholeCoords[0] - mouse.get_position()[0]) * Strength / math.sqrt((blackholeCoords[0] - mouse.get_position()[0]) ** 2 + (blackholeCoords[1] - mouse.get_position()[1]) ** 2)) + " " + str((blackholeCoords[1] - mouse.get_position()[1]) * Strength / math.sqrt((blackholeCoords[0] - mouse.get_position()[0]) ** 2 + (blackholeCoords[1] - mouse.get_position()[1]) ** 2)), 0, 7, "center", "center")
    score += 13.5 / max(((blackholeCoords[0] - mouse.get_position()[0]) ** 2 + (blackholeCoords[1] - mouse.get_position()[1]) ** 2) ** 0.55, 180)

    blackHole["Time"] -= 1
    if blackHole["Time"] == 0:
        return True

def Reaction(TimeRange: float, Repetitions: int):
    global score
    if reaction["Repetitions"] == 0:
        reaction["Time"] = random.randint(TimeRange[0], TimeRange[1])
        reaction["Repetitions"] = Repetitions
    reaction["Time"] -= 1
    if reaction["Time"] <= 0:
        pyterm.addItem(str(assets["ReactionFlash"]), 0, 0, "center", "centre")
        if mousedetect.ClickDetect("Left", "On"):
            reaction["Repetitions"] -= 1
            reaction["Time"] = random.randint(TimeRange[0], TimeRange[1])
        else:
            score += 0.16
    elif mousedetect.ClickDetect("Left", "On"):
        score += 1

    if reaction["Repetitions"] == 0:
        return True
    return False

def Shielded(Range: float, Time: int, Unpredictability: int, MaxWait: int):
    global score, location
    if shielded["Time"] == 0:
        shielded["Time"] = Time
        shielded["PastTime"] = Time
        shielded["Location"] = (random.randint(-Range[0], Range[0]), random.randint(-Range[1], Range[1]))
    shielded["Time"] -= 1
    if (random.randint(1, Unpredictability) == 1) or ((shielded["PastTime"] - shielded["Time"]) >= MaxWait):
        shielded["Location"] = (random.randint(-Range[0], Range[0]), random.randint(-Range[1], Range[1]))
        shielded["PastTime"] = shielded["Time"]
    shieldedpos = pyterm.addItem(str(assets["Shielded"]), shielded["Location"][0], shielded["Location"][1], "center", "centre")
    score += math.sqrt((location[0] - shieldedpos[0]) ** 2 + (location[1] - shieldedpos[1]) ** 2) / 1800

    if shielded["Time"] <= 0:
        return True
    return False

def KeyboardDefend(Range: float, Inputs: list, Speed: int, Time: int, SpawnSpeed: int):
    ""

def CircleDefend(SpawnRate: int, SpeedRange: float, Time: int):
    global score, location
    if circleDefend["Time"] <= 0:
        circleDefend["Time"] = Time
        circleDefend["SpeedRange"] = SpeedRange
        circleDefend["SpawnRate"] = SpawnRate
        circleDefend["Spawns"] = []
    centercoords = pyterm.addItem(str(assets["BlackHole"]), 0, 0, "center", "center")
    circleDefend["SpawnRate"] -= 1
    if circleDefend["SpawnRate"] <= 0:
        spawnlocationx = 1
        spawnlocationy = 1
        while 0 <= spawnlocationx <= os.get_terminal_size().columns:
            spawnlocationx = random.randint(round(-0.5 * os.get_terminal_size().columns), round(1.5 * os.get_terminal_size().columns))
        while 0 <= spawnlocationy <= os.get_terminal_size().lines:
            spawnlocationy = random.randint(round(-0.5 * os.get_terminal_size().lines), round(1.5 * os.get_terminal_size().lines))
        circleDefend["Spawns"].append({"Location": (spawnlocationx, spawnlocationy), "Speed": random.randint(circleDefend["SpeedRange"][0], circleDefend["SpeedRange"][1]) / 100})
        circleDefend["SpawnRate"] = SpawnRate
    for i in circleDefend["Spawns"]:
        i["Location"] = (i["Location"][0] + (centercoords[0] - i["Location"][0]) * i["Speed"] / max(math.sqrt((centercoords[0] - i["Location"][0]) ** 2 + (centercoords[1] - i["Location"][1]) ** 2), 0.1), i["Location"][1] + (centercoords[1] - i["Location"][1]) * i["Speed"] / max(math.sqrt((centercoords[0] - i["Location"][0]) ** 2 + (centercoords[1] - i["Location"][1]) ** 2), 0.1))
        pyterm.addItem("#", round(i["Location"][0]), round(i["Location"][1]))
        if (i["Location"][0] - 2 <= location[0] <= i["Location"][0] + 2) and (i["Location"][1] - 1 <= location[1] <= i["Location"][1] + 1):
            circleDefend["Spawns"].remove(i)
            continue
        elif math.sqrt((centercoords[0] - i["Location"][0]) ** 2 + (centercoords[1] - i["Location"][1]) ** 2) <= 3:
            score += 1.2
            circleDefend["Spawns"].remove(i)
            continue
    
    circleDefend["Time"] -= 1
    if circleDefend["Time"] <= 0:
        return True
    return False

def MouseMinigame(Speed: int, Time: int):
    global score
    Inputs = ["Left", "Right", "Middle", "Not Left", "Not Right", "Not Middle", "Not Left Or Right"]
    if mouseMinigame["TotalTime"] <= 0:
        mouseMinigame["Speed"] = Speed
        mouseMinigame["TotalTime"] = Time
        mouseMinigame["Next"] = 0
        mouseMinigame["CurrentKey"] = random.choice(Inputs)
    Inputs.remove(mouseMinigame["CurrentKey"])
    if ((mouseMinigame["CurrentKey"] == "Left") or (mouseMinigame["CurrentKey"] == "Not Right") or (mouseMinigame["CurrentKey"] == "Not Middle")) and (mousedetect.ClickDetect("Left", "On")):
        mouseMinigame["Next"] = 0
        mouseMinigame["CurrentKey"] = random.choice(Inputs)
        score += 0.75
        time.sleep(0.1)
    elif ((mouseMinigame["CurrentKey"] == "Right") or (mouseMinigame["CurrentKey"] == "Not Left") or (mouseMinigame["CurrentKey"] == "Not Middle")) and (mousedetect.ClickDetect("Right", "On")):
        mouseMinigame["Next"] = 0
        mouseMinigame["CurrentKey"] = random.choice(Inputs)
        score += 0.75
        time.sleep(0.1)
    elif ((mouseMinigame["CurrentKey"] == "Middle") or (mouseMinigame["CurrentKey"] == "Not Right") or (mouseMinigame["CurrentKey"] == "Not Left") or (mouseMinigame["CurrentKey"] == "Not Left Or Right")) and (mousedetect.ClickDetect("Middle", "On")):
        mouseMinigame["Next"] = 0
        mouseMinigame["CurrentKey"] = random.choice(Inputs)
        score += 0.75
        time.sleep(0.1)
    elif mouseMinigame["Next"] >= mouseMinigame["Speed"]:
        mouseMinigame["Next"] = 0
        mouseMinigame["CurrentKey"] = random.choice(Inputs)
        score -= 0.5
        score = max(score, 0)
    mouseMinigame["TotalTime"] -= 1
    mouseMinigame["Next"] += 1
    if mouseMinigame["CurrentKey"] == "Left":
        pyterm.addItem("Press ⇤", 0, 7, "center", "center")
    elif mouseMinigame["CurrentKey"] == "Right":
        pyterm.addItem("Press ⇥", 0, 7, "center", "center")
    elif mouseMinigame["CurrentKey"] == "Middle":
        pyterm.addItem("Press ↧", 0, 7, "center", "center")
    elif mouseMinigame["CurrentKey"] == "Not Left":
        pyterm.addItem("Press ⇜", 0, 7, "center", "center")
    elif mouseMinigame["CurrentKey"] == "Not Right":
        pyterm.addItem("Press ⇝", 0, 7, "center", "center")
    elif mouseMinigame["CurrentKey"] == "Not Middle":
        pyterm.addItem("Press ↯", 0, 7, "center", "center")
    elif mouseMinigame["CurrentKey"] == "Not Left Or Right":
        pyterm.addItem("Press ↭", 0, 7, "center", "center")
    if mouseMinigame["TotalTime"] <= 0:
        return True
    return False

def DodgeGrid(Character: str, SpeedRange: float, Time: int, SpawnRate: int, InverseBias = 10):
    global score, dodgeGrid
    if dodgeGrid["Time"] <= 0:
        dodgeGrid["Time"] = Time
        dodgeGrid["SpeedRange"] = SpeedRange
        dodgeGrid["Character"] = Character
        dodgeGrid["SpawnRate"] = SpawnRate
        dodgeGrid["Hurt"] = []
        dodgeGrid["Location"] = [0, 0]
    pyterm.addItem(str(assets["GridMove"]), 0, 0, "center", "center")
    if keyboard.is_pressed("w"):
        dodgeGrid["Location"][1] -= 0.2
        if mousedetect.KeyboardDetect("w", "on"):
            dodgeGrid["Location"][1] -= 0.3
    if keyboard.is_pressed("s"):
        dodgeGrid["Location"][1] += 0.2
        if mousedetect.KeyboardDetect("s", "on"):
            dodgeGrid["Location"][1] += 0.3
    if keyboard.is_pressed("a"):
        dodgeGrid["Location"][0] -= 0.5
        if mousedetect.KeyboardDetect("a", "on"):
            dodgeGrid["Location"][0] -= 0.7
    if keyboard.is_pressed("d"):
        dodgeGrid["Location"][0] += 0.5
        if mousedetect.KeyboardDetect("d", "on"):
            dodgeGrid["Location"][0] += 0.7
    if (not keyboard.is_pressed("d")) and (not keyboard.is_pressed("a")):
        dodgeGrid["Location"][0] = round(dodgeGrid["Location"][0])
    if (not keyboard.is_pressed("w")) and (not keyboard.is_pressed("s")):
        dodgeGrid["Location"][1] = round(dodgeGrid["Location"][1])
    
    dodgeGrid["Location"][0] = max(min(dodgeGrid["Location"][0], 40), -39)
    dodgeGrid["Location"][1] = max(min(dodgeGrid["Location"][1], 13), -13)
    pyterm.addItem(str(dodgeGrid["Character"]), round(dodgeGrid["Location"][0]), round(dodgeGrid["Location"][1]), "center", "center")

    dodgeGrid["SpawnRate"] -= 1
    if dodgeGrid["SpawnRate"] <= 0:
        dodgeGrid["SpawnRate"] = SpawnRate
        if random.randint(1, InverseBias) == 1:
            dodgeGrid["Hurt"].append({"Location": [dodgeGrid["Location"][0], -random.randint(os.get_terminal_size().lines + 1, round(os.get_terminal_size().lines * 1.3))], "Speed": random.randint(SpeedRange[0], SpeedRange[1]) / 100})
        dodgeGrid["Hurt"].append({"Location": [(random.randint(-39, 40)), -random.randint(os.get_terminal_size().lines + 1, round(os.get_terminal_size().lines * 1.3))], "Speed": random.randint(SpeedRange[0], SpeedRange[1]) / 100})
    for i in dodgeGrid["Hurt"]:
        i["Location"][1] += i["Speed"]
        pyterm.addItem("X", round(i["Location"][0]), round(i["Location"][1]), "center", "center")
        if (round(dodgeGrid["Location"][0]) == round(i["Location"][0])) and (round(dodgeGrid["Location"][1]) == round(i["Location"][1])):
            score -= 0.65

    dodgeGrid["Time"] -= 1
    if dodgeGrid["Time"] <= 0:
        return True
    return False

def TrackingMinigame(Character: int, SpawnRate: int, SpeedRange: float, DespawnRate: int, Time: int):
    global score, trackingMinigame, location
    if trackingMinigame["Time"] <= 0:
        trackingMinigame["Time"] = Time
        trackingMinigame["SpeedRange"] = SpeedRange
        trackingMinigame["Character"] = Character
        trackingMinigame["SpawnRate"] = SpawnRate
        trackingMinigame["DespawnRate"] = DespawnRate
        trackingMinigame["Hurt"] = []
        trackingMinigame["Location"] = [0, 0]
    pyterm.addItem(str(assets["GridMove"]), 0, 0, "center", "center")
    if keyboard.is_pressed("w"):
        trackingMinigame["Location"][1] -= 0.2
        if mousedetect.KeyboardDetect("w", "on"):
            trackingMinigame["Location"][1] -= 0.3
    if keyboard.is_pressed("s"):
        trackingMinigame["Location"][1] += 0.2
        if mousedetect.KeyboardDetect("s", "on"):
            trackingMinigame["Location"][1] += 0.3
    if keyboard.is_pressed("a"):
        trackingMinigame["Location"][0] -= 0.5
        if mousedetect.KeyboardDetect("a", "on"):
            trackingMinigame["Location"][0] -= 0.7
    if keyboard.is_pressed("d"):
        trackingMinigame["Location"][0] += 0.5
        if mousedetect.KeyboardDetect("d", "on"):
            trackingMinigame["Location"][0] += 0.7
    if (not keyboard.is_pressed("d")) and (not keyboard.is_pressed("a")):
        trackingMinigame["Location"][0] = round(trackingMinigame["Location"][0])
    if (not keyboard.is_pressed("w")) and (not keyboard.is_pressed("s")):
        trackingMinigame["Location"][1] = round(trackingMinigame["Location"][1])
    
    trackingMinigame["Location"][0] = max(min(trackingMinigame["Location"][0], 40), -39)
    trackingMinigame["Location"][1] = max(min(trackingMinigame["Location"][1], 13), -13)
    pyterm.addItem(str(trackingMinigame["Character"]), round(trackingMinigame["Location"][0]), round(trackingMinigame["Location"][1]), "center", "center")

    trackingMinigame["SpawnRate"] -= 1
    if trackingMinigame["SpawnRate"] <= 0:
        trackingMinigame["SpawnRate"] = SpawnRate
        spawnlocationx = 0
        spawnlocationy = 0
        while (-40 < spawnlocationx < 41) and (-14 < spawnlocationy < 14):
            spawnlocationx = random.randint(round(-0.5 * os.get_terminal_size().columns), round(0.5 * os.get_terminal_size().columns))
            spawnlocationy = random.randint(round(-0.5 * os.get_terminal_size().lines), round(0.5 * os.get_terminal_size().lines))
        trackingMinigame["Hurt"].append({"Location": [spawnlocationx, spawnlocationy], "Speed": random.randint(trackingMinigame["SpeedRange"][0], trackingMinigame["SpeedRange"][1]) / 100, "DespawnRate": trackingMinigame["DespawnRate"]})
    for i in trackingMinigame["Hurt"]:
        i["Location"] = [i["Location"][0] + (trackingMinigame["Location"][0] - i["Location"][0]) * i["Speed"] / max(math.sqrt((trackingMinigame["Location"][0] - i["Location"][0]) ** 2 + (trackingMinigame["Location"][1] - i["Location"][1]) ** 2), 0.1), i["Location"][1] + (trackingMinigame["Location"][1] - i["Location"][1]) * i["Speed"] / max(math.sqrt((trackingMinigame["Location"][0] - i["Location"][0]) ** 2 + (trackingMinigame["Location"][1] - i["Location"][1]) ** 2), 0.1)]
        i["DespawnRate"] -= 1
        if i["DespawnRate"] <= 0:
            trackingMinigame["Hurt"].remove(i)
            continue
        
        if math.sqrt((trackingMinigame["Location"][0] - i["Location"][0]) ** 2 + (trackingMinigame["Location"][1] - i["Location"][1]) ** 2) <= i["Speed"]:
            i["Location"][0] = trackingMinigame["Location"][0]
            i["Location"][1] = trackingMinigame["Location"][1]

        pyterm.addItem("X", round(i["Location"][0]), round(i["Location"][1]), "center", "center")
        if (trackingMinigame["Location"][0] == i["Location"][0]) and (trackingMinigame["Location"][1] == i["Location"][1]):
            score -= 1
            trackingMinigame["Hurt"].remove(i)
            continue
        
    trackingMinigame["Time"] -= 1
    if trackingMinigame["Time"] <= 0:
        return True
    return False


trackingMinigame = {"Location": [0, 0], "Character": "", "Hurt": [], "Time": 0, "SpeedRange": (0, 0), "SpawnRate": 0, "DespawnRate": 0}

dodgeGrid = {"Location": [0, 0], "Character": "", "Hurt": [], "Time": 0, "SpeedRange": (0, 0), "SpawnRate": 0}
#Hurt: {Location: [0, 0], Speed: 0}

mouseMinigame = {"Speed": 0, "Next": 0, "TotalTime": 0, "CurrentKey": 0}


circleDefend = {"SpawnRate": 0, "SpeedRange": (0, 0), "Time": 0, "Spawns": []}
#Spawns: [{"Location": (0, 0), "Speed": 0}]

shielded = {"Location": (0, 0), "Time": 0, "PastTime": 0}

reaction = {"Repetitions": 0, "Time": 0}

blackHole = {"Location": (0, 0), "Time": 0}

simonSays = {"Order": [], "Time": 0, "Phase": "", "PlayerFrame": 0, "InitialSpeed": 0, "PhaseInitialTime": 0, "PhaseInitialFrame": 0}

spamMinigame = {"Time": 0, "Key": 0}

keyboardMinigame = {"Speed": 0, "Next": 0, "TotalTime": 0, "CurrentKey": ""}

aimMinigame = {"Speed": 10, "CurrentFrame": 0, "Repeats": 0, "CurrentWait": 0}

circleStay = {"location": (0, 0), "Time": 0, "rotation": 0, "absoluteloc": (0, 0)}

buttons = []

timed = 99
AimTarget = []
character_size = (19, 37)
# character_size = Cursor.initialize(2)
score = 0

clickbufferDelay = False
clickbuffer = False

while False:
    startTime = time.perf_counter()
    pyterm.clearLetters()
    pyterm.updateKeys()
    MainClock += 1

    #Code Start
    location = Cursor.get_mouse_coords(character_size, True)

    #First Atk - Target
    # if timed >= 13:
    #     AddAttackAim((round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), 20, True)
    #     timed = 0
    # score += AttackAim()
    # pyterm.addItem(str(score))

    # pyterm.addItem(str(location), 0, 0, "top right", "top right")
    # pyterm.addItem(str(buttons), 0, 0, "bottom left", "bottom left")
    

    #Circles
 
    # CircleStay((round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), 10000, 0.5, 25)
    # pyterm.addItem(str(circleStay), 0, 0, "bottom left", "bottom left")

    #Aim Minigame
    
    # if AimMinigame((3, 5), 12):
    #     input("\r")
    #     score = 0
    
    # pyterm.addItem(str(aimMinigame["Repeats"]), 0, 0, "bottom left", "bottom left")

    #KeyboardSpam

    # if KeyboardMinigame("a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" "), 0.7 * pyterm.fps, 8 * pyterm.fps):
    #     input("\r")
    #     score = 0


    #Spam

    # if Spam(8 * pyterm.fps):
    #     input("\r")
    #     score = 0


    #Simon Says Grid

    # if SimonSays(8, 30, 20 * pyterm.fps):
    #     input("\r")
    #     score = 0




    #BlackHole
    # if BlackHole((round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), 300, 30, 8.5 * pyterm.fps):
    #     input("\r")
    #     score = 0

    
    #Reaction
    # if Reaction((1 * pyterm.fps, 3 * pyterm.fps), 3):
    #     input("\r")
    #     score = 0


    #ShieldSpam
    # if Shielded((round(os.get_terminal_size().columns / 3), round(os.get_terminal_size().lines / 3)), 10 * pyterm.fps, 60, 1 * pyterm.fps):
    #     input("\r")
    #     score = 0


    #CircleDefend
    # if CircleDefend(0.1875 * pyterm.fps, (20, 45), 15 * pyterm.fps):
    #     input("\r")
    #     score = 0


    #DodgeGrid
    if DodgeGrid("O", (10, 70), 20 * pyterm.fps, 0.025 * pyterm.fps, 4):
        input("\r")
        score = 0

    #Tracking
    # if TrackingMinigame("O", 0.06125 * pyterm.fps, (13, 25), 4 * pyterm.fps, 20 * pyterm.fps):
    #     input("\r")
    #     score = 0


    # if MouseMinigame(1.5 * pyterm.fps, 8 * pyterm.fps):
    #     input("\r")
    #     score = 0


    #The Extras

    timed += 1
    pyterm.addItem(str(score))
    pyterm.addItem(str(time.time() - FalseTime), 0, 0, "top right", "top right")

    #Code End

    pyterm.renderScreen()
    elapsedTime = time.perf_counter() - startTime
    if elapsedTime < (1 / pyterm.fps):
        time.sleep((1 / pyterm.fps) - elapsedTime)
    pyterm.displayScreen()



