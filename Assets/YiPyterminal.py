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
screenWidthLimit = 156
screenHeightLimit = 41
lettersToRender = {}
screenRender = []
debugMessages = []
itemObjects = CodingAssets.itemObjects
keyBindsStatus = CodingAssets.keyBindsStatus
mouseStatus = CodingAssets.mouseStatus
# Variables: Other
screenWidth = os.get_terminal_size().columns
screenHeight = os.get_terminal_size().lines
debugMode = True
threadingLock = threading.Lock()
endEscapeCode = CodingAssets.endEscapeCode
styleCodes = CodingAssets.styleCodes
colorCodes = CodingAssets.colorCodes
assets = CodingAssets.assets


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
    global characterSize
    prepareTerminalInitialization()
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
    return (
        xAnchor + math.floor(longestRowLen / 2),
        yAnchor + math.floor(len(splitItem) / 2),
    )


def renderScreen(
    backgroundCharacter: str = " ",
    constantlyCheckScreenSize: bool = False,
    displayDebugMessages: bool = True,
) -> None:
    if constantlyCheckScreenSize == True:
        updateScreenSize()
    if displayDebugMessages == True:
        renderDebugMessages()
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
    isOverwriteExistingItem: bool = True,
    isUpdateItemSize: bool = True,
    isUpdateItemLocation: bool = True,
) -> None:
    if isOverwriteExistingItem == False:
        if name in itemObjects:
            return None
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
    if isUpdateItemSize == True:
        updateItemSize(name)
    if isUpdateItemLocation == True:
        updateItemLocation(name)


