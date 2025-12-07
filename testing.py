assets = {
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
    ],
}
import Assets.YiPyterminal as YiPyterminal

mobsStatus = {
    "Slime": {
        "Attacks": [{"AttackType": "BasicAttack", "Weight": 10}],
        "Stats": {
            "MaxHealth": 100,
            "CurrentHp": 100,
            "Regen": 5,
            "Defence": 0,
            "MagicDefence": 0,
            "Strength": 0,
            "MagicPower": 0,
            "CritChance": 5,
            "CritPower": 100,
            "TrueAttack": 0,
            "TrueDefence": 0,
        },
        "SpawnChance": 1,
        "Drops": [{"Item": None, "Weight": 10}],
        "Special": None,
        "Name": "Slime",
    },
}
selectedViewMobOption = "Slime"
x = (
    YiPyterminal.assets["enemy information box"][1]
    .replace(
        ">      PLACEHOLDERNAME       <",
        str(mobsStatus[selectedViewMobOption]["Name"]).center(30),
    )
    .replace("[hp]", str(mobsStatus[selectedViewMobOption]["Stats"]["CurrentHp"]))
    .replace("[max hp]", str(mobsStatus[selectedViewMobOption]["Stats"]["MaxHealth"]))
    .replace("[hp regen]", str(mobsStatus[selectedViewMobOption]["Stats"]["Regen"]))
    .replace("[def]", str(mobsStatus[selectedViewMobOption]["Stats"]["Defence"]))
    .replace(
        "[magic def]",
        str(mobsStatus[selectedViewMobOption]["Stats"]["MagicDefence"]),
    )
    .replace("[strength]", str(mobsStatus[selectedViewMobOption]["Stats"]["Strength"]))
    .replace(
        "[magic power]",
        str(mobsStatus[selectedViewMobOption]["Stats"]["MagicPower"]),
    )
    .replace(
        "[crit chance]",
        str(mobsStatus[selectedViewMobOption]["Stats"]["CritChance"]),
    )
    .replace(
        "[crit power]", str(mobsStatus[selectedViewMobOption]["Stats"]["CritPower"])
    )
    .replace(
        "[true attack]",
        str(mobsStatus[selectedViewMobOption]["Stats"]["TrueAttack"]),
    )
    .replace(
        "[true def]", str(mobsStatus[selectedViewMobOption]["Stats"]["TrueDefence"])
    )
)
print("______________________________________________")
print(YiPyterminal.assets["enemy information box"][1])
print(x)
