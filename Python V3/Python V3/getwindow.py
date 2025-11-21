# from textual.app import App, ComposeResult
# from textual.widgets import Button, Static

# class MyApp(App):
#     def compose(self) -> ComposeResult:
#         yield Static("Select an option:")
#         yield Button("Start")
#         yield Button("Settings")
#         yield Button("Exit")

#     def on_button_pressed(self, event: Button.Pressed) -> None:
#         if event.button.label == "Exit":
#             self.exit()
#         else:
#             print(f"You pressed {event.button.label}")

# MyApp().run()

# import win32gui, mouse

# print(mouse.get_position())
# #521 - 523, #217-219
# def callback(hwnd, extra):
#     rect = win32gui.GetWindowRect(hwnd)
#     x = rect[0]
#     y = rect[1]
#     w = rect[2] - x
#     h = rect[3] - y
#     if win32gui.GetWindowText(hwnd) == "Windows PowerShell":
#     # if (x != 0) or (y != 0) or (w != 0) or (h != 0):
#         print("Window %s:" % win32gui.GetWindowText(hwnd))
#         print("\tLocation: (%d, %d)" % (x, y))
#         print("\t    Size: (%d, %d)" % (w, h))

# def main():
#     win32gui.EnumWindows(callback, None)
#     win32gui.FindWindow()

# if __name__ == '__main__':
#     main()


# from win32gui import FindWindow, GetClientRect, GetWindowRect
# import screeninfo, mouse, ctypes, time, math, os
# from ctypes.wintypes import HWND, DWORD, RECT

# # def GetWindowRectFromName(name:str)-> tuple:
# #     hwnd = ctypes.windll.user32.FindWindowW(0, name)
# #     rect = ctypes.wintypes.RECT()
# #     ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
# #     print(hwnd)
# #     print(rect)
# #     return (rect.left, rect.top, rect.right, rect.bottom)

# # if __name__ == "__main__":
# #     print(GetWindowRectFromName('Windows PowerShell'))
# #     pass

# dwmapi = ctypes.WinDLL("dwmapi")

# hwnd = ctypes.windll.user32.FindWindowW(0, "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.2544.0_x64__qbz5n2kfra8p0\python3.13.exe")    # refer to the other answers on how to find the hwnd of your window
# # hwnd = ctypes.windll.user32.FindWindowW(0, "Windows PowerShell")    # refer to the other answers on how to find the hwnd of your window

# rect = RECT()
# print(rect.left, rect.top, rect.right, rect.bottom)

# DMWA_EXTENDED_FRAME_BOUNDS = 9
# dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS),
#                              ctypes.byref(rect), ctypes.sizeof(rect))
# print(rect.left, rect.top, rect.right, rect.bottom)




# window_handle = FindWindow(None, "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.2544.0_x64__qbz5n2kfra8p0\python3.13.exe")
# # window_handle = FindWindow(None, "Windows PowerShell")
# rect2 = GetWindowRect(window_handle)
# clientRect = GetClientRect(window_handle)
# windowOffset = math.floor(((rect2[2]-rect2[0])-clientRect[2])/2)
# titleOffset = (rect2[3]-clientRect[3])
# print(titleOffset)

# print(rect.left, rect.top, rect.right, rect.bottom)
# mouse.move(rect.left/2, rect.top/2 + titleOffset/2.5)
# time.sleep(999)

# while True:
#     os.system('cls')
#     rect = RECT()
#     DMWA_EXTENDED_FRAME_BOUNDS = 9
#     dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS), ctypes.byref(rect), ctypes.sizeof(rect))

#     rect2 = GetWindowRect(window_handle)
#     clientRect = GetClientRect(window_handle)
#     windowOffset = math.floor(((rect2[2]-rect2[0])-clientRect[2])/2)
#     titleOffset = ((rect.bottom/2 - rect.top/2 - clientRect[3] + (rect2[3] - rect.bottom/2)))
#     print(rect2[3] - rect2[1])
#     print(clientRect[3])
#     print(rect2)
#     print((rect.left/2, rect.top/2, rect.right/2, rect.bottom/2))
#     print(clientRect)
#     print(titleOffset)

#######################
# import win32api, win32gui, ctypes, os
# hwnd = ctypes.windll.user32.FindWindowW(0, "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.2544.0_x64__qbz5n2kfra8p0\python3.13.exe")


# def getRelativePos():
#     pt = win32api.GetCursorPos()  #get current cursor pos
#     hwnd = ctypes.windll.user32.FindWindowW(0, "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.2544.0_x64__qbz5n2kfra8p0\python3.13.exe")
#     rect = win32gui.GetWindowRect(hwnd) #get screen coordinate rect of the console window
#     IsIn = win32gui.PtInRect(rect,pt)  # check if the pt is in the rect
#     if IsIn:
#         return win32gui.ScreenToClient(hwnd,pt) #convert screen coordinate to client coordinate of hwnd.
#     else:
#         return win32gui.ScreenToClient(hwnd,pt) #convert screen coordinate to client coordinate of hwnd.
    
# while True:
#     os.system("mode con cols=100 lines=1")
#     print(getRelativePos())



# import pygetwindow
# while True:
#     win = pygetwindow.getWindowsWithTitle('Windows PowerShell')[0]
#     print(win.topleft)


# import ctypes

# ctypes.windll.shcore.SetProcessDpiAwareness(2)
# print(ctypes.windll.user32.GetSystemMetrics(4))

#python -m pip install --upgrade pywin32

import mouse, ctypes, time, win32gui
from ctypes.wintypes import HWND, DWORD, RECT
dwmapi = ctypes.WinDLL("dwmapi")


def callback(hwnd, extra):
    global save
    if "Power" in win32gui.GetWindowText(hwnd):
        save = win32gui.GetWindowText(hwnd)

def main():
    win32gui.EnumWindows(callback, None)

if __name__ == '__main__':
    main()

hwnd = ctypes.windll.user32.FindWindowW(0, save)    # refer to the other answers on how to find the hwnd of your window

rect = RECT()
DMWA_EXTENDED_FRAME_BOUNDS = 9
dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DMWA_EXTENDED_FRAME_BOUNDS),
                            ctypes.byref(rect), ctypes.sizeof(rect))

print(rect.left, rect.top, rect.right, rect.bottom)
ctypes.windll.shcore.SetProcessDpiAwareness(2)
mouse.move(rect.left, rect.top + ctypes.windll.user32.GetSystemMetrics(4) * 2)
print(ctypes.windll.user32.GetSystemMetrics(4))
time.sleep(999)
