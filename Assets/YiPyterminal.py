from pynput import mouse
import Assets.CodingAssets as CodingAssets
import keyboard
import threading
import math
import time
import sys
import os

# Variables: Constants
FPS = 100
# Variables: Lists and Dictionaries
lettersToRender = {}
screenRender = []
debugMessages = []
items = {
    "example target": {
        "animation frames": [
            """
šššš|šššš
šššš|šššš
----+----
šššš|šššš
šššš|šššš
""",
            """
šš|šš
--+--
šš|šš
""",
            """
+
""",
        ],
        "x": 0,
        "y": 0,
        "x bias": 0,
        "y bias": 0,
        "width": 1,
        "length": 1,
        "current frame": 0,
        "parent object": "screen",
        "parent anchor": "top left",
        "child anchor": "center",
    },
}
keyBindsStatus = {
    "up": {"state": False, "keybind": "w"},
    "left": {"state": False, "keybind": "a"},
    "down": {"state": False, "keybind": "s"},
    "right": {"state": False, "keybind": "d"},
}
mouseStatus = {
    "absolute position": (0, 0),
    "left button": False,
    "right button": False,
    "middle button": False,
    "scroll x": 0,
    "scroll y": 0,
}
# Variables: Other
screenWidth = os.get_terminal_size().columns
screenHeight = os.get_terminal_size().lines
debugMode = True
constantlyCheckScreenSize = True
threadingLock = threading.Lock()
endEscapeCode = CodingAssets.endEscapeCode
styleCodes = CodingAssets.styleCodes
colorCodes = CodingAssets.colorCodes


# Functions: Rendering
def addLetter(coords: tuple, letter: str, overwrite: bool = True) -> None:
    if overwrite == False:
        if coords in lettersToRender:
            pass
            addDebugMessage("You are trying to overwrite something")
    lettersToRender[coords] = letter


def renderLiteralItem(
    item: str,
    xBias: int = 0,
    yBias: int = 0,
    screenAnchor: str = "top left",
    itemAnchor: str = "top left",
    emptySpaceLetter: str = "š",
) -> None:

    splitItem = item.splitlines()
    longestRowLen = 0
    for rowNum in range(len(splitItem)):
        if len(splitItem[rowNum]) > longestRowLen:
            longestRowLen = len(splitItem[rowNum])
        splitItem[rowNum] = list(splitItem[rowNum])
    if screenAnchor == "top left":
        xAnchor, yAnchor = 0, 0
    elif screenAnchor == "top right":
        xAnchor, yAnchor = screenWidth, 0
    elif screenAnchor == "bottom left":
        xAnchor, yAnchor = 0, screenHeight
    elif screenAnchor == "bottom right":
        xAnchor, yAnchor = screenWidth, screenHeight
    elif screenAnchor == "center" or screenAnchor == "centre":
        xAnchor, yAnchor = math.ceil(screenWidth / 2), math.ceil(screenHeight / 2)
    else:

        addDebugMessage(
            "".join(["Invalid input for screenAnchor in addItem():", screenAnchor])
        )
    if itemAnchor == "top left":
        yAnchor -= 0
        xAnchor -= 0
    elif itemAnchor == "top right":
        xAnchor -= longestRowLen
        yAnchor -= 0
    elif itemAnchor == "bottom left":
        xAnchor -= 0
        yAnchor -= len(splitItem)
    elif itemAnchor == "bottom right":
        xAnchor -= longestRowLen
        yAnchor -= len(splitItem)
    elif itemAnchor == "center" or itemAnchor == "centre":
        xAnchor -= math.ceil(longestRowLen / 2)
        yAnchor -= math.ceil(len(splitItem) / 2)
    else:

        addDebugMessage(
            "".join(["Invalid input for itemAnchor in addItem():", itemAnchor])
        )
    xAnchor += xBias
    yAnchor += yBias
    for rowNum in range(len(splitItem)):
        for columnNum in range(len(splitItem[rowNum])):
            if splitItem[rowNum][columnNum] != emptySpaceLetter:
                addLetter(
                    (columnNum + xAnchor, rowNum + yAnchor),
                    splitItem[rowNum][columnNum],
                )


def renderScreen() -> None:
    if constantlyCheckScreenSize == True:
        updateScreenSize()
    global screenRender
    screenRender = [[" " for _ in range(screenWidth)] for _ in range(screenHeight)]
    for row in range(screenHeight):
        for coords in lettersToRender:
            if coords[1] == row:
                if 0 <= coords[0] < len(screenRender[row]):
                    screenRender[row][coords[0]] = lettersToRender[coords]
    for row in range(len(screenRender)):
        screenRender[row] = "".join(screenRender[row])


def displayScreen(advanceMode: bool = True, clearScreen: bool = False) -> None:
    if clearScreen:
        os.system("cls")

    if advanceMode == True:
        sys.stdout.write("\033[H")
        for rowNum in range(len(screenRender)):
            sys.stdout.write(f"\033[{rowNum+1};1f{''.join(screenRender[rowNum])}")
            sys.stdout.write(f"\033[{screenHeight};{screenWidth}H")
            sys.stdout.flush()

    else:
        print(screenRender, end="")