def renderItem(
    item: str,
    emptySpaceLetter: str = "š",
    xBias: str = 0,
    yBias: str = 0,
    createItemIfNotExists: bool = False,
    createItemArgs: dict | None = None,
    screenLimits: None | tuple = (screenWidthLimit, screenHeightLimit),
    screenLimitsBias: tuple = (0, 0),
) -> None:
    if item not in itemObjects and createItemIfNotExists == True:
        if createItemArgs == None:
            createItemArgs = {}
        createItem(item, **createItemArgs)
    updateItemLocation(item)
    splitItem = itemObjects[item]["animation frames"][
        itemObjects[item]["current frame"]
    ].splitlines()
    for rowNum in range(len(splitItem)):
        for columnNum in range(len(splitItem[rowNum])):
            coords = (
                columnNum + xBias + itemObjects[item]["x"],
                rowNum + yBias + itemObjects[item]["y"],
            )
            if splitItem[rowNum][columnNum] != emptySpaceLetter:
                if screenLimits != None:
                    if (
                        not (math.ceil((screenWidth - 1) / 2) - screenLimits[0] // 2)
                        + screenLimitsBias[0]
                        <= coords[0]
                        <= (math.ceil((screenWidth - 1) / 2) + screenLimits[0] // 2)
                        + screenLimitsBias[0]
                    ) or (
                        not (math.ceil((screenHeight - 1) / 2) - screenLimits[1] // 2)
                        + screenLimitsBias[1]
                        <= coords[1]
                        <= (math.ceil((screenHeight - 1) / 2) + screenLimits[1] // 2)
                        + screenLimitsBias[1]
                    ):
                        continue
                addLetter(
                    coords,
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
    item: str,
    button: str = "left",
    onlyCheckRelease: bool = False,
    mouseCoords: tuple | None = None,
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
            try:
                if itemFrame[relativeY][relativeX] != "š":
                    if button == "left":
                        return mouseStatusCopy[
                            (
                                "left button"
                                if onlyCheckRelease == False
                                else "left button release"
                            )
                        ]
                    elif button == "right":
                        return mouseStatusCopy[
                            (
                                "right button"
                                if onlyCheckRelease == False
                                else "right button release"
                            )
                        ]
                    elif button == "middle":
                        return mouseStatusCopy[
                            (
                                "middle button"
                                if onlyCheckRelease == False
                                else "middle button release"
                            )
                        ]
                    else:
                        addDebugMessage("Invalid button input in checkItemIsClicked()")
                else:
                    return False
            except Exception as e:
                print(
                    str(e)
                    + " "
                    + str(itemFrame)
                    + " "
                    + str(mouseCoords[0])
                    + " "
                    + str(itemTopLeftX)
                )
                exit()
        if button == "left":
            return mouseStatusCopy[
                "left button" if onlyCheckRelease == False else "left button release"
            ]
        elif button == "right":
            return mouseStatusCopy[
                "right button" if onlyCheckRelease == False else "right button release"
            ]
        elif button == "middle":
            return mouseStatusCopy[
                (
                    "middle button"
                    if onlyCheckRelease == False
                    else "middle button release"
                )
            ]


def checkItemIsHovered(item: str, mouseCoords: tuple | None = None) -> bool:
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
                return True
            else:
                return False
        return True
    return False


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
            anchorX, anchorY = screenWidth - 1, 0
        elif parentAnchor == "bottom left":
            anchorX, anchorY = 0, screenHeight - 1
        elif parentAnchor == "bottom right":
            anchorX, anchorY = screenWidth - 1, screenHeight - 1
        elif parentAnchor == "center" or parentAnchor == "centre":
            anchorX, anchorY = math.ceil((screenWidth - 1) / 2), math.ceil(
                (screenHeight - 1) / 2
            )
        elif parentAnchor == "top center" or parentAnchor == "top centre":
            anchorX, anchorY = math.ceil((screenWidth - 1) / 2), 0
        elif parentAnchor == "bottom center" or parentAnchor == "bottom centre":
            anchorX, anchorY = math.ceil((screenWidth - 1) / 2), screenHeight - 1
        elif parentAnchor == "left center" or parentAnchor == "left centre":
            anchorX, anchorY = 0, math.ceil((screenHeight - 1) / 2)
        elif parentAnchor == "right center" or parentAnchor == "right centre":
            anchorX, anchorY = screenWidth - 1, math.ceil((screenHeight - 1) / 2)
        else:
            addDebugMessage(
                "".join(["Invalid input for parentAnchor in addItem():", parentAnchor])
            )
            return
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
        elif parentAnchor == "top center" or parentAnchor == "top centre":
            anchorX, anchorY = getTopCenter(parentObject)
        elif parentAnchor == "bottom center" or parentAnchor == "bottom centre":
            anchorX, anchorY = getBottomCenter(parentObject)
        elif parentAnchor == "left center" or parentAnchor == "left centre":
            anchorX, anchorY = getLeftCenter(parentObject)
        elif parentAnchor == "right center" or parentAnchor == "right centre":
            anchorX, anchorY = getRightCenter(parentObject)
        else:
            addDebugMessage(
                "".join(["Invalid input for parentAnchor in addItem():", parentAnchor])
            )
            return
    else:

        addDebugMessage(
            "".join(["Invalid input for parentObject in addItem():", parentObject])
        )
        return
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
        anchorX -= width - 1
        anchorY -= 0
    elif childAnchor == "bottom left":
        anchorX -= 0
        anchorY -= height - 1
    elif childAnchor == "bottom right":
        anchorX -= width - 1
        anchorY -= height - 1
    elif childAnchor == "center" or childAnchor == "centre":
        anchorX -= math.ceil((width - 1) / 2)
        anchorY -= math.ceil((height - 1) / 2)
    elif childAnchor == "top center" or childAnchor == "top centre":
        anchorX -= math.ceil((width - 1) / 2)
        anchorY -= 0
    elif childAnchor == "bottom center" or childAnchor == "bottom centre":
        anchorX -= math.ceil((width - 1) / 2)
        anchorY -= height - 1
    elif childAnchor == "left center" or childAnchor == "left centre":
        anchorX -= 0
        anchorY -= math.ceil((height - 1) / 2)
    elif childAnchor == "right center" or childAnchor == "right centre":
        anchorX -= width - 1
        anchorY -= math.ceil((height - 1) / 2)
    else:
        addDebugMessage(
            "".join(["Invalid input for childAnchor in addItem():", childAnchor])
        )
        return
    if childObject != None and isChildObjectLiteralStr == False:
        anchorX += itemObjects[childObject]["x bias"]
        anchorY += itemObjects[childObject]["y bias"]
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


def changeCurrentItemFrame(item: str, newFrame: int) -> None:
    itemObjects[item]["current frame"] = newFrame
    updateItemSize(item)
    updateItemLocation(item)


def changeItemFrameContent(
    item: str,
    newFrameContents: str | list,
    selectedFrame: int = 0,
    specificFrame: bool = False,
) -> None:
    if specificFrame == False:
        if newFrameContents is str:
            itemObjects[item]["animation frame"][selectedFrame] = newFrameContents
        else:
            addDebugMessage(
                "changeItemFrameContent() received incorrect type for variable newFrameContents."
            )
    elif specificFrame == True:
        if newFrameContents is list:
            itemObjects[item]["animation frame"] = newFrameContents
        else:
            addDebugMessage(
                "changeItemFrameContent() received incorrect type for variable newFrameContents."
            )


def moveItem(item: str, x: int = 0, y: int = 0) -> None:
    itemObjects[item]["x bias"] += x
    itemObjects[item]["y bias"] += y
    updateItemLocation(item)


def getAnchor(item: str, anchor: str) -> tuple:
    if anchor == "top left":
        return getTopLeft(item)
    elif anchor == "top right":
        return getTopRight(item)
    elif anchor == "bottom left":
        return getBottomLeft(item)
    elif anchor == "bottom right":
        return getBottomRight(item)
    elif anchor == "center" or anchor == "centre":
        return getCenter(item)
    elif anchor == "top center" or anchor == "top centre":
        return getTopCenter(item)
    elif anchor == "bottom center" or anchor == "bottom centre":
        return getBottomCenter(item)
    elif anchor == "left center" or anchor == "left centre":
        return getLeftCenter(item)
    elif anchor == "right center" or anchor == "right centre":
        return getRightCenter(item)
    else:
        addDebugMessage("".join(["Invalid input for anchor in getAnchor():", anchor]))


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
            itemObjects[item]["x"] + math.ceil((itemObjects[item]["width"] - 1) / 2),
            itemObjects[item]["y"] + math.ceil((itemObjects[item]["height"] - 1) / 2),
        )


def getTopCenter(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"] + math.ceil((itemObjects[item]["width"] - 1) / 2),
            itemObjects[item]["y"],
        )


def getBottomCenter(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"] + math.ceil((itemObjects[item]["width"] - 1) / 2),
            itemObjects[item]["y"] + itemObjects[item]["height"] - 1,
        )


def getLeftCenter(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"],
            itemObjects[item]["y"] + math.ceil((itemObjects[item]["height"] - 1) / 2),
        )


def getRightCenter(item: str) -> tuple:
    if item in itemObjects:
        return (
            itemObjects[item]["x"] + itemObjects[item]["width"] - 1,
            itemObjects[item]["y"] + math.ceil((itemObjects[item]["height"] - 1) / 2),
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
            if pressed == False:
                if mouseStatus["left button"] == True:
                    mouseStatus["left button release"] = True
            mouseStatus["left button"] = pressed
        if str(button) == "Button.right":
            if pressed == False:
                if mouseStatus["right button"] == True:
                    mouseStatus["right button release"] = True
            mouseStatus["right button"] = pressed
        if str(button) == "Button.middle":
            if pressed == False:
                if mouseStatus["middle button"] == True:
                    mouseStatus["middle button release"] = True
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
            mouseStatus["left button release"] = False
            mouseStatus["right button release"] = False
            mouseStatus["middle button release"] = False
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
    borderCharacter: dict = {"top": "-", "bottom": "-", "left": "|", "right": "|"},
    cornerCharacter: dict = {
        "top left": "┌",
        "top right": "┐",
        "bottom left": "└",
        "bottom right": "┘",
    },
    padding: dict = {"top": 0, "bottom": 0, "left": 1, "right": 1},
    paddingCharacter: str = " ",
    lineAdjustmentFunction: str = "middle",
) -> str:
    lines = ["" for _ in range(padding["top"])]
    lines.extend(text.splitlines())
    lines.extend(["" for _ in range(padding["bottom"])])
    maxLen = max(len(line) for line in lines)
    innerWidth = maxLen + padding["left"] + padding["right"]
    borderedLines = []
    if top:
        borderedLines.append(
            (cornerCharacter["top left"] if left else "")
            + str(borderCharacter["top"]) * innerWidth
            + (cornerCharacter["top right"] if right else "")
        )
    for line in lines:
        if lineAdjustmentFunction == "left":
            paddedLine = line.ljust(maxLen, paddingCharacter)
        elif lineAdjustmentFunction == "right":
            paddedLine = line.rjust(maxLen, paddingCharacter)
        else:
            paddedLine = line.center(maxLen, paddingCharacter)
        borderedLine = ""
        if left:
            borderedLine += (
                str(borderCharacter["left"]) + paddingCharacter * padding["left"]
            )
        borderedLine += paddedLine
        if right:
            borderedLine += paddingCharacter * padding["right"] + str(
                borderCharacter["right"]
            )
        borderedLines.append(borderedLine)
    if bottom:
        borderedLines.append(
            (cornerCharacter["bottom left"] if left else "")
            + str(borderCharacter["bottom"]) * innerWidth
            + (cornerCharacter["bottom right"] if right else "")
        )
    return "\n".join(borderedLines)


def generateLine(
    point1: tuple, point2: tuple, character: str = "#", backgroundCharacter: str = "š"
) -> str:
    point1X, point1Y = point1
    point2X, point2Y = point2
    width = abs(point2X - point1X) + 1
    height = abs(point2Y - point1Y) + 1
    minX = min(point1X, point2X)
    minY = min(point1Y, point2Y)
    sx1, sy1 = point1X - minX, point1Y - minY
    sx2, sy2 = point2X - minX, point2Y - minY
    canvas = [[backgroundCharacter for _ in range(width)] for _ in range(height)]
    dx = abs(sx2 - sx1)
    dy = abs(sy2 - sy1)
    x, y = sx1, sy1
    sx = 1 if sx1 < sx2 else -1
    sy = 1 if sy1 < sy2 else -1
    err = dx - dy
    while True:
        canvas[y][x] = character
        if x == sx2 and y == sy2:
            break
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
