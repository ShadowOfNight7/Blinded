itemObjects = {
    "example target": {
        "animation frames": [
            """
šššš|šššš
šššš|šššš
----+----
šššš|šššš
šššš|šššš
""",
            """
šš|šš
--+--
šš|šš
""",
            """
+
""",
        ],
        "x": 0,
        "y": 0,
        "x bias": 0,
        "y bias": 0,
        "width": 1,
        "height": 1,
        "current frame": 0,
        "parent object": "screen",
        "parent anchor": "top left",
        "child anchor": "center",
        "is empty character part of hitbox": False,
    },
}
keyBindsStatus = {
    "up": {"state": False, "keybind": "w"},
    "left": {"state": False, "keybind": "a"},
    "down": {"state": False, "keybind": "s"},
    "right": {"state": False, "keybind": "d"},
}
mouseStatus = {
    "absolute position": (0, 0),
    "left button": False,
    "right button": False,
    "middle button": False,
    "left button release": False,
    "right button release": False,
    "middle button release": False,
    "scroll x": 0,
    "scroll y": 0,
}
endEscapeCode = "\033[0m"
styleCodes = {
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
colorCodes = {
    "Black": 30,
    "Red": 31,
    "Green": 32,
    "Yellow": 33,
    "Blue": 34,
    "Magenta": 35,
    "Cyan": 36,
    "White": 37,
}
print("INFORMATION".center(30) + "|")
exit()
assets = {
    # ┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
    # │                              │                              │                              │                              │
    # │            FIGHT             │            ITEMS             │         INFORMATION          │            MERCY             │
    # │                              │                              │                              │                              │
    # ┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
    # │ ╔            ╦             ╗ │                              │                              │                              │
    # │ ║      >>> FIGHT <<<       ║ │            ITEMS             │         INFORMATION          │            MERCY             │
    # │ ╚            ╩             ╝ │                              │                              │                              │
    "center barrier": [
        """
┬
│
│
│
"""
    ],
    "left barrier": [
        """
┌
│
│
│
"""
    ],
    "right barrier": [
        """
┐
│
│
│
"""
    ],
    "fight button": [
        """
──────────────────────────────
                              
            FIGHT             
                              
""",
        """
──────────────────────────────
                              
        >>> FIGHT <<<         
                              
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║          FIGHT           ║ 
 ╚            ╩             ╝ 
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║      >>> FIGHT <<<       ║ 
 ╚            ╩             ╝ 
""",
    ],
    "items button": [
        """
──────────────────────────────
                              
            ITEMS             
                              
""",
        """
──────────────────────────────
                              
        >>> ITEMS <<<         
                              
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║          ITEMS           ║ 
 ╚            ╩             ╝ 
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║      >>> ITEMS <<<       ║ 
 ╚            ╩             ╝ 
""",
    ],
    "information button": [
        """
──────────────────────────────
                              
         INFORMATION          
                              
""",
        """
──────────────────────────────
                              
     >>> INFORMATION <<<      
                              
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║       INFORMATION        ║ 
 ╚            ╩             ╝ 
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║   >>> INFORMATION <<<    ║ 
 ╚            ╩             ╝ 
""",
    ],
    "items button": [
        """
──────────────────────────────
                              
            MERCY             
                              
""",
        """
──────────────────────────────
                              
        >>> MERCY <<<         
                              
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║          MERCY           ║ 
 ╚            ╩             ╝ 
""",
        """
──────────────────────────────
 ╔            ╦             ╗ 
 ║      >>> MERCY <<<       ║ 
 ╚            ╩             ╝ 
""",
    ],
}
mobInfo = {
    "slime": {
        "animation frames": [
            """
ššš__________ššš
šš/          \\šš
š/     (O)    \\š
/______________\\

"""
        ],
        "health": 100,
        "attacks": {
            "spit": {"damage": 5},
            "crush": {
                "damage": 10,
            },
        },
        "defence": 2,
    }
}
