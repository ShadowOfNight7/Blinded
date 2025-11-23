from ctypes.wintypes import HWND, DWORD, RECT
import Assets.CodingAssets as CodingAssets
from pynput import mouse
import pygetwindow
import threading
import keyboard
import win32gui
import ctypes
import math
import time
import copy
import sys
import os

# Variables: Constants
FPS = 100
# Variables: Lists and Dictionaries
lettersToRender = {}
screenRender = []
debugMessages = []
itemObjects = {
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
        "height": 1,
        "current frame": 0,
        "parent object": "screen",
        "parent anchor": "top left",
        "child anchor": "center",
        "is empty character part of hitbox": False,
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
    "position": (0, 0),
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


# Functions: Terminal Initialization
def prepareTerminalInitialization() -> None:
    global dwmapi, hwnd, fullScreenRect, maximizedScreenRect, win
    dwmapi = ctypes.WinDLL("dwmapi")
    hwnd = ctypes.windll.user32.FindWindowW(
        0, win32gui.GetWindowText(win32gui.GetForegroundWindow())
    )
    ctypes.windll.user32.SetProcessDPIAware()
    fullScreenRect = (
        0,
        0,
        ctypes.windll.user32.GetSystemMetrics(0),
        ctypes.windll.user32.GetSystemMetrics(1),
    )
    maximizedScreenRect = (
        0,
        0,
        ctypes.windll.user32.GetSystemMetrics(16),
        ctypes.windll.user32.GetSystemMetrics(17),
    )
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    win = pygetwindow.getActiveWindow()


def initializeTerminal(
    repetitions: int = 2,
    overrideValue: tuple | None = None,
) -> tuple:
    prepareTerminalInitialization()
    global characterSize
    if overrideValue != None:
        characterSize = overrideValue
        return characterSize
    charSize = []
    for i in range(repetitions):
        charSize.append(getCharacterSize())
        time.sleep(0.1)
    charx, chary = 0, 0
    for i in charSize:
        charx += i[0]
        chary += i[1]
    pygetwindow.getActiveWindow().size = (
        maximizedScreenRect[2],
        maximizedScreenRect[3],
    )
    characterSize = (round(charx / repetitions), round(chary / repetitions))
    return characterSize


def getCharacterSize(sleepTime: float = 0.025) -> tuple:
    pygetwindow.getActiveWindow().size = (0, 0)
    time.sleep(sleepTime * 2)
    currentSize = pygetwindow.getActiveWindow().size
    currentLines = os.get_terminal_size().lines
    while os.get_terminal_size().lines == currentLines:
        pygetwindow.getActiveWindow().size = (
            pygetwindow.getActiveWindow().size[0],
            pygetwindow.getActiveWindow().size[1] + 1,
        )
        time.sleep(sleepTime)
    currentSize = pygetwindow.getActiveWindow().size
    currentLines = os.get_terminal_size().lines
    while os.get_terminal_size().lines == currentLines:
        pygetwindow.getActiveWindow().size = (
            pygetwindow.getActiveWindow().size[0],
            pygetwindow.getActiveWindow().size[1] + 1,
        )
        time.sleep(sleepTime)
    charHeight = pygetwindow.getActiveWindow().size[1] - currentSize[1]
    currentSize = pygetwindow.getActiveWindow().size
    currentCol = os.get_terminal_size().columns
    while os.get_terminal_size().columns == currentCol:
        pygetwindow.getActiveWindow().size = (
            pygetwindow.getActiveWindow().size[0] + 1,
            pygetwindow.getActiveWindow().size[1],
        )
        time.sleep(sleepTime)
    currentSize = pygetwindow.getActiveWindow().size
    currentCol = os.get_terminal_size().columns
    while os.get_terminal_size().columns == currentCol:
        pygetwindow.getActiveWindow().size = (
            pygetwindow.getActiveWindow().size[0] + 1,
            pygetwindow.getActiveWindow().size[1],
        )
        time.sleep(sleepTime)
    charWidth = pygetwindow.getActiveWindow().size[0] - currentSize[0]
    return (charWidth, charHeight)


def checkIfFullScreen() -> bool | str:
    try:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
        rect = win32gui.GetWindowRect(hWnd)
        if rect == fullScreenRect:
            return True
        elif (rect[2] >= maximizedScreenRect[2]) and (
            rect[3] >= maximizedScreenRect[3]
        ):
            return "maximized"
        else:
            return False
    except:
        return False


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
) -> tuple:

    splitItem = item.splitlines()
    longestRowLen = 0
    for rowNum in range(len(splitItem)):
        if len(splitItem[rowNum]) > longestRowLen:
            longestRowLen = len(splitItem[rowNum])
        splitItem[rowNum] = list(splitItem[rowNum])
    xAnchor, yAnchor = getAnchorPosition(
        itemAnchor,
        item,
        screenAnchor,
        width=longestRowLen,
        height=len(splitItem),
        isChildObjectLiteralStr=True,
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
    return (xAnchor + math.floor(longestRowLen / 2), yAnchor + math.floor(len(splitItem) / 2))


def renderScreen(backgroundCharacter: str = " ") -> None:
    if constantlyCheckScreenSize == True:
        updateScreenSize()
    global screenRender
    screenRender = [
        [backgroundCharacter for _ in range(screenWidth)] for _ in range(screenHeight)
    ]
    for row in range(screenHeight):
        for coords in lettersToRender:
            if coords[1] == row:
                if 0 <= coords[0] < len(screenRender[row]):
                    screenRender[row][coords[0]] = lettersToRender[coords]
    for row in range(len(screenRender)):
        screenRender[row] = "".join(screenRender[row])


def displayScreen(
    clearScreenData: dict = {"clear lettersToRender": True, "clear screenRender": True},
    # resetMouseStatusAfterPrinting: bool = True,
    displayDebugMessages: bool = True,
    advanceMode: bool = True,
    clearScreenBeforePrinting: bool = False,
) -> None:
    if clearScreenBeforePrinting:
        os.system("cls")

    if advanceMode == True:
        sys.stdout.write("\033[H")
        for rowNum in range(len(screenRender)):
            sys.stdout.write(f"\033[{rowNum+1};1f{''.join(screenRender[rowNum])}")
            sys.stdout.write(f"\033[{screenHeight};{screenWidth}H")
            sys.stdout.flush()

    else:
        print(screenRender, end="")
    if clearScreenData["clear lettersToRender"] == True:
        clearLettersToRender()
    if clearScreenData["clear screenRender"] == True:
        clearScreenRender()
    # if resetMouseStatusAfterPrinting == True:
    #     resetMouseStatus()
    if displayDebugMessages == True:
        renderDebugMessages()


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
    isEmptyCharacterPartOfHitbox: bool = False,
) -> None:
    itemObjects[name] = {
        "animation frames": animationFrames,
        "x": None,
        "y": None,
        "x bias": xBias,
        "y bias": yBias,
        "width": None,
        "height": None,
        "current frame": currentFrame,
        "parent object": parentObject,
        "parent anchor": parentAnchor,
        "child anchor": childAnchor,
        "is empty character part of hitbox": isEmptyCharacterPartOfHitbox,
    }
    updateItemSize(name)
    updateItemLocation(name)


