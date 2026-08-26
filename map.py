# Imports
from character import Character

nightmare = Character(False, "Nightmare", 50, 15, (1, 12), None)
goblin = Character(False, "The Goblin", 20, 10, (2, 10), None)

def garden_puzzle():
    colors = ["red", "yellow", "blue", "green", "orange", "purple"]

    sequence = [
        "red",
        "blue",
        "purple",
        "green",
        "blue"
    ]

    print("Six colored flowers begin to glow.\nRed, Yellow, Blue, Green, Orange, and Purple.\nIt looks like they're trying to show you a pattern...")

    for round_number in range(1, len(sequence) + 1):
        correct_sequence = sequence[:round_number]

        print("The flowers glow:")
        print(", ".join(correct_sequence))

        answer = input("Repeat the sequence: ").replace(",", " ").replace(";", " ")

        player_sequence = [
            color.strip()
            for color in answer.split()
        ]

        if player_sequence != correct_sequence:
            print("The flowers suddenly go dark.")
            print("That wasn't the correct sequence.")
            return False

        print("Correct!\n")

    print("All six flowers begin to glow brightly.")
    print("You hear the door unlock.")

    return True


def hop_scotch_puzzle():
    path = ["1", "2", "3", "4", "5", "6", "7"]

    print("""
            Jump across the court! :
            
            23 25 07 19 14
            15 05 21 06 18
            12 20 04 22 16
            13 17 03 02 11
            24 09 01 10 08
            """)

    for square in path:
        jump = input("Jump to square: ").strip()

        if jump != square:
            print("You jumped on the wrong square.")
            return False

    print("You completed the hopscotch path. The door unlocks.")
    return True

"""
Map
Key = {"I" : "Item room", "R" : " Empty room" "P" : "puzzle room", "B" : "boss room", "E" : "enemy room", "H" : "hidden room"}

                    I00
    B00             E00
I01 R00 I02     R01 I03
    I04 R02 R03 I05
    I06 I07 P00
    H00 E01 R06


Room structure
Room
 ├── description
 ├── exits
 ├── item
 ├── enemy
 ├── locked exits
 ├── puzzle function
 └── solved state
"""
rooms = {
    "Entrance" : { #E01
            "description" : "You woke up in this room. It feels oddly familiar.",
            "exits" : {"north": "Hallway"},
            "item" : [],
            "enemy" : None,
            "locked exits" : {},
            "puzzle" : None,
            "solved" : True
    },

    "Mom's Room" : { #H00
            "description" : "Wait!\n This is Mom's room!\n Now the Nightmare can't bother you. \n Sweet Dreams Hero.",
            "exits" :{"east" :"Entrance"},
            "item": [],
            "enemy": None,
            "locked exits": {},
            "puzzle": None,
            "solved": True
    },

    "Hallway" : { #I07
            "description" : "A dark hallway with two rooms.",
            "exits" : {"west" : "Item Room 6", "east" : "Hop Scotch Room"},
            "item": [],
            "enemy": None,
            "locked exits": {},
            "puzzle": None,
            "solved": True
    },

    "Item Room 6" : { #I06
            "description" : "Oh look a chest!",
            "exits" : {"east" : "Hallway"},
            "item": [],
            "enemy": None,
            "locked exits": {},
            "puzzle": None,
            "solved": True
    },

    "Hop Scotch Room" : { #P00
            "description" : "Look Hopscotch!",
            "exits" : {"west" : "Hallway", "south" : "Room with stairs up"},
            "item": [],
            "enemy": None,
            "locked exits": {"south"},
            "puzzle": hop_scotch_puzzle,
            "solved": False
    },

    "Room with stairs up" : { #R06
            "description" : "Where do those stairs lead?.",
            "exits" : {"up" : "Room with stairs down", "north" : "Hop Scotch Room"},
            "item": [],
            "enemy": None,
            "locked exits": {},
            "puzzle": None,
            "solved": True
    },

    "Room with stairs down" : { #I03
            "description" : "What are those?.",
            "exits" : {"down" : "Room with stairs up", "west" : "Empty Room", "north" : "Monster Room"},
            "item": [],
            "enemy": None,
            "locked exits": {},
            "puzzle": None,
            "solved": True
    },

    "Monster Room" : { #E00
            "description" : "AHH!\n A monster!.",
            "exits" : {"north" : "Treasure Room", "south" : "Room with stairs down"},
            "item": [],
            "enemy": goblin,
            "locked exits": {"north", "south"},
            "puzzle": None,
            "solved": True
    },

    "Treasure Room": {  # I00
        "description": "Ohh, a fancy chest!",
        "exits": {"south": "Monster Room"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Empty Room": {  # R01
        "description": "This room is a little chilly.",
        "exits": {"east" : "Room with stairs down", "south": "Item Room 5"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Item Room 5": {  # I05
        "description": "Oh! A thing.",
        "exits": {"west" : "Long Hall", "north": "Empty Room"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Long Hall": {  # R03
        "description": "This hall goes forever!",
        "exits": {"west" : "Garden", "east": "Item Room 5"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Garden": {  # R02
        "description": "Wow, a candy garden!",
        "exits": {"west" : "Item room 4", "north": "Item room 2", "east": "Long Hall"},
        "item": [],
        "enemy": None,
        "locked exits": {"east"},
        "puzzle": garden_puzzle,
        "solved": False
    },

    "Item room 4": {  # I04
        "description": "Another Chest!\n I wonder what it holds.",
        "exits": {"east" : "Garden"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Item room 2": {  # I02
        "description": "Oh look Something.", #needs item inputed
        "exits": {"south" : "Garden", "west" : "Cross Road"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Cross Road": {  # R00
        "description": "Oh look Something.",  # needs item inputed
        "exits": {"east" : "Item room 2", "west" : "Item room 1", "north" : "Nightmare's Room"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Item room 1": {  # I01
        "description": "Oh look Something.",  # needs item inputed
        "exits": {"east": "Cross Road"},
        "item": [],
        "enemy": None,
        "locked exits": {},
        "puzzle": None,
        "solved": True
    },

    "Nightmare's Room": {  # B00
        "description": "Oh look Something.",  # needs item inputed
        "exits": {"south": "Cross Road"},
        "item": [],
        "enemy": nightmare,
        "locked exits": {"south"},
        "puzzle": None,
        "solved": True
    }
}
