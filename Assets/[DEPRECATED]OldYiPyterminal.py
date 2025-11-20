from pynput import mouse
import keyboard
import threading
import math
import time
import sys
import os
import random

playerX = 10
playerY = 10
xSpeed = 0.18 * 3
ySpeed = 0.1 * 3
diag = math.sqrt((ySpeed**2) + (xSpeed**2))
assets = {
    "bars": """ HP: 75/100 | >===============-----< 
 Mana: 50/100 | >==========----------< """,
    "numbers": "12345678901234567890123456789012345678901234567890",
    "crosshair": """ššš|ššš
---+---
ššš|ššš
""",
    "background": R"""|--___                                                                                                                                                ___--|
|╔####¯¯---___                                                                                                                                ___---¯¯╔═══╗|
|╠############¯¯--___                                                                                                                  ___--¯¯╔═══╦═══╣\╔═╣|
|╠###################¯¯---________________________________________________________________________________________________________---¯¯╔══╦═══╣\╔═╩═╦═╩═╣\╣|
|╠#########################╗|╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦╗|╔═╦═══╦╝\╔╩═╦═╩═╣\╔═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦╝\╔╩═╦═╩═╣\╔╦╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩══╣|╠═╦═╩═╦═╩═╦╝╔═══╦═╩═╣╚═╔╬═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦══╣|╠═╩═╦═╩═╦═╩═╣\╔═╩═╦═╩═╦╝╚═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╣╔╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩╝║\╔═╩═╦═╩═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╣\╔╦╩═╦═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣╚═╦╩═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╗╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╝\╔╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╩╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═__________________________________________╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═| ▄                                    ▄ |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   \-\----------------------------/-/   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═|   | \-\                      /-/   |   |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   |  \-\                   /-/     |   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═|   |     \-\              /-/       |   |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   |       \-\          /-/         |   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═|   |         \-\      /-/           |   |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   |           \-\  /-/             |   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═|   |            \/-/                |   |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠#########################╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   |            /-/\-\              |   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠#########################╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═|   |         /-/      \-\           |   |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠#########################╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   |       /-/          \-\         |   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠#########################╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═|   |     /-/              \-\       |   |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠#########################╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   |   /-/                  \-\     |   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠#########################╣|
|╠#########################╣|╠═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═|   | /-/                       \-\  |   |╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦╣|╠#########################╣|
|╠#########################╣|╠═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═|   /-/                            \-\   |╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩═╦═╩╣|╠═══╦══╗##################╣|
|╠#########################╝|╚═╩═══╩═══╩═══╩═══╩═══╩═══╩═| ▀ |                                | ▀ |╩═══╩═══╩═══╩═══╩═══╩═══╩══╝|╚═══╩╗#╚═══════╗##########╣|
|╠#####################__---¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯---__╚═══════╗#╚═══════╗##╣|
|╠#############___--¯¯¯      ¯¯¯¯¯   ____            ¯¯¯¯¯¯          ________                   ¯¯¯¯¯¯¯         ____                 ¯¯¯--___╚═══════╗#╚══╣|
|╚#####___--¯¯¯           ___                       __                            ¯¯¯¯¯¯                _______              ¯¯¯¯     ___    ¯¯¯--___╚════╝|
|__--¯¯                              ¯¯¯¯¯¯                                     ______                                     ____                      ¯¯--__|""",
}


