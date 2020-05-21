text_rules = {
    "When CARDNAME enters the battlefield": "ETB_EFFECT",
    "CARDNAME enters the battlefield tapped.": "ENTER_TAPPED",
    "Defender (This creature can't attack.)": "DEFENDER",
    "Defender": "DEFENDER",
    "Flash (You may cast this spell any time you could cast an instant.)": "FLASH",
    "Flash": "FLASH",
    "Reach (This creature can block creatures with flying.)": "REACH",
    "Reach": "REACH",
    "Flying (This creature can't be blocked except by creatures with flying or reach.)": "FLYING",
    "Flying": "FLYING",
    "Haste (This creature can attack and {T} as soon as it comes under your control.)": "HASTE",
    "Haste": "HASTE",
    "Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.)": "TRAMPLE",
    "Trample": "TRAMPLE",
    "Vigilance (Attacking doesn't cause this creature to tap.)": "VIGILANCE",
    "Vigilance": "VIGILANCE",
    "Double strike (This creature deals both first-strike and regular combat damage.)": "DOUBLE_STRIKE",
    "Double strike": "DOUBLE_STRIKE",
    "Deathtouch (Any amount of damage this deals to a creature is enough to destroy it.)": "DEATHTOUCH",
    "Deathtouch": "DEATHTOUCH",
    "This spell can't be countered": "CANT_BE_COUNTER",
    "Lifelink (Damage dealt by this creature also causes you to gain that much life.)": "LIFELINK",
    "Lifelink": "LIFELINK",
    "Protection from green (This creature can't be blocked, targeted, dealt damage, enchanted, or equipped by anything green.)": "PROTECTION_FROM_GREEN",
    "Protection from red (This creature can't be blocked, targeted, dealt damage, enchanted, or equipped by anything red.)": "PROTECTION_FROM_RED",
    "Protection from black (This creature can't be blocked, targeted, dealt damage, enchanted, or equipped by anything black.)": "PROTECTION_FROM_BLACK",
    "Protection from blue (This creature can't be blocked, targeted, dealt damage, enchanted, or equipped by anything blue.)": "PROTECTION_FROM_BLUE",
    "Protection from white (This creature can't be blocked, targeted, dealt damage, enchanted, or equipped by anything white.)": "PROTECTION_FROM_WHITE",
    "(As this Saga enters and after your draw step, add a lore counter. Sacrifice after III.)": "SAGA_3",
    "(As this Saga enters and after your draw step, add a lore counter. Sacrifice after IV.)": "SAGA_4",
}

text_patterns = {
    "([A|a]s long as it's your turn[,.]?)": "YOUR_TURN",
    "([A|a]s long as it's attacking[,.]?)": "IS_ATTACKING",
}
