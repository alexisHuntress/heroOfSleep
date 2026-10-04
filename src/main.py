# === Imports ===
from game import *
# import pygame_ui


# === Game Loop ===
def game_loop():  # TODO: Game Loop
    retry = True

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
                    "help",
                    "quit"
                ]
            )

            if command == "quit":
                running = False

            elif command == "collect":
                collect_equipment(player, room, characters)

            elif command == "equipment":
                player.display_equipment()

            elif command == "move":
                enemy_name = room["enemy"]

                if enemy_name is not None and characters[enemy_name].is_alive:
                    print(f"{characters[enemy_name].name} blocks your path! You must Attack or Run.")
                else:
                    print("Exits:", ", ".join(room["exits"].keys()))
                    direction = input("Which direction? ").lower().strip()
                    direction = correct_input(
                        direction,
                        ["north", "south", "east", "west", "up", "down"]
                    )

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
