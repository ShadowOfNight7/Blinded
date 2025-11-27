import win32api, win32con

ClickLeftBefore = False
ClickRightBefore = False
ClickMiddleBefore = False

def ClickDetect(Type = "Left", SubType = "Held"):
    global ClickLeftBefore, ClickRightBefore, ClickMiddleBefore
    if win32api.GetAsyncKeyState(win32con.VK_LBUTTON):
        if Type.lower() == "left":
            if SubType.lower() == "held":
                ClickLeftBefore = True
                return True
            elif SubType.lower() == "on":
                if ClickLeftBefore == False:
                    ClickLeftBefore = True
                    return True
                else:
                    return False
            ClickLeftBefore = True
    else:
        if Type.lower() == "left":
            if SubType.lower() == "off":
                if ClickLeftBefore == True:
                    ClickLeftBefore = False
                    return True
                else:
                    ClickLeftBefore = False
                    return False
            ClickLeftBefore = False

    if win32api.GetAsyncKeyState(win32con.VK_RBUTTON):
        if Type.lower() == "right":
            if SubType.lower() == "held":
                ClickRightBefore = True
                return True
            elif SubType.lower() == "on":
                if ClickRightBefore == False:
                    ClickRightBefore = True
                    return True
                else:
                    return False
            ClickRightBefore = True
    else:
        if Type.lower() == "right":
            if SubType.lower() == "off":
                if ClickRightBefore == True:
                    ClickRightBefore = False
                    return True
                else:
                    ClickRightBefore = False
                    return False
            ClickRightBefore = False
    
    if win32api.GetAsyncKeyState(win32con.VK_MBUTTON):
        if Type.lower() == "middle":
            if SubType.lower() == "held":
                ClickMiddleBefore = True
                return True
            elif SubType.lower() == "on":
                if ClickMiddleBefore == False:
                    ClickMiddleBefore = True
                    return True
                else:
                    return False
            ClickMiddleBefore = True
    else:
        if Type.lower() == "middle":
            if SubType.lower() == "off":
                if ClickMiddleBefore == True:
                    ClickMiddleBefore = False
                    return True
                else:
                    ClickMiddleBefore = False
                    return False
            ClickMiddleBefore = False
    return False

Letters = {"a": False, "b": False, "c": False, "d": False, "e": False, "f": False, "g": False, "h": False, "i": False, "j": False, "k": False, "l": False, "m": False, "n": False, "o": False, "p": False, "q": False, "r": False, "s": False, "t": False, "u": False, "v": False, "w": False, "x": False, "y": False, "z": False}

def KeyboardDetect(Type: str, SubType = "Held"):
    global Letters
    if win32api.GetAsyncKeyState(ord(Type.lower()) - 32):
        if SubType.lower() == "held":
            Letters[Type.lower()] = True
            return True
        elif SubType.lower() == "on":
            if Letters[Type.lower()] == False:
                Letters[Type.lower()] = True
                return True
            else:
                return False
    else:
        if SubType.lower() == "off":
            if Letters[Type.lower()] == True:
                Letters[Type.lower()] = False
                return True
            else:
                Letters[Type.lower()] = False
                return False
        Letters[Type.lower()] = False
        return False
    return False

General = {}

def GeneralDetect(Type: int, SubType = "Held"):
    global General
    if not str(Type) in General.keys():
        General.update({str(Type): False})
    if win32api.GetAsyncKeyState(Type):
        if SubType.lower() == "held":
            General[Type] = True
            return True
        elif SubType.lower() == "on":
            if General[Type] == False:
                General[Type] = True
                return True
            else:
                return False
    else:
        if SubType.lower() == "off":
            if General[Type] == True:
                General[Type] = False
                return True
            else:
                General[Type] = False
                return False
        General[Type] = False
        return False
    return False

