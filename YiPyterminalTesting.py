import Assets.YiPyterminal as YiPyterminal

# print(YiPyterminal.FPS)
# print(
#     YiPyterminal.items["example target"]["animation frames"][
#         YiPyterminal.items["example target"]["current frame"]
#     ]
# )
# YiPyterminal.addLetter((0, 0), "#")
# print(YiPyterminal.lettersToRender)
# YiPyterminal.clearLetters()
# print(YiPyterminal.lettersToRender)
# x, y = (1, 2)
# print(x)
# print(y)


# print(YiPyterminal.items["example target"])
# YiPyterminal.renderItem("example target")
# YiPyterminal.renderScreen()
# print(YiPyterminal.lettersToRender)
# print(YiPyterminal.screenRender)
# YiPyterminal.displayScreen()

# x = YiPyterminal.generateLine((0, 0), (27, 18))
# for i in x.splitlines():
#     print(i)
# exit()

(9, 19)
YiPyterminal.initializeTerminal(repetitions=1)

YiPyterminal.createItem(
    "line1",
    [
        YiPyterminal.generateLine((0, 0), (20, 10)),
        YiPyterminal.generateLine((0, 0), (10, 10)),
        YiPyterminal.generateLine((0, 0), (5, 5)),
    ],
    xBias=0,
    yBias=0,
)
YiPyterminal.startAsynchronousMouseListener()
while True:
    YiPyterminal.copyMouseStatus(resetMouseStatusAfterCopy=True)
    YiPyterminal.addDebugMessage(YiPyterminal.mouseStatusCopy)
    # print(YiPyterminal.mouseStatusCopy)
    if YiPyterminal.checkItemIsClicked("line1"):
        YiPyterminal.updateItemFrame("line1", 1)
    if YiPyterminal.checkItemIsClicked("line1", button="right"):
        YiPyterminal.updateItemFrame("line1", 0)
    if YiPyterminal.getKeyboardBindStatus("up", update=True) == True:
        YiPyterminal.updateItemFrame("line1", 2)
    YiPyterminal.renderItem("line1")
    YiPyterminal.renderScreen()
    YiPyterminal.displayScreen()