def renderItem(
    item: str,
    emptySpaceLetter: str = "š",
    xBias: str = 0,
    yBias: str = 0,
) -> None:
    splitItem = itemObjects[item]["animation frames"][
        itemObjects[item]["current frame"]
    ].splitlines()
    for rowNum in range(len(splitItem)):
        for columnNum in range(len(splitItem[rowNum])):
            if splitItem[rowNum][columnNum] != emptySpaceLetter:
                addLetter(
                    (
                        columnNum
                        + xBias
                        + itemObjects[item]["x bias"]
                        + itemObjects[item]["x"],
                        rowNum
                        + yBias
                        + itemObjects[item]["y bias"]
                        + itemObjects[item]["y"],
                    ),
                    splitItem[rowNum][columnNum],
                )


def updateItemLocation(item: str) -> None:
    itemObjects[item]["x"], itemObjects[item]["y"] = getAnchorPosition(
        itemObjects[item]["child anchor"],
        item,
        itemObjects[item]["parent anchor"],
        itemObjects[item]["parent object"],
    )


def checkItemIsClicked(
    item: str, button: str = "left", mouseCoords: tuple | None = None
) -> bool:
    if mouseCoords is None:
        mouseCoords = mouseStatusCopy["position"]
    itemTopLeftX, itemTopLeftY = getTopLeft(item)
    itemBottomRightX, itemBottomRightY = getBottomRight(item)
    if (
        itemTopLeftX <= mouseCoords[0] <= itemBottomRightX
        and itemTopLeftY <= mouseCoords[1] <= itemBottomRightY
    ):
        if itemObjects[item]["is empty character part of hitbox"] == False:
            itemFrame = itemObjects[item]["animation frames"][
                itemObjects[item]["current frame"]
            ].splitlines()
            relativeX = mouseCoords[0] - itemTopLeftX
            relativeY = mouseCoords[1] - itemTopLeftY
            if itemFrame[relativeY][relativeX] != "š":
                if button == "left":
                    return mouseStatusCopy["left button"]
                elif button == "right":
                    return mouseStatusCopy["right button"]
                elif button == "middle":
                    return mouseStatusCopy["middle button"]
                else:
                    addDebugMessage("Invalid button input in checkItemIsClicked()")
            else:
                return False
        if button:
            return mouseStatusCopy["left button"]
        else:
            return mouseStatusCopy["right button"]


