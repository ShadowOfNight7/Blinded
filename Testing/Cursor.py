import mouse, ctypes, time, win32gui, os, math, pygetwindow
from ctypes.wintypes import HWND, DWORD, RECT

dwmapi = ctypes.WinDLL("dwmapi")
hwnd = ctypes.windll.user32.FindWindowW(
    0, win32gui.GetWindowText(win32gui.GetForegroundWindow())
)
ctypes.windll.user32.SetProcessDPIAware()

full_screen_rect = (
    0,
    0,
    ctypes.windll.user32.GetSystemMetrics(0),
    ctypes.windll.user32.GetSystemMetrics(1),
)
maximized_screen_rect = (
    0,
    0,
    ctypes.windll.user32.GetSystemMetrics(16),
    ctypes.windll.user32.GetSystemMetrics(17),
)

ctypes.windll.shcore.SetProcessDpiAwareness(2)

win = pygetwindow.getActiveWindow()


def is_full_screen():
    try:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
        rect = win32gui.GetWindowRect(hWnd)
        if rect == full_screen_rect:
            return True
        elif (rect[2] >= maximized_screen_rect[2]) and (
            rect[3] >= maximized_screen_rect[3]
        ):
            return "maximized"
        else:
            return False
    except:
        return False


def getsize():
    pygetwindow.getActiveWindow().size = (0, 0)
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
        pygetwindow.getActiveWindow().size = ( pygetwindow.getActiveWindow().size[0] + 1, pygetwindow.getActiveWindow().size[1])
        time.sleep(0.025)
    currentsize = pygetwindow.getActiveWindow().size
    currentcol = os.get_terminal_size().columns
    while os.get_terminal_size().columns == currentcol:
        pygetwindow.getActiveWindow().size = ( pygetwindow.getActiveWindow().size[0] + 1, pygetwindow.getActiveWindow().size[1])
        time.sleep(0.025)

    charwidth = pygetwindow.getActiveWindow().size[0] - currentsize[0]
    return (charwidth, charheight)


def initialize(repetitions=1):
    charsize = []
    for i in range(repetitions):
        charsize.append(getsize())
        time.sleep(0.1)
    charx, chary = 0, 0
    for i in charsize:
        charx += i[0]
        chary += i[1]
    pygetwindow.getActiveWindow().size = (maximized_screen_rect[2], maximized_screen_rect[3])
    return (round(charx / repetitions), round(chary / repetitions))


# charactersize = initialize(5)
# pygetwindow.getActiveWindow().size = (maximized_screen_rect[2],maximized_screen_rect[3])


def get_mouse_coords(charactersize, get_text=False):
    rect = RECT()
    DMWA_EXTENDED_FRAME_BOUNDS = 9
    dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS), ctypes.byref(rect), ctypes.sizeof(rect) )
    # Relative to screen
    mouse_coords = (win32gui.ScreenToClient(hwnd, mouse.get_position())[0] + ctypes.windll.user32.GetSystemMetrics(5) * 2, win32gui.ScreenToClient(hwnd, mouse.get_position())[1] - ctypes.windll.user32.GetSystemMetrics(4) * 2)
    if not get_text:
        return mouse_coords
    if is_full_screen() == True:
        return (math.floor(mouse_coords[0] / charactersize[0]) - 1, math.floor(mouse_coords[1] / charactersize[1]) + 2)
    elif is_full_screen() == "maximized":
        return (math.floor(mouse_coords[0] / charactersize[0]) - 1, math.floor(mouse_coords[1] / charactersize[1] + 0.5))
    else:
        return (math.floor(mouse_coords[0] / charactersize[0]) - 1, math.floor(mouse_coords[1] / charactersize[1]))


def get_pixel_coords(charactersize, character_mouse_coords):
    rect = RECT()
    DMWA_EXTENDED_FRAME_BOUNDS = 9
    dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS), ctypes.byref(rect), ctypes.sizeof(rect))
    if is_full_screen() == True:
        mouse_coords = ((character_mouse_coords[0] + 1 + 0.5) * charactersize[0], (character_mouse_coords[1] - 2 + 0.5) * charactersize[1])
    elif is_full_screen() == "maximized":
        mouse_coords = ((character_mouse_coords[0] + 1 + 0.5) * charactersize[0], (character_mouse_coords[1] - 0.5 + 0.5) * charactersize[1])
    else:
        mouse_coords = ((character_mouse_coords[0] + 1 + 0.5) * charactersize[0], (character_mouse_coords[1] + 0.5) * charactersize[1])

    return win32gui.ClientToScreen(hwnd, (round(mouse_coords[0] - ctypes.windll.user32.GetSystemMetrics(5) * 2), round(mouse_coords[1] + ctypes.windll.user32.GetSystemMetrics(4) * 2)))
