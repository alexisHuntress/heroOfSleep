# === Imports ===
from utils import hangman_guesses
from items import items
import random


# === Puzzles ===
def garden_puzzle():
    """This function is a loop that replicates the game, simon says."""

    sequence = ["red", "blue", "purple", "green", "blue"]

    print(
        "Six colored flowers begin to glow.\n"
        "Red, Yellow, Blue, Green, Orange, and Purple.\n"
        "It looks like they're trying to show you a pattern...")

    for round_number in range(1, len(sequence) + 1):
        correct_sequence = sequence[:round_number]

        print("The flowers glow before dimming:")
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
    """This function takes a user input and compares it
     against a list of lists to "move" across a hopscotch court."""
    path = [["1"], {"2", "3"}, ["4"], {"5", "6"}, ["7"]]

    # Output the court and take user input.
    for square in path:
        print("""Jump across the court!

                 [ 7 ]
              ( 5 ) ( 6 )
                 [ 4 ]
              ( 3 ) ( 2 )
                 [ 1 ]
            """)
        print(f"Which square do you jump on?")
        jump = input("Jump: ").replace(",", " ").split()

        # Compare inputs
        if jump != square:
            print("You jumped on the wrong square.")
            return False

    print("You completed the hopscotch path. The door unlocks.")
    return True


def hangman_puzzle():
    """This function replicates the classic game hangman.
    At the start of each play through, the function selects a
    random word from the available list.
    The function then enters a while loop taking user input until either the
    word is guessed or the max number of guesses is exceeded."""

    words = [
        "Nightmare", "Lantern", "Serenity", "Dream", "Castle",
        "Goblin", "Hero", "Shield", "Crown", "Slumber",
        "Shadow", "Monster", "Adventure", "Treasure", "Puzzle",
        "Garden", "Guardian", "Victory", "Dungeon", "Dragon"
    ]

    max_wrong_guesses = hangman_guesses
    word = random.choice(words)
    hidden_word = "-" * len(word)
    check_word = word.lower()
    guessed_letters = []
    repeat_warnings = []
    wrong_guesses = 0
    guess = 1

    print(f"A secret word begins to form on the door.\n"
          f"You can see how long the word is but the letters are blurry.\n"
          f"Guess one letter at a time, or try to guess the whole word.\n"
          f"You have {hangman_guesses} wrong attempts to guess the word.")

    while wrong_guesses < max_wrong_guesses and "-" in hidden_word:

        print(hidden_word)
        print(f"Wrong guesses: {wrong_guesses}/{max_wrong_guesses}")

        user_input = input(
            f"Enter a character or guess the word (guess #{guess}): "
        ).lower()

        # Guess the whole word
        if len(user_input) > 1:
            if user_input == check_word:
                hidden_word = word
                print("You guessed the word!")
            else:
                print(f"'{user_input}' is not the word!")
                wrong_guesses += 1

        # Guess a letter
        elif len(user_input) == 1:

            # Check if this letter was already guessed
            if user_input in guessed_letters:

                # First repeat gets a warning
                if user_input not in repeat_warnings:
                    print(f"You already guessed '{user_input.upper()}'. Try again.")
                    repeat_warnings.append(user_input)

                # Second repeat counts as a wrong guess
                else:
                    print(f"You already guessed '{user_input.upper()}' twice!")
                    wrong_guesses += 1

            else:
                guessed_letters.append(user_input)
                print(f"You have guessed {', '.join(guessed_letters).upper()}")

                # Count how many times the letter appears
                num_occurrences = check_word.count(user_input)

                if num_occurrences > 0:

                    position = -1

                    for occurrence in range(num_occurrences):
                        # Find the next occurrence
                        position = check_word.find(
                            user_input,
                            position + 1
                        )

                        # Reveal the original correctly cased character
                        hidden_word = (
                            hidden_word[:position]
                            + word[position]
                            + hidden_word[position + 1:]
                        )

                else:
                    wrong_guesses += 1

        else:
            print("Please enter a character or guess the word.")

        guess += 1

    print(hidden_word)


# === Map ===
"""
Map
Key = {
        "I" : "Item room",
        "R" : "Empty room"
        "P" : "Puzzle room",
        "B" : "Boss room",
        "E" : "Enemy room",
        "H" : "Hidden room"
       }

                    I00
    B00             E00
I01 R00 I02     R01 I03
    I04 R02 R03 I05
            I06 I07 P00
            H00 E01 R06


Room structure
Room
 ├── name
 ├── description
 ├── empty description
 ├── exits
 ├── item
 ├── enemy
 ├── locked exits
 ├── puzzle function
 └── solved state
"""

