import Assets.YiPyterminal as YiPyterminal
import time

# exit()

(9, 19)
YiPyterminal.initializeTerminal(repetitions=1)
YiPyterminal.startAsynchronousMouseListener()
while True:
    YiPyterminal.renderItem(
        "line1",
        createItemIfNotExists=True,
        createItemArgs={
            "animationFrames": [
                YiPyterminal.generateLine((0, 0), (20, 10)),
                YiPyterminal.generateLine((0, 0), (10, 10)),
                YiPyterminal.generateLine((0, 0), (5, 5)),
                YiPyterminal.generateLine((5, 0), (5, 5)),
            ],
            "xBias": 0,
            "yBias": 0,
            "parentAnchor": "center",
            "childAnchor": "center",
        },
    )
    YiPyterminal.copyMouseStatus(resetMouseStatusAfterCopy=True)
    # YiPyterminal.addDebugMessage(YiPyterminal.mouseStatusCopy)
    YiPyterminal.addDebugMessage(YiPyterminal.itemObjects["line1"])
    # print(YiPyterminal.mouseStatusCopy)
    if YiPyterminal.checkItemIsClicked("line1"):
        YiPyterminal.changeCurrentItemFrame("line1", 1)
    if YiPyterminal.checkItemIsClicked("line1", button="right"):
        YiPyterminal.changeCurrentItemFrame("line1", 0)
    if YiPyterminal.getKeyboardBindStatus("up", update=True) == True:
        YiPyterminal.changeCurrentItemFrame("line1", 2)
    if YiPyterminal.getKeyboardBindStatus("down", update=True) == True:
        YiPyterminal.changeCurrentItemFrame("line1", 3)
    # YiPyterminal.renderItem("line1")
    YiPyterminal.renderScreen()
    YiPyterminal.displayScreen()