def getAnchorPosition(
    childAnchor: str,
    childObject: str,
    parentAnchor: str,
    parentObject: str = "screen",
    width: int | None = None,
    height: int | None = None,
    xBias: int | None = None,
    yBias: int | None = None,
    isChildObjectLiteralStr: bool = False,
) -> tuple:
    if parentObject == "screen":
        if parentAnchor == "top left":
            anchorX, anchorY = 0, 0
        elif parentAnchor == "top right":
            anchorX, anchorY = screenWidth, 0
        elif parentAnchor == "bottom left":
            anchorX, anchorY = 0, screenHeight
        elif parentAnchor == "bottom right":
            anchorX, anchorY = screenWidth, screenHeight
        elif parentAnchor == "center" or parentAnchor == "centre":
            anchorX, anchorY = math.ceil(screenWidth / 2), math.ceil(screenHeight / 2)
        else:
            pass
            addDebugMessage(
                "".join(["Invalid input for parentAnchor in addItem():", parentAnchor])
            )
    elif parentObject in itemObjects:
        if parentAnchor == "top left":
            anchorX, anchorY = getTopLeft(parentObject)
        elif parentAnchor == "top right":
            anchorX, anchorY = getTopRight(parentObject)
        elif parentAnchor == "bottom left":
            anchorX, anchorY = getBottomLeft(parentObject)
        elif parentAnchor == "bottom right":
            anchorX, anchorY = getBottomRight(parentObject)
        elif parentAnchor == "center" or parentAnchor == "centre":
            anchorX, anchorY = getCenter(parentObject)
        else:

            addDebugMessage(
                "".join(["Invalid input for parentAnchor in addItem():", parentAnchor])
            )
    else:

        addDebugMessage(
            "".join(["Invalid input for parentObject in addItem():", parentObject])
        )
    if isChildObjectLiteralStr == False:
        if width == None:
            width = itemObjects[childObject]["width"]
        if height == None:
            height = itemObjects[childObject]["height"]
    elif isChildObjectLiteralStr == True:
        width, height = getStrWidthAndHeight(childObject)
    if childAnchor == "top left":
        anchorY -= 0
        anchorX -= 0
    elif childAnchor == "top right":
        anchorX -= width
        anchorY -= 0
    elif childAnchor == "bottom left":
        anchorX -= 0
        anchorY -= height
    elif childAnchor == "bottom right":
        anchorX -= width
        anchorY -= height
    elif childAnchor == "center" or childAnchor == "centre":
        anchorX -= math.ceil(width / 2)
        anchorY -= math.ceil(height / 2)
    else:
        addDebugMessage(
            "".join(["Invalid input for childAnchor in addItem():", childAnchor])
        )
    if childObject != None and isChildObjectLiteralStr == False:
        anchorX + itemObjects[childObject]["x bias"]
        anchorY + itemObjects[childObject]["y bias"]
    else:
        if xBias != None:
            anchorX += xBias
        if yBias != None:
            anchorY += yBias
    return (anchorX, anchorY)


