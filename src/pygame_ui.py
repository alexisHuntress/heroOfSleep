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

    font = pygame.font.Font(None, 36)
    description_font = pygame.font.Font(None, 28)
    button_font = pygame.font.Font(None, 24)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hero of Sleep")

    clock = pygame.time.Clock()
    running = True

    user_input = ""
    command_state = None
    message = ""

    puzzle_data = {}
    run_data = {}

    input_box = pygame.Rect(50, 530, 700, 40)

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
        y = 440 + row * 40

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
                "path": ["1", "2", "3", "4", "5", "6", "7"],
                "position": 0
            }

            message = (
                "Jump across the court!\n\n"
                "23 25 07 19 14\n"
                "15 05 21 06 18\n"
                "12 20 04 22 16\n"
                "13 17 03 02 11\n"
                "24 09 01 10 08\n\n"
                "Jump to square:"
            )

            command_state = "hopscotch"

        elif puzzle_name == "garden_puzzle":
            puzzle_data = {
                "sequence": [
                    "red",
                    "blue",
                    "purple",
                    "green",
                    "blue"
                ],
                "round": 1
            }

            message = (
                "Six colored flowers begin to glow.\n"
                "Red, Yellow, Blue, Green, Orange, and Purple.\n\n"
                "The flowers glow:\n"
                "red\n\n"
                "Repeat the sequence:"
            )

            command_state = "garden"

        elif puzzle_name == "hangman_puzzle":
            words = [
                "Nightmare", "Lantern", "Serenity", "Dream",
                "Castle", "Goblin", "Hero", "Shield", "Crown",
                "Slumber", "Shadow", "Monster", "Adventure",
                "Treasure", "Puzzle", "Garden", "Guardian",
                "Victory", "Dungeon", "Dragon"
            ]

            word = random.choice(words)

            puzzle_data = {
                "word": word,
                "check_word": word.lower(),
                "hidden_word": "-" * len(word),
                "wrong_guesses": 0,
                "guessed_letters": [],
                "repeat_warnings": [],
                "guess": 1
            }

            message = (
                f"{puzzle_data['hidden_word']}\n"
                "Wrong guesses: 0/6\n\n"
                "Enter a character:"
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                elif event.key == pygame.K_RETURN:
                    submitted_command = user_input.lower().strip()
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
                expected = puzzle_data["path"][
                    puzzle_data["position"]
                ]

                if command != expected:
                    message = (
                        "You jumped on the wrong square.\n"
                        "The puzzle remains unsolved."
                    )

                    command_state = None

                else:
                    puzzle_data["position"] += 1

                    if puzzle_data["position"] == len(
                        puzzle_data["path"]
                    ):
                        room["solved"] = True
                        room["locked exits"].clear()

                        message = (
                            "You completed the hopscotch path.\n"
                            "The door unlocks."
                        )

                        command_state = None

                    else:
                        message = "Correct!\nJump to square:"

            # === Garden ===
            elif command_state == "garden":
                answer = (
                    command
                    .replace(",", " ")
                    .replace(";", " ")
                )

                player_sequence = [
                    color.strip()
                    for color in answer.split()
                ]

                round_number = puzzle_data["round"]

                correct_sequence = puzzle_data["sequence"][
                    :round_number
                ]

                if player_sequence != correct_sequence:
                    message = (
                        "The flowers suddenly go dark.\n"
                        "That wasn't the correct sequence.\n"
                        "The puzzle remains unsolved."
                    )

                    command_state = None

                else:
                    puzzle_data["round"] += 1

                    if puzzle_data["round"] > len(
                        puzzle_data["sequence"]
                    ):
                        room["solved"] = True
                        room["locked exits"].clear()

                        message = (
                            "All six flowers begin to glow brightly.\n"
                            "You hear the door unlock."
                        )

                        command_state = None

                    else:
                        next_sequence = puzzle_data["sequence"][
                            :puzzle_data["round"]
                        ]

                        message = (
                            "Correct!\n\n"
                            "The flowers glow:\n"
                            + ", ".join(next_sequence)
                            + "\n\nRepeat the sequence:"
                        )

            # === Hangman ===
            elif command_state == "hangman":
                if len(command) != 1:
                    message = "Please enter only one character."

                else:
                    guessed_letters = puzzle_data[
                        "guessed_letters"
                    ]

                    repeat_warnings = puzzle_data[
                        "repeat_warnings"
                    ]

                    if command in guessed_letters:
                        if command not in repeat_warnings:
                            repeat_warnings.append(command)

                            message = (
                                f"You already guessed '{command}'. "
                                "Try again."
                            )

                        else:
                            puzzle_data["wrong_guesses"] += 1

                            message = (
                                f"You already guessed '{command}' twice!"
                            )

                    else:
                        guessed_letters.append(command)

                        check_word = puzzle_data["check_word"]
                        hidden_word = puzzle_data["hidden_word"]

                        if command in check_word:
                            new_hidden_word = ""

                            for index in range(len(check_word)):
                                if check_word[index] == command:
                                    new_hidden_word += (
                                        puzzle_data["word"][index]
                                    )
                                else:
                                    new_hidden_word += (
                                        hidden_word[index]
                                    )

                            puzzle_data["hidden_word"] = (
                                new_hidden_word
                            )

                        else:
                            puzzle_data["wrong_guesses"] += 1

                    puzzle_data["guess"] += 1

                    hidden_word = puzzle_data["hidden_word"]
                    wrong_guesses = puzzle_data[
                        "wrong_guesses"
                    ]

                    if "-" not in hidden_word:
                        room["solved"] = True
                        room["locked exits"].clear()

                        message = (
                            f"{hidden_word}\n"
                            "Winner! "
                            f"The word was {puzzle_data['word']}."
                        )

                        command_state = None

                    elif wrong_guesses >= 6:
                        message = (
                            f"{hidden_word}\n"
                            "Loser! "
                            f"The word was {puzzle_data['word']}.\n"
                            "The puzzle remains unsolved."
                        )

                        command_state = None

                    else:
                        message = (
                            f"\n\n{hidden_word}\n"
                            f"Wrong guesses: {wrong_guesses}/6\n"
                            "Enter a character:"
                        )

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

        # === Drawing ===

        screen.fill("black")

        room = rooms[current_room]

        room_name = font.render(
            current_room,
            True,
            "white"
        )

        screen.blit(room_name, (50, 30))

        # Room description
        y = 75

        for line in room["description"].split("\n"):
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
            for line in message.split("\n"):
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

        # Input box
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
            (
                input_box.x + 10,
                input_box.y + 8
            )
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