class YiPyterminal:
    """
    Letter: a single "pixel" on the terminal screen.
    Item: a group of letters in a docstring.
    Whitespace: In an item it represents a whitespace.
    Empty-space: In an item it is designated as "š" and will leave the location empty.
    For example:
    HP: 75/100 | >===============-----<
    Mana: 50/100 | >==========----------<"""

    class Item:
        itemCount = 0

        def __init__(
            self,
            spriteSheet: list,
            # hitboxSheet: list | None = None,
            xBias=0,
            yBias=0,
            isButton=False,
            isVisible=False,
            isHibernation=True,
            parentObject="screen",
            parentAnchor="top left",
            childAnchor="top left",
            isButtonHitboxVisible=False,
            hitboxColor="bright cyan",
            hoverColor="bright blue",
            clickColor="blue",
        ):
            self.__class__.itemCount += 1
            self.spriteSheet = spriteSheet
            # self.hitboxSheet = hitboxSheet
            self.spriteSheetFrame = 0
            self.xBias = xBias
            self.yBias = yBias
            self.isVisible = isVisible
            # self.isHibernation = isHibernation
            self.isButton = isButton
            self.isButtonHitboxVisible = isButtonHitboxVisible
            self.isClick = False
            self.isHover = False
            self.hitboxColor = hitboxColor
            self.hoverColor = hoverColor
            self.clickColor = clickColor
            self.parentObject = parentObject
            self.parentAnchor = parentAnchor
            self.childAnchor = childAnchor
            self.updateDimensions()
            self.updateLocation()

        @classmethod
        def getItemCount(cls):
            return cls.getItemCount

        def updateDimensions(self):
            processedSpriteSheetFrame = self.spriteSheet[
                self.spriteSheetFrame
            ].splitlines()
            self.height = len(processedSpriteSheetFrame)
            self.width = 0
            for row in range(self.height):
                if len(processedSpriteSheetFrame[row]) > self.width:
                    self.width = len(processedSpriteSheetFrame[row])

        def display(self, overwriteIsVisible=False):
            if overwriteIsVisible == True:
                self.isVisible = True
            if self.isVisible == True:
                pyterm.addItem(
                    self.spriteSheet[self.spriteSheetFrame],
                    self.absoluteX,
                    self.absoluteY,
                )

        def move(self, x=0, y=0, absolute=False):
            pyterm.addDebugMessage("move method requires updating")
            return ""
            if absolute == True:
                self.xBias = x
                self.yBias = y
            else:
                self.xBias += x
                self.yBias += y

        def updateLocation(self):
            if self.parentObject == "screen":
                if self.parentAnchor == "top left":
                    absoluteX, absoluteY = 0, 0
                elif self.parentAnchor == "top right":
                    absoluteX, absoluteY = pyterm.screenWidth, 0
                elif self.parentAnchor == "bottom left":
                    absoluteX, absoluteY = 0, pyterm.screenHeight
                elif self.parentAnchor == "bottom right":
                    absoluteX, absoluteY = pyterm.screenWidth, pyterm.screenHeight
                elif self.parentAnchor == "center" or self.parentAnchor == "centre":
                    absoluteX, absoluteY = math.ceil(pyterm.screenWidth / 2), math.ceil(
                        pyterm.screenHeight / 2
                    )
                else:
                    pyterm.addDebugMessage(
                        "".join(
                            [
                                "Invalid input for self.parentAnchor in updateLocation():",
                                self.parentAnchor,
                            ]
                        )
                    )
            else:
                if self.parentAnchor == "top left":
                    absoluteX, absoluteY = self.parentObject.topLeft
                elif self.parentAnchor == "top right":
                    absoluteX, absoluteY = self.parentObject.topRight
                elif self.parentAnchor == "bottom left":
                    absoluteX, absoluteY = self.parentObject.bottomLeft
                elif self.parentAnchor == "bottom right":
                    absoluteX, absoluteY = self.parentObject.bottomRight
                elif self.parentAnchor == "center" or self.parentAnchor == "centre":
                    absoluteX, absoluteY = self.parentObject.center
                else:
                    pyterm.addDebugMessage(
                        "".join(
                            [
                                "Invalid input for self.parentAnchor in updateLocation():",
                                self.parentAnchor,
                            ]
                        )
                    )
            if self.childAnchor == "top left":
                absoluteY -= 0
                absoluteX -= 0
            elif self.childAnchor == "top right":
                absoluteX -= self.width
                absoluteY -= 0
            elif self.childAnchor == "bottom left":
                absoluteX -= 0
                absoluteY -= self.height
            elif self.childAnchor == "bottom right":
                absoluteX -= self.width
                absoluteY -= self.height
            elif self.childAnchor == "center" or self.childAnchor == "centre":
                absoluteX -= math.ceil(self.width / 2)
                absoluteY -= math.ceil(self.height / 2)
            else:
                pyterm.addDebugMessage(
                    "".join(
                        [
                            "Invalid input for self.childAnchor in updateLocation():",
                            self.childAnchor,
                        ]
                    )
                )
            absoluteX += self.xBias
            absoluteY += self.yBias
            self.absoluteX = absoluteX
            self.absoluteY = absoluteY

        def changeAnchors(
            self,
            parentObject: str | object | None = None,
            parentAnchor: str | None = None,
            childAnchor: str | None = None,
        ):
            if parentObject != None:
                self.parentObject = parentObject
            if parentAnchor != None and parentAnchor in [
                "top left",
                "top right",
                "bottom left",
                "bottom right",
                "center",
                "centre",
            ]:
                self.parentAnchor = parentAnchor
            if childAnchor != None and childAnchor in [
                "top left",
                "top right",
                "bottom left",
                "bottom right",
                "center",
                "centre",
            ]:
                self.childAnchor = childAnchor

        @property
        def x(self):
            return self.absoluteX

        @property
        def y(self):
            return self.absoluteY

        @property
        def topLeft(self) -> tuple:
            return (self.absoluteX, self.absoluteY)

        @property
        def topRight(self) -> tuple:
            return (self.absoluteX + self.width - 1, self.absoluteY)

        @property
        def bottomLeft(self) -> tuple:
            return (self.absoluteX, self.absoluteY + self.height - 1)

        @property
        def bottomRight(self) -> tuple:
            return (self.absoluteX + self.width - 1, self.absoluteY + self.height - 1)

        @property
        def center(self) -> tuple:
            return (
                math.ceil(self.absoluteX + self.width / 2),
                math.ceil(self.absoluteY + self.height / 2),
            )

        @property
        def centre(self) -> tuple:
            return self.center

        def remove(self):
            self.__class__.itemCount -= 1
            del self

    def __init__(self):
        """Defining varibles, such as screen size, fps, etc."""
        self.screenWidth = os.get_terminal_size().columns
        self.screenHeight = os.get_terminal_size().lines
        self.constantlyCheckScreenSize = True
        self.lettersToRender = {
            (10, 12): "O",
            (9, 12): "\\",
            (11, 12): "/",
        }
        self.screenRender = []
        self.fps = 60
        self.debugMessages = []
        self.keyBindsStatus = {
            "up": {"state": False, "keybind": "w"},
            "left": {"state": False, "keybind": "a"},
            "down": {"state": False, "keybind": "s"},
            "right": {"state": False, "keybind": "d"},
        }
        self.mouseStatus = {
            "absolute position": (0, 0),
            "left button": False,
            "right button": False,
            "middle button": False,
            "scroll x": 0,
            "scroll y": 0,
        }
        self.lock = threading.Lock()
        self.endEscapeCode = "\033[0m"
        self.styleCodes = {
            "reset": 0,
            "normal": 0,
            "bold": 1,
            "dim": 2,
            "italic": 3,
            "underline": 4,
            "blink": 5,
            "inverse": 7,
            "reverse": 7,
            "invisible": 8,
            "hidden": 8,
            "strikethrough": 9,
        }
        self.colorCodes = {
            "Black": 30,
            "Red": 31,
            "Green": 32,
            "Yellow": 33,
            "Blue": 34,
            "Magenta": 35,
            "Cyan": 36,
            "White": 37,
        }

    # Controls the printing of errors to prevent breaking of UI
    # Arg message: the message which will be printed
    def addDebugMessage(self, message):
        self.debugMessages.append(
            "".join(["> ", time.strftime("%H:%M:%S", time.localtime()), " | ", message])
        )

    def clearDebugMessages(self):
        self.debugMessages = []

    def removeDebugMessage(self, position, firstAdded=True):
        if firstAdded == True:
            self.debugMessages[position].pop()
        else:
            self.debugMessages[len(self.debugMessages) - position].pop()

    def renderDebugMessages(self, messageLimit=5):
        for row in range(min(messageLimit, len(self.debugMessages))):
            self.addItem(
                self.debugMessages[len(self.debugMessages) - 1 - row],
                yBias=-1 * row,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )
        if len(self.debugMessages) - messageLimit == 1:
            self.addItem(
                "".join(
                    [
                        "> There is 1 more debug message",
                    ],
                ),
                yBias=-1 * messageLimit,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )
        elif len(self.debugMessages) > messageLimit:
            self.addItem(
                "".join(
                    [
                        "> There are ",
                        str(len(self.debugMessages) - messageLimit),
                        " more debug messages",
                    ],
                ),
                yBias=-1 * messageLimit,
                itemAnchor="bottom right",
                screenAnchor="bottom right",
            )

    # Adds a single letter into the dictionary of letters to be rendered
    # Not the recommended way to remove letters use removeLetter() instead
    # Arg coords: the key which the letter will be asigned to
    # Arg letter: the letter which will be assigned to the coords
    # Arg overwrite: allows the user to choose if they wish to allow overwrites
    def addLetter(self, coords: tuple, letter: str, overwrite=True):
        if overwrite == False:
            if coords in self.lettersToRender:
                self.addDebugMessage("You are trying to overwrite something")
        self.lettersToRender[coords] = letter

    # Removes all letters from dictionary of letters to be rendered
    def clearLetters(self):
        self.lettersToRender = {}

    # Removes both the key and value of a given position from the dictionary of letters to be rendered
    # Using this will prevent clashing with addLetter()'s overwrite protection function and prevents the breaking of UI
    # Arg coords: the key which along with its value will be removed
    def removeLetter(self, coords: tuple):
        del self.lettersToRender[coords]

    # Returns the value of a given key in the dictionary of letters to be rendered
    # Arg coords: the key which the value will be returned
    def getLetter(self, coords: tuple):
        return self.lettersToRender[coords]

    # Adds a border aroun
    @staticmethod
    def addBorder(
        text,
        top=True,
        bottom=True,
        left=True,
        right=True,
        borderCharacter="-",
        cornerCharacter="+",
    ):
        lines = text.splitlines()
        maxLen = max(len(line) for line in lines)
        borderedLines = []
        if top:
            borderedLines.append(
                (cornerCharacter if left else "")
                + (
                    borderCharacter
                    * (maxLen + (1 if right else 0) + (1 if left else 0))
                )
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
                + (
                    borderCharacter
                    * (maxLen + (1 if right else 0) + (1 if left else 0))
                )
                + (cornerCharacter if right else "")
            )
        return "\n".join(borderedLines)

    def addItem(
        self,
        item: str,
        xBias=0,
        yBias=0,
        screenAnchor="top left",
        itemAnchor="top left",
        emptySpaceLetter="š",
    ):

        splitItem = item.splitlines()
        longestRowLen = 0
        for rowNum in range(len(splitItem)):
            if len(splitItem[rowNum]) > longestRowLen:
                longestRowLen = len(splitItem[rowNum])
            splitItem[rowNum] = list(splitItem[rowNum])
        if screenAnchor == "top left":
            xAnchor, yAnchor = 0, 0
        elif screenAnchor == "top right":
            xAnchor, yAnchor = self.screenWidth, 0
        elif screenAnchor == "bottom left":
            xAnchor, yAnchor = 0, self.screenHeight
        elif screenAnchor == "bottom right":
            xAnchor, yAnchor = self.screenWidth, self.screenHeight
        elif screenAnchor == "center" or screenAnchor == "centre":
            xAnchor, yAnchor = math.ceil(self.screenWidth / 2), math.ceil(
                self.screenHeight / 2
            )
        else:
            self.addDebugMessage(
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
            self.addDebugMessage(
                "".join(["Invalid input for itemAnchor in addItem():", itemAnchor])
            )
        xAnchor += xBias
        yAnchor += yBias
        for rowNum in range(len(splitItem)):
            for columnNum in range(len(splitItem[rowNum])):
                if splitItem[rowNum][columnNum] != emptySpaceLetter:
                    self.addLetter(
                        (columnNum + xAnchor, rowNum + yAnchor),
                        splitItem[rowNum][columnNum],
                    )

    def checkScreenSize(self, override=False):
        if self.constantlyCheckScreenSize == True or override == True:
            self.screenWidth = os.get_terminal_size().columns
            self.screenHeight = os.get_terminal_size().lines

    def renderScreen(self):
        if self.constantlyCheckScreenSize == True:
            self.checkScreenSize()
        self.screenRender = [
            [" " for _ in range(self.screenWidth)] for _ in range(self.screenHeight)
        ]
        for row in range(self.screenHeight):
            for coords in self.lettersToRender:
                if coords[1] == row:
                    if 0 <= coords[0] < len(self.screenRender[row]):
                        self.screenRender[row][coords[0]] = self.lettersToRender[coords]
        for row in range(len(self.screenRender)):
            self.screenRender[row] = "".join(self.screenRender[row])

    def displayScreen(self, advanceMode=True, clearScreen=False):
        if clearScreen:
            os.system("cls")

        if advanceMode == True:
            sys.stdout.write("\033[H")
            for rowNum in range(len(self.screenRender)):
                sys.stdout.write(
                    f"\033[{rowNum+1};1f{''.join(self.screenRender[rowNum])}"
                )
                sys.stdout.write(f"\033[{self.screenHeight};{self.screenWidth}H")
                sys.stdout.flush()

        else:
            print(self.screenRender, end="")

    def updateKeys(self, keysBinds=["all"]):
        if keysBinds == ["all"]:
            for key in self.keyBindsStatus:
                self.keyBindsStatus[key]["state"] = keyboard.is_pressed(
                    self.keyBindsStatus[key]["keybind"]
                )
        elif keysBinds != [] and type(keysBinds) is list:
            for key in keysBinds:
                self.keyBindsStatus[key]["state"] = keyboard.is_pressed(
                    self.keyBindsStatus[key]["keybind"]
                )

    def getKeyBinds(self, keyBind: str, update=False) -> bool:
        if update == True:
            self.keyBindsStatus[keyBind]["state"] = keyboard.is_pressed(
                self.keyBindsStatus[keyBind]["keybind"]
            )
        return self.keyBindsStatus[keyBind]["state"]

    def onMove(self, x, y):
        with self.lock:
            self.mouseStatus["aboslute position"] = (x, y)

    def onClick(self, x, y, button, pressed):
        with self.lock:
            self.mouseStatus["aboslute position"] = (x, y)
            if str(button) == "Button.left":
                self.mouseStatus["left button"] = pressed
            if str(button) == "Button.right":
                self.mouseStatus["right button"] = pressed
            if str(button) == "Button.middle":
                self.mouseStatus["middle button"] = pressed

    def onScroll(self, x, y, dx, dy):
        with self.lock:
            self.mouseStatus["aboslute position"] = (x, y)
            self.mouseStatus["scroll x"] = dx
            self.mouseStatus["scroll y"] = dy

    @property
    def mouseInfo(self):
        return self.mouseStatus

    @property
    def mousePosition(self):
        return self.mouseStatus["aboslute position"]

    @property
    def mousePositionX(self):
        return self.mouseStatus["aboslute position"][0]

    @property
    def mousePositionY(self):
        return self.mouseStatus["aboslute position"][1]

    @property
    def leftMouseButton(self):
        return self.mouseStatus["left button"]

    @property
    def rightMouseButton(self):
        return self.mouseStatus["right button"]

    @property
    def middleMouseButton(self):
        return self.mouseStatus["middle button"]

    @property
    def mouseScroll(self):
        return (self.mouseStatus["scroll x"], self.mouseStatus["scroll y"])

    @property
    def mouseScrollX(self):
        return self.mouseStatus["scroll x"]

    @property
    def mouseScrollY(self):
        return self.mouseStatus["scroll y"]

    def style(
        self,
        text,
        styling: list = [],
        foreground=None,
        background=None,
        brightColors=False,
        start=0,
        end=-0,
    ):
        startEscapeCode = "\033["
        stylingAdded = []
        if styling == [] or ("normal" or "reset") in styling:
            "".join([startEscapeCode, "0;"])
        else:
            for style in styling:
                stylecode = self.styleCodes[style]
                if stylecode != stylingAdded:
                    "".join([startEscapeCode, str(stylecode), ";"])
                    stylingAdded.append(stylecode)

        if foreground != None:
            if foreground in self.colorCodes:
                if brightColors:
                    "".join(
                        [startEscapeCode, str(self.colorCodes[background] + 60), ";"]
                    )
                else:
                    "".join([startEscapeCode, str(self.colorCodes[foreground]), ";"])
        if background != None:
            if background in self.colorCodes:
                if brightColors:
                    "".join(
                        [
                            startEscapeCode,
                            str(self.colorCodes[background] + 70),
                            ";",
                        ]
                    )
                else:
                    "".join(
                        [startEscapeCode, str(self.colorCodes[background] + 10), ";"]
                    )
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
        processedString.insert(end, self.endEscapeCode)
        return "".join(processedString)


pyterm = YiPyterminal()
item = pyterm.Item(
    [
        pyterm.addBorder(
            pyterm.addBorder(assets["bars"]), top=False, right=False, left=False
        ),
    ],
    isVisible=True,
    isHibernation=False,
    xBias=0,
    yBias=0,
)
item2 = pyterm.Item(
    [
        pyterm.addBorder(assets["bars"]),
    ],
    isVisible=True,
    isHibernation=False,
    xBias=0,
    yBias=0,
    parentObject=item,
    parentAnchor="bottom right",
)
item.display()
item2.display()
pyterm.renderScreen()
pyterm.displayScreen()
print(item.topLeft)
print(item.height)
print(item.center)

print(item2.parentObject.topLeft)
print(item2.topLeft)
time.sleep(1111)

pyterm.addDebugMessage("example error 1")
pyterm.addDebugMessage("example error 2: blah blah blah")
pyterm.addDebugMessage("example error 3: smthing idk aaaaaaaaa")
pyterm.addDebugMessage("example error 4: adwwadaw")
pyterm.addDebugMessage("example error 5: blah blah")
pyterm.addDebugMessage("example error 6: CRITICAL ERROR (or smthing)")
while True:
    startTime = time.perf_counter()
    pyterm.clearLetters()
    pyterm.addItem(assets["background"], itemAnchor="center", screenAnchor="center")
    pyterm.addLetter((round(playerX), round(playerY)), "O")
    pyterm.addLetter((round(playerX) - 1, round(playerY)), "\\")
    pyterm.addLetter((round(playerX) + 1, round(playerY)), "/")
    pyterm.addItem(
        pyterm.addBorder(assets["bars"], top=False, left=False),
    )
    pyterm.addItem(
        pyterm.addBorder(assets["bars"], top=False, right=False),
        itemAnchor="top right",
        screenAnchor="top right",
    )
    pyterm.addItem(
        assets["numbers"],
        itemAnchor="bottom right",
        screenAnchor="bottom right",
    )
    pyterm.addItem(assets["crosshair"], itemAnchor="center", screenAnchor="center")

    pyterm.renderDebugMessages()
    # if pyterm.getKey("up") and pyterm.getKey("down"):
    #     pyterm.getKey("up"), pyterm.getKey("down") = False, False
    # if pyterm.getKey("left") and pyterm.getKey("right"):
    #     pyterm.getKey("left"), pyterm.getKey("right") = False, False
    pyterm.updateKeys()
    if pyterm.getKeyBinds("up") and pyterm.getKeyBinds("right"):
        playerX += diag
        playerY -= diag
    elif pyterm.getKeyBinds("up") and pyterm.getKeyBinds("left"):
        playerX -= diag
        playerY -= diag
    elif pyterm.getKeyBinds("down") and pyterm.getKeyBinds("left"):
        playerX -= diag
        playerY += diag
    elif pyterm.getKeyBinds("down") and pyterm.getKeyBinds("right"):
        playerX += diag
        playerY += diag
    elif pyterm.getKeyBinds("up"):
        playerY -= ySpeed
    elif pyterm.getKeyBinds("left"):
        playerX -= xSpeed
    elif pyterm.getKeyBinds("down"):
        playerY += ySpeed
    elif pyterm.getKeyBinds("right"):
        playerX += xSpeed
    if playerX > pyterm.screenWidth - 2:
        playerX = pyterm.screenWidth - 2
    elif 1 > playerX:
        playerX = 1
    if playerY > pyterm.screenHeight - 1:
        playerY = pyterm.screenHeight - 1
    elif 0 > playerY:
        playerY = 0
    pyterm.renderScreen()
    elapsedTime = time.perf_counter() - startTime
    if elapsedTime < (1 / pyterm.fps):
        time.sleep((1 / pyterm.fps) - elapsedTime)
    pyterm.displayScreen()
    # print("   ", pyterm.screenWidth)
    # print("   ", pyterm.screenHeight)


# def on_click(x, y, button, pressed):
#     if pressed:
#         print(f"Mouse clicked at ({x}, {y}) with {button}")
#     else:
#         print(f"Mouse released at ({x}, {y}) with {button}")


# with mouse.Listener(on_click=on_click) as listener:
#     listener.join()