def updateItemSize(item: str) -> None:
    splitItem = itemObjects[item]["animation frames"][
        itemObjects[item]["current frame"]
    ].splitlines()
    longestRowLen = 0
    for rowNum in range(len(splitItem)):
        if len(splitItem[rowNum]) > longestRowLen:
            longestRowLen = len(splitItem[rowNum])
    itemObjects[item]["width"] = longestRowLen
    itemObjects[item]["height"] = len(splitItem)


def getStrWidthAndHeight(itemStr: str) -> tuple:
    splitItem = itemStr.splitlines()
    longestRowLen = 0
    for rowNum in range(len(splitItem)):
        if len(splitItem[rowNum]) > longestRowLen:
            longestRowLen = len(splitItem[rowNum])
    return (longestRowLen, len(splitItem))


def updateItemFrame(item: str, newFrame: int) -> None:
    itemObjects[item]["current frame"] = newFrame
    updateItemSize(item)
    updateItemLocation(item)


def getTopLeft(item: str) -> tuple:
    if item in itemObjects:
        return (itemObjects[item]["x"], itemObjects[item]["y"])


def getTopRight(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"] + itemObjects[item]["width"] - 1,
            itemObjects[item]["y"],
        )


def getBottomLeft(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"],
            itemObjects[item]["y"] + itemObjects[item]["height"] - 1,
        )


def getBottomRight(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"] + itemObjects[item]["width"] - 1,
            itemObjects[item]["y"] + itemObjects[item]["height"] - 1,
        )


def getCenter(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"] + math.ceil(itemObjects[item]["width"] / 2),
            itemObjects[item]["y"] + math.ceil(itemObjects[item]["height"] / 2),
        )


def deleteItem(item: str) -> None:
    del itemObjects[item]


# Functions: Key Binds
def updateKeyboardBindStatus(keysBinds: list = ["all"]) -> None:
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


def getKeyboardBindStatus(keyBind: str, update: bool = False) -> bool:
    if update == True:
        updateKeyboardBindStatus(keysBinds=[keyBind])
    return keyBindsStatus[keyBind]["state"]


def copyKeyboardBindStatus(update: bool = False) -> dict:
    if update == True:
        updateKeyboardBindStatus()
    return copy.deepcopy(getKeyboardBindStatus)


def changeKeyboardBind(keyBind: str, newKey: str) -> None:
    keyBindsStatus[keyBind]["keybind"] = newKey


# Functions: Mouse Binds
def onMove(x: int, y: int):
    with threadingLock:
        mouseStatus["absolute position"] = (x, y)


def onClick(x: int, y: int, button: object, pressed: bool):
    with threadingLock:
        mouseStatus["absolute position"] = (x, y)
        if str(button) == "Button.left":
            mouseStatus["left button"] = pressed
        if str(button) == "Button.right":
            mouseStatus["right button"] = pressed
        if str(button) == "Button.middle":
            mouseStatus["middle button"] = pressed


def onScroll(x: int, y: int, dx: int, dy: int):
    with threadingLock:
        mouseStatus["absolute position"] = (x, y)
        mouseStatus["scroll x"] = dx
        mouseStatus["scroll y"] = dy


def startAsynchronousMouseListener() -> mouse.Listener:
    global mouseListener
    mouseListener = mouse.Listener(on_move=onMove, on_click=onClick, on_scroll=onScroll)
    mouseListener.start()
    return mouseListener


def copyMouseStatus(resetMouseStatusAfterCopy: bool = False) -> dict:
    with threadingLock:
        global mouseStatusCopy
        mouseStatusCopy = copy.deepcopy(mouseStatus)
        if resetMouseStatusAfterCopy == True:
            # mouseStatus["left button"] = False
            # mouseStatus["right button"] = False
            # mouseStatus["middle button"] = False
            mouseStatus["scroll x"] = 0
            mouseStatus["scroll y"] = 0
    mouseStatusCopy["position"] = getRelativeMouseCoords(
        mouseStatusCopy["absolute position"]
    )
    return mouseStatusCopy


