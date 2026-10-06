# === Imports ===
from contextlib import redirect_stdout
from io import StringIO
from game import *
import random
import pygame


# === Pygame ===
def pygame_loop():
    pygame.init()

    player, characters, rooms = reset_game()
    current_room = "Entrance"

    font = pygame.font.SysFont("consolas", 32)
    description_font = pygame.font.SysFont("consolas", 24)
    button_font = pygame.font.SysFont("consolas", 20)
    map_font = pygame.font.SysFont("consolas", 14)

    screen = pygame.display.set_mode((1000, 650))
    pygame.display.set_caption("Hero of Sleep")

    clock = pygame.time.Clock()
    running = True

    user_input = ""
    last_command = ""
    command_state = None
    message = (
        "Welcome, Hero!\n"
        "Use the command buttons below or type a command.\n"
        "Choose Help at any time to see what each command does."
    )

    visited_rooms = {current_room}

    puzzle_data = {}
    run_data = {}

    flower_flash = None
    flower_flash_index = 0
    flower_flash_on = False
    flower_flash_time = 0
    flower_click_flash = None
    flower_click_flash_until = 0

    input_box = pygame.Rect(50, 580, 650, 40)

    direction_positions = {
        "north": (775, 455),
        "south": (775, 535),
        "west": (695, 495),
        "east": (855, 495),
        "up": (695, 455),
        "down": (855, 455)
    }
    direction_buttons = {
        direction: pygame.Rect(x, y, 70, 32)
        for direction, (x, y) in direction_positions.items()
    }

    hop_buttons = {
        "1": pygame.Rect(325, 480, 50, 32),
        "3": pygame.Rect(295, 440, 50, 32),
        "2": pygame.Rect(355, 440, 50, 32),
        "4": pygame.Rect(325, 400, 50, 32),
        "5": pygame.Rect(295, 360, 50, 32),
        "6": pygame.Rect(355, 360, 50, 32),
        "7": pygame.Rect(325, 320, 50, 32)
    }

    flower_names = ["red", "yellow", "blue", "green", "orange", "purple"]
    flower_buttons = {
        color: pygame.Rect(280 + (index % 2) * 120,
                           300 + (index // 2) * 42, 105, 32)
        for index, color in enumerate(flower_names)
    }

    flower_colors = {
        "red": (255, 0, 0),
        "yellow": (255, 255, 0),
        "blue": (0, 100, 255),
        "green": (0, 200, 0),
        "orange": (255, 165, 0),
        "purple": (160, 32, 240)
    }

    commands = [
        "Move",
        "Attack",
        "Collect",
        "Puzzle",
        "Run",
        "Equipment",
        "Help",
        "Quit"
    ]

    command_buttons = {}

    button_width = 165
    button_height = 35

    for index, command_name in enumerate(commands):
        row = index // 4
        column = index % 4

        x = 50 + column * 175
        y = 490 + row * 40

        command_buttons[command_name.lower()] = pygame.Rect(
            x,
            y,
            button_width,
            button_height
        )

    def capture_output(function, *args):
        output = StringIO()

        with redirect_stdout(output):
            result = function(*args)

        return result, output.getvalue().strip()

    def reset_pygame_game():
        new_player, new_characters, new_rooms = reset_game()

        return (
            new_player,
            new_characters,
            new_rooms,
            "Entrance"
        )

    map_positions = {
        "Entrance": (4, 6), "Mom's Room": (3, 6), "Hallway": (4, 5),
        "Item Room 6": (3, 5), "Hop Scotch Room": (5, 5),
        "Room with stairs up": (5, 6), "Room with stairs down": (5, 3),
        "Monster Room": (5, 2), "Treasure Room": (5, 1),
        "Empty Room": (4, 3), "Item Room 5": (4, 4), "Long Hall": (3, 4),
        "Garden": (2, 4), "Item room 4": (1, 4), "Empty room 2": (2, 3),
        "Cross Road": (1, 3), "Item room 1": (0, 3), "Nightmare's Room": (1, 2)
    }

    def wrap_text(text, text_font, max_width):
        wrapped_lines = []

        for paragraph in text.split("\n"):
            if not paragraph:
                wrapped_lines.append("")
                continue

            words = paragraph.split()
            line = words[0]

            for word in words[1:]:
                test_line = f"{line} {word}"

                if text_font.size(test_line)[0] <= max_width:
                    line = test_line
                else:
                    wrapped_lines.append(line)
                    line = word

            wrapped_lines.append(line)

        return wrapped_lines

    def draw_minimap():
        map_x, map_y, cell, room_size = 715, 35, 36, 16
        screen.blit(button_font.render("Mini Map", True, "white"), (map_x, map_y - 25))
        drawn_connections = set()

        for room_key in visited_rooms:
            if room_key not in map_positions:
                continue
            x1, y1 = map_positions[room_key]
            center1 = (map_x + x1 * cell + room_size // 2,
                       map_y + y1 * cell + room_size // 2)
            for destination in rooms[room_key]["exits"].values():
                if destination not in visited_rooms or destination not in map_positions:
                    continue
                connection = frozenset((room_key, destination))
                if connection in drawn_connections:
                    continue
                x2, y2 = map_positions[destination]
                center2 = (map_x + x2 * cell + room_size // 2,
                           map_y + y2 * cell + room_size // 2)
                pygame.draw.line(screen, "gray", center1, center2, 2)
                drawn_connections.add(connection)

        for room_key in visited_rooms:
            if room_key not in map_positions:
                continue
            grid_x, grid_y = map_positions[room_key]
            rect = pygame.Rect(map_x + grid_x * cell, map_y + grid_y * cell,
                               room_size, room_size)
            pygame.draw.rect(screen, "white", rect, 0 if room_key == current_room else 2)

        screen.blit(map_font.render("Filled = You", True, "white"),
                    (map_x, map_y + 7 * cell))

    def start_puzzle(room):
        nonlocal command_state
        nonlocal message
        nonlocal puzzle_data

        if room["puzzle"] is None:
            message = "There is no puzzle here."
            return

        if room["solved"]:
            message = "You have already solved this puzzle."
            return

        puzzle_name = room["puzzle"].__name__

        if puzzle_name == "hop_scotch_puzzle":
            puzzle_data = {
                "path": [["1"], ["3", "2"], ["4"], ["5", "6"], ["7"]],
                "position": 0,
                "jump": []
            }
            message = (
                "Jump across the court!\n"
                "Click the square or type each jump.\n"
                "For double squares, choose both numbers.\n"
                "Which square do you jump on?"
            )
            command_state = "hopscotch"

        elif puzzle_name == "garden_puzzle":
            nonlocal flower_flash
            nonlocal flower_flash_index
            nonlocal flower_flash_on
            nonlocal flower_flash_time

            puzzle_data = {
                "sequence": ["red", "blue", "purple", "green", "blue"],
                "round": 1,
                "player_sequence": []
            }
            message = (
                "Six colored flowers begin to glow.\n"
                "Watch the pattern, then repeat it."
            )
            command_state = "garden"
            flower_flash = puzzle_data["sequence"][:puzzle_data["round"]]
            flower_flash_index = 0
            flower_flash_on = True
            flower_flash_time = pygame.time.get_ticks()

        elif puzzle_name == "hangman_puzzle":
            words = [
                "Nightmare", "Lantern", "Serenity", "Dream", "Castle",
                "Goblin", "Hero", "Shield", "Crown", "Slumber",
                "Shadow", "Monster", "Adventure", "Treasure", "Puzzle",
                "Garden", "Guardian", "Victory", "Dungeon", "Dragon"
            ]
            word = random.choice(words)
            puzzle_data = {
                "word": word, "check_word": word.lower(),
                "hidden_word": "-" * len(word), "wrong_guesses": 0,
                "guessed_letters": [], "repeat_warnings": [], "guess": 1
            }
            message = (
                "A secret word begins to form on the door.\n"
                "You can see how long the word is but the letters are blurry.\n"
                "Guess one letter at a time, or try to guess the whole word.\n"
                "You have 6 wrong attempts to guess the word.\n\n"
                f"{puzzle_data['hidden_word']}\n"
                "Wrong guesses: 0/6\n"
                "Enter a character or guess the word:"
            )
            command_state = "hangman"

    while running:
        submitted_command = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if command_state is None:
                    for command_name, button in command_buttons.items():
                        if button.collidepoint(event.pos):
                            submitted_command = command_name
                            break

                elif command_state == "move":
                    for direction, button in direction_buttons.items():
                        if direction in rooms[current_room]["exits"] and button.collidepoint(event.pos):
                            submitted_command = direction
                            break

                elif command_state == "hopscotch":
                    for square, button in hop_buttons.items():
                        if button.collidepoint(event.pos):
                            submitted_command = square
                            break

                elif command_state == "garden" and flower_flash is None:
                    for color, button in flower_buttons.items():
                        if button.collidepoint(event.pos):
                            submitted_command = color
                            flower_click_flash = color
                            flower_click_flash_until = pygame.time.get_ticks() + 250
                            break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                elif event.key == pygame.K_UP:
                    user_input = last_command

                elif event.key == pygame.K_RETURN:
                    typed_command = user_input.lower().strip()
                    if typed_command:
                        last_command = typed_command
                    if command_state != "garden" or flower_flash is None:
                        submitted_command = typed_command
                    user_input = ""

                else:
                    user_input += event.unicode

        if submitted_command is not None:
            command = submitted_command.lower().strip()
            room = rooms[current_room]

            # === Retry ===
            if command_state == "retry":
                if command in ["yes", "y"]:
                    (
                        player,
                        characters,
                        rooms,
                        current_room
                    ) = reset_pygame_game()

                    command_state = None
                    message = ""
                    visited_rooms = {current_room}

                elif command in ["no", "n"]:
                    running = False

                else:
                    message = "Please enter Yes or No."

            # === Game Over ===
            elif command_state == "game_over":
                if command in ["quit", "exit"]:
                    running = False

                elif command in ["restart", "retry"]:
                    (
                        player,
                        characters,
                        rooms,
                        current_room
                    ) = reset_pygame_game()

                    command_state = None
                    message = ""
                    visited_rooms = {current_room}

            # === Move Direction ===
            elif command_state == "move":
                if command not in [
                    "north",
                    "south",
                    "east",
                    "west",
                    "up",
                    "down"
                ]:
                    message = "That is not a valid direction."
                    command_state = None

                else:
                    old_room = current_room

                    new_room, move_message = try_moving(
                        current_room,
                        rooms,
                        command
                    )

                    current_room = new_room
                    visited_rooms.add(current_room)

                    if current_room == old_room:
                        message = move_message

                    else:
                        message = ""

                        if current_room == "Entrance":
                            _, hidden_message = capture_output(
                                check_hidden_room,
                                player,
                                rooms
                            )

                            if hidden_message:
                                message = hidden_message

                        if current_room == "Mom's Room":
                            message = (
                                "You climb into bed beside Mom and close your eyes.\n"
                                "The Nightmare can't hurt you here.\n\n"
                                "=== Secret Victory ===\n"
                                "Sweet dreams, Hero.\n\n"
                                "Type Restart to play again or Quit to exit."
                            )

                            command_state = "game_over"

                    if command_state != "game_over":
                        command_state = None

            # === Run Direction ===
            elif command_state == "run":
                available_exits = run_data["available_exits"]
                enemy = run_data["enemy"]

                if command not in available_exits:
                    message = "You can't run that way!"
                    command_state = None

                else:
                    if run_data["enemy_name"] == "mini_boss":
                        enemy.hp = enemy.max_hp

                    current_room = room["exits"][command]
                    visited_rooms.add(current_room)
                    command_state = None
                    message = "You escaped!"

                    if current_room == "Entrance":
                        _, hidden_message = capture_output(
                            check_hidden_room,
                            player,
                            rooms
                        )

                        if hidden_message:
                            message += "\n" + hidden_message

            # === Hopscotch ===
            elif command_state == "hopscotch":
                expected = puzzle_data["path"][puzzle_data["position"]]
                entered = command.replace(",", " ").split()

                if len(expected) == 1:
                    puzzle_data["jump"] = entered
                else:
                    puzzle_data["jump"].extend(entered)
                    if len(puzzle_data["jump"]) < len(expected):
                        message = "Choose the other square in this jump."
                        continue

                if set(puzzle_data["jump"]) != set(expected):
                    message = "You jumped on the wrong square.\nThe puzzle remains unsolved."
                    command_state = None
                else:
                    puzzle_data["position"] += 1
                    puzzle_data["jump"] = []
                    if puzzle_data["position"] == len(puzzle_data["path"]):
                        room["solved"] = True
                        room["locked exits"].clear()
                        message = "You completed the hopscotch path. The door unlocks."
                        command_state = None
                    else:
                        message = "Correct!\nWhich square do you jump on?"

            # === Garden ===
            elif command_state == "garden":
                entered = command.replace(",", " ").replace(";", " ").split()
                puzzle_data["player_sequence"].extend(entered)
                correct_sequence = puzzle_data["sequence"][:puzzle_data["round"]]

                if puzzle_data["player_sequence"] != correct_sequence[:len(puzzle_data["player_sequence"])]:
                    message = ("The flowers suddenly go dark.\n"
                               "That wasn't the correct sequence.\n"
                               "The puzzle remains unsolved.")
                    command_state = None
                elif len(puzzle_data["player_sequence"]) == len(correct_sequence):
                    puzzle_data["round"] += 1
                    puzzle_data["player_sequence"] = []
                    if puzzle_data["round"] > len(puzzle_data["sequence"]):
                        room["solved"] = True
                        room["locked exits"].clear()
                        message = "All six flowers begin to glow brightly.\nYou hear the door unlock."
                        command_state = None
                    else:
                        flower_flash = puzzle_data["sequence"][:puzzle_data["round"]]
                        flower_flash_index = 0
                        flower_flash_on = True
                        flower_flash_time = pygame.time.get_ticks()
                        message = "Correct!\nWatch the next pattern..."

            # === Hangman ===
            elif command_state == "hangman":
                guessed_letters = puzzle_data["guessed_letters"]
                repeat_warnings = puzzle_data["repeat_warnings"]
                feedback = ""

                if len(command) > 1:
                    if command == puzzle_data["check_word"]:
                        puzzle_data["hidden_word"] = puzzle_data["word"]
                        feedback = "You guessed the word!"
                    else:
                        puzzle_data["wrong_guesses"] += 1
                        feedback = f"'{command}' is not the word!"
                elif len(command) == 1:
                    if command in guessed_letters:
                        if command not in repeat_warnings:
                            repeat_warnings.append(command)
                            feedback = f"You already guessed '{command.upper()}'. Try again."
                        else:
                            puzzle_data["wrong_guesses"] += 1
                            feedback = f"You already guessed '{command.upper()}' twice!"
                    else:
                        guessed_letters.append(command)
                        check_word = puzzle_data["check_word"]
                        hidden_word = puzzle_data["hidden_word"]
                        if command in check_word:
                            new_hidden_word = ""
                            for index in range(len(check_word)):
                                if check_word[index] == command:
                                    new_hidden_word += puzzle_data["word"][index]
                                else:
                                    new_hidden_word += hidden_word[index]
                            puzzle_data["hidden_word"] = new_hidden_word
                            feedback = f"'{command.upper()}' is in the word!"
                        else:
                            puzzle_data["wrong_guesses"] += 1
                            feedback = f"'{command.upper()}' is not in the word!"
                else:
                    feedback = "Please enter a character or guess the word."

                puzzle_data["guess"] += 1
                hidden_word = puzzle_data["hidden_word"]
                wrong_guesses = puzzle_data["wrong_guesses"]

                if "-" not in hidden_word:
                    room["solved"] = True
                    room["locked exits"].clear()
                    message = f"{hidden_word}\nWinner! The word was {puzzle_data['word']}."
                    command_state = None
                elif wrong_guesses >= 6:
                    message = (f"{hidden_word}\nLoser! The word was {puzzle_data['word']}.\n"
                               "The puzzle remains unsolved.")
                    command_state = None
                else:
                    message = (f"{feedback}\n\n{hidden_word}\n"
                               f"Wrong guesses: {wrong_guesses}/6\n"
                               "Enter a character or guess the word:")

            # === Normal Commands ===
            elif command == "move":
                enemy_name = room["enemy"]

                if (
                    enemy_name is not None
                    and characters[enemy_name].is_alive
                ):
                    message = (
                        f"{characters[enemy_name].name} "
                        "blocks your path!\n"
                        "You must Attack or Run."
                    )

                else:
                    message = "Exits:\n" + ", ".join(
                        direction.capitalize()
                        for direction in room["exits"].keys()
                    )

                    message += "\nWhich direction?"
                    command_state = "move"

            elif command == "attack":
                boss_defeated, combat_message = capture_output(
                    combat,
                    player,
                    room,
                    characters
                )

                message = combat_message

                if boss_defeated:
                    if len(player.equipment) == 8:
                        message += (
                            "\n\n=== Heroic Victory ===\n"
                            "Armed with every legendary treasure, "
                            "you defeated the Nightmare!\n"
                            "The kingdom can dream peacefully "
                            "once again."
                        )

                    else:
                        message += (
                            "\n\n=== Brave Victory ===\n"
                            "You faced the Nightmare without every "
                            "legendary treasure and still emerged "
                            "victorious!\n"
                            "The kingdom can dream peacefully "
                            "once again."
                        )

                    message += (
                        "\n\nType Restart to play again "
                        "or Quit to exit."
                    )

                    command_state = "game_over"

            elif command == "collect":
                _, message = capture_output(
                    collect_equipment,
                    player,
                    room,
                    characters
                )

            elif command in ["puzzle", "play"]:
                start_puzzle(room)

            elif command == "run":
                enemy_name = room["enemy"]

                if enemy_name is None:
                    message = "There is nothing to run from."

                else:
                    enemy = characters[enemy_name]

                    if not enemy.is_alive:
                        message = "There is nothing to run from."

                    elif enemy_name == "nightmare":
                        message = (
                            "You can't run from your Nightmare!"
                        )

                    else:
                        available_exits = [
                            direction
                            for direction in room["exits"]
                            if direction not in room[
                                "locked exits"
                            ]
                        ]

                        if not available_exits:
                            message = "There is nowhere to run!"

                        elif random.randint(1, 100) <= 65:
                            _, attack_message = capture_output(
                                enemy.attack,
                                player
                            )

                            if not player.is_alive:
                                message = (
                                    "You try to run!\n"
                                    "You found an opening!\n"
                                    + attack_message
                                )

                            else:
                                run_data = {
                                    "available_exits": (
                                        available_exits
                                    ),
                                    "enemy": enemy,
                                    "enemy_name": enemy_name
                                }

                                message = (
                                    "You try to run!\n"
                                    "You found an opening!\n"
                                    + attack_message
                                    + "\n\nExits:\n"
                                    + ", ".join(
                                        direction.capitalize()
                                        for direction
                                        in available_exits
                                    )
                                    + "\nRun which direction?"
                                )

                                command_state = "run"

                        else:
                            _, attack_message = capture_output(
                                enemy.attack,
                                player
                            )

                            message = (
                                "You try to run!\n"
                                "You couldn't get away!\n"
                                + attack_message
                            )

            elif command == "equipment":
                _, message = capture_output(
                    player.display_equipment
                )

            elif command == "help":
                message = (
                    "=== Help ===\n"
                    "Move - Move to another room\n"
                    "Attack - Attack an enemy\n"
                    "Collect - Collect an item in the room\n"
                    "Puzzle - Attempt to solve a puzzle\n"
                    "Run - Attempt to escape from an enemy\n"
                    "Equipment - View collected equipment\n"
                    "Quit - End the game"
                )

            elif command == "quit":
                running = False

            elif command:
                message = "I don't understand that command."

            # Check for death after any action
            if (
                running
                and not player.is_alive
                and command_state not in ["retry", "game_over"]
            ):
                message += (
                    "\n\nWould you like to try again? [Yes/No]"
                )

                command_state = "retry"

        # === Flower animation ===
        now = pygame.time.get_ticks()

        if flower_click_flash is not None and now >= flower_click_flash_until:
            flower_click_flash = None

        if command_state == "garden" and flower_flash is not None:
            elapsed = now - flower_flash_time

            if flower_flash_on and elapsed >= 500:
                flower_flash_on = False
                flower_flash_time = now

            elif not flower_flash_on and elapsed >= 250:
                flower_flash_index += 1

                if flower_flash_index >= len(flower_flash):
                    flower_flash = None
                    message = "Repeat the sequence:"
                else:
                    flower_flash_on = True
                    flower_flash_time = now

        # === Drawing ===

        screen.fill("black")

        room = rooms[current_room]

        room_name = font.render(
            room["name"],
            True,
            "white"
        )

        screen.blit(room_name, (50, 30))
        draw_minimap()

        # Room description
        y = 75

        text_max_width = 625

        for line in wrap_text(room["description"], description_font, text_max_width):
            description_text = description_font.render(
                line,
                True,
                "white"
            )

            screen.blit(description_text, (50, y))
            y += 28

        # Living enemy warning
        enemy_name = room["enemy"]

        if (
                enemy_name is not None
                and characters[enemy_name].is_alive
        ):
            enemy_text = description_font.render(
                f"{characters[enemy_name].name} blocks your path!",
                True,
                "white"
            )

            screen.blit(enemy_text, (50, y))
            y += 35

        # Message area
        message_y = max(y + 10, 175)

        if message:
            for line in wrap_text(message, button_font, text_max_width):
                message_text = button_font.render(
                    line,
                    True,
                    "white"
                )

                screen.blit(
                    message_text,
                    (50, message_y)
                )

                message_y += 22

        # Command buttons
        if command_state is None:
            for command_name, button in command_buttons.items():
                pygame.draw.rect(
                    screen,
                    "white",
                    button,
                    2
                )

                button_text = button_font.render(
                    command_name.capitalize(),
                    True,
                    "white"
                )

                text_rect = button_text.get_rect(
                    center=button.center
                )

                screen.blit(
                    button_text,
                    text_rect
                )

        # Direction buttons only appear while Move is active.
        if command_state == "move":
            for direction, button in direction_buttons.items():
                if direction in room["exits"]:
                    pygame.draw.rect(screen, "white", button, 2)
                    label = button_font.render(direction.capitalize(), True, "white")
                    screen.blit(label, label.get_rect(center=button.center))

        # Hopscotch squares are clickable while the puzzle is active.
        if command_state == "hopscotch":
            for square, button in hop_buttons.items():
                pygame.draw.rect(screen, "white", button, 2)
                label = button_font.render(square, True, "white")
                screen.blit(label, label.get_rect(center=button.center))

        # Simon Says flowers are clickable while the puzzle is active.
        if command_state == "garden":
            active_flower = None

            if flower_flash is not None and flower_flash_on:
                active_flower = flower_flash[flower_flash_index]
            elif flower_click_flash is not None:
                active_flower = flower_click_flash

            for color, button in flower_buttons.items():
                base_color = flower_colors[color]
                dim_color = tuple(channel // 4 for channel in base_color)
                fill_color = base_color if color == active_flower else dim_color

                pygame.draw.rect(screen, fill_color, button)
                pygame.draw.rect(screen, "white", button, 2)

                label = button_font.render(color.capitalize(), True, "white")
                screen.blit(label, label.get_rect(center=button.center))

        # Input box
        pygame.draw.rect(
            screen,
            "white",
            input_box,
            2
        )

        keyboard_active = not (
                command_state == "garden"
                and flower_flash is not None
        )

        input_text = description_font.render(
            "Command: " + user_input,
            True,
            "white"
        )

        text_x = input_box.x + 10
        text_y = input_box.y + 9

        screen.blit(input_text, (text_x, text_y))

        if keyboard_active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = text_x + input_text.get_width() + 2
            cursor_height = 20
            cursor_y = input_box.centery - cursor_height // 2

            pygame.draw.rect(
                screen,
                "white",
                (cursor_x, cursor_y, 8, cursor_height)
            )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
