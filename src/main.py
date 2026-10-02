# Imports
from character import Character
import random
import pygame
import copy
import map


# === Admin/Debug ===  # TODO: ADMIN
def admin(current_room, rooms, characters):
    while True:
        room = rooms[current_room]

        print(f"\n[ADMIN] {current_room}")
        print("Commands: [Kill] [Solve] [Exit]")
        print("Directions:", ", ".join(room["exits"].keys()))

        command = input("[ADMIN] > ").lower().strip()

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

        elif command in room["exits"]:
            current_room = room["exits"][command]
            print(rooms[current_room]["description"])

        else:
            print("[ADMIN] Invalid command.")

# === Game Setup ===


def create_characters():
    player = Character(True, "You", 15, 11, (2, 6), [], True)

    characters = {
        "nightmare": Character(False, "Nightmare", 50, 15, (1, 12), [], True),
        "minion_1": Character(False, "Nightmare Minion", 8, 8, (1, 4), [], True),
        "minion_2": Character(False, "Nightmare Minion", 14, 10, (1, 6), [], True),
        "minion_3": Character(False, "Nightmare Minion", 18, 11, (1, 6), [], True),
        "mini_boss": Character(False, "Nightmare Guardian", 25, 12, (1, 8), [], True),
        "artemis": Character(False, "Artemis", 15, 15, (1, 6), [], True)
    }

    return player, characters


def reset_game():
    player, characters = create_characters()
    rooms = copy.deepcopy(map.rooms)

    return player, characters, rooms


# === Movement ===

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


# === Combat ===

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


def run_from_combat(player, room, rooms, characters):
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

    if random.randint(1, 100) <= 65:  # TODO: Decide if this is okay hard or needs to be a var.
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


# === Equipment ===

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

        print(f"You collected {item['name']}!")
    else:
        print("There is nothing to collect.")


# === Commands ===

def game_commands():
    print(
        "Commands: [Move] [Attack] [Collect] [Puzzle] [Run] "
        "[Equipment] [Help] [Quit]"
    )


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


# === Game Loop ===

def game_loop():
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
            print(current_room)

            game_commands()
            command = input("> ").lower().strip()

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
                    rooms,
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
                current_room = admin(current_room, rooms, characters)

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


# TODO: Pygame

# === Pygame ===
def pygame_loop():
    pygame.init()

    player, characters, rooms = reset_game()
    current_room = "Entrance"

    font = pygame.font.Font(None, 36)
    description_font = pygame.font.Font(None, 28)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hero of Sleep")

    clock = pygame.time.Clock()
    running = True

    user_input = ""
    input_active = True
    command_state = None
    message = ""

    input_box = pygame.Rect(50, 500, 700, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                elif event.key == pygame.K_RETURN:
                    command = user_input.lower().strip()
                    user_input = ""
                    if command_state == "move":
                        new_room, description = try_moving(
                            current_room,
                            rooms,
                            command
                        )
                        current_room = new_room
                        message = ""
                        command_state = None

                    elif command == "move":
                        room = rooms[current_room]
                        message = "Exits: \n" + ", ".join(
                            direction.capitalize()
                            for direction in room["exits"].keys()
                        )
                        message += "\nWhich direction?"
                        command_state = "move"

                    else:
                        message = "I don't understand that command."

                else:
                    user_input += event.unicode

        screen.fill("black")

        room = rooms[current_room]

        room_name = font.render(
            current_room,
            True,
            "white"
        )

        room_description = description_font.render(
            room["description"],
            True,
            "white"
        )

        screen.blit(room_name, (50, 50))
        screen.blit(room_description, (50, 100))

        pygame.draw.rect(
            screen,
            "white",
            input_box,
            2
        )

        input_text = description_font.render(
            "> " + user_input,
            True,
            "white"
        )

        screen.blit(
            input_text,
            (input_box.x + 10, input_box.y + 8)
        )

        if message:
            y = 150

            for line in message.split("\n"):
                message_text = description_font.render(
                    line,
                    True,
                    "white"
                )

                screen.blit(message_text, (50, y))
                y += 30

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    pygame_loop()
