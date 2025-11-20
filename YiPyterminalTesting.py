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
print(YiPyterminal.items["example target"])
YiPyterminal.renderItem("example target")
YiPyterminal.renderScreen()
print(YiPyterminal.lettersToRender)
print(YiPyterminal.screenRender)
YiPyterminal.displayScreen()
