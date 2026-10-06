# Imports

""" Item dictionary
 ├── name
 ├── description
 ├── modifier
 ├── type
 ├── target
"""

items = {
    "socks": {
        "name": "Socks of Serenity",
        "description": "Soft socks that bring you peace.",
        "modifier": 1,
        "stat": "ac",
        "target": "self"
    },

    "leggings": {
        "name": "Leggings of Recovery",
        "description": "Soft bear leggings that keep you warm.",
        "modifier": 5,
        "stat": "recovery",
        "target": "self"
    },

    "tunic": {
        "name": "Tunic of Rest",
        "description": "This bear tunic bears a bear.",
        "modifier": 2,
        "stat": "ac",
        "target": "self"
    },

    "crown": {
        "name": "Crown of Dreams",
        "description": "Sweet dreams follow those who wear this.",
        "modifier": 1,
        "stat": "ac",
        "target": "self"
    },

    "stick": {
        "name": "Cypress stick",
        "description": "Could this be the legendary Hero's sword?",
        "modifier": 3,
        "stat": "damage",
        "target": "self"
    },

    "cloud": {
        "name": "Cloud shield",
        "description": "It's soft like a cloud.",
        "modifier": 5,
        "stat": "ac",
        "target": "self"
    },

    "lantern": {
        "name": "Lantern of Lulling",
        "description": "Its soft light reveals things hidden in the darkness.",
        "hiddenDescription": "A soft light reveals the hidden stairs.",
        "modifier": -3,
        "stat": "ac",
        "unlock": "Mom",
        "target": "target"

    },

    "beast": {
        "character": "artemis",
        "name": "Artemis the Mythical Beast",
        "description": "A true friend, cute and cuddly.\n"
                       "You're safe with her.",
        "modifier": None,
        "stat": None,
        "target": "target"
    }
}
