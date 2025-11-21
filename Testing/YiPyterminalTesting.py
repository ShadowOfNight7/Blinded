# import Assets.YiPyterminal as YiPyterminal

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


def generateLine(p1: tuple, p2: tuple, char: str):
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1
    line = [[" " for _ in range(dx)] for _ in range(dy)]
    if abs(dx) >= abs(dy):
        step = 1 if dx > 0 else -1
        for x in range(x1, x2, step):
            y = y1 + dy * ((x + 0.5 - x1) / dx)
            y = round(y)
            if 0 <= y < len(line) and 0 <= x < len(line[0]):
                line[y][x] = char
                if 0 <= x - step < len(line[0]):
                    line[y][x - step] = char
    else:
        step = 1 if dy > 0 else -1
        for y in range(y1, y2, step):
            x = x1 + dx * ((y + 0.5 - y1) / dy)
            x = round(x)
            if 0 <= y < len(line) and 0 <= x < len(line[0]):
                line[y][x] = char
                if 0 <= y - step < len(line):
                    line[y - step][x] = char

    return "\n".join("".join(row) for row in line)


print(1)
print(generateLine((2, 0), (20, 10), "*"))
print(2)
