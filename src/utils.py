# === Constants ===
escape_chance = 65
hangman_guesses = 7

# === Character Values ===
characters = {
    "player": {
        "is_player": True,
        "is_alive": True,
        "damage_dice": (1, 8),
        "equipment": [],
        "name": "You",
        "hp": 20,
        "ac": 12
    },

    "nightmare": {
        "is_player": False,
        "is_alive": True,
        "damage_dice": (1, 12),
        "equipment": [],
        "name": "Nightmare",
        "hp": 50,
        "ac": 13
    },

    "minion_1": {
        "is_player": False,
        "is_alive": True,
        "damage_dice": (1, 4),
        "equipment": [],
        "name": "Nightmare Minion",
        "hp": 8,
        "ac": 8
    },

    "minion_2": {
        "is_player": False,
        "is_alive": True,
        "damage_dice": (1, 4),
        "equipment": [],
        "name": "Nightmare Minion",
        "hp": 14,
        "ac": 10
    },

    "minion_3": {
        "is_player": False,
        "is_alive": True,
        "damage_dice": (1, 6),
        "equipment": [],
        "name": "Nightmare Minion",
        "hp": 18,
        "ac": 11
    },

    "mini_boss": {
        "is_player": False,
        "is_alive": True,
        "damage_dice": (1, 8),
        "equipment": [],
        "name": "Nightmare Guardian",
        "hp": 25,
        "ac": 12
    },

    "artemis": {
        "is_player": False,
        "is_alive": True,
        "damage_dice": (1, 6),
        "equipment": [],
        "name": "Artemis",
        "hp": 15,
        "ac": 15
    }
}

