# === Imports ===
from character import Character
import difflib
import random
import utils
import copy
import map


# === Admin/Debug ===  # TODO: ADMIN
def admin(current_room, rooms, characters, player):
    while True:
        room = rooms[current_room]

        print(f"\n[ADMIN] {current_room}")
        print("Commands: [Kill] [Solve] [Collect] [Recover] [Exit]")
        print("Directions:", ", ".join(room["exits"].keys()))

        command = input("[ADMIN] > ").lower().strip()
        command = correct_input(
            command,
            [
                "kill",
                "solve",
                "collect",
                "recover",
                "exit",
                "north",
                "south",
                "east",
                "west",
                "up",
                "down"
            ]
        )

        if command == "exit":
            return current_room

        elif command == "kill":
            if room["enemy"] is not None:
                enemy = characters[room["enemy"]]
                enemy.hp = 0
                enemy.is_alive = False
                room["locked exits"].clear()
                print(f"[ADMIN] {enemy.name} defeated.")
            else:
                print("[ADMIN] No enemy in this room.")

        elif command == "solve":
            if room["puzzle"] is not None:
                room["solved"] = True
                room["locked exits"].clear()
                print("[ADMIN] Puzzle solved.")
            else:
                print("[ADMIN] No puzzle in this room.")

        elif command == "collect":
            if room["item"] is not None:
                item = room["item"]

                player.equipment.append(item)

                if item["target"] == "self" and item["stat"] != "recovery":
                    player.modify_stats(item)

                room["description"] = room["empty description"]
                room["item"] = None

                print(f"[ADMIN] Collected {item['name']}.")
            else:
                print("[ADMIN] No item in this room.")

        elif command == "recover":
            player.hp = player.max_hp
            print(f"[ADMIN] HP restored to {player.hp}.")

        elif command in room["exits"]:
            current_room = room["exits"][command]
            print(rooms[current_room]["description"])

        else:
            print("[ADMIN] Invalid command.")


# === Game Setup ===
def create_character(character):
    return Character(
        character["is_player"],
        character["name"],
        character["hp"],
        character["ac"],
        character["damage_dice"],
        character["equipment"].copy(),
        character["is_alive"]
    )


def create_characters():
    player = create_character(utils.characters["player"])

    characters = {
        "nightmare": create_character(utils.characters["nightmare"]),
        "minion_1": create_character(utils.characters["minion_1"]),
        "minion_2": create_character(utils.characters["minion_2"]),
        "minion_3": create_character(utils.characters["minion_3"]),
        "mini_boss": create_character(utils.characters["mini_boss"]),
        "artemis": create_character(utils.characters["artemis"])
    }

    return player, characters


def reset_game():
    player, characters = create_characters()
    rooms = copy.deepcopy(map.rooms)

    return player, characters, rooms


# === Movement ===  # TODO: Movement
def try_moving(current_room, rooms, direction):
    room = rooms[current_room]

    if direction not in room["exits"]:
        return current_room, "You can't travel in that direction."

    if direction in room["locked exits"]:
        return current_room, "That way is locked."

    current_room = room["exits"][direction]
    description = rooms[current_room]["description"]

    return current_room, description


def check_hidden_room(player, rooms):
    has_lantern = any(
        item["name"] == "Lantern of Lulling"
        for item in player.equipment
    )

    if has_lantern and "west" not in rooms["Entrance"]["exits"]:
        rooms["Entrance"]["exits"]["west"] = "Mom's Room"

        print(
            "The Lantern's soft light reveals something in the wall.\n"
            "A hidden passage leads west!"
        )


# === Combat ===  # TODO: Combat
def combat(player, room, characters):
    enemy_name = room["enemy"]

    if enemy_name is None:
        print("There is nothing to attack.")
        return False

    enemy = characters[enemy_name]

    if not enemy.is_alive:
        print(f"{enemy.name} has already been defeated.")
        return False

    player.attack(enemy)

    # Artemis attacks with the player
    has_artemis = any(
        item["name"] == "Artemis the Mythical Beast"
        for item in player.equipment
    )

    if has_artemis and enemy.is_alive:
        artemis = characters["artemis"]
        artemis.attack(enemy)

    if not enemy.is_alive:
        if enemy_name == "nightmare":
            return True

        if enemy_name == "minion_1":
            room["description"] = "The hallway is quiet now."

        elif enemy_name == "mini_boss":
            room["description"] = "The room is quiet now."

        # Leggings of Recovery
        for item in player.equipment:
            if item["stat"] == "recovery":
                old_hp = player.hp
                player.hp = min(player.hp + item["modifier"], player.max_hp)

                if player.hp > old_hp:
                    print(f"You recovered {player.hp - old_hp} HP!")

        if room["locked exits"]:
            room["locked exits"].clear()
            print("The way is now clear!")

        return False

    enemy.attack(player)

    return False


def run_from_combat(player, room, characters):
    enemy_name = room["enemy"]

    if enemy_name is None:
        print("There is nothing to run from.")
        return None

    enemy = characters[enemy_name]

    if not enemy.is_alive:
        print("There is nothing to run from.")
        return None

    if enemy_name == "nightmare":
        print("You can't run from your Nightmare!")
        return None

    available_exits = [
        direction
        for direction in room["exits"]
        if direction not in room["locked exits"]
    ]

    if not available_exits:
        print("There is nowhere to run!")
        return None

    print("You try to run!")

    if random.randint(1, 100) <= utils.escape_chance:
        print("You found an opening!")

        enemy.attack(player)

        if not player.is_alive:
            return None

        print("Exits:", ", ".join(available_exits))
        direction = input("Run which direction? ").lower().strip()

        if direction not in available_exits:
            print("You can't run that way!")
            return None

        if enemy_name == "mini_boss":
            enemy.hp = enemy.max_hp

        return room["exits"][direction]

    print("You couldn't get away!")
    enemy.attack(player)

    return None


# === Equipment ===  # TODO: Equipment

def collect_equipment(player, room, characters):
    enemy_name = room["enemy"]

    if enemy_name is not None:
        enemy = characters[enemy_name]

        if enemy.is_alive:
            print(f"You can't open the chest while {enemy.name} is guarding it!")
            return

    if room["item"]:
        item = room["item"]

        player.equipment.append(item)

        if item["target"] == "self" and item["stat"] != "recovery":
            player.modify_stats(item)

        room["description"] = room["empty description"]
        room["item"] = None

        print(f"You equipped {item['name']}!\n"
              f"{item["description"]}")
    else:
        print("There is nothing to collect.")


# === Commands ===  # TODO: Commands

def game_commands():
    print(
        "Commands: [Move] [Attack] [Collect] [Puzzle] [Run] "
        "[Equipment] [Help] [Quit]"
    )


def correct_input(user_input, options):
    if user_input in options:
        return user_input

    match = difflib.get_close_matches(
        user_input,
        options,
        n=1,
        cutoff=0.7
    )

    if match:
        return match[0]

    return user_input


def help_menu():
    print(
        "\n=== Help ===\n"
        "Move      - Move to another room\n"
        "Attack    - Attack an enemy\n"
        "Collect   - Collect an item in the room\n"
        "Puzzle    - Attempt to solve a puzzle\n"
        "Run       - Attempt to escape from an enemy\n"
        "Equipment - View your collected equipment\n"
        "Quit      - End the game"
    )
