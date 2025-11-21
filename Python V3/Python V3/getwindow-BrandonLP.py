import mouse, ctypes, time, win32gui, keyboard, os, sys, math, pygetwindow, random
from ctypes.wintypes import HWND, DWORD, RECT
dwmapi = ctypes.WinDLL("dwmapi")

hwnd = ctypes.windll.user32.FindWindowW(0, win32gui.GetWindowText(win32gui.GetForegroundWindow()))

# rect = RECT()
# DMWA_EXTENDED_FRAME_BOUNDS = 9
# dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS),
#                             ctypes.byref(rect), ctypes.sizeof(rect))



ctypes.windll.user32.SetProcessDPIAware() # optional, makes functions return real pixel numbers instead of scaled values

full_screen_rect = (0, 0, ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
maximized_screen_rect = (0, 0, ctypes.windll.user32.GetSystemMetrics(16), ctypes.windll.user32.GetSystemMetrics(17))

def is_full_screen():
    try:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
        rect = win32gui.GetWindowRect(hWnd)
        if rect == full_screen_rect:
            return True
        elif (rect[2] >= maximized_screen_rect[2]) and (rect[3] >= maximized_screen_rect[3]):
            return "maximized"
        else:
            return False
    except:
        return False


# print(rect.left, rect.top, rect.right, rect.bottom)
ctypes.windll.shcore.SetProcessDpiAwareness(2)

x, y = 3, 3
gravity = 1
screen = [["#" for i in range(os.get_terminal_size().columns)] for i in range(os.get_terminal_size().lines - 1)]
screen.insert(0, [" " * os.get_terminal_size().columns])

win = pygetwindow.getActiveWindow()

def getsize():
    pygetwindow.getActiveWindow().size = (0,0)
    time.sleep(0.05)
    currentsize = pygetwindow.getActiveWindow().size
    currentlines = os.get_terminal_size().lines
    while os.get_terminal_size().lines == currentlines:
        pygetwindow.getActiveWindow().size = (pygetwindow.getActiveWindow().size[0], pygetwindow.getActiveWindow().size[1] + 1)
        time.sleep(0.025)
    currentsize = pygetwindow.getActiveWindow().size
    currentlines = os.get_terminal_size().lines
    while os.get_terminal_size().lines == currentlines:
        pygetwindow.getActiveWindow().size = (pygetwindow.getActiveWindow().size[0], pygetwindow.getActiveWindow().size[1] + 1)
        time.sleep(0.025)

    charheight = pygetwindow.getActiveWindow().size[1] - currentsize[1]

    currentsize = pygetwindow.getActiveWindow().size
    currentcol = os.get_terminal_size().columns
    while os.get_terminal_size().columns == currentcol:
        pygetwindow.getActiveWindow().size = (pygetwindow.getActiveWindow().size[0] + 1, pygetwindow.getActiveWindow().size[1])
        time.sleep(0.025)
    currentsize = pygetwindow.getActiveWindow().size
    currentcol = os.get_terminal_size().columns
    while os.get_terminal_size().columns == currentcol:
        pygetwindow.getActiveWindow().size = (pygetwindow.getActiveWindow().size[0] + 1, pygetwindow.getActiveWindow().size[1])
        time.sleep(0.025)

    charwidth = pygetwindow.getActiveWindow().size[0] - currentsize[0]
    return (charwidth, charheight)

def initialize(repetitions = 1):
    charsize = []
    for i in range(repetitions):
            charsize.append(getsize())
            time.sleep(0.1)
    charx, chary = 0, 0
    for i in charsize:
        charx += i[0]
        chary += i[1]
    return (round(charx/repetitions), round(chary/repetitions))

charactersize = initialize(5)
pygetwindow.getActiveWindow().size = (2000,1000)

#Colours!

def colourText(rgb: list, text: str):
    return "\033[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m" + text + "\033[0m"

def bgcolourText(rgb: list, text: str):
    return "\033[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m" + text + "\033[0m"

mousergb = [255, 0, 0]


while True:

    screen = [["#" for i in range(os.get_terminal_size().columns)] for i in range(os.get_terminal_size().lines - 1)]
    screen.insert(0, [" " * os.get_terminal_size().columns])


    rect = RECT()
    DMWA_EXTENDED_FRAME_BOUNDS = 9
    dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS),
                                ctypes.byref(rect), ctypes.sizeof(rect))

    mouse_coords = (win32gui.ScreenToClient(hwnd, mouse.get_position())[0] + ctypes.windll.user32.GetSystemMetrics(5) * 2, win32gui.ScreenToClient(hwnd, mouse.get_position())[1] - ctypes.windll.user32.GetSystemMetrics(4) * 2)

    if is_full_screen() == True:
        mouse_text_coords = (math.floor(mouse_coords[0] / charactersize[0]) - 1, math.floor(mouse_coords[1] / charactersize[1]) + 2)
    elif is_full_screen() == "maximized":
        mouse_text_coords = (math.floor(mouse_coords[0] / charactersize[0]) - 1, math.floor(mouse_coords[1] / charactersize[1] + 0.5))
    else:
        mouse_text_coords = (math.floor(mouse_coords[0] / charactersize[0]) - 1, math.floor(mouse_coords[1] / charactersize[1]))

    try:
        screen[round(mouse_text_coords[1])][round(mouse_text_coords[0])] = colourText(mousergb, "X")
    except:
        ""
    a = 0
    for i in screen:
        a += 1
        sys.stdout.write("\033[" + str(a) +";0f" + "".join(i))
        sys.stdout.flush()
    
    mousergb = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    time.sleep(1/10000)












#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
#     ############################################################################################################################################################