rooms = {
    "Entrance": {  # R00
        "name": "The Waking Room",
        "description": "You woke up in this room. It feels oddly familiar.\n"
                       "There's a fancy stick in the center of the room\n"
                       "It may be dangerous to go alone without it.",
        "empty description": "You took the fancy stick from here",
        "exits": {"north": "Hallway"},
        "item": items["stick"],
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Mom's Room": {  # H00
        "name": "Mom's Room",
        "description": "Wait!\n"
                       "This is Mom's room!\n"
                       "Now the Nightmare can't bother you.\n"
                       "Sweet Dreams Hero.",
        "exits": {"east": "Entrance"},
        "item": None,
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Hallway": {  # E00
        "name": "Shadow Hall",
        "description": "A dark hallway stretches ahead. You hear something moving in the shadows.",
        "exits": {"west": "Item Room 6", "east": "Hop Scotch Room", "south": "Entrance"},
        "item": None,
        "enemy": "minion_1",
        "locked exits": ["west"],
        "puzzle": None,
        "solved": True
    },

    "Item Room 6": {  # I00
        "name": "The Bear Room",
        "description": "A small chest sits against the wall.\n"
                       "Little bears are carved into the lid.",
        "empty description": "An empty wooden chest rests against the wall.",
        "exits": {"east": "Hallway"},
        "item": items["leggings"],
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Hop Scotch Room": {  # P00
        "name": "Hopscotch Court",
        "description": "A giant hopscotch court covers the floor. Maybe you should play!",
        "exits": {"west": "Hallway", "south": "Room with stairs up"},
        "item": None,
        "enemy": None,
        "locked exits": ["south"],
        "puzzle": hop_scotch_puzzle,
        "solved": False
    },

    "Room with stairs up": {  # R01
        "name": "The Dark Stairway",
        "description": "A staircase disappears into the darkness above. Where does it lead?",
        "exits": {"up": "Room with stairs down", "north": "Hop Scotch Room"},
        "item": None,
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Room with stairs down": {  # I01
        "name": "The Upper Landing",
        "description": "You reach the top of the stairs. Something shiny catches your eye.",
        "empty description": "You reach the top of the stairs.",
        "exits": {"down": "Room with stairs up", "west": "Empty Room", "north": "Monster Room"},
        "item": items["crown"],
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Monster Room": {  # E01
        "name": "The Guardian's Hall",
        "description": "Something much bigger is waiting in the darkness.",
        "exits": {"north": "Treasure Room", "south": "Room with stairs down"},
        "item": None,
        "enemy": "mini_boss",
        "locked exits": ["north"],
        "puzzle": None,
        "solved": True
    },

    "Treasure Room": {  # I02
        "name": "The Guardian's Cage",
        "description": "You hear a familiar sound from inside the chest. Something in there wants out!",
        "empty description": "An empty chest sits open in the room.",
        "exits": {"south": "Monster Room"},
        "item": items["beast"],
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Empty Room": {  # I03
        "name": "The Dark Room",
        "description": "A small lantern glows softly in the dark room.\n"
                       "Somehow, the shadows don't seem as scary anymore.",
        "empty description": "The room is dark, but somehow the shadows don't seem as scary anymore.",
        "exits": {"east": "Room with stairs down", "south": "Item Room 5"},
        "item": items["lantern"],
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Item Room 5": {  # E02
        "name": "The Cloud Chamber",
        "description": "Another chest! This one looks soft for some reason.",
        "empty description": "An empty chest sits open in the room.",
        "exits": {"west": "Long Hall", "north": "Empty Room"},
        "item": items["cloud"],
        "enemy": "minion_2",
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Long Hall": {  # R02
        "name": "The Endless Hall",
        "description": "This hallway goes on forever!\n"
                       "Well...\n"
                       "Almost forever.",
        "exits": {"west": "Garden", "east": "Item Room 5"},
        "item": None,
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Garden": {  # P01
        "name": "The Candy Garden",
        "description": "Wow, a candy garden!\n"
                       "Six colorful flowers glow softly among the sweets.",
        "exits": {"west": "Item room 4", "north": "Empty room 2", "east": "Long Hall"},
        "item": None,
        "enemy": None,
        "locked exits": ["west"],
        "puzzle": garden_puzzle,
        "solved": False
    },

    "Item room 4": {  # I04
        "name": "The Bear's Den",
        "description": "Another chest!\n"
                       "I wonder what this one holds.",
        "empty description": "An empty chest sits open in the room.",
        "exits": {"east": "Garden"},
        "item": items["tunic"],
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Empty room 2": {  # E03
        "name": "The Noisy Room",
        "description": "You hear strange noises upon entering this room.",
        "exits": {"south": "Garden", "west": "Cross Road"},
        "item": None,
        "enemy": "minion_3",
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Cross Road": {  # P02
        "name": "The Crossroads",
        "description": "The hallway splits in several directions.\n"
                       "Something about the path ahead feels scary.\n"
                       "Strange symbols cover the door.",
        "exits": {"east": "Empty room 2", "west": "Item room 1", "north": "Nightmare's Room"},
        "item": None,
        "enemy": None,
        "locked exits": ["north"],
        "puzzle": hangman_puzzle,
        "solved": False
    },

    "Item room 1": {  # I05
        "name": "The Lonely Room",
        "description": "Oh look, a chest! I wonder what's inside?",
        "empty description": "An empty chest sits open in the room.",
        "exits": {"east": "Cross Road"},
        "item": items["socks"],
        "enemy": None,
        "locked exits": [],
        "puzzle": None,
        "solved": True
    },

    "Nightmare's Room": {  # B00
        "name": "The Nightmare's Chamber",
        "description": "The room grows dark and cold.\n"
                       "A terrible shadow rises before you.\n"
                       "The Nightmare has been waiting.",
        "exits": {"south": "Cross Road"},
        "item": None,
        "enemy": "nightmare",
        "locked exits": ["south"],
        "puzzle": None,
        "solved": True
    }
}