def clearLettersToRender() -> None:
    global lettersToRender
    lettersToRender = {}


def clearScreenRender() -> None:
    global screenRender
    screenRender = []


def removeLetter(coords: tuple) -> None:
    del lettersToRender[coords]


def getLetter(coords: tuple) -> str:
    return lettersToRender[coords]


# Functions: Items Sudo-objects
def createItem(
    name: str,
    animationFrames: list,
    parentObject: str = "screen",
    parentAnchor: str = "top left",
    childAnchor: str = "top left",
    currentFrame: int = 0,
    xBias: int = 0,
    yBias: int = 0,
) -> None:
    items[name] = {
        "animation frames": animationFrames,
        "x": None,
        "y": None,
        "x bias": xBias,
        "y bias": yBias,
        "width": None,
        "length": None,
        "current frame": currentFrame,
        "parent object": parentObject,
        "parent anchor": parentAnchor,
        "child anchor": childAnchor,
    }
    updateItemLocation(name)


def renderItem(
    item: str,
    emptySpaceLetter: str = "š",
    xBias: str = 0,
    yBias: str = 0,
) -> None:
    splitItem = items[item]["animation frames"][
        items[item]["current frame"]
    ].splitlines()

    longestRowLen = 0
    for rowNum in range(len(splitItem)):
        if len(splitItem[rowNum]) > longestRowLen:
            longestRowLen = len(splitItem[rowNum])
        splitItem[rowNum] = list(splitItem[rowNum])

    xAnchor = xBias + items[item]["x bias"]
    yAnchor = yBias + items[item]["y bias"]
    for rowNum in range(len(splitItem)):
        for columnNum in range(len(splitItem[rowNum])):
            if splitItem[rowNum][columnNum] != emptySpaceLetter:
                addLetter(
                    (columnNum + xAnchor, rowNum + yAnchor),
                    splitItem[rowNum][columnNum],
                )


def updateItemLocation(item: str) -> None:
    parentObject = items[item]["parent object"]
    parentAnchor = items[item]["parent anchor"]
    childAnchor = items[item]["child anchor"]
    if parentObject == "screen":
        if parentAnchor == "top left":
            xAnchor, yAnchor = 0, 0
        elif parentAnchor == "top right":
            xAnchor, yAnchor = screenWidth, 0
        elif parentAnchor == "bottom left":
            xAnchor, yAnchor = 0, screenHeight
        elif parentAnchor == "bottom right":
            xAnchor, yAnchor = screenWidth, screenHeight
        elif parentAnchor == "center" or parentAnchor == "centre":
            xAnchor, yAnchor = math.ceil(screenWidth / 2), math.ceil(screenHeight / 2)
        else:
            pass
            addDebugMessage(
                "".join(["Invalid input for parentAnchor in addItem():", parentAnchor])
            )
    elif parentObject in items:
        if parentAnchor == "top left":
            xAnchor, yAnchor = getTopLeft(parentObject)
        elif parentAnchor == "top right":
            xAnchor, yAnchor = getTopRight(parentObject)
        elif parentAnchor == "bottom left":
            xAnchor, yAnchor = getBottomLeft(parentObject)
        elif parentAnchor == "bottom right":
            xAnchor, yAnchor = getBottomRight(parentObject)
        elif parentAnchor == "center" or parentAnchor == "centre":
            xAnchor, yAnchor = getCenter(parentObject)
        else:

            addDebugMessage(
                "".join(["Invalid input for parentAnchor in addItem():", parentAnchor])
            )
    else:

        addDebugMessage(
            "".join(["Invalid input for parentObject in addItem():", parentObject])
        )

    if childAnchor == "top left":
        yAnchor -= 0
        xAnchor -= 0
    elif childAnchor == "top right":
        xAnchor -= items[item]["width"]
        yAnchor -= 0
    elif childAnchor == "bottom left":
        xAnchor -= 0
        yAnchor -= items[item]["length"]
    elif childAnchor == "bottom right":
        xAnchor -= items[item]["width"]
        yAnchor -= items[item]["length"]
    elif childAnchor == "center" or childAnchor == "centre":
        xAnchor -= math.ceil(items[item]["width"] / 2)
        yAnchor -= math.ceil(items[item]["length"] / 2)
    else:

        addDebugMessage(
            "".join(["Invalid input for childAnchor in addItem():", childAnchor])
        )
    items[item]["x"] = xAnchor + items[item]["x bias"]
    items[item]["y"] = yAnchor + items[item]["y bias"]


def getTopLeft(item: str) -> tuple:
    if item in items:
        return (item[item]["x"], item[item]["y"])


def getTopRight(item: str) -> tuple:
    if item in items:
        return (item[item]["x"] + items[item]["width"], item[item]["y"])


def getBottomLeft(item: str) -> tuple:
    if item in items:
        return (item[item]["x"], item[item]["y"] + items[item]["height"])


