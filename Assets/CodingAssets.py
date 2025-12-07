itemObjects = {
    "example target": {
        "animation frames": [
            """
šššš│šššš
šššš│šššš
----+----
šššš│šššš
šššš│šššš
""",
            """
šš│šš
--+--
šš│šš
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
assets = {
    #
    # ┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
    # │                              │                              │                              │                              │
    # │            FIGHT             │            ITEMS             │         INFORMATION          │            MERCY             │
    # │                              │                              │                              │                              │
    # ┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
    # │ ╔            ╦             ╗ │                              │                              │                              │
    # │ ║      >>> FIGHT <<<       ║ │            ITEMS             │         INFORMATION          │            MERCY             │
    # │ ╚            ╩             ╝ │                              │                              │                              │
    "center barrier": [
        R"""┬
│
│
│""",
        R"""┼
│
│
│""",
    ],
    "left barrier": [
        R"""┌
│
│
│""",
        R"""├
│
│
│""",
    ],
    "right barrier": [
        R"""┐
│
│
│""",
        R"""┤
│
│
│""",
    ],
    "fight button": [
        R"""──────────────────────────────
                              
            FIGHT             
                              """,
        R"""──────────────────────────────
                              
        >>> FIGHT <<<         
                              """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║          FIGHT           ║ 
 ╚            ╩             ╝ """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║      >>> FIGHT <<<       ║ 
 ╚            ╩             ╝ """,
    ],
    "items button": [
        R"""──────────────────────────────
                              
            ITEMS             
                              """,
        R"""──────────────────────────────
                              
        >>> ITEMS <<<         
                              """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║          ITEMS           ║ 
 ╚            ╩             ╝ """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║      >>> ITEMS <<<       ║ 
 ╚            ╩             ╝ """,
    ],
    "information button": [
        R"""──────────────────────────────
                              
         INFORMATION          
                              """,
        R"""──────────────────────────────
                              
     >>> INFORMATION <<<      
                              """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║       INFORMATION        ║ 
 ╚            ╩             ╝ """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║   >>> INFORMATION <<<    ║ 
 ╚            ╩             ╝ """,
    ],
    "mercy button": [
        R"""──────────────────────────────
                              
            MERCY             
                              """,
        R"""──────────────────────────────
                              
        >>> MERCY <<<         
                              """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║          MERCY           ║ 
 ╚            ╩             ╝ """,
        R"""──────────────────────────────
 ╔            ╦             ╗ 
 ║      >>> MERCY <<<       ║ 
 ╚            ╩             ╝ """,
    ],
    # ┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
    # │>        PLACEHOLDER1        <│>        PLACEHOLDER2        <│>        PLACEHOLDER3        <│>        PLACEHOLDER4        <│
    # ├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
    # │>        PLACEHOLDER5        <│>        PLACEHOLDER6        <│>        PLACEHOLDER7        <│>        PLACEHOLDER8        <│
    "fight box": [
        R"""┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│>        PLACEHOLDER1        <│>        PLACEHOLDER2        <│>        PLACEHOLDER3        <│>        PLACEHOLDER4        <│
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│>        PLACEHOLDER5        <│>        PLACEHOLDER6        <│>        PLACEHOLDER7        <│>        PLACEHOLDER8        <│"""
    ],
    "items box": [
        R"""┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│>        PLACEHOLDER1        <│>        PLACEHOLDER2        <│>        PLACEHOLDER3        <│>        PLACEHOLDER4        <│
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│>        PLACEHOLDER5        <│>        PLACEHOLDER6        <│>        PLACEHOLDER7        <│>        PLACEHOLDER8        <│"""
    ],
    "information box": [
        R"""┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│>        PLACEHOLDER1        <│>        PLACEHOLDER2        <│>        PLACEHOLDER3        <│>        PLACEHOLDER4        <│
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│>        PLACEHOLDER5        <│>        PLACEHOLDER6        <│>        PLACEHOLDER7        <│>        PLACEHOLDER8        <│"""
    ],
    "mercy box": [
        R"""┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│>        PLACEHOLDER1        <│>        PLACEHOLDER2        <│>        PLACEHOLDER3        <│>        PLACEHOLDER4        <│
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│>        PLACEHOLDER5        <│>        PLACEHOLDER6        <│>        PLACEHOLDER7        <│>        PLACEHOLDER8        <│"""
    ],
    "enemy selection box": [
        """──────────────────────────────┐
                              │
>        PLACEHOLDER1        <│
                              │
──────────────────────────────┤
                              │
>        PLACEHOLDER2        <│
                              │╲
──────────────────────────────┼─╲
                              │ E╲
>        PLACEHOLDER3        <│ N │
                              │ E │
──────────────────────────────┤ M │
                              │ Y │
>        PLACEHOLDER4        <│   │
                              │ S │
──────────────────────────────┤ E │
                              │ L │
>        PLACEHOLDER5        <│ E │
                              │ C │
──────────────────────────────┤ T │
                              │ I │
>        PLACEHOLDER6        <│ O │
                              │ N╱
──────────────────────────────┼─╱
                              │╱
>        PLACEHOLDER7        <│
                              │
──────────────────────────────┤
                              │
>        PLACEHOLDER8        <│
                              │
──────────────────────────────┘"""
    ],
    "enemy selection option": [
        """ ╔                          ╗ 
 ║>                        <║ 
 ╚                          ╝ """,
    ],
    "enemy information box": [
        """┌──────────────────────────────
│             ...
├──────────────────────────────
│ Select an enemy on the left
│ to attack and view
│ information...
│
│
│
│
│
│
│
│
│
│
│
│
│
│
│
│
└──────────────────────────────""",
        """┌──────────────────────────────
│>      PLACEHOLDERNAME       <
├──────────────────────────────
│ Health: [hp]/[max hp]
│
│ Health Regen: [hp regen]
│
│ Defence: [def]
│
│ Magic Defence: [magic def]
│
│ Strength: [strength]
│
│ Magic Power: [magic power]
│
│ Critical Chance: [crit chance]
│
│ Critical Power: [crit power]
│
│ True Attack: [true attack]
│
│ True Defence: [true def]
└──────────────────────────────""",
        """┌──────────────────────────────
│>      PLACEHOLDERNAME       <
├──────────────────────────────
│ Health: [hp]/[max hp]
│
│ Health Regen: [hp regen]
│
│ Defence: [def]
│
│ Magic Defence: [magic def]
│
│ Strength: [strength]
│
│ Magic Power: [magic power]
│
│ Critical Chance: [crit chance]
│
│ Critical Power: [crit power]
│
│ True Attack: [true attack]
│
│ True Defence: [true def]
└──────────────────────────────""",
    ],
    "mercy bar": [
        """
     ┌──────│
     │  ┌───│
   ╱┬┴──┴┬  │
  ╱ │    │  │
 ╱  │    │  │
╱   │    │  │
│ M │    │  │
│ E │    │  │
│ R │    │  │
│ C │░░░░│  │
│ Y │▓▓▓▓│  │
╲   │████│  │
 ╲  │████│  │
  ╲ │████│  │
   ╲┴┬──┬┴  │
     │  └───│
     └──────│

"""
    ],
    "Slime": [
        R"""
ššš__________ššš
šš/          \šš
š/     (O)    \š
/______________\\"""
    ],
}
[
    "┐",
    "└",
    "┴",
    "┬",
    "├",
    "─",
    "┼",
    "┘",
    "┌",
    "│",
    "┤",
    "╱",
    "╲",
    "╳",
    "╣",
    "║",
    "╗",
    "╝",
    "╚",
    "╔",
    "╩",
    "╦",
    "╠",
    "═",
    "╬",
    "░",
    "▒",
    "▓",
    "█",
    "▄",
    "▀",
    "■",
]