def resetMouseStatus(onlyResetScroll=False) -> None:
    with threadingLock:
        if onlyResetScroll == True:
            mouseStatus["left button"] = False
            mouseStatus["right button"] = False
            mouseStatus["middle button"] = False
        mouseStatus["scroll x"] = 0
        mouseStatus["scroll y"] = 0


def getRelativeMouseCoords(
    absoluteMouseCoords: tuple | None = None,
) -> tuple:
    rect = RECT()
    DMWA_EXTENDED_FRAME_BOUNDS = 9
    dwmapi.DwmGetWindowAttribute(
        HWND(hwnd),
        DWORD(DMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect),
    )
    if absoluteMouseCoords == None:
        absoluteMouseCoords = mouseStatusCopy["absolute position"]
    relativeMouseCoords = (
        win32gui.ScreenToClient(hwnd, absoluteMouseCoords)[0]
        + ctypes.windll.user32.GetSystemMetrics(5) * 2,
        win32gui.ScreenToClient(hwnd, absoluteMouseCoords)[1]
        - ctypes.windll.user32.GetSystemMetrics(4) * 2,
    )
    if checkIfFullScreen() == True:
        return (
            math.floor(relativeMouseCoords[0] / characterSize[0]) - 1,
            math.floor(relativeMouseCoords[1] / characterSize[1]) + 2,
        )
    elif checkIfFullScreen() == "maximized":
        return (
            math.floor(relativeMouseCoords[0] / characterSize[0]) - 1,
            math.floor(relativeMouseCoords[1] / characterSize[1] + 0.5),
        )
    else:
        return (
            math.floor(relativeMouseCoords[0] / characterSize[0]) - 1,
            math.floor(relativeMouseCoords[1] / characterSize[1]),
        )


# Functions: Debug Messages
def addDebugMessage(message: any) -> None:
    debugMessages.append(
        "".join(
            ["> ", time.strftime("%H:%M:%S", time.localtime()), " | ", str(message)]
        )
    )


def clearDebugMessages() -> None:
    global debugMessages
    debugMessages = []


def removeDebugMessage(position: int, firstAdded: bool = True) -> None:
    if firstAdded == True:
        debugMessages[position].pop()
    else:
        debugMessages[len(debugMessages) - position].pop()


def renderDebugMessages(displayMessageLimit: int = 5) -> None:
    if debugMode == True:
        for row in range(min(displayMessageLimit, len(debugMessages))):
            renderLiteralItem(
                debugMessages[len(debugMessages) - 1 - row],
                yBias=-1 * row,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )
        if len(debugMessages) - displayMessageLimit == 1:
            renderLiteralItem(
                "".join(
                    [
                        "> There is 1 more debug message",
                    ],
                ),
                yBias=-1 * displayMessageLimit,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )
        elif len(debugMessages) > displayMessageLimit:
            renderLiteralItem(
                "".join(
                    [
                        "> There are ",
                        str(len(debugMessages) - displayMessageLimit),
                        " more debug messages",
                    ],
                ),
                yBias=-1 * displayMessageLimit,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )


def setDebugMode(state: bool) -> None:
    global debugMode
    debugMode = state


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


def generateLine(
    point1: tuple, point2: tuple, character: str = "#", backgroundCharacter: str = "š"
) -> str:
    point1X, point1Y = point1
    point2X, point2Y = point2
    width = abs(point2X - point1X)
    height = abs(point2Y - point1Y)
    minX = min(point1X, point2X)
    minY = min(point1Y, point2Y)
    sx1, sy1 = point1X - minX, point1Y - minY
    sx2, sy2 = point2X - minX, point2Y - minY
    canvas = [[backgroundCharacter for _ in range(width+1)] for _ in range(height+1)]
    dx = abs(sx2 - sx1)
    dy = abs(sy2 - sy1)
    x, y = sx1, sy1
    sx = 1 if sx1 < sx2 else -1
    sy = 1 if sy1 < sy2 else -1
    err = dx - dy
    while not (x == sx2 and y == sy2):
        canvas[y][x] = character
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return "\n".join("".join(row) for row in canvas)


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