def getBottomRight(item: str) -> tuple:
    if item in items:
        return (
            item[item]["x"] + items[item]["width"],
            item[item]["y"] + items[item]["height"],
        )


def getCenter(item: str) -> tuple:
    if item in items:
        return (
            item[item]["x"] + math.ceil(items[item]["width"] / 2),
            item[item]["y"] + math.ceil(items[item]["height"] / 2),
        )


def deleteItem(item: str) -> None:
    del items[item]


# Functions: Key Binds
def updateKeys(keysBinds: list = ["all"]) -> None:
    if keysBinds == ["all"]:
        for key in keyBindsStatus:
            keyBindsStatus[key]["state"] = keyboard.is_pressed(
                keyBindsStatus[key]["keybind"]
            )
    elif keysBinds != [] and type(keysBinds) is list:
        for key in keysBinds:
            keyBindsStatus[key]["state"] = keyboard.is_pressed(
                keyBindsStatus[key]["keybind"]
            )


def getKeyBinds(keyBind: str, update: bool = False) -> bool:
    if update == True:
        keyBindsStatus[keyBind]["state"] = keyboard.is_pressed(
            keyBindsStatus[keyBind]["keybind"]
        )
    return keyBindsStatus[keyBind]["state"]


# Functions: Mouse Binds
pass


# Functions: Debug Messages
def addDebugMessage(message: str) -> None:
    debugMessages.append(
        "".join(["> ", time.strftime("%H:%M:%S", time.localtime()), " | ", message])
    )


def clearDebugMessages() -> None:
    global debugMessages
    debugMessages = []


def removeDebugMessage(position: int, firstAdded: bool = True) -> None:
    if firstAdded == True:
        debugMessages[position].pop()
    else:
        debugMessages[len(debugMessages) - position].pop()


def renderDebugMessages(messageLimit: int = 5) -> None:
    if debugMode == True:
        for row in range(min(messageLimit, len(debugMessages))):
            renderLiteralItem(
                debugMessages[len(debugMessages) - 1 - row],
                yBias=-1 * row,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )
        if len(debugMessages) - messageLimit == 1:
            renderLiteralItem(
                "".join(
                    [
                        "> There is 1 more debug message",
                    ],
                ),
                yBias=-1 * messageLimit,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )
        elif len(debugMessages) > messageLimit:
            renderLiteralItem(
                "".join(
                    [
                        "> There are ",
                        str(len(debugMessages) - messageLimit),
                        " more debug messages",
                    ],
                ),
                yBias=-1 * messageLimit,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )


# Functions: Miscellaneous
def updateScreenSize() -> None:
    global screenWidth, screenHeight
    screenWidth = os.get_terminal_size().columns
    screenHeight = os.get_terminal_size().lines


def addBorder(
    text: str,
    top: bool = True,
    bottom: bool = True,
    left: bool = True,
    right: bool = True,
    borderCharacter: str = "-",
    cornerCharacter: str = "+",
) -> str:
    lines = text.splitlines()
    maxLen = max(len(line) for line in lines)
    borderedLines = []
    if top:
        borderedLines.append(
            (cornerCharacter if left else "")
            + (borderCharacter * (maxLen + (1 if right else 0) + (1 if left else 0)))
            + (cornerCharacter if right else "")
        )
    for line in lines:
        padded = line.ljust(maxLen)
        borderedLine = ""
        if left:
            borderedLine += "| "
        borderedLine += padded
        if right:
            borderedLine += " |"
        borderedLines.append(borderedLine)
    if bottom:
        borderedLines.append(
            (cornerCharacter if left else "")
            + (borderCharacter * (maxLen + (1 if right else 0) + (1 if left else 0)))
            + (cornerCharacter if right else "")
        )
    return "\n".join(borderedLines)


def style(
    text: str,
    styling: list = [],
    foreground: bool = None,
    background: bool = None,
    brightColors: bool = False,
    start: int = 0,
    end: int = -0,
) -> str:
    startEscapeCode = "\033["
    stylingAdded = []
    if styling == [] or ("normal" or "reset") in styling:
        "".join([startEscapeCode, "0;"])
    else:
        for style in styling:
            stylecode = styleCodes[style]
            if stylecode != stylingAdded:
                "".join([startEscapeCode, str(stylecode), ";"])
                stylingAdded.append(stylecode)

    if foreground != None:
        if foreground in colorCodes:
            if brightColors:
                "".join([startEscapeCode, str(colorCodes[background] + 60), ";"])
            else:
                "".join([startEscapeCode, str(colorCodes[foreground]), ";"])
    if background != None:
        if background in colorCodes:
            if brightColors:
                "".join(
                    [
                        startEscapeCode,
                        str(colorCodes[background] + 70),
                        ";",
                    ]
                )
            else:
                "".join([startEscapeCode, str(colorCodes[background] + 10), ";"])
    "".join(
        [
            startEscapeCode.strip(";"),
            "m",
        ]
    )
    processedString = list(text)
    processedString.insert(start, startEscapeCode)
    if math.copysign(1, end) == -1:
        end = len(text)
    processedString.insert(end, endEscapeCode)
    return "".join(processedString)
