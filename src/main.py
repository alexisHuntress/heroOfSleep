# === Imports ===
from utils import direction_shortcuts
from game import *

from pygame_ui import pygame_loop


# === Game Loop ===
def game_loop():
    retry = True

    print("""
    Once upon a time, in a land of dreams and wonder, a kingdom lived in peace.
    They slept happily and dreamed happy dreams.

    Yet, there was one person whose dreams weren't so kind.
    He dreamed of monsters and ghouls.

    He grew tired of the peace of the kingdom and, using foul magic,
    unleashed his nightmares into the land.

    He took over the castle and declared that happy dreams would be no more.
    From this moment on, the people would only dream of nightmares and monsters.

    Yet all hope was not lost.

    There lay an innocent child who dreamed of heroes and adventure.

    This is the story of how he became one.
    """)
    print(
        "\nWelcome, Hero!\n"
        "\n"
        "Your goal is to explore the dungeon, collect equipment,\n"
        "and defeat the Nightmare to save the kingdom of dreams.\n"
        "\n"
        "HOW TO PLAY:\n"
        "Type MOVE to choose a direction and explore the castle.\n"
        "Use COLLECT to pick up equipment you discover.\n"
        "Use ATTACK to fight enemies or RUN to escape.\n"
        "Use PUZZLE to solve challenges blocking your path.\n"
        "Use EQUIPMENT to review the items you've collected.\n"
        "\n"
        "Type HELP at any time to review the available commands.\n"
        "\n"
        "Your adventure begins now!\n"
    )

    while retry:
        player, characters, rooms = reset_game()

        current_room = "Entrance"
        running = True

        print(rooms[current_room]["description"])

        while running and player.is_alive:
            room = rooms[current_room]

            enemy_name = room["enemy"]

            if enemy_name is not None:
                enemy = characters[enemy_name]

                if enemy.is_alive:
                    print(f"{enemy.name} blocks your path!")

            print()
            print(room["name"])

            game_commands()
            command = input("> ").lower().strip()

            direction = None
            parts = command.replace(":", " ").split()

            item_name = None

            if command.startswith("collect "):
                item_name = command.removeprefix("collect ").strip()
                command = "collect"

            if len(parts) == 2 and parts[0] in ["move", "go"]:
                direction = direction_shortcuts.get(parts[1], parts[1])
                command = "move"

            elif len(parts) == 1 and parts[0] in direction_shortcuts:
                direction = direction_shortcuts[parts[0]]
                command = "move"

            elif command == "go":
                command = "move"

            command = correct_input(
                command,
                [
                    "move",
                    "attack",
                    "collect",
                    "puzzle",
                    "play",
                    "run",
                    "equipment",
                    "examine",
                    "help",
                    "quit"
                ]
            )

            if command == "quit":
                running = False

            elif command == "collect":
                collect_equipment(player, room, characters, item_name)

            elif command == "equipment":
                player.display_equipment()

            elif command == "move":
                enemy_name = room["enemy"]
                if enemy_name is not None and characters[enemy_name].is_alive:
                    print(f"{characters[enemy_name].name} blocks your path! You must Attack or Run.")

                else:
                    print("Exits:", ", ".join(direction.capitalize() for direction in room["exits"]))
                    if direction is None:
                        direction = input("Which direction? ").lower().strip()
                        direction = direction_shortcuts.get(direction, direction)
                    direction = correct_input(direction, ["north", "south", "east", "west", "up", "down"])

                    if direction in ["north", "south", "east", "west", "up", "down"]:
                        new_room, description = try_moving(current_room, rooms, direction)
                        if new_room != current_room:
                            current_room = new_room
                            if current_room == "Entrance":
                                check_hidden_room(player, rooms)
                        print(description)

                        if current_room == "Mom's Room":
                            print(
                                "\nYou climb into bed beside Mom and close your eyes.\n"
                                "The Nightmare can't hurt you here.\n"
                                "\n=== Secret Victory ===\n"
                                "Sweet dreams, Hero."
                            )
                            running = False
                    else:
                        print("That is not a valid direction.")

            elif command == "attack":
                boss_defeated = combat(player, room, characters)

                if boss_defeated:
                    if len(player.equipment) == 8:
                        print(
                            "\n=== Heroic Victory ===\n"
                            "Armed with every legendary treasure, "
                            "you defeated the Nightmare!\n"
                            "The kingdom can dream peacefully once again."
                        )
                    else:
                        print(
                            "\n=== Brave Victory ===\n"
                            "You faced the Nightmare without every legendary treasure "
                            "and still emerged victorious!\n"
                            "The kingdom can dream peacefully once again."
                        )

                    running = False

            elif command == "run":
                new_room = run_from_combat(
                    player,
                    room,
                    characters
                )

                if new_room is not None:
                    current_room = new_room

                    if current_room == "Entrance":
                        check_hidden_room(player, rooms)

                    print(rooms[current_room]["description"])

            elif command in ["puzzle", "play"]:
                if room["puzzle"] is None:
                    print("There is no puzzle here.")

                elif room["solved"]:
                    print("You have already solved this puzzle.")

                else:
                    solved = room["puzzle"]()

                    if solved:
                        room["solved"] = True
                        room["locked exits"].clear()
                    else:
                        print("The puzzle remains unsolved.")

            elif command in ["examine"]:
                print(f"\n{room['name']}")
                print(room["description"])

                if room["item"] is not None:
                    print(f"There is something you can collect here: {room["item"]["name"]}.")

                if room["enemy"] is not None:
                    enemy = characters[room["enemy"]]

                    if enemy.is_alive:
                        print(f"A {enemy.name} is here!")
                        print(f"HP: {enemy.hp}/{enemy.max_hp}")

                if room["puzzle"] is not None and not room["solved"]:
                    print("There is an unsolved puzzle in this room.")

                print("Exits:", ", ".join(room["exits"]))

            elif command == "help":
                help_menu()

            elif command == "admin":  # TODO: Delete this?
                current_room = admin(current_room, rooms, characters, player)

            else:
                print("I don't understand that command.")

        if not player.is_alive:
            choice = input(
                "\nWould you like to try again? [Yes/No]: "
            ).lower().strip()

            if choice not in ["yes", "y"]:
                retry = False

        else:
            retry = False


if __name__ == "__main__":
    game_loop()
    # pygame_loop()
